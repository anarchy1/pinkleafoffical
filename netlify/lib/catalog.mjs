// Reads the store's own price table out of index.html, so the server charges
// exactly what the page shows. index.html stays the single source of truth;
// there is no second copy of any price to drift.
//
// The parsing mirrors tools/build_product_schema.py. If the shape of
// ALL_STORE_ITEMS, ITEM_PRICES or SUBSTRATE_DB changes, change both.

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

function block(html, start, end) {
    const i = html.indexOf(start);
    if (i === -1) throw new Error('catalog: missing ' + start);
    const rest = html.slice(i);
    const j = rest.indexOf(end);
    if (j === -1) throw new Error('catalog: unterminated ' + start);
    return rest.slice(0, j);
}

export function parseCatalog(html) {
    const itemsSrc = block(html, 'const ALL_STORE_ITEMS', '\n        ];');
    const items = {};
    const itemRe = /\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*availability:\s*\[([^\]]*)\][^}]*?status:\s*"(\w+)"/g;
    for (const m of itemsSrc.matchAll(itemRe)) {
        items[m[1]] = {
            id: m[1],
            name: m[2],
            grades: [...m[3].matchAll(/"([^"]+)"/g)].map(g => g[1]),
            status: m[4],
        };
    }

    const pricesSrc = block(html, 'const ITEM_PRICES', '\n        };');
    const prices = {};
    for (const m of pricesSrc.matchAll(/"([^"]+)":\s*(\d+)/g)) prices[m[1]] = Number(m[2]);

    const subSrc = block(html, 'const SUBSTRATE_DB', '\n        };');
    const substrate = {};
    const subRe = /"(\w+)":\s*\{\s*name:\s*"([^"]+)"[^\n]*?prices:\s*\{([^}]*)\}/g;
    for (const m of subSrc.matchAll(subRe)) {
        const sizes = {};
        for (const s of m[3].matchAll(/(\w+):\s*(\d+)/g)) sizes[s[1]] = Number(s[2]);
        substrate[m[1]] = { name: m[2], sizes };
    }

    const soldSrc = block(html, 'const SUBSTRATE_SOLD_OUT', ';');
    const substrateSoldOut = {};
    for (const m of soldSrc.matchAll(/"?(\w+)"?\s*:\s*\[([^\]]*)\]/g)) {
        substrateSoldOut[m[1]] = [...m[2].matchAll(/"([^"]+)"/g)].map(g => g[1]);
    }

    const ship = html.match(/const SHIPPING_FLAT_ILS\s*=\s*(\d+|null)\s*;/);
    const shipping = ship && ship[1] !== 'null' ? Number(ship[1]) : null;

    if (!Object.keys(items).length || !Object.keys(prices).length) {
        throw new Error('catalog: parsed an empty store');
    }
    return { items, prices, substrate, substrateSoldOut, shipping };
}

// index.html is bundled with the function (netlify.toml, included_files).
// Where it lands depends on the runtime, so look in the likely places.
export function loadCatalog() {
    const here = dirname(fileURLToPath(import.meta.url));
    const candidates = [
        join(process.cwd(), 'index.html'),
        join(here, '..', '..', 'index.html'),
        join(here, 'index.html'),
        '/var/task/index.html',
    ];
    for (const p of candidates) {
        if (existsSync(p)) return parseCatalog(readFileSync(p, 'utf8'));
    }
    throw new Error('catalog: index.html not found in function bundle');
}

// Turns what the browser sent into priced lines, using only server prices.
// Anything unknown, not for sale, or out of range is rejected, not guessed.
export function priceOrder(catalog, lines, fulfilment) {
    if (!Array.isArray(lines) || lines.length === 0) return { error: 'empty' };
    if (lines.length > 40) return { error: 'too_many_lines' };
    const out = [];
    for (const l of lines) {
        const qty = Number(l && l.qty);
        if (!Number.isInteger(qty) || qty < 1 || qty > 10) return { error: 'bad_qty' };
        if (l.kind === 'substrate') {
            const s = catalog.substrate[l.id];
            const price = s && s.sizes[l.size];
            if (!price) return { error: 'unknown_item', id: l.id };
            if ((catalog.substrateSoldOut[l.id] || []).includes(l.size)) return { error: 'sold_out', id: l.id };
            const label = String(l.size).replace(/^l/, '') + 'L';
            out.push({ id: l.id, name: s.name.split(' / ').pop() + ' ' + label, qty, price });
        } else {
            const item = catalog.items[l.id];
            if (!item || item.status !== 'available') return { error: 'unavailable', id: l.id };
            if (!item.grades.includes(l.grade)) return { error: 'unknown_grade', id: l.id };
            // A from-price that depends on size. Confirmed with the studio.
            if (l.grade === 'Mature Plant') return { error: 'unpriced', id: l.id };
            const price = catalog.prices[l.id + '_' + l.grade];
            if (typeof price !== 'number' || price <= 0) return { error: 'unpriced', id: l.id };
            out.push({ id: l.id, name: item.name + ' (' + l.grade + ')', qty, price });
        }
    }
    const items = out.reduce((s, l) => s + l.price * l.qty, 0);
    const pickup = fulfilment === 'pickup';
    // No flat fee set: charge the items only; the studio arranges delivery.
    const shippingSeparate = !pickup && catalog.shipping === null;
    const shipping = pickup || shippingSeparate ? 0 : catalog.shipping;
    return { lines: out, items, shipping, shippingSeparate, total: items + shipping };
}
