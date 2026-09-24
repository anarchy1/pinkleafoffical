# Deploy handoff

Paste this into a Claude session running **on the Mac** (Cowork or the CLI in
the repo folder). A cloud session cannot do it: the Netlify connector there has
read access only and every deploy upload returns 403, tried four times across
2026-09-19 to 2026-09-24. The cloud sandbox also cannot reach pinkleaf.co.il at
all, so it can never confirm the result either.

---

## The situation

`pinkleaf.co.il` is served by the Netlify project `pinkleaf` (team `kdtatt`).
That project is **not building from the repo**. Its published production deploy
was a manual upload dated **2026-09-09** with no commit ref. Everything
committed to `main` since then has never reached a visitor.

That is now a large backlog, including a customer-facing privacy fix and a
working checkout.

## What to do, in order

1. **Deploy what is on main.**

   ```
   cd <the repo>
   git checkout main && git pull
   npx netlify-cli deploy --prod --dir .
   ```

   If it asks to link, pick the existing `pinkleaf` project. Do not create a
   new site.

2. **Verify, do not assume.** Open these and check:
   - `pinkleaf.co.il/tools/pricing-calculator.html` must 404. If it loads, the
     deploy did not go through, and internal markup maths is public.
   - `pinkleaf.co.il/encyclopedia/` must list 26 entries.
   - The store must show a CARE tab, and substrate must be addable to the bag.

3. **Then stop it happening again.** In Netlify: Project configuration,
   Build and deploy, Link repository, GitHub, `anarchy1/pinkleafoffical`,
   branch `main`, publish directory `.`, no build command. After that a push
   deploys by itself and this handoff is never needed again.

## What is waiting in the backlog

- The pricing calculator, which exposed base import cost, a markup multiplier
  and a loss buffer, deleted. It is live right now if the Sept 9 upload
  included it.
- Acclimation supply-chain state removed from the store source.
- A working substrate checkout with order references.
- 9 new encyclopedia entries, bilingual, and both hub pages.
- Product structured data for all 79 plants, corrected to match the store.
- 37 MB of image weight removed, and Tailwind's dev-only CDN replaced.

## Two things only Kat can supply

- **Substrate delivery fee.** `SUBSTRATE_SHIPPING_ILS` in index.html is `null`,
  so delivery says shipping is confirmed with the order. Set it to a number and
  the checkout shows an exact total.
- **Meshulam payment page URL.** Paste it into `PAYMENT.card.pageUrl` and card
  checkout appears on its own. Bit already works.
