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

---

## 26 September 2026, hourly pass 4

All eight points clear, including the behavioural smoke test: 65 available
plants offer ADD TO BAG, 15 coming-soon offer the waitlist, no JS errors.
No new findings.

**Consolidated the check into `tools/health_check.py`.** It had been ad hoc
shell and python retyped each pass, and that drifted: two false alarms in four
runs, first flagging the word "deflasked" in public teaching articles, then
counting a config comment as a config flag. Both were noise, and noise is how a
real finding gets scrolled past. One command now, and a fix to a check stays
fixed.

Nothing else was actionable. The queue is blocked on Kat: sticker shortlist,
Strawberry Shake price, the Google Sheet URL, a Meshulam account, and approval
on the seasonal palettes. The `filteredItems` crash fix is still waiting on a
deploy to reach the live store.

---

## 26 September 2026, hourly passes 5 and 6

Both clean on all eight points, no new findings.

**Took the one open item that was not actually blocked on Kat.**
`STOCK_SHEET_CSV` has been flagged as an unbuilt switch on every pass. The code
was never the blocker: the store already parses a published Google Sheet, honours
`qty`, `price` and `status`, and falls back safely when the sheet is missing.
What was missing was anyone telling Kat what the sheet should contain.

So: `docs/pinkleaf-stock-sheet.csv` is generated from the live store with all 83
rows, one per plant per size, ids, variants and current prices already filled.
Only `qty` needs entering. `docs/STOCK-SHEET-SETUP.md` covers publishing it as
CSV and the one line change to turn it on.

This matters more than it sounds. Every stock error this project has had traces
to there being no current count: Bambino proposed twice for a live quote when
the corms never germinated, a doubled dragon count, a Regal Shield quoted to a
customer that turned out to be a guest plant. The September shelf count is the
best record there is and it is already wrong.

Note for whoever wires it up: the published sheet is public. Keep it to id,
variant, qty, price and status. No cost, no supplier, no customer names, no
guest-plant flags.

---

## 26 September 2026, hourly passes 7 to 16

All clean on all eight points, every pass, no new findings and no commits. The
check is doing its job by being quiet.

---

## 27 September 2026, hourly pass 17

All eight points clear again.

**Found: the site had no 404 page.** Netlify serves its own branded not-found
page when the publish directory has no `404.html`, so anyone who mistyped a
URL, or followed an old link to an encyclopedia entry that moved, landed on a
Netlify page in English with no logo, no Hebrew and no way back to the store.
The store, the encyclopedia and the guides were all one click away and the
visitor was shown none of them.

`404.html` is now at the repo root: Hebrew RTL with an English block, on the
same cream and green palette as `/stickers/`, with the four real destinations,
the WhatsApp concierge, and `noindex, follow` so it never enters search
results. No external fonts or CDNs, so it renders the same in the sandbox as in
production. Checked at 1280px and 390px: no horizontal overflow, no JS errors,
and the handle renders `@pinkleaf.studio` rather than reversed.

**The eight blocking rules now point at it.** They were `to = "/"`, which meant
a request for `/CLAUDE.md` returned the entire homepage under a 404 status. It
hid the file, which was the point, but it was a strange thing to serve. They
now resolve to `/404.html`.

Health check point 5 parses `404.html` too, so it cannot rot.

**Customer visible, so it is Kat's call before it ships.** It only ever appears
on a URL that today shows a Netlify page, so the downside of shipping it is
close to zero, but the copy is new copy and she approves copy.

---

## 27 September 2026, deep audit

Kat asked for a full inspection rather than the standing eight point check.
This went wider: page weight measured in a browser, every internal link,
sitemap against real files, the store driven through search, tabs, filters,
sorts, cart and waitlist, robots and crawl rules, content integrity.

### The big one: the store ships 2.3 MB of photos to a phone

Measured on a 390px viewport over a real server, opening the store and
scrolling six screens pulls **2.7 MB, of which 2.3 MB is 21 plant photos**.
Each store card is a 140px circle and loads the full 1400px photo into it.
The heaviest single card is PV117 at 402 KB. That is roughly a hundred times
more pixels than the circle can show.

The fix is a thumbnail set. Measured on a random 25 photo sample:

| | total | per photo |
| --- | --- | --- |
| as shipped today | 4609 KB | 184 KB |
| as 420px webp | 625 KB | 25 KB |

**87% smaller.** Across the whole set that is 36 MB of photos becoming about
4 MB, and the store scroll dropping from 2.3 MB to roughly 300 KB. The full
size photo stays exactly as it is for the product modal. Nothing about how the
site looks changes.

