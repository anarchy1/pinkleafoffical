# Turning on the live stock feed

The store already knows how to read stock from a Google Sheet. The feature has
been sitting finished and switched off since it was built, because
`STOCK_SHEET_CSV` in `index.html` is an empty string and nobody wrote down what
the sheet is supposed to contain.

This is the missing half. Twenty minutes of counting, once, and the website
stops offering plants that are gone.

## Why it is worth the twenty minutes

Every stock mistake this project has had traces back to there being no current
count. In one day: Bambino Pink was proposed twice for a live customer quote
when there are none, because the corms never germinated. A dragon count was
doubled. A Regal Shield quoted to a customer turned out to be a guest plant.

The 13 September shelf count is the most recent record and it is already wrong.
A sheet Kat edits on her phone is the only version of this that stays true.

## Step 1: the sheet

Start from `pinkleaf-stock-sheet.csv`, which already has all 83 rows, one per
plant per size, with ids, variants and current prices filled in. Import it into
a new Google Sheet. **Only the `qty` column needs filling.**

| Column | Required | What it does |
| --- | --- | --- |
| `id` | yes | The plant's id, for example `PV82`. Already filled |
| `variant` | yes | The size or grade, for example `Albo`. Already filled |
| `qty` | no | How many you have. `0` marks it sold out. **Leave blank if you have not counted it** |
| `price` | no | Overrides the price in the code. The sheet wins |
| `status` | no | `available` or `coming`, to retire or launch a plant with no code change |
| plant name | no | Ignored by the site. It is there so the sheet is readable |

**Blank is not zero.** A blank `qty` means "not counted" and the plant stays on
sale. Only an explicit `0` marks something sold out. A plant with two sizes is
only hidden once both are counted and both are zero, so a half-finished count
can never hide something you actually have.

## Step 2: publish it as CSV

In the sheet: File, Share, Publish to web. Choose the sheet tab, pick
**Comma-separated values (.csv)**, publish, and copy the link.

It should end in `output=csv`. A normal share link will not work.

## Step 3: paste the link in

In `index.html`, find `const STOCK_SHEET_CSV = '';` and put the published URL
between the quotes. Then commit, push and deploy.

That is the whole change. One line.

## What the site does once it is on

- A plant with `qty` 0 across all its sizes shows **Sold Out** instead of ADD TO BAG
- A plant with one unit left shows **Last One**
- A price in the sheet overrides the price in the code, so a price change is one
  edit on your phone rather than a commit
- A `status` of `coming` or `available` moves a plant in or out of the store

If the sheet is unreachable or malformed the site logs a warning and falls back
to the built-in list. It never breaks the store, it just stops being live.

## One thing to be careful about

**The published sheet is public.** Anyone with the URL can read it. Keep it to
id, variant, qty, price and status. Do not add cost, supplier, customer names or
which plants are guests. That is the same rule as the repo, for the same reason.
