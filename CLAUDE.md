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
- Site: `pinkleaf.co.il`, a static site on GitHub Pages (custom domain via CNAME).
- Bilingual: Hebrew (RTL) and English (LTR). Currency is ILS (`₪`).
- Owner: Kat. Visits by appointment. Nationwide shipping across Israel is active.
- Instagram is `@pinkleaf.studio`. NOT `@pinkleaf.store` (that is an unrelated
  India dropship store; using it was a real past bug, fixed across 35 files).

### Store direction (current plan)
- Replace the card/carousel "game" layout. It is overengineered for the need.
- Standardize the store into THREE categories: **Alocasia, Monstera, Philodendron.**
- Lay it out like a standard rare-plant niche store (clean product grid).

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
- This repo deploys via GitHub Pages; pushing to `main` goes live in ~60s.
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
- **Customer names, phone numbers, addresses, WhatsApp threads, order history.**
  Aggregate anonymous stats are fine; individual records are never in source.
- **Supplier names on individual SKUs.** Min Hui, PlantHero, individual
  hobbyists, private growers. Fine in Notion, never in the deployed site.
- **Internal freight / customs / phyto costs and dates.**
- **Kat's personal contact info beyond what is already on the public page
  footer.**

If any past session left one of these in a deployed file, strip it. If you are
unsure whether something is safe to ship, default to NO and ask.

Chat output rule: even when the user asks "is X live?", answer yes/no and give
a count. Do not paste the raw contents of the list into the chat unless the
user explicitly asks for the full contents. A chat transcript can be
screenshotted or shared; treat it like any other surface.

> If any decision above is wrong or out of date, correct it here so it stays
> correct for every future session.