Not built yet: it adds about 4 MB of generated files and changes how every
product card loads its image, and the last time a change like that went in
without her seeing it the store spent hours unbuyable. Her call.

### 32 MB of files nothing loads

- **28 MB of `.webp` plant photos.** 221 files. The site references exactly
  four of them, the `leaf*.webp` streak icons. Every plant photo loads as
  `.jpg`. Someone started a webp migration and never wired it up. Worth
  knowing before generating thumbnails, because 61 of the 80 store plants
  already have a webp sitting there.
- **4.5 MB of `.MP4`** in `plants/` (`plantyouwin`, `planthappy`,
  `plantmastercollector`). Reward clips from the game that was removed. No
  file references them.

Both are served to the public and sit in a public repo. Deleting needs Kat to
name them, per the standing rule.

### robots.txt was cancelling its own rules for Google

The file had a long `User-agent: *` block disallowing `/tools/`, `/src/`,
`/.claude/`, `/docs/`, `/brand/` and `/content/`, and then:

```
User-agent: Googlebot
Allow: /
```

A crawler obeys only the most specific group that matches it and ignores `*`
entirely. So for Googlebot, and Googlebot-Image, every one of those Disallow
lines did nothing, and the file was actively pointing Google at the internal
folders. The `force = true` 404s in `netlify.toml` meant it got a 404 rather
than the files, so nothing leaked, but the invitation should never have been
there. **Fixed:** both Google groups now repeat the rules in full.

### The checks were testing an unstyled page

`tools/smoke_test.py` loaded `index.html` over `file://`. Under `file://` a
root-relative path like `/assets/pinkleaf-tailwind.css` resolves to the
filesystem root and 404s. So every smoke run, and every visual check this
project has done in a sandbox, was of a page with **no Tailwind and no
`pinkleaf-enhancements.js`**. A bug in either was invisible to the test.

**Fixed:** the smoke test now starts a local HTTP server on a random port and
loads the page the way a visitor gets it, with two new assertions, that every
local asset returns 200 and that both stylesheets actually applied. Nine
checks now, all passing.

### `optimize_images.py` stays silent about photos it skips

The size skip runs before the dimension check, so a photo over the 1400px cap
that already weighs under 150 KB is never resized and never mentioned. Thirteen
photos are above the cap, one at 2000x2000, while the run printed
"0 also resized". **Fixed the reporting**, so it now names them. Did not
re-encode them: that is Kat's photography and a lossy rewrite is not something
to do unasked.

### An orphan encyclopedia page

`encyclopedia/acclimation-from-sphagnum-to-soil.html`, 1058 words, is in
`sitemap.xml` but is not in `entries.json` and is not linked from
`encyclopedia/index.html` or anywhere else. Google is told it exists; no
visitor can navigate to it. Same shape as the stickers page last week.

It is clean, for the record. A first pass flagged eight private-data hits in
it and every one was the CSS property `margin` matching a sloppy throwaway
grep. That is exactly the noise CLAUDE.md warns about, caught before it was
reported.

Left alone: putting it back in the index is customer visible, and it may have
been pulled deliberately.

### Checked and clean

- **No broken internal links** across 53 HTML files.
- **Sitemap**: 52 URLs, none dead. All 27 encyclopedia and 16 article pages listed.
- **MASTER_DB**: 171 ids, every one has a photo.
- **Store behaviour**, driven in a browser: search narrows and clears
  correctly, the empty state shows a message rather than a blank grid, the five
  category tabs filter and restore, all four price bands filter, all four sorts
  reorder correctly, add to bag persists, the waitlist button is wired to
  `joinWaitlist`. No JS errors through any of it.
- **No horizontal overflow** at 390px or 1280px on any page.
- **Accessibility panel** is present and correct: eight toggles with
  `aria-label` and `aria-pressed`, plus dark mode.
- **Social post standing rule**: all 26 entries in `entries.json` have a post
  in `content/`.
- Every store item without a photo is one of the eight known `X_` placeholders.

### Three things I flagged and then disproved

Worth recording, because reporting them would have wasted her time:

1. "An 81st store card with no data." It is the quiz image on the lab page,
   which shares the `.portal` class. 80 store cards is correct.
2. "The sort control does nothing." My probe selected the price filter instead
   of `#store-sort`, then compared plant ids that happened to be identical for
   the first three. All four sorts work.
