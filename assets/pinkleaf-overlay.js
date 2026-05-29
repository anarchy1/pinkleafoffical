/* ─────────────────────────────────────────────────────────
   Pink Leaf — Overlay Manager
   Vanilla JS, no dependencies.

   What this does
   ──────────────
   1. Creates a single #pl-overlay container at the very top
      of <body>. This container hosts every persistent UI
      control so cards/carousels can never affect them.
   2. Moves the existing controls into it:
        - WhatsApp FAB
        - Language toggle (injected by pinkleaf-enhancements.js)
        - Accessibility trigger + drawer
        - Carousel arrows (prev/next)
   3. Marks each control with data-pl-layer so the layer-
      system CSS can apply the correct z-index token.
   4. Tags <body> with pl-page-<name> based on which <main>
      is currently visible, so controls (like carousel
      arrows) can be hidden on irrelevant pages.

   Safe to load multiple times — every step is idempotent.
   Runs as early as DOM allows, then keeps watching for
   late-inserted controls so order-of-execution issues with
   pinkleaf-enhancements.js (which injects .pl-lang-toggle)
   don't matter.
   ───────────────────────────────────────────────────────── */
(function () {
    'use strict';

    const PL = window.PinkLeaf || (window.PinkLeaf = {});
    const OVERLAY_ID = 'pl-overlay';

    /* ─── 1. ENSURE #pl-overlay EXISTS ──────────────────── */
    function ensureOverlay() {
        let overlay = document.getElementById(OVERLAY_ID);
        if (overlay) return overlay;

        overlay = document.createElement('div');
        overlay.id = OVERLAY_ID;
        overlay.setAttribute('role', 'presentation');
        // Insert as the FIRST child of <body> so its visual
        // order is predictable and it's not nested inside
        // any other stacking context.
        if (document.body.firstChild) {
            document.body.insertBefore(overlay, document.body.firstChild);
        } else {
            document.body.appendChild(overlay);
        }
        return overlay;
    }

    /* ─── 2. RE-PARENT A CONTROL INTO THE OVERLAY ───────── */
    // Moves element into overlay and tags it. No-ops if the
    // element is already there or doesn't exist yet.
    function adopt(overlay, el, layer, opts) {
        if (!el) return null;
        if (el.parentNode === overlay) return el;

        if (layer) el.setAttribute('data-pl-layer', layer);
        if (opts && opts.onlyOn) el.setAttribute('data-pl-only-on', opts.onlyOn);
        if (opts && opts.arrow)  el.setAttribute('data-pl-arrow', opts.arrow);

        // Strip a few inline styles that fight the layer
        // system (the FAB ships with z-index inline for the
        // no-JS fallback; the layer-system CSS handles z
        // once the FAB is inside the overlay).
        if (opts && opts.stripInlineZ && el.style) {
            el.style.zIndex = '';
        }
        // Strip classes whose positioning assumed a different
        // parent (e.g. `.arrow-pos-left { left:0 !important }`
        // is meaningful inside `.store-frame` but wrong inside
        // the viewport-fixed overlay).
        if (opts && opts.stripClasses) {
            opts.stripClasses.forEach((c) => el.classList.remove(c));
        }

        overlay.appendChild(el);
        return el;
    }

    /* ─── 3. ADOPT KNOWN CONTROLS ───────────────────────── */
    function adoptKnownControls(overlay) {
        // WhatsApp FAB
        adopt(
            overlay,
            document.querySelector('a[aria-label="Chat on WhatsApp"]'),
            'whatsapp',
            { stripInlineZ: true }
        );

        // Accessibility trigger + drawer
        adopt(overlay, document.getElementById('acc-trigger'), 'a11y-trigger');
        adopt(overlay, document.getElementById('acc-drawer'),  'a11y-drawer');

        // Language toggle (injected late by enhancements.js)
        adopt(overlay, document.querySelector('.pl-lang-toggle'), 'lang');

        // Carousel arrows. Live inside <main id="page-store">,
        // possibly nested in a frame wrapper (`.store-frame`).
        // Use the explicit position classes when present
        // (`.arrow-pos-left` / `.arrow-pos-right`), otherwise
        // fall back to source order.
        const storeMain = document.getElementById('page-store');
        if (storeMain) {
            const left  = storeMain.querySelector('.side-arrow.arrow-pos-left, .side-arrow:not(.arrow-pos-right):first-of-type');
            const right = storeMain.querySelector('.side-arrow.arrow-pos-right, .side-arrow:not(.arrow-pos-left):last-of-type');
            const arrowOpts = { onlyOn: 'store', stripClasses: ['arrow-pos-left', 'arrow-pos-right', '-left-4', '-right-4', 'sm:-left-8', 'sm:-right-8'] };
            if (left)  adopt(overlay, left,  'arrow', Object.assign({ arrow: 'prev' }, arrowOpts));
            if (right) adopt(overlay, right, 'arrow', Object.assign({ arrow: 'next' }, arrowOpts));
        }
    }

    /* ─── 4. PAGE-AWARE BODY CLASS ──────────────────────── */
    // Sets body.pl-page-<name> based on which <main> doesn't
    // have the .hidden class. Used by the layer-system CSS
    // to show/hide controls (e.g. carousel arrows only on
    // the store page).
    function syncPageClass() {
        const visible = document.querySelector('main:not(.hidden)');
        const current = visible && visible.id ? visible.id.replace(/^page-/, '') : null;

        // Clear any prior pl-page-* class
        const toRemove = [];
        document.body.classList.forEach((c) => {
            if (c.indexOf('pl-page-') === 0) toRemove.push(c);
        });
        toRemove.forEach((c) => document.body.classList.remove(c));

        if (current) document.body.classList.add('pl-page-' + current);
    }

    /* ─── 5. OBSERVE LATE-MOUNT + PAGE CHANGES ──────────── */
    function startObservers(overlay) {
        // Watch <main> visibility (class changes) so we know
        // when showPage() switches pages.
        const mains = document.querySelectorAll('main[id^="page-"]');
        if (mains.length && 'MutationObserver' in window) {
            const pageObs = new MutationObserver(syncPageClass);
            mains.forEach((m) => pageObs.observe(m, {
                attributes: true,
                attributeFilter: ['class']
            }));
        }

        // Watch <body> for newly-inserted controls (the lang
        // toggle is injected by enhancements.js after we run).
        // We only need a shallow observation — the controls
        // we care about are all body-level.
        if ('MutationObserver' in window) {
            const bodyObs = new MutationObserver((mutations) => {
                let needsAdopt = false;
                for (const m of mutations) {
                    for (const n of m.addedNodes) {
                        if (n.nodeType !== 1) continue;
                        if (
                            n.matches &&
                            n.matches('.pl-lang-toggle, a[aria-label="Chat on WhatsApp"], #acc-trigger, #acc-drawer')
                        ) {
                            needsAdopt = true;
                            break;
                        }
                    }
                    if (needsAdopt) break;
                }
                if (needsAdopt) adoptKnownControls(overlay);
            });
            bodyObs.observe(document.body, { childList: true });
        }
    }

    /* ─── 6. PUBLIC API ─────────────────────────────────── */
    PL.overlay = {
        // Manually mount a custom control. Useful for ad-hoc
        // overlay elements added by feature code later.
        mount(el, layer, opts) {
            const overlay = ensureOverlay();
            return adopt(overlay, el, layer, opts || {});
        },
        // Force a re-sync (e.g. after a page-renderer rebuilds DOM).
        refresh() {
            const overlay = ensureOverlay();
            adoptKnownControls(overlay);
            syncPageClass();
        }
    };

    /* ─── 7. INIT ───────────────────────────────────────── */
    function init() {
        const overlay = ensureOverlay();
        adoptKnownControls(overlay);
        syncPageClass();
        startObservers(overlay);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
