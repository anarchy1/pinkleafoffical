# Store redesign research, 2026-06-09

Durable notes for the store standardization. Goal: replace the card/carousel
"game" with a clean, standard rare-plant store, three categories (Alocasia,
Monstera, Philodendron), nationwide IL shipping, PayPlus checkout.

## Studio overhaul decisions (set by Kat, 2026-06-15)
These came out of the "system architecture overhaul" manifest. Reality check
first: the site is a static single index.html on GitHub Pages, no backend, no
database, no cloud functions. So decisions were scoped to what a static site can
honestly do, plus external automation.

- ARCHITECTURE: stay static + external automation. No fake client-side "login"
  (a static site cannot secure one; View Source defeats it). Real SMS/email and
  any B2B gating go through an external no-code service (Make/Zapier) plus forms,
  not a server in this repo. Do NOT build a gated /lab-portal with JS-only auth.
- ACCLIMATION GATING (Task 1, DONE): ALL_STORE_ITEMS entries can carry an
  optional `acclimation` stage ("in-transit", "customs", "deflasked",
  "hardening"). A gated plant hides its price, shows a "Limited Release" badge and
  "Price Tier: Premium Collector - inquire for current sheet", and swaps Add to
  Bag for a "Join Studio Waitlist" button (requestAllocation -> WhatsApp
  concierge, bilingual). PV19/PV81/PV25 are flagged as the genuine incoming
  imports. To gate or ungate a plant, edit the `acclimation` key on its entry.
- THEME (Task 3, DONE, preview only): the existing day/night toggle is UNCHANGED.
  Only the CSS variables inside body.dark-mode were retuned to the obsidian
  "Botanical Lab" look: --bg #121212, --text #ffffff, accent --pink overridden to
  emerald #00E676 (flows to all --pink/--border/--glow surfaces). Do not rewrite
  the toggle. Lives on branch claude/checkout-card-plans-bcwo6h for preview before
  any merge to main.
- PRICING BUFFER (Task 2, DONE): delivered as an internal calculator at
  tools/pricing-calculator.html (noindex), NOT a live cloud function. Formula
  Final = (Base * Markup) / (1 - Buffer), default buffer 0.20 for high-risk
  variegates. Back-office only; use it to set the number, then type the price in.
- SCARCITY: honest "limited release / by allocation" framing only. Do NOT cap
  visible units below real stock (dark pattern, consumer-protection risk in
  Israel under חוק הגנת הצרכן). The waitlist gating supplies real scarcity.
- STILL OPEN (need Kat / an external service before building): the B2B
  micropropagation intake and the auto SMS/email-on-acclimation webhook both need
  a Make/Zapier endpoint URL. Scaffold once Kat provides it; do not build
  speculative dead UI.

## Reference stores in the niche (what good ones do)
- Foliage Factory (foliage-factory.com/category/shop-aroids): category filters
  kept consistent across the shop. Strong filter-driven grid.
- Carnivero, Raroid (raroid.co.uk), Aroid Empire (aroidempire.com), Logee's,
  Aroid Market, Tropics@Home: all use a simple product GRID with category
  navigation, large product photo, name, price, clear in-stock state.

Common pattern worth copying:
- Top-level category tabs / sections (here: Alocasia | Monstera | Philodendron).
- Responsive product grid (2 cols mobile, 3-4 desktop), one card per plant.
- Card = photo, name, short variegation/size note, price, single clear CTA.
- "In stock" / "Coming soon" / "Sold" badge.
- No carousel, no game. Standard, fast, scannable.

## Payments: PayPlus on a static site
PayPlus supports credit/debit, Apple Pay, Bit, Max. Integration options:
payment links, hosted payment page (redirect), and iframe/hosted-fields.

- Static-site-safe path (recommended first): PayPlus hosted payment page /
  payment links via redirect. No server, no exposed API key. Generate a payment
  page UID per product or use per-amount payment links; the product CTA sends
  the buyer to PayPlus, then back.