3. "No empty-state message." It says "No plants match. Try clearing the search
   or filters" and my probe only searched for Hebrew phrasings.

Which points at a small real thing: **the store's own strings are English
only.** A Hebrew visitor on a Hebrew RTL page gets "80 plants" and
"No plants match. Try clearing the search or filters". Minor, and copy, so hers.
## 28 September 2026, full re-audit

Kat asked for a competitor study, a design comparison with the most modern
stores, and for the payment system to actually work. The full write-up is in
`docs/competitor-audit-2026-09-28.md`.

### Health check

- **Branch drift:** none. Branch and `main` were level before this work.
- **Production:** Netlify's current deploy is 26 Sep 10:17 UTC, after the
  last commit on `main`, with the six redirect rules `netlify.toml` defines,
  so production most likely matches `main`. Still a CLI upload with no commit
  ref.
- **Schema against store:** regenerating changed nothing. In sync.
- **Store data:** 80 items, no duplicate ids, 83 price rows, no orphans,
  every available plant's grades priced.
- **Private data:** no assignment-shaped supply chain fields, no supplier
  names, no cost fields in deployed files.
- **It still runs:** all inline scripts pass `node --check`, all `ld+json`
  parses. But see the first fix below: parsing is not the same as running.
- **Unbuilt switches:** `STOCK_SHEET_CSV` still empty. New one:
  `I4U_API_KEY` in Netlify switches card payment on (see the audit file).

### Fixed this session

| What | Why it mattered |
| --- | --- |
| `renderStore()` called an undefined `filteredItems` and threw on every render | Every `#/plant/` link, the kind shared on Instagram and WhatsApp, fell back to the plain store instead of opening the plant. `view_item` analytics never fired. `node --check` cannot catch this; only running the page does, so the health check now needs a browser pass too |
| Logo swap inverted in three places | After using dark mode, or the accessibility reset, the white wordmark sat on a white page |
| Organization schema logo was the white wordmark | Google would show a near invisible logo |
| Floating buttons over the bag drawer on mobile | Covered the drawer title and main button |
| Plants had no checkout; card option never appeared | Built: see the audit file, section 3 |

### Lesson for the health check

Add a **browser pass** to check 5: load the page in headless Chromium and
fail on any `pageerror`. Syntax checks passed for days while the store threw
on every render.

### Open, needs Kat

1. Deploy this branch. Customer visible: the new checkout with ₪37 shipping
   shown up front, the smaller logo on inner pages, the deeper rose buttons.
2. Add `I4U_API_KEY` in Netlify to switch card payment on, then place one
   small real order.
3. Confirm which phone number takes Bit (the site and the registry disagree).
4. Approve or change the checkout's refund line and write a cancellation
   policy.
5. Stale crawlable store text (one plant listed as available that is coming).

---

## 29 September 2026, second pass

- **Drift:** branch 3 ahead of `main`, 0 behind. Nothing deployed since
  26 Sep.
- **Found: work recorded but never committed.** Notion's inventory page says
  the Philodendron Radiatum was switched to available on 28 Sep. No branch
  had that change. Applied here and the schema regenerated. If a Mac session
  made it locally, expect a trivial merge.
- **Delivery:** the courier behind the 37 shekel rate stopped operating.
  `SHIPPING_FLAT_ILS` is now null: delivery orders pay for the plants only and
  the studio arranges delivery. Browser and function tests re-run clean.
- **Still open from yesterday:** Bit number, refund line, cancellation
  policy, stale crawlable store text, `STOCK_SHEET_CSV` empty.

---

## 30 September 2026, SEO pass on articles and encyclopedia

45 pages checked (27 encyclopedia, 18 articles). The basics are sound on every
page: canonical, one h1, Open Graph, structured data, sitemap entry, internal
links, no duplicate titles or descriptions.

What holds them back in search:

1. **38 of 45 titles are English only.** Israeli buyers search in Hebrew.
   Only 10 pages declare `lang="he"`; the encyclopedia pages carry Hebrew
   content under `lang="en" dir="ltr"`.
2. **23 titles are over 65 characters** and get cut off in Google results.
3. **30 meta descriptions are outside 70 to 170 characters** (some over 200,
   some under 50).
4. **26 pages have no `datePublished`**, so search engines cannot see them as
   fresh.
5. **Cadence:** Kat's plan was five new topics a week. The encyclopedia has 26
   entries in total. The gap is the pipeline, not the pages.

Fixing 1 to 3 is new customer-facing copy in Google results, so it waits for
Kat's approval.

### Fixed 1 Oct 2026 (Kat approved)

