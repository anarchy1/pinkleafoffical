/* ─────────────────────────────────────────────────────────
   Pink Leaf — Frontend enhancements
   Vanilla JS, no dependencies. Static-site friendly.
   Loads:
     1. Blur-up lazy loading via IntersectionObserver
     2. WebP/AVIF picture-tag enhancement (graceful fallback)
     3. HE ↔ EN language toggle with dir/lang attribute swap
     4. Price-Concierge generator (replaces vulgar prices)
     5. Mobile pop-up collision guard (JS-side belt+suspenders)

   All functions are namespaced under window.PinkLeaf
   to avoid colliding with anything else on the page.
   ───────────────────────────────────────────────────────── */
(function () {
    'use strict';

    const PinkLeaf = window.PinkLeaf || {};

    // ─── 1. BLUR-UP LAZY LOADING ─────────────────────────
    // Usage: <img class="pl-lazy" data-src="full.jpg" src="tiny.jpg">
    // The tiny.jpg is the inline placeholder (LQIP). When the
    // image enters the viewport, swap src → data-src and remove blur.
    PinkLeaf.initLazyImages = function () {
        const lazyImgs = document.querySelectorAll('img.pl-lazy[data-src]');
        if (!lazyImgs.length) return;

        // Older browsers without IntersectionObserver: load everything immediately.
        if (!('IntersectionObserver' in window)) {
            lazyImgs.forEach((img) => {
                img.src = img.dataset.src;
                img.classList.add('pl-loaded');
            });
            return;
        }

        const io = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    const img = entry.target;
                    const fullSrc = img.dataset.src;
                    if (!fullSrc) return;

                    // Preload the full image to avoid the blur jumping
                    // before the file actually arrives.
                    const preloader = new Image();
                    preloader.onload = () => {
                        img.src = fullSrc;
                        img.classList.add('pl-loaded');
                        // also handle <picture><source> if present
                        const picture = img.closest('picture');
                        if (picture) picture.classList.add('pl-loaded');
                    };
                    preloader.onerror = () => {
                        // Network issue — drop the blur anyway so user sees something
                        img.classList.add('pl-loaded');
                    };
                    preloader.src = fullSrc;
                    observer.unobserve(img);
                });
            },
            { rootMargin: '200px 0px', threshold: 0.01 }
        );

        lazyImgs.forEach((img) => io.observe(img));
    };

    // ─── 2. WEBP / AVIF PICTURE WRAPPER ──────────────────
    // For each <img class="pl-modern" src="x.jpg">, wraps in
    //   <picture>
    //     <source srcset="x.avif" type="image/avif">
    //     <source srcset="x.webp" type="image/webp">
    //     <img src="x.jpg">
    //   </picture>
    // Browsers that support AVIF use it; others fall back to WebP;
    // ancient browsers fall back to the original JPG. Strategy assumes
    // that x.avif and x.webp exist alongside x.jpg in /plants/.
    // (You can pre-generate them with: cwebp x.jpg -o x.webp; avifenc x.jpg x.avif)
    PinkLeaf.upgradeImagesToPicture = function () {
        const modernImgs = document.querySelectorAll('img.pl-modern:not([data-pl-wrapped])');
        modernImgs.forEach((img) => {
            const src = img.getAttribute('src');
            if (!src || src.startsWith('data:')) return;

            const lastDot = src.lastIndexOf('.');
            if (lastDot === -1) return;
            const base = src.slice(0, lastDot);
            const ext = src.slice(lastDot + 1).toLowerCase();
            // Don't upgrade GIFs/SVGs — keep them as-is
            if (['svg', 'gif'].includes(ext)) return;

            const picture = document.createElement('picture');
            picture.className = 'pl-picture';

            const sourceAvif = document.createElement('source');
            sourceAvif.srcset = base + '.avif';
            sourceAvif.type = 'image/avif';
            picture.appendChild(sourceAvif);

            const sourceWebp = document.createElement('source');
            sourceWebp.srcset = base + '.webp';
            sourceWebp.type = 'image/webp';
            picture.appendChild(sourceWebp);

            // Move img inside the picture
            img.setAttribute('data-pl-wrapped', '1');
            img.parentNode.insertBefore(picture, img);
            picture.appendChild(img);
        });
    };

    // ─── 3. LANGUAGE TOGGLE (HE ↔ EN) ────────────────────
    // Reads/writes the selected language to localStorage so it
    // persists across pages. Updates <html lang> and <html dir>
    // dynamically without a page reload, then dispatches a
    // 'pl:langchange' event so other modules can react.
    PinkLeaf.LANG_KEY = 'pinkleaf_lang';
    PinkLeaf.SUPPORTED_LANGS = ['he', 'en'];

    PinkLeaf.getCurrentLang = function () {
        return document.documentElement.getAttribute('lang') || 'he';
    };

    PinkLeaf.setLang = function (lang) {
        if (!PinkLeaf.SUPPORTED_LANGS.includes(lang)) return;
        const html = document.documentElement;
        html.setAttribute('lang', lang);
        html.setAttribute('dir', lang === 'he' ? 'rtl' : 'ltr');

        try {
            localStorage.setItem(PinkLeaf.LANG_KEY, lang);
        } catch (e) {
            /* private mode / quota exceeded — silently continue */
        }

        // Toggle data-lang on body so CSS can target language-specific blocks
        document.body.setAttribute('data-lang', lang);

        // Show/hide elements that opt into language-specific visibility
        document.querySelectorAll('[data-lang-only]').forEach((el) => {
            const targetLang = el.getAttribute('data-lang-only');
            el.style.display = targetLang === lang ? '' : 'none';
        });

        // Update toggle button label if present
        const toggleBtn = document.querySelector('.pl-lang-toggle');
        if (toggleBtn) {
            toggleBtn.textContent = lang === 'he' ? 'English' : 'עברית';
            toggleBtn.setAttribute('aria-label',
                lang === 'he' ? 'Switch to English' : 'החלף לעברית');
        }

        // Notify other modules
        window.dispatchEvent(new CustomEvent('pl:langchange', { detail: { lang } }));
    };

    PinkLeaf.toggleLang = function () {
        const current = PinkLeaf.getCurrentLang();
        PinkLeaf.setLang(current === 'he' ? 'en' : 'he');
    };

    PinkLeaf.initLangToggle = function () {
        // Restore from localStorage if user previously chose
        let saved = null;
        try {
            saved = localStorage.getItem(PinkLeaf.LANG_KEY);
        } catch (e) { /* noop */ }

        if (saved && PinkLeaf.SUPPORTED_LANGS.includes(saved)) {
            PinkLeaf.setLang(saved);
        } else {
            // First visit: respect <html lang> set in markup
            PinkLeaf.setLang(PinkLeaf.getCurrentLang());
        }

        // Inject the toggle button if not already present
        if (!document.querySelector('.pl-lang-toggle')) {
            const btn = document.createElement('button');
            btn.className = 'pl-lang-toggle';
            btn.type = 'button';
            const current = PinkLeaf.getCurrentLang();
            btn.textContent = current === 'he' ? 'English' : 'עברית';
            btn.setAttribute('aria-label',
                current === 'he' ? 'Switch to English' : 'החלף לעברית');
            btn.addEventListener('click', PinkLeaf.toggleLang);
            document.body.appendChild(btn);
        }
    };

    // ─── 4. PRICE CONCIERGE GENERATOR ────────────────────
    // Replaces any element with class .price-vulgar (e.g. plain
    // "₪199-₪350" text) with the wabi-sabi concierge card.
    // Reads data-low and data-high attributes for the range, and
    // data-product for the WhatsApp message text.
    PinkLeaf.replaceVulgarPrices = function () {
        document.querySelectorAll('.price-vulgar:not([data-pl-replaced])').forEach((el) => {
            const low = el.dataset.low;
            const high = el.dataset.high;
            const product = el.dataset.product || 'this plant';
            const isHe = PinkLeaf.getCurrentLang() === 'he';

            const wrapper = document.createElement('div');
            wrapper.className = 'price-concierge';
            wrapper.setAttribute('data-pl-replaced', '1');

            const label = document.createElement('p');
            label.className = 'price-concierge__label';
            label.textContent = isHe ? '· מחיר קונסייז\'·' : '· Concierge Pricing ·';

            const range = document.createElement('p');
            range.className = 'price-concierge__range';
            if (low && high && low !== high) {
                range.innerHTML = (isHe ? 'מ-' : 'From ') +
                    '<strong>₪' + low + '</strong>' +
                    (isHe ? ' עד ' : ' to ') +
                    '<strong>₪' + high + '</strong>';
            } else if (low) {
                range.innerHTML = (isHe ? '₪' : '₪') + '<strong>' + low + '</strong>';
            } else {
                range.textContent = isHe ? 'מחיר במסר' : 'Price on Inquiry';
            }

            const hint = document.createElement('p');
            hint.className = 'price-concierge__hint';
            hint.textContent = isHe
                ? 'כל צמח ייחודי. נשלח לך תמונות אמיתיות וגודל מדויק לפני ההזמנה.'
                : 'Every plant is unique. We send you real photos and exact size before you commit.';

            const cta = document.createElement('a');
            cta.className = 'price-concierge__cta';
            cta.target = '_blank';
            cta.rel = 'noopener';
            const msg = encodeURIComponent(
                (isHe ? 'היי! התעניינתי ב-' : 'Hi! I’m interested in ') + product
            );
            cta.href = 'https://wa.me/972559116990?text=' + msg;
            cta.textContent = isHe ? 'בקש פרטים בוואטסאפ' : 'Inquire on WhatsApp';

            wrapper.appendChild(label);
            wrapper.appendChild(range);
            wrapper.appendChild(hint);
            wrapper.appendChild(cta);

            el.parentNode.replaceChild(wrapper, el);
        });
    };

    // Re-render concierge prices when language changes
    window.addEventListener('pl:langchange', () => {
        // Reverse the data-pl-replaced flag won't help us — we'd need
        // the original elements. Instead, re-update the labels in place.
        document.querySelectorAll('.price-concierge').forEach((el) => {
            const isHe = PinkLeaf.getCurrentLang() === 'he';
            const label = el.querySelector('.price-concierge__label');
            const hint = el.querySelector('.price-concierge__hint');
            const cta = el.querySelector('.price-concierge__cta');
            if (label) label.textContent = isHe ? '· מחיר קונסייז\'·' : '· Concierge Pricing ·';
            if (hint) hint.textContent = isHe
                ? 'כל צמח ייחודי. נשלח לך תמונות אמיתיות וגודל מדויק לפני ההזמנה.'
                : 'Every plant is unique. We send you real photos and exact size before you commit.';
            if (cta) cta.textContent = isHe ? 'בקש פרטים בוואטסאפ' : 'Inquire on WhatsApp';
        });
    });

    // ─── 5. MOBILE COLLISION GUARD (JS belt+suspenders) ──
    // CSS already hides the registry/XP popups <768px, but on
    // some Android browsers backdrop-filter can keep them painted.
    // We force display:none in JS too so the WhatsApp FAB is alone.
    PinkLeaf.guardMobileCollision = function () {
        const isMobile = window.matchMedia('(max-width: 768px)').matches;
        if (!isMobile) return;
        const ids = ['registry-float', 'xp-counter'];
        ids.forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });
    };

    // ─── INIT ────────────────────────────────────────────
    function init() {
        try { PinkLeaf.upgradeImagesToPicture(); } catch (e) { console.warn('[PinkLeaf] picture upgrade failed', e); }
        try { PinkLeaf.initLazyImages(); } catch (e) { console.warn('[PinkLeaf] lazy init failed', e); }
        try { PinkLeaf.initLangToggle(); } catch (e) { console.warn('[PinkLeaf] lang toggle failed', e); }
        try { PinkLeaf.replaceVulgarPrices(); } catch (e) { console.warn('[PinkLeaf] price concierge failed', e); }
        try { PinkLeaf.guardMobileCollision(); } catch (e) { console.warn('[PinkLeaf] collision guard failed', e); }
    }

    // Re-run collision guard on resize (rotation, devtools, etc.)
    window.addEventListener('resize', () => {
        if (PinkLeaf.guardMobileCollision) PinkLeaf.guardMobileCollision();
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose globally
    window.PinkLeaf = PinkLeaf;
})();