- Upgrade path (optional, later): iframe/hosted-fields embed needs a small
  serverless endpoint (e.g. Netlify/Vercel function) to mint the page link so
  the API key stays server-side. Docs: docs.payplus.co.il, sample repo
  PayPlus-Gateway/hosted-fields-sample.

## Build direction
- Keep the existing WhatsApp "Price Concierge" as a secondary CTA / fallback,
  but make checkout the primary buy action once payment pages are configured.
- Product data should be category-tagged (alocasia / monstera / philodendron)
  so the grid can filter cleanly.

## Payment provider update (2026-06-15)
- The PayPlus notes above are SUPERSEDED. Per CLAUDE.md, the chosen provider is
  now Meshulam (Grow): Israeli cards plus Bit, hosted payment pages / payment
  links that work from a static site. The static-site-safe pattern is the same:
  redirect to a Meshulam hosted page, no exposed secret key. Kat has not created
  the Meshulam account yet (as of this date), so checkout still routes to
  WhatsApp until credentials exist.

## Israeli competitor reference: Al-Haderech (provided by Kat, 2026-06-15)
Could not fetch their site from the cloud container (HTTP 403 bot block), so
these facts came from Kat directly.

| Feature         | Al-Haderech                  |
|-----------------|------------------------------|
| Platform        | WooCommerce                  |
| Location        | Rishon LeZion                |
| Delivery        | Ashdod to Netanya only       |
| Min order       | NIS 100                      |
| Delivery cost   | NIS 28 to NIS 100            |
| Lead time       | 48h local / 5 days regional  |
| Self-pickup     | Free by coordination         |
| Club membership | 10% discount                 |
| Security        | ICP certified                |
| Catalog         | 2,000+ SKUs                  |

What this tells us for our build:
- They run WooCommerce, a dynamic CMS with a real cart, accounts, and club
  discounts. We are a static GitHub Pages site, so we do NOT replicate Woo
  natively. Meshulam hosted pages are how we get a real checkout without a
  server. This is the key architectural difference, not a shortfall.
- Their delivery is regional only (Ashdod to Netanya). Pink Leaf already ships
  nationwide across Israel, so nationwide shipping is a genuine advantage to
  state plainly on the store and product pages.
- Policy levers worth a decision from Kat: minimum order (they use NIS 100),
  tiered delivery pricing (they use NIS 28 to NIS 100), free self-pickup by
  coordination (we already do appointment visits, so easy to mirror), and a
  loyalty/club discount (they give 10%).
- "ICP certified" is the Israeli card-clearing standard. Using Meshulam, a
  licensed Israeli gateway, covers the equivalent trust signal for us.

## Shipping and checkout policy (set by Kat, 2026-06-15)
- NO minimum order. A single plant can check out on its own.
- Shipping is QUOTED PER ORDER, not a fixed online fee, because the cost depends
  on parcel size. The online total is plants only; Kat confirms shipping per
  order. (Earlier in the same conversation a flat NIS 35 fee was briefly built,
  then reversed in favor of quote-per-order. Do not re-add a fixed fee unless
  Kat asks.)
- Standard parcel is 40x40 cm. If the plant does not fit the 40x40 box, the
  shipping fee is DOUBLED. No per-item size data in the catalog yet, so this is
  a manual confirmation; STORE_POLICY.oversizeMultiplier (=2) documents it for
  later automation if oversized SKUs get tagged.
- Shipping days are Sunday and Monday ONLY, so a parcel never sits over the
  Israeli weekend. Delivery can take up to 5 business days. This is shown to the
  customer at checkout.
- Implemented in index.html: computeBagTotals() returns plants-only subtotal and
  total (no shipping line); the bag drawer shows a Hebrew note that price
  excludes shipping, shipping is confirmed per order, ships Sun/Mon, up to 5
  business days, over 40x40 cm doubles. The WhatsApp concierge message carries
  the same. Lives on branch claude/checkout-card-plans-bcwo6h, not yet on main.