All 45 pages now have titles of 60 characters or fewer, descriptions of 115
to 160, Hebrew-first titles and descriptions on the 27 encyclopedia pages, and
datePublished / dateModified from git history. Seven garbled Hebrew
descriptions that Google was showing were rewritten. Source of truth:
`tools/seo_meta.json`, applied by `tools/apply_seo_meta.py`. Page language
attributes were left as they are: the encyclopedia pages carry both languages,
and flipping their direction would move the layout.

## 2 Oct 2026: store restyle (Pink Modern) and branch drift

Kat chose the pink direction from the mockups. The store grid is rebuilt:
square photos two across on phones (was one plant per screen), family chips
in the visitor's language, search first, one deep rose button per card, and
family plus "young plant" under every name so the grown photo is not taken
for what ships. Only exception badges show (sold out, coming soon, last one,
sale).

Found while doing it:

- **Branch drift.** `main` had two store commits this branch lacked (Hebrew
  store strings via `ST()`, filled ADD TO BAG). Merged in; the Hebrew labels
  are kept.
- **Button contrast.** That filled button was #b97a8e under white text,
  about 3.2:1, below the 4.5:1 for normal text. Now `--rose` #B04A6F, about
  5.2:1.
- **Stale delivery line.** The store still said "Nationwide shipping across
  Israel" after the courier stopped on 28 Sep. Now: pickup from the studio,
  delivery arranged per order.
- **Unescaped names in handlers.** Store cards passed plant names raw into
  `onclick`; a name with an apostrophe would break the button. Now `pdEsc`.

Health check: inline scripts pass `node --check`, JSON-LD parses, no
supply-chain fields, schema matches prices, browser pass with no `pageerror`,
add to bag and both checkout paths work. Not deployed: waits on Kat.

## 25 October 2026

Kat reported the store was wrong (plants she had taken off sale still for
sale, prices she had set not showing, a Wentii Pink card carrying a yellow
aurea photo, neon green dark mode).

### What was actually wrong

- 37 commits of her corrections from 26 Sep to 22 Oct sat on
  `claude/find-order-lists-chat-yxu11j`, never merged into main, never
  deployed. Main was at 3 Oct. The Mac clone was at 26 Aug.
- Dark mode used an emerald accent (`#00E676`). Kat hates it.

### Fixed and deployed (deploy 6ade1d71eb7118a2346e14e5, green)

- main fast-forwarded to the branch. Everything on it is live.
- Dark mode accent is the brand pink `#ECA9A5` on a deep ink ground.
- Health check: schema 83 offers in sync, 0 unpriced, private data clean,
  no page errors, 63 plants buyable, 17 on waitlist.

### Still open

- Photo audit: several cards still carry stock photos that do not match the
  variety (Wentii Pink shows an aurea plant, PV18.jpg). Needs Kat's own
  photos, location to be confirmed with her.
- 24 plants are listed available but absent from the 13 Sep shelf count.
  List given to Kat 25 Oct, waiting on her yes/no per plant.
- `STOCK_SHEET_CSV` still empty.
- The Python `smoke_test.py` cannot launch Chromium in the sandbox (browser
  version mismatch); the same assertions were run with Node Playwright and
  passed. Worth switching the script to Node.

## 26 October 2026: photo assignment audit

Trigger: Kat forwarded a live check of all 80 cards. Snapshot of the
catalogue as it stood after the fixes: `docs/catalogue-snapshot-2026-10-26.json`
(id, name, status, image file, md5, prices). Git history is the full backup;
the state before this pass is commit c3c84ec.

### How the pieces link

A card is `{id, name, availability[], status}` in `ALL_STORE_ITEMS`. Its photo
is always `plants/<id>.jpg` (fallback `assets/photo-coming.svg`), in the grid,
the detail view, the Vault and the quiz alike, so one file fix corrects all
four. Prices are `ITEM_PRICES["<id>_<grade>"]`. Kat's own label per id is
`MASTER_DB` (from `tools/plant-db.csv`). Descriptions exist only for four
products in `RICH` inside `tools/build_product_schema.py`; the detail view
shows a generic sentence plus the grade name.

### Cause

Commit 2f41065 (22 Jul 2026, "Add real photos") wrote Kat's photos to the
wrong ids: the Bambino photo went to PV119 and the Cuprea Aurea Latte photo
to PV113. Before that commit both ids carried unrelated images (an Anthurium
and a Philodendron), so the swap was never visible as a regression. The
"Pink Lava" text was the grade label on the PV113 option, invented by a
session, not Kat's label.

