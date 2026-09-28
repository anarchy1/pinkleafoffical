// Card checkout. The browser sends what is in the bag; this function prices it
// from the store's own table (never from the browser), then asks Invoice4U for
// a hosted Meshulam payment page and hands its URL back. Invoice4U issues the
// receipt on success and emails it to the customer and to the studio.
//
// Switched on by one environment variable in Netlify (Project configuration,
// Environment variables):
//   I4U_API_KEY        Invoice4U organisation API key (Settings, API)
// Optional:
//   I4U_QA_MODE        "true" to run against Invoice4U's test environment
//   I4U_CLEARING_TYPE  clearing company code, 7 = Meshulam (default)
//
// While I4U_API_KEY is missing, GET reports { card: false } and the checkout
// page offers Bit, bank transfer and WhatsApp only. Nothing breaks.

import { loadCatalog, priceOrder } from '../lib/catalog.mjs';

const PROD = 'https://api.invoice4u.co.il/Services/ApiService.svc';
const QA = 'https://apiqa.invoice4u.co.il/Services/ApiService.svc';

const json = (status, body) => new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
});

// Plain text only on the payment page and the receipt.
const clean = (s, max) => String(s == null ? '' : s)
    .replace(/[<>{}|\\"`]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, max);

const israeliPhone = p => /^0(5\d|[2-4]|[89]|7\d)\d{7}$/.test(String(p).replace(/[\s-]/g, ''));
const email = e => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(e));
const orderRef = r => /^PL-\d{6}-[A-Z0-9]{4}$/.test(String(r));

export default async (req) => {
    const key = process.env.I4U_API_KEY;

    if (req.method === 'GET') return json(200, { card: Boolean(key) });
    if (req.method !== 'POST') return json(405, { error: 'method' });
    if (!key) return json(503, { error: 'card_off' });

    let body;
    try { body = await req.json(); } catch { return json(400, { error: 'bad_json' }); }

    const c = body.customer || {};
    const name = clean(c.name, 60);
    const phone = clean(c.phone, 20).replace(/[\s-]/g, '');
    const mail = clean(c.email, 80);
    const pickup = body.fulfilment === 'pickup';
    const city = clean(c.city, 40);
    const street = clean(c.street, 80);
    const notes = clean(c.notes, 300);
    const ref = clean(body.ref, 20);
    const lang = body.lang === 'en' ? 'en' : 'he';

    if (name.split(' ').filter(Boolean).length < 2) return json(400, { error: 'name' });
    if (!israeliPhone(phone)) return json(400, { error: 'phone' });
    if (!email(mail)) return json(400, { error: 'email' });
    if (!pickup && (!city || !street)) return json(400, { error: 'address' });
    if (!orderRef(ref)) return json(400, { error: 'ref' });

    let catalog;
    try { catalog = loadCatalog(); } catch (e) {
        console.error(e);
        return json(500, { error: 'catalog' });
    }
    const order = priceOrder(catalog, body.lines, pickup ? 'pickup' : 'delivery');
    if (order.error) return json(409, order);

    // The total the customer saw must match the server's. If a price changed
    // between page load and checkout, stop and let them see the new number.
    if (Number(body.expectedTotal) !== order.total) {
        return json(409, { error: 'price_changed', total: order.total });
    }

    const docLines = order.lines.map(l => ({ name: clean(l.name, 80), qty: l.qty, price: l.price }));
    if (order.shipping > 0) docLines.push({ name: lang === 'he' ? 'משלוח' : 'Shipping', qty: 1, price: order.shipping });

    const site = (process.env.URL || 'https://pinkleaf.co.il').replace(/\/$/, '');
    const fulfilLine = pickup
        ? (lang === 'he' ? 'איסוף עצמי מהסטודיו' : 'Studio pickup')
        : (lang === 'he' ? 'משלוח: ' : 'Delivery: ') + street + ', ' + city;

    const request = {
        Invoice4UUserApiKey: key,
        Sum: order.total,
        Currency: 'NIS',
        Type: 1,
        CreditCardCompanyType: Number(process.env.I4U_CLEARING_TYPE || 7),
        FullName: name,
        Phone: phone,
        Email: mail,
        IsAutoCreateCustomer: true,
        Description: 'Pink Leaf ' + ref,
        OrderIdClientUsage: ref,
        Platform: 'pinkleaf.co.il',
        Language: lang,
        DocLanguage: lang,
        IsDocCreate: true,
        DocHeadline: 'Pink Leaf ' + ref,
        // The receipt email is the studio's order record, so it carries
        // everything needed to pack and ship.
        DocComments: clean([ref, fulfilLine, phone, notes].filter(Boolean).join(' · '), 480),
        IsManualDocCreationsWithParams: true,
        DocItemName: docLines.map(l => l.name).join('|'),
        DocItemQuantity: docLines.map(l => l.qty).join('|'),
        DocItemPrice: docLines.map(l => l.price).join('|'),
        // Must be present and the same length as the other lists, or the
        // API throws a 500 (documented quirk). Empty = account default VAT.
        DocItemTaxRate: docLines.map(() => '').join('|'),
        ReturnUrl: site + '/?paid=' + encodeURIComponent(ref) + '#/checkout',
        IsQaMode: process.env.I4U_QA_MODE === 'true',
    };

    const base = request.IsQaMode ? QA : PROD;
    let data;
    try {
        const res = await fetch(base + '/ProcessApiRequestV2', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ request }),
        });
        data = await res.json();
    } catch (e) {
        console.error('invoice4u unreachable', e);
        return json(502, { error: 'provider' });
    }

    const r = data && data.ProcessApiRequestV2Result;
    const errors = (r && r.Errors) || [];
    if (!r || errors.length || !r.ClearingRedirectUrl) {
        // Log the provider's reason for the studio, never the API key.
        console.error('invoice4u refused', ref, JSON.stringify(errors).slice(0, 500));
        return json(502, { error: 'provider' });
    }

    console.log('payment page created', ref, order.total);
    return json(200, { url: r.ClearingRedirectUrl, total: order.total });
};

export const config = { path: '/api/checkout' };
