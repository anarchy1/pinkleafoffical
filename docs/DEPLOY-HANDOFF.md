# Deploy handoff, 26 September 2026

For a session running on Kat's Mac. A cloud session cannot deploy: the Netlify
connection it gets is read-only and every upload returns 403 from Netlify.
The Mac has the real credentials.

## The commands

Run from the repo root. Adjust the path if the repo lives elsewhere.

```sh
cd ~/pinkleafoffical

# 1. get the branch
git fetch origin

# 2. move to main and make sure it is current
git checkout main
git pull origin main

# 3. merge. This is a clean fast-forward, verified: origin/main is an
#    ancestor of the branch, so no conflicts are possible.
git merge origin/claude/find-order-lists-chat-yxu11j

# 4. push
git push origin main

# 5. deploy. THIS is what actually publishes. Pushing does not.
npx netlify-cli deploy --prod --dir .
```

If step 5 asks to link a project, pick the existing `pinkleaf` project. Do not
create a new one.

## If git refuses to commit or push

A stale lock file is the usual cause on the Mac:

```sh
rm -f .git/index.lock
```

`fix_git_lock.command` on the Desktop does the same thing.

## What this ships

17 commits. The important ones, in order of why they matter:

**1. Kat's price corrections reach the live store for the first time.**
They had been stranded on a branch. The live store is still showing the old
round numbers. After this, the worked-out prices are live, for example
Alocasia Albo moves from 850 to 831, Aurea from 420 to 422, and so on across
the whole table.

**2. A supply-chain leak in the live file gets closed.** A CSS comment reading
"imports in transit, customs, or hardening" is in view-source on pinkleaf.co.il
right now. Nobody sees it on the page. It is still public.

**3. Google stops being told the wrong prices.** The product structured data
was advertising the old prices for 79 of 80 products while the store charged
the new ones. Regenerated with `tools/build_product_schema.py`.

**4. The acclimation gating is gone from the branch too.** It had survived
there as dead code. `CLAUDE.md` forbids shipping supply-chain state, and a key
name in public source is still that state.

**5. New: a collectible stickers page** at `/stickers/`, linked from the intro
buttons and the crawlable index.

**6. New: a seasonal theme system, switched OFF.** Sukkot, winter and
Tu BiShvat palettes are drafted but `SEASON_THEMES.enabled` is `false`, so the
site looks identical to today. Nothing seasonal appears until Kat approves a
palette and it is flipped on.

**7. Housekeeping:** `brand/` with the logo rules and assets, `brand/references/`
as the inbox for design material, the site health check written into
`CLAUDE.md`, and `/brand/*` blocked from being served.

## What a customer will actually notice

- Prices on the store change from round numbers to worked-out ones.
- Sold out plants can now read as sold out, but only once
  `STOCK_SHEET_CSV` has a Google Sheet URL. It is empty, so today this
  changes nothing.
- A new Hebrew stickers page, and a new button on the intro to reach it.

Nothing else is visually different. The seasonal themes are off.

## How to confirm it worked

1. `npx netlify-cli` prints a deploy URL. Open it.
2. Check the store shows 831 for Alocasia Azlanii Albo, not 850.
3. Check `pinkleaf.co.il/stickers/` loads.
4. View source and search for "in transit". It should not be there.

## Verified before handoff

- Fast-forward merge, no conflicts possible
- All five inline scripts pass `node --check`
- Both `ld+json` blocks parse, 83 offers, zero price mismatches against the store
- 80 store items, every purchasable option priced, no orphans, no duplicate ids
- Stickers page HTML well formed, renders correctly at 1100px and 390px
