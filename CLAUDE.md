# Project instructions

## FIRST: read the operations registry

**Before doing ANY work on orders, customers, suppliers, inventory, refunds or
money, open this page and read it:**

> **Pink Leaf Operations Registry (START HERE)**
> https://app.notion.com/p/3dcbce507fd3810aa211e95a6b16eb24

It is the durable record of this business. It holds the active order records,
the supplier list, the standing rules, and the documentation protocol. Kat
should never have to re-explain something that is already written there.

Chat history does not persist between sessions. The registry does. So:

1. **Read it first.** Do not ask Kat to re-explain context that is on that page.
2. **Write to it last.** Before finishing any session that touches orders,
   customers, suppliers or money, record what happened: decisions made, money
   moved (date, amount, method, reference), what is still open and who owns it,
   and any new standing rule Kat states.
3. **Respect the standing rules** in that page. They exist because they were
   already argued once. Do not re-litigate them.

If a record for the thing you are working on does not exist, create it in
Notion under "Pink Leaf Business Overview" and link it in the registry's
Active Records table.

Never put customer names, order history, cost basis, supplier names per SKU, or
shipping method discussions into this repo. That data lives in Notion only. See
the private data rules below.

## SECOND: read the brand spec before designing anything

**Before putting the logo on anything (Instagram card, post, slide, label,
document, page), read `brand/README.md`.**

It says which logo file is which, what each one is for, and what is missing.
The short version, because it has already gone wrong twice:

- **Never crop the logo, rebuild it in text, or substitute an emoji.** Use a
  file from `brand/` whole.
- `logo-light.png` and `logo-dark.png` in the repo root are the **website
  header pair**. They are not general purpose assets.
- `favicon.png` is a different drawing entirely. It is not the logo.
- Kat's real design pack lives on her Mac and does NOT reach cloud sessions.
  If the asset needed is not in `brand/`, ask her for it. Do not improvise.

## THIRD: audit the site on your own initiative, do not wait to be asked

Kat's standing instruction, 26 September 2026: check, learn, compare against
what the site could be, and improve it. Often. Without being asked. Make sure
everything is functional, the store included.

So every session that touches this repo runs the health check below before
finishing, and reports what it found even when the answer is "nothing broke".
Findings and their status live in `docs/website-health.md`. Read that first so
you are not re-reporting something already known or already fixed.

**Run it with one command: `python3 tools/health_check.py`.** It does all eight
points below and exits non-zero if anything needs attention. Do not retype the
checks by hand: doing that four times produced two false alarms, once flagging
the word "deflasked" in public teaching articles and once counting a config
comment as a config flag. A check that cries wolf gets ignored, which is worse
than no check. If a point is wrong, fix it in the script so the fix sticks.

**The health check.** Each of these has caught a real bug already:

1. **Branch drift.** `git log --oneline origin/main..HEAD` and the reverse. Work
   stranded on a branch is work that is not live. This was missed once and Kat's
   price corrections sat unshipped for days.
2. **Schema against store.** Every price in the Product structured data must
   match `ITEM_PRICES`. When a price changes, run
   `python3 tools/build_product_schema.py`. It drifted twice.
3. **Store data integrity.** Every purchasable option has a price, no price rows
   point at options that do not exist, no duplicate ids, every item has a photo
   or the shared placeholder.
4. **Private data in deployed files.** Grep `index.html` and everything else that
   ships for acclimation and supply chain state, cost, wholesale, margin,
   supplier names, customer details. Check comments too, not just rendered text.
   A dead CSS comment naming customs and hardening shipped to production once.
   **Match the state, not the vocabulary.** The forbidden thing is a per-plant
   field such as `acclimation: "deflasked"`, not the word in a public article
   teaching customers what deflasking is. Search for the assignment shape
   (`acclimation:`, `"in-transit"`, `"customs"`, `stage:`) rather than bare
   words, or the encyclopedia articles light up every pass and the real signal
   gets lost in the noise.
