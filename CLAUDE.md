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

## Claude Code project brief (read first)

A fast orientation for any new session. Detail lives in the sections below.

### What Pink Leaf is
Rare and variegated plant studio in Ramat Gan, Israel. Owner: Kat. It imports
tissue-culture aroids (Alocasia, Monstera, Philodendron) from suppliers abroad,
acclimates them, and sells to Israeli collectors. Bilingual (Hebrew RTL /
English), currency ILS. Instagram `@pinkleaf.studio`. By-appointment studio plus
nationwide shipping in Israel.

### What we do here
Claude acts as the operations brain: pricing decisions, drafting customer replies
(Hebrew and English), building supplier sourcing lists, producing social content
(Instagram/Facebook cards, a product catalog, care guides), setting up payments,
and above all building a reliable inventory system.

### Where everything is stored
- Website and code: GitHub repo `anarchy1/pinkleafoffical`, on GitHub Pages, live
  at `pinkleaf.co.il`. Push to `main` goes live in about 60 seconds.
- Branches: `main` is the live site. `claude/checkout-card-plans-bcwo6h` is the
  feature/storage branch where social cards and generated content live, NOT the
  website.
- Business, financial, and personal data (money, inventory, client names, prices,
  orders): NEVER in the repo. It lives in Notion (the "Pink Leaf Business
  Overview" space: Full Inventory, Customer Orders, market research) and in chat.
- Durable project decisions: this `CLAUDE.md`.
- Channels: Kat handles WhatsApp, Instagram, and Facebook herself. Claude has NO
  access to those and works from Kat's screenshots. Claude does have Gmail,
  Notion, Google Calendar, and GitHub.

### Standing rules (do not break)
- Never use em dashes anywhere (see Writing style above).
- Never put business/financial/personal data in the repo.
- Never push to `main` (the live site) without asking first.
- Social/card content goes to the feature branch, never the live site.
- Never reveal stock quantities in public captions.
- Tell the truth, do not flatter, own mistakes plainly.
- The real inventory source of truth is the Notion inventory, NOT the repo's
  `SUPPLIER_TOTALS.md` (that file is planned/ordered quantities and has proven
  unreliable against the physical count).
- ALWAYS upload durable business info to Notion (the Pink Leaf Business Overview
  space): new products, orders, supplier details, prices, receipts, decisions.
  Do not let it live only in chat. If the Notion connector is disconnected at the
  moment, stage the content (scratchpad) and push it to Notion as soon as it
  reconnects. Financial/price data still never gets committed to the repo, it goes
  to Notion and chat only.

### Where we're at (snapshot, update as it changes)
- Mid a fresh physical inventory count, box by box, to establish a true baseline
  because the stored records kept disagreeing with reality. Goal: one live Notion
  inventory as the single source of truth that every sale registers against.
- A supplier shipment is stuck in customs; some requested plants are in that box,
  not lost.
- Catalog rebuild in progress: an earlier 9-page catalog had bugs (reversed
  Hebrew, wrong/placeholder/watermarked photos). A corrected sample page is proven
  (proper RTL Hebrew, clean tiles). It needs Kat's real photos to finish and must
  not go to customers until stock is confirmed.
- Payments: Invoice4u account created. Next, generate the hosted payment link
  inside the account, then wire it into the product Buy buttons. Do not go live
  until inventory is verified clean.

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
- LEADING PICK (2026-07-06): **Invoice4u**. Why it beats Meshulam for us: it does
  card + Bit checkout via an embeddable payment button / hosted payment page (works
  on our static GitHub Pages site, no server) AND auto-issues the tax invoice/receipt
  (חשבונית מס קבלה) on payment, which Meshulam does not. One system for payments +
  invoicing + expenses, cutting Kat's admin load and covering the 2026 חשבונית ישראל
  reform. FEES (from invoice4u.co.il, 2026-07): 60-day free trial; invoicing plan
  from ~19-21₪/mo on annual + VAT (up to 1,000 docs/mo); card clearing 0.9% monthly
  payout (0.8% above 50k/mo), 1.2% weekly payout, 1.4% for 24h payout. The 0.9% is
  low for Israel (typical 1.5-2.5%), and beats Meshulam, which also lacks the bundled
  invoicing. Confirm the exact plan tier on signup; needs merchant approval. Plan:
  Kat registers (free trial), generates a payment button/link, Claude wires it into
  the product Offer URLs (replacing the WhatsApp routing).
- Earlier pick: **Meshulam (Grow)** (2026-06-15, superseded PayPlus). Valid fallback
  if Invoice4u fees come back worse.
- Current live flow: WhatsApp "Price Concierge" inquiry links plus bank transfer.
  Product schema carries real prices for Google rich results, but Offer URLs
  currently route to WhatsApp rather than a checkout.
- Goal: integrate a real hosted checkout (payment page / payment links, since the
  site is static and cannot process cards server-side).

### Deploy / dev environment notes
- This repo deploys via GitHub Pages; pushing to `main` goes live in ~60s.
- Pushing from a cloud Claude session works fine.
- On the Mac, git sometimes gets a stuck `.git/index.lock` that blocks commits
  and pushes (this is what `fix_git_lock.command` on the Desktop clears). When a
  Mac session "can't push," that lock is the usual cause.

> If any decision above is wrong or out of date, correct it here so it stays
> correct for every future session.