### Changed

| id | name | old image | new image |
| --- | --- | --- | --- |
| PV113 | Alocasia Bambino Pink Variegated | rounded metallic Cuprea foliage (was PV113.jpg) | arrow-shaped variegated Bambino (the former PV119.jpg) |
| PV119 | Alocasia Cuprea Aurea Latte | arrow-shaped Bambino foliage (was PV119.jpg) | rounded metallic Cuprea Aurea Latte (the former PV113.jpg) |
| PV13 | Rhaphidophora Tetrasperma Variegated (Coming Soon) | all-green specimen | placeholder; file kept in content/retired-photos |
| PV113 | grade label | "Pink Lava" | "Variegated" (price 706 unchanged) |

Also on 25 Oct: 13 card names restored to Kat's labels, 21 plants absent from
the shelf count moved to Coming Soon, PV154's watermarked third-party photo
retired.

### Checked, no change

- No two cards share a photo file (md5 check across all PV and X ids).
- No description is copied from another plant: only PV19, PV81, PV25, PV48
  have one, each its own.
- Prices, availability and design untouched. 42 available, 38 Coming Soon.
- Detail views render in Hebrew at 390px with the correct photo (PV113,
  PV119 screenshots taken), no page errors, buy and waitlist buttons present.

### Unresolved, needs Kat's photo

Cards whose photo does not prove the name (all her own files, just not
showing the variegation): PV117 Chantrieri Pink, PV152 Watsoniana Doff Albo,
PV77 Watsoniana Doff Pink, PV127 Metallic Blue Albo, PV199 Red Congo,
PV206 Verrucosum Mint. Nine cards on the placeholder: Melo Aurea,
Watsoniana Glossy, Radiatum, Venom Aurea, Angela Aurea, Black Cardinal,
Jungle Mint, Brown Beauty, Atabapoense Pink. Do not guess a photo for any
of these.

The Vault and quiz show MASTER_DB plants beyond the store (PV1 to PV210);
their photo mappings outside the 80 store ids were not audited.

## 26 October 2026 (second pass): the forwarded live check

Kat forwarded an outside check of all 80 cards listing PV113, PV119, PV13 and
nine placeholders. All three photo faults were already fixed in f58fa3c and
published in deploy 6adf0c168116296f93f4b02a (08:15 UTC), so the check most
likely ran against the earlier deploy. Re-verified in a browser at 390px in
both languages: PV113 shows the arrow-shaped variegated Bambino, PV119 the
rounded Cuprea Aurea Latte, PV13 the placeholder, no "Pink Lava" anywhere.

### Fixed

- **Quiz could ask about a placeholder.** It picks from all of MASTER_DB, and
  PV13 and PV154 have no photo since their files were retired. When a quiz
  photo fails it now picks another plant (up to five tries).
- `tools/smoke_test.py` matched the waitlist label case-sensitively, so in
  English ("Notify me") it would count zero. Now case-insensitive.

### Checked, no change

- The Vault and quiz build the same `plants/<id>.jpg` path as the store, so
  the PV113 / PV119 / PV13 fixes reach them too. No separate mapping exists.
- No duplicate photo files among plants. `basalt-chips.jpg` and `pumice.jpg`
  are identical but nothing references either.

### For Kat (not changed: names follow her labels, copy is hers)

- Store names that differ from MASTER_DB by more than spelling: PV80 store
  "Scalprum Mint" vs her "Scalprum white"; PV151 "Venom Variegated" (grade
  "Pink High Var") vs her "Venom"; PV179 adds "Banana"; PV79 "Nobilis Pink K"
  vs "Nobilis Pink Var"; PV23 "Black Velvet Gold" vs "Black Velvet Aurea".
- ~~The Hebrew detail view shows the description and Light / Humidity labels
  in English.~~ Fixed 26 Oct on Kat's go-ahead ("it needs to be repaired"):
  care line, description and both labels now follow the language, and the
  open panel re-renders when the language is switched. Also fixed: plants
  outside the three family tabs read "a tissue-culture propagated Others";
  they now name their genus (Rhaphidophora, etc.).
- PV13 Tetrasperma carries the grade "Mint", not in Kat's label
  ("Rhaphidophora Tetrasperma Var"). Coming soon, so nothing is sold under
  it; hers to confirm.
- Still waiting on her photos: the nine placeholder cards plus PV13 and
  PV154, and the six cards whose photo does not show the variegation (listed
  in the section above).