5. **It still runs.** All inline scripts pass `node --check`, all `ld+json`
   blocks parse, no references to helpers a merge removed.
   Then load the page in headless Chromium (Playwright is preinstalled) and
   fail on any `pageerror`. Syntax passing is not running: on 28 Sep 2026 the
   store threw on every render (`filteredItems` undefined) and broke every
   `#/plant/` link while `node --check` stayed green.
6. **Unbuilt switches.** Flag config that is wired but empty, for example
   `STOCK_SHEET_CSV`. The feature reads as done and does nothing.
7. **Every internal folder is blocked.** `netlify.toml` publishes the repo root,
   so a new top-level folder is served the moment it is committed. Compare the
   directories in the repo root against the 404 rules in `netlify.toml` and the
   Disallow lines in `robots.txt`, and add any that are missing. This was found
   by a session on the Mac, not by this check: `docs/` and `.claude/` had been
   served the whole time, and adding files to `docs/` made it worse without
   anyone noticing. Adding a folder means adding a rule, every time.
   **Do not assume a folder is public because its name sounds public.** `src/`
   was waved through on the first run of this check on the grounds that a
   folder called src must be site source. It is dead code referenced by nothing,
   full of old marketing drafts, and it carried the `#PinkLeafStore` hashtag,
   the wrong-handle bug that was supposedly fixed across 35 files. Open the
   folder and check what actually references it before calling it public.

8. **The store still works.** Run `python3 tools/smoke_test.py`. It loads the
   real page in a real browser and asserts that available plants offer ADD TO
   BAG and coming-soon plants offer the waitlist. **This is the only check here
   that tests behaviour rather than shape.** On 26 September a merge resolution
   left the buy button on the wrong branch of an if, so every available plant
   showed NOTIFY ME and nothing could be bought, in production. Every other
   check passed: the scripts parsed, the schema matched, nothing was undefined.
   A logic inversion is valid code that happens to be wrong, and no amount of
   grepping finds it. Run this after every merge, without exception.

**What you may do alone, and what needs Kat.** Fixing drift, regenerating
derived files, closing a data leak, and repairing something broken are ordinary
repo work: do them and say so. Anything customer visible, a price on the live
store, a layout change, new copy, is hers to approve before it ships.

**Deploying is not yours.** The live host is Netlify and pushing to `main` does
not deploy. A cloud session cannot deploy at all. The deploy runs from Kat's Mac,
so finish by telling her exactly what is waiting and what it will change.

## Writing style

**HARD RULE: Never use em dashes.**

This applies everywhere with no exceptions: chat replies, commit messages, PR
descriptions, code comments, and every file written into this repository
(articles, HTML, JSON entries, encyclopedia content, etc.).

- Do not use the em dash character `-` (U+2014).
- Do not use the horizontal bar `-` (U+2015) as a substitute.
- Rewrite the sentence instead. Use a comma, a colon, parentheses, two separate
  sentences, or a plain hyphen `-` where a short joiner is genuinely needed.

This rule is enforced automatically: a `PostToolUse` hook runs the Humanizer
(`.claude/scripts/humanizer.py`) on every file written or edited, which strips
em dashes from file content as a safety net. Write clean text in the first
place; treat the hook as a backstop, not a license to be sloppy.

---

## Project context and standing decisions

This section is the durable memory for this project. Past sessions kept losing
context because their notes lived in machine-local Claude memory on the Mac
(`~/.claude/projects/-Users-kat-pinkleafoffical/memory/`), which does NOT travel
with the git repo. Cloud sessions only see the repo. So: record any decision
that should survive across sessions HERE, in the repo.

### The business
- Pink Leaf Botanical Studios: rare and variegated plant studio, Ramat Gan, Israel.
- Site: `pinkleaf.co.il`, a static site served by **Netlify** (see the deploy
  notes below). The `CNAME` file in the repo is a leftover from the old GitHub
  Pages setup and does not control the live domain.
