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
4. ~~Store direction not started.~~ **Wrong, corrected same day.** The clean
   product grid was already built on 23 September and is live in the code. That
   claim came from reading a stale `CLAUDE.md` before the merge brought the
   current one in. Lesson for the audit: read `CLAUDE.md` after merging main,
   not before, or you will report finished work as outstanding.
5. **Cannot see production from a cloud session.** `pinkleaf.co.il` and the
   Netlify preview URLs are blocked by the network egress policy, so audits are
   code-level only. Kat can open this in the cloud environment's network access
   settings.
6. **Seasonal theming: mechanism built, OFF, awaiting Kat's approval of a
   look.** `SEASON_THEMES` in index.html switches the same six palette tokens
   dark mode already uses, by date window, repeating yearly. Sukkot, winter and
   Tu BiShvat palettes are drafted. `enabled` is `false`, so the site looks
   exactly as it does today and nothing ships until she says yes. Seasons apply
   in light mode only so they never fight the Botanical Lab dark palette.
   Two things she has to do: approve a palette, and check the Sukkot and
   Tu BiShvat windows each year, since Hebrew dates move against the Gregorian
   calendar. Winter does not move.
7. ~~Sticker page requested.~~ **Built 26 September**, at `/stickers/`, and
   linked from the intro buttons and the crawlable index. Shows the one printed
   sticker; the other five are a single panel rather than five empty tiles,
   which had made the phone page 8000px of mostly nothing. Still open: Kat's
   shortlist of the final six, so the page can fill in.
8. **The round online logo is not in the site code.** Kat uses
   `brand/logo-round-online.jpg` as the logo online, but the site still loads
   the old `logo-light.png` / `logo-dark.png` pair. She calls the round one
   temporary, so this is on hold rather than a defect, but the two are out of
   step and someone will notice.

---

## 26 September 2026, hourly pass 1

Health check: branch drift 0 behind and 16 ahead, schema 83 offers 0 mismatches,
store data clean at 80 items, no private data, everything parses,
`STOCK_SHEET_CSV` still empty.

**Fixed: the stickers page was orphaned.** It shipped with nothing linking to
it, reachable only by typing the URL. Added a button on the intro beside
Instagram, and an entry in the crawlable index so search engines find it. A page
nobody can reach is the same as no page.

**Tightened health check 4.** It was matching bare words like "deflasked" and
flagging two public teaching articles every pass. The forbidden thing is a
per-plant field such as `acclimation: "deflasked"`, not the word in an article
explaining deflasking to customers. The check now looks for the assignment
shape, so real leaks are not buried in noise.

Nothing else was actionable. The remaining queue is blocked on Kat: the sticker
shortlist, the Google Sheet URL for the stock feed, a Meshulam account, and
approval on the seasonal palettes.

---

## 26 September 2026, deployed

A session on the Mac merged the branch and deployed it. Live and verified by
that session: corrected prices in the store (Alocasia Albo reads 831),
`/stickers/` opens, GA4 and the article WhatsApp buttons intact, the
"imports in transit" comment gone from page source, encyclopedia and store
both load.

**It found something this check had missed.** `docs/` and `.claude/` were being
served. `netlify.toml` publishes the repo root, so any new top-level folder is
public the moment it is committed, and this session had been adding files to
`docs/` without ever asking whether `docs/` was blocked. Health check point 7
now compares the repo's top-level directories against the 404 rules, so a new
folder cannot be added without a rule.

**Drift, again, in the other direction.** The Mac deployed from a separate copy
and did not push to GitHub. So the live site currently carries a fix that exists
nowhere in the repository, and Kat's own Mac folder still holds the older
version. This is the same failure that stranded the price corrections, just
reversed. The repo now has the equivalent fix committed, but it is not live
until the next deploy, and GitHub is not current until someone pushes.

Open: push to GitHub, and refresh Kat's Mac folder before anyone works in it.

---

## 26 September 2026, hourly pass 2

All seven check points clean: no drift into the branch, 83 offers with zero
schema mismatches, 80 store items with no gaps, no per-plant supply chain
state, everything parses, `STOCK_SHEET_CSV` still empty.

**Found: `src/` was being served, and it is dead code.** Nothing in any HTML
file references it. It holds `quick-config.js` and `social-media-content.js`,
old Instagram content planning from around March, plus a stale copy of
`entries.json`. No secrets in it.

It does carry **`#PinkLeafStore` five times**, which is the wrong-handle bug
that was supposedly fixed across 35 files. It survived precisely because
nothing references the folder, so no search for the bad handle ever visited it.
Now 404d and disallowed in robots.

**The check itself was the problem.** Its first run waved `src/` through on the
grounds that a folder called src must be site source. Point 7 now says to check
what references a folder before calling it public.

**Open for Kat: `src/` should probably be deleted, not just hidden.** It is
dead, it is stale, and it contradicts the brand. Blocking it stops the site
serving it, but the repo is public on GitHub so the wrong handle is still
readable there. Deleting needs her word, per the standing rule about never
deleting anything she has not named.

---

## 26 September 2026, hourly pass 3

The Mac pushed to GitHub, so the repository and the live site agree again. All
of this branch's work is on main.

**I broke the store and did not catch it.** The merge in 6eba2cc left the buy
button on the wrong branch of an if, so every available plant showed NOTIFY ME
and nothing on pinkleaf.co.il could be bought. A session on the Mac found it
and fixed it in f5b3d5c. It was live for some hours.

Every check in place passed while that was true. The scripts parsed, the schema
matched the store, no variable was undefined, no private data shipped. **A
logic inversion is valid code that is simply wrong**, and nothing that looks at
shape can see it.

**So there is now a behavioural check.** `tools/smoke_test.py` loads the page in
a real browser and asserts that available plants offer ADD TO BAG and
coming-soon plants offer the waitlist. It is health check point 8 and it runs
after every merge.

**It found a second live bug on its first run.** `renderStore` referenced
`filteredItems`, which is not defined anywhere. The local variable is `items`.
This threw on every store render, on main and therefore in production, killing
the GA4 view_item event and anything after it in that call stack. Fixed.

**Also from main: `force = true` on the 404 rules.** Without it Netlify serves a
file that exists and never applies the redirect, so the internal-folder blocking
this branch added was doing nothing at all. Main's version is now kept, with
`/.claude/*` and `/src/*` added on top.

Waiting on Kat: a deploy, so the `filteredItems` fix reaches the live store.
