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
- Owner: Kat. Visits by appointment. Nationwide shipping across Israel is active.
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

### Encyclopedia and social (standing rule)
- **Every new encyclopedia entry gets a social post.** Set by Kat 2026-09-19.
  An entry is not done when it deploys, it is done when the post copy exists
  alongside it. Write the post in the same commit as the entry.
- Format: one post per entry, Hebrew and English, both ready to paste, plus a
  platform, a visual suggestion and a goal. Follow
  `content/week-2026-04-10-social.md` and
  `content/encyclopedia-posts-2026-09-19.md`.
- Every post links to the entry page on `pinkleaf.co.il/encyclopedia/`.
- Claude cannot publish to Instagram from a session. It drafts, Kat posts.
- **The posting cadence and the queue live in `content/content-system.md`.**
  Three posts a week (Sunday education, Tuesday plant spotlight, Thursday is
  Kat's freestyle slot), drawn from a bank of entries that have no post yet.
  When asked for content, read that file, draft the next weeks in the queue,
  and update its drafted log. Kat's own ideas always take priority over the
  queue; the queue is the floor for a week with no inspiration, not a cap.

### Payments
- Chosen provider: **Meshulam (Grow)** (Israeli gateway; supports Israeli cards
  and Bit, and hosted payment pages / payment links that work from a static
  site). Updated 2026-06-15 by Kat; supersedes the earlier PayPlus pick.
- Current live flow: WhatsApp "Price Concierge" inquiry links plus bank transfer.
  Product schema carries real prices for Google rich results, but Offer URLs
  currently route to WhatsApp rather than a checkout.
- Goal: integrate a real Meshulam checkout (hosted payment page / payment links,
  since the site is static and cannot process cards server-side).

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