- Bilingual: Hebrew (RTL) and English (LTR). Currency is ILS (`₪`).
- Owner: Kat. **Kat is a woman: every Hebrew draft written in her voice uses
  feminine first person** (שמחה, הייתי הולכת, ממליצה), never masculine. Address
  each customer in their own gender. Set by Kat 2026-09-29.
- **Never offer a studio visit, a pickup address or an appointment in anything
  written for a customer.** Standing rule, Kat, 19 Oct 2026. She has been
  deleting that line by hand out of every list and menu a session hands her.
  The studio is not a place she receives people, and she does not want her
  growing setup shown. No menu, quote, bundle, caption or post mentions
  visiting, dropping by, collecting in person, or booking a time.
  **This is still live on the website and is hers to decide, not a session's
  to change.** The lines are `index.html:54` (the schema description says
  by-appointment visits), `index.html:3812` and `index.html:4818` (checkout
  offers pickup from the studio in Ramat Gan, by appointment).
- Nationwide shipping: **paused as a fixed
  service since 2026-09-28**, the courier stopped operating. Delivery is
  arranged per order until Kat picks a new courier (see Payments below).
- Instagram is `@pinkleaf.studio`. NOT `@pinkleaf.store` (that is an unrelated
  India dropship store; using it was a real past bug, fixed across 35 files).

### Store direction (DONE, 2026-09-23)
The plan below was already built by an earlier session and is live in the code.
Recording it as done so no future session rebuilds it.
- Clean product grid, no carousel and no game. Category tabs, search, price
  filter, sort, result count, availability badges.
- Tabs are generated from the catalogue, not hard-coded, so a plant can never
  end up in no tab. Alocasia, Monstera and Philodendron are the standard three;
  an OTHER tab appears only while something sits outside them (currently 2).
- Acclimation gating is GONE, not just unused. The stage vocabulary
  ("in-transit", "customs", "deflasked", "hardening") sat in the deployed
  source as dead code after the data was stripped. Do not reintroduce it: the
  private data rules below forbid shipping supply-chain state, and a key name
  in public source is still that state.
- A plant that is not in stock offers a waitlist button ("NOTIFY ME" /
  "עדכנו אותי") that opens the WhatsApp concierge. It used to be a disabled
  dead button on 15 plants.

### Brand colour (standing rule, Kat 2 Oct 2026)
- **The brand is pink, and it is the logo's pink.** Not black, and not a
  dusty or deep "old" rose either. Kat rejected both. Take colours from
  `brand/logo-round-online.jpg`: leaf pink `#ECA9A5`, mauve wordmark
  `#916065`, cream ground. In index.html these are `--rose`, `--mauve`,
  `--on-rose` (deep mauve `#5E3540` for text on the pink, 5.2:1; white on
  this pink is unreadable) and `--blush`.
