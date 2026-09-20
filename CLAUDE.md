# Project instructions

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
- Site: `pinkleaf.co.il`, a static site hosted on Netlify (custom domain via
  CNAME). NOT GitHub Pages. See Deploy / dev environment notes below.
- Bilingual: Hebrew (RTL) and English (LTR). Currency is ILS (`₪`).
- Owner: Kat. Visits by appointment. Nationwide shipping across Israel is active.
- Instagram is `@pinkleaf.studio`. NOT `@pinkleaf.store` (that is an unrelated
  India dropship store; using it was a real past bug, fixed across 35 files).

### Business plans and personal strategy documents (HARD RULE, set by Kat 2026-09-20)
- A business plan, or anything like it, personal or strategic, not code, not
  site content, never gets written into this repo or pushed anywhere, draft
  or final, even to a feature branch, even with private numbers already
  stripped out. This repo is public. Writing a document like that here puts
  it online, full stop.
- Deliver documents like this directly instead, as a file handed to Kat in
  the session, so it stays on her device. Ask before committing anything
  like this. The "record durable decisions in the repo" practice above is
  for facts about the business and the codebase, never for documents like
  this.
- This rule exists because a business-plan draft got committed and pushed to
  a public branch here before Kat had seen it. It was removed, then the
  branch it was on was rewritten from scratch to clear it from history too,
  at her request. Do not repeat it, and do not go looking for it in old
  commits.

### Store direction (current plan)
- Replace the card/carousel "game" layout. It is overengineered for the need.
- Standardize the store into THREE categories: **Alocasia, Monstera, Philodendron.**
- Lay it out like a standard rare-plant niche store (clean product grid).

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
- Pushing from a cloud Claude session works fine.
- On the Mac, git sometimes gets a stuck `.git/index.lock` that blocks commits
  and pushes (this is what `fix_git_lock.command` on the Desktop clears). When a
  Mac session "can't push," that lock is the usual cause.

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
