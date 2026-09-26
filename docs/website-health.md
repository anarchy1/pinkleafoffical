# Website health log

Running record of what the site audit found, what got fixed, and what is still
open. Read this before auditing so you do not re-report something known.

The check itself is defined in `CLAUDE.md` under "audit the site on your own
initiative". Add a dated section each time it runs.

---

## 26 September 2026

Ran after Kat asked for the Netlify deploy to be verified, then asked for the
audit to become a standing habit.

### Deploy

Green. Published 00:02 UTC, built in 14 seconds, no errors, 242 files, 4
redirect rules applied.

One thing to know about how it got there: the deploy record carries no commit
reference, `deploy_source` is `cli`, and its title names a commit that does not
exist in this repository. The live site was pushed from a folder on the Mac, not
from git. Git and production are therefore not guaranteed to match in either
direction. Do not treat `origin/main` as proof of what is live.

### Fixed this session

| What | Why it mattered |
| --- | --- |
| Branch was 22 commits behind `main` while holding 9 commits of unmerged store work | Kat's price corrections and the stock feed were not live and nobody knew |
| Acclimation gating still present on the branch | Ships supply chain state to a public file, which `CLAUDE.md` forbids. Resolved in favour of `main`, which had already removed it |
| CSS comment reading "imports in transit, customs, or hardening" | Live in `index.html` view-source on production today. Rewritten |
| Product schema advertised old prices for 79 of 80 products | Google would have been told prices the store does not charge. Regenerated with `tools/build_product_schema.py` |

### Checked and clean

- 80 store items, 65 available, 15 coming. Every purchasable option has a price.
- No price rows pointing at options that do not exist. No duplicate ids.
- 8 items without a photo, all of them the `X_` entries that already use the
  shared placeholder. Not a defect.
- All five inline scripts pass `node --check`. Both `ld+json` blocks parse.
- No surviving references to the gating helpers the merge removed.
- `tools/`, `content/`, `CLAUDE.md` and `RESET.md` are 404'd by redirect rules,
  so internal files in the published root are not served.
- `tools/plant-db.csv` carries id, name and family only. No cost data.
- Pricing calculator is gone from both branches.

### Open

1. **Nothing above is live.** It needs a merge to `main` and a deploy from the
   Mac. The customer visible change is the price table moving off round numbers,
   and sold out plants reading as sold out. Waiting on Kat.
2. **`STOCK_SHEET_CSV` is empty.** The Google Sheet stock feed is wired and
   guarded, so it fails quietly and changes nothing. Until Kat supplies the
   sheet URL, "sold out means sold out" is not actually working.
3. **No checkout.** Offer URLs route to WhatsApp. Meshulam through Invoice4U is
   the chosen provider and the payment link is generated per order by hand.
4. **Store direction not started.** The agreed plan is to drop the card and
   carousel layout for a clean product grid in three categories, Alocasia,
   Monstera and Philodendron. The current layout is still the old one.
5. **Cannot see production from a cloud session.** `pinkleaf.co.il` and the
   Netlify preview URLs are blocked by the network egress policy, so audits are
   code-level only. Kat can open this in the cloud environment's network access
   settings.
6. **Seasonal theming requested.** Kat wants the look to change for holidays.
   Not started. Should be one theme token set switched by date, not hand edits.