- **Shapes are square, not rounded** (Kat, 2 Oct 2026: she chose the squared
  mockup's shapes, in pink). Corners use `--radius: 4px` in index.html; no
  pill buttons or round photo frames on the store.
- **Design assets come from Kat.** She has a ChatGPT plan and has it draw
  headers, banners and social visuals. When a page or post needs artwork,
  ask her for that specific piece rather than generating or improvising
  one (Kat, 2 Oct 2026). Plants shown for sale or as a variety reference
  must be real photos, not drawn ones.

### Encyclopedia and social (standing rule)
- **Every new encyclopedia entry gets a social post.** Set by Kat 2026-09-19.
  An entry is not done when it deploys, it is done when the post copy exists
  alongside it. Write the post in the same commit as the entry.
- Format: one post per entry, Hebrew and English, both ready to paste, plus a
  platform, a visual suggestion and a goal. Follow
  `content/week-2026-04-10-social.md` and
  `content/encyclopedia-posts-2026-09-19.md`.
- Every post links to the entry page on `pinkleaf.co.il/encyclopedia/`.
- **Kat posts. That is her choice, not a limitation, since 19 Oct 2026.**
  The Instagram account `pinkleaf.studio` is connected through **Composio** and
  the connection is live. From a session it can publish photos, carousels,
  Reels and Stories, read and reply to comments, read DM threads and reply
  inside an existing one, and pull account and per-post insights. It cannot
  start a new DM to someone who has never written.
  Nothing customer visible goes out without her say-so, so the standing rule is
  unchanged: Claude drafts, Kat posts. What changed is that posting is now
  available if she ever asks for it.
  Publishing needs the image at a public HTTPS URL that Meta can fetch, or
  uploaded through the toolkit's file field. A local path will not work.
- **The posting cadence and the queue live in `content/content-system.md`.**
  Three posts a week (Sunday education, Tuesday plant spotlight, Thursday is
  Kat's freestyle slot), drawn from a bank of entries that have no post yet.
  When asked for content, read that file, draft the next weeks in the queue,
  and update its drafted log. Kat's own ideas always take priority over the
  queue; the queue is the floor for a week with no inspiration, not a cap.

### Pricing (HARD, added 2026-09-28)

**Kat sends the prices you give her straight to the customer, unedited.** She
said so on 28 September: "when clients ask me for something, I send them the
prices you give me, I don't question it." So a number in a chat reply is not a
suggestion, it is a live quote on a real plant. Treat it that way.

Three rules follow from that, and all of them were broken in one session:

1. **Never invent a price.** Every number handed over must come from one of:
   a price Kat set, a price a customer actually paid, or the documented rule
   applied to a known cost. If none of those exist for a plant, write
   **"needs your price"** and leave it empty. An empty row costs her one
   question. A guessed row costs her the difference on a sale.
2. **Say where each number came from.** Kat cannot sanity check a list that
   looks equally authoritative all the way down. Mark which lines are hers and
   which are derived, every time.
3. **Never apply a flat percentage across a list.** On 28 September an 18% cut
   was applied to every plant at once. It undercut three prices a customer had
   paid five weeks earlier, put one plant below its own cost, and set another
   above a price Kat had already cut. Price moves are per plant, against the
   cost list and the sold-at record.

The cost list, the 4x rule, the sold-at floors and the non-round-numbers rule
all live on the Notion **🏷️ Pink Leaf Selling Prices** page. Read it before
quoting anything. The rule there says TC cost × 4 **for a plant with no price
yet**: read that literally, because a plant Kat already priced is not a gap to
fill.

**Size tiers are the recovery when a quote went out too low.** Kat already
prices by specimen (Polly Pink grown 350 / baby 250; Watsoniana corm 620 /
TC 452). If a list price was set for a small plant and the customer picks the
most developed one, quoting that specimen at its own higher price is honest
and is existing practice. It is not the same as raising a price after the fact.

### Payments
- Chosen provider: **Meshulam (Grow)** (Israeli gateway; supports Israeli cards
  and Bit, and hosted payment pages / payment links that work from a static
  site). Updated 2026-06-15 by Kat; supersedes the earlier PayPlus pick.
- Current live flow: WhatsApp "Price Concierge" inquiry links plus bank transfer.
  Product schema carries real prices for Google rich results, but Offer URLs
  currently route to WhatsApp rather than a checkout.
- **Checkout built 2026-09-28, card switch off until Kat adds the key.** One
  checkout for plants and substrate. Card payment goes through Invoice4U
  (which clears via Meshulam and issues the receipt) from the Netlify
  Function `netlify/functions/checkout.mjs`. It prices orders from
  index.html's own tables on the server, via `netlify/lib/catalog.mjs`, which
  mirrors the parser in `tools/build_product_schema.py`: change both if the
  data shape changes. Switched on by the Netlify env var `I4U_API_KEY`;
  without it the card option is hidden and Bit/WhatsApp work as before.
  Shipping is `SHIPPING_FLAT_ILS` in index.html, read by page and server.
  **It is `null` since 2026-09-28:** the courier behind the 37 shekel rate
  stopped operating. With null, delivery orders are charged for the plants
  only and the studio arranges delivery. Put a number back only when Kat
  names a new courier and rate.
  The receipt email is the order record (order number, address, notes).
  Details and Kat's switch-on steps: `docs/competitor-audit-2026-09-28.md`.

### Deploy / dev environment notes
- **The live host is Netlify, not GitHub Pages.** `pinkleaf.co.il` is served by
  the Netlify project `pinkleaf` (team `kdtatt`,
  https://app.netlify.com/projects/pinkleaf). The domain's DNS does not point at
  GitHub Pages IPs.
- **Pushing to `main` does NOT deploy.** Checked 2026-09-19: the Netlify project
  is not building from the repo. Its published production deploy was created by
  a manual upload ("Deploy triggered by upload", no commit ref) dated
  2026-09-09. Every commit after that sat on `main` without reaching the site.
  Until someone links the repo in Netlify (Project configuration, Build and
  deploy, Link repository), a push has to be followed by an actual Netlify
  deploy.
- The old `pages build and deployment` workflow still runs green on every push
  to `main`. It proves nothing about the live site. Do not cite it as evidence
  that something shipped; check the Netlify project's current deploy instead.
- `netlify.toml` publishes the repo root with no build, so **everything in the
  repo is served**, internal files included. See the private data rules below
  before adding anything to the repo.
- **A cloud Claude session cannot deploy to Netlify.** Tried three times across
  2026-09-19 and 2026-09-23: the Netlify connector can read the project fine
  but every deploy upload returns 403 Forbidden from Netlify, not from the
  sandbox. The connection has read access only. Do not burn time retrying it.
  Deploy from the Mac instead: `npx netlify-cli deploy --prod --dir .` in the
  repo, or drag the folder onto the Deploys tab. The lasting fix is linking the
  repo in Netlify so a push deploys by itself.
- The sandbox also cannot reach `pinkleaf.co.il` at all (egress blocked), so a
  cloud session can never confirm what is live by fetching it. Check the
  Netlify project's current deploy instead, or ask Kat.
- The sandbox blocks most third-party hosts, so a cloud session renders the
  site WITHOUT the external CDNs a visitor gets. Tailwind was blocked this
  whole time, which means earlier visual checks were of an unstyled-ish page.
  Self-hosting Tailwind (above) fixed that for Tailwind; Firebase, confetti and
  Google Fonts are still blocked in the sandbox and load fine in production.
- Pushing from a cloud Claude session works fine.
- On the Mac, git sometimes gets a stuck `.git/index.lock` that blocks commits
  and pushes (this is what `fix_git_lock.command` on the Desktop clears). When a
  Mac session "can't push," that lock is the usual cause.

### Build scripts (run these, do not hand-edit what they own)

All of these run from the repo root and are idempotent.

- `python3 content/build-entries.py content/new-entries-YYYY-MM-DD.json`
  Wires a batch of encyclopedia entries into entries.json, standalone pages,
  footer links and the sitemap. Each entry needs a `short` field for the
  footer label.
- `python3 tools/build_product_schema.py`
  Regenerates all Product structured data from `ALL_STORE_ITEMS` and
  `ITEM_PRICES`, which are the store's source of truth. Run it after any
  price or status change, or the schema and the store drift apart again.
  Hand-written detail (description, SKU, Hebrew name) lives in the RICH map
  inside the script; price and availability deliberately cannot be set there.
- `python3 tools/build_index_pages.py`
  Regenerates `/encyclopedia/index.html` and `/articles/index.html` from
  entries.json and the article files. Run it after adding either.
- `python3 tools/build_hreflang.py`
  Maintains hreflang on the three genuine article translation pairs, and
  strips any hreflang that appears outside its managed block.
- `python3 tools/apply_seo_meta.py`
  Sets the Google title, description and og/twitter tags of every article and
  encyclopedia page from `tools/seo_meta.json`, and adds datePublished /
  dateModified from git. Edit the JSON, not the pages. Titles at most 60
  characters, Hebrew first on encyclopedia pages (Israeli buyers search in
  Hebrew). A new page is not done until it has a line in that JSON. Needs a
  full clone (`git fetch --unshallow`) for the dates.
- `python3 tools/optimize_images.py [--dry-run]`
  Caps photos at 1400px on the long edge, quality 85. Run it after adding
  images. Skips anything already under 150 KB.
- `sh tools/build_tailwind.sh`
  Regenerates `assets/pinkleaf-tailwind.css` from the utility classes used in
  index.html. Run it after adding a new Tailwind class, or that class will
  silently do nothing. The site used to load Tailwind's Play CDN, which their
  docs say is development only; it shipped about 360 KB of JS and built the
  stylesheet in the browser on every visit.
- `python3 tools/build_plant_db.py`
  Regenerates MASTER_DB in index.html from `tools/plant-db.csv`.
- `python3 tools/price_photo.py PHOTO PRICE [PHOTO PRICE ...] [--outdir DIR]`
  Puts a rose price badge on a plant photo for Kat to send. **Use this rather
  than writing the overlay by hand each time.** Her photos are Display P3 with
  an embedded colour profile; Pillow drops that profile on save unless it is
  carried across, and a file with no profile gets read as sRGB, which flattens
  every colour. A set of Atabapoense photos went out dim on 30 September for
  exactly this reason and the pinks, the whole reason anyone buys these plants,
  suffered most. The script preserves the profile and EXIF, and prints the
  worst pixel difference outside the badge so a regression shows as a number.

Gotcha worth knowing: the Humanizer hook rewrites long dashes inside any
file it touches, source code included. It once turned a script's own
dash-stripping helper into a plain-hyphen replacer. Build those characters
with `chr(0x2014)` rather than writing them literally or as an escape.

### Private data rules (HARD)

The site is a static HTML/JS build. Anything you put in `index.html` (or any
other file that gets deployed) ships to the public, even if it is not visually
rendered on the page. `view-source:` and browser dev tools reveal all of it.

Never write these into any file that deploys:

- **Acclimation / supply-chain state per plant.** Do NOT add fields like
  `acclimation: "in-transit"`, `"customs"`, `"deflasked"`, `"hardening"`,
  `"quarantine"` on store items, MASTER_DB entries, or anywhere else in the
  source. If a plant is not for sale, use `status: "coming"` and nothing more.
  The customer-facing badge only ever says "Coming Soon".
- **Cost basis / wholesale / margin numbers.** Retail price on offer schema is
  fine. Internal cost, MOQ, supplier invoice numbers, and margin math are not.
  A margin calculator (`tools/pricing-calculator.html`: base import cost,
  markup multiplier, acclimation loss buffer) was live on the site until
  2026-09-19 and has been deleted. It is still in the git history of a public
  repo, so treat the numbers in it as burned.
- **Customer names, phone numbers, addresses, WhatsApp threads, order history.**
  Aggregate anonymous stats are fine; individual records are never in source.
- **Supplier names on individual SKUs.** Min Hui, PlantHero, individual
  hobbyists, private growers. Fine in Notion, never in the deployed site.
- **Internal freight / customs / phyto costs and dates.**
- **Kat's personal contact info beyond what is already on the public page
  footer.**

If any past session left one of these in a deployed file, strip it. If you are
unsure whether something is safe to ship, default to NO and ask.

`netlify.toml` blocks `/tools/*`, `/content/*`, `/CLAUDE.md` and `/RESET.md`
with a 404, and `robots.txt` disallows the first two. That is a backstop for
working files, not a place to hide private data: the repo is public on GitHub,
so anything committed is readable there whether or not the site serves it.

Chat output rule: even when the user asks "is X live?", answer yes/no and give
a count. Do not paste the raw contents of the list into the chat unless the
user explicitly asks for the full contents. A chat transcript can be
screenshotted or shared; treat it like any other surface.

> If any decision above is wrong or out of date, correct it here so it stays
> correct for every future session.
