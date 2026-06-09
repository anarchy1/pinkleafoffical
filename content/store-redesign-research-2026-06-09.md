# Store redesign research, 2026-06-09

Durable notes for the store standardization. Goal: replace the card/carousel
"game" with a clean, standard rare-plant store, three categories (Alocasia,
Monstera, Philodendron), nationwide IL shipping, PayPlus checkout.

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
  but make PayPlus the primary buy action once payment pages are configured.
- Product data should be category-tagged (alocasia / monstera / philodendron)
  so the grid can filter cleanly.
