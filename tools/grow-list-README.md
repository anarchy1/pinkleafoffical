# Grow list (private tracker)

This is Kat's internal list of plants in propagation. It is NOT the store. It
never gets shown to customers. It lives in the repo on purpose, so it survives
across sessions and stops disappearing into chat.

`tools/grow-list.csv` is the file. One row is one plant in propagation.

## Columns

| column            | what goes here                                                        |
|-------------------|-----------------------------------------------------------------------|
| `name`            | plant name, however you write it (e.g. Alocasia Frydek Albo)          |
| `type`            | `Corm` or `TC`. They acclimate on different clocks, so keep them apart |
| `qty`             | how many of this variety are in propagation                           |
| `acclimation_start` | the date it went into acclimation, as `YYYY-MM-DD` (e.g. 2026-06-10) |
| `category`        | `Alocasia`, `Monstera`, or `Philodendron`                             |
| `price_ils`       | price in shekels. Leave blank if not researched yet                   |
| `status`          | leave blank. Derived from the dates (see below)                       |
| `notes`           | anything: "hatched, rooting", "mother plant", number of corms, etc.   |

## How "ready" is estimated for corms

A corm's clock starts on `acclimation_start`. From there, a rough runway to a
sellable, rooted, hardened plant:

- Corm to first sprout and roots: about 2 to 6 weeks (warmth and humidity speed it up)
- Sprout to a stable potted plant ready to ship: another 4 to 8 weeks

So plan on roughly 6 to 14 weeks total, call it about 2 to 3 months, from the
acclimation start date. This is an estimate to set customer expectations, not a
guarantee. Your eyes on the actual plant always win; put the real state in
`notes` and the estimate gives way to that.

Default used for the store handoff: a corm is shown as "coming soon" until
about 10 weeks after `acclimation_start`, then flips to "available". Override
any single plant by writing `ready: YYYY-MM-DD` in its `notes`.

(TC plants run on a different, usually longer runway. When we start the TC
batch we set its own default here.)

## Workflow

1. Kat adds rows to `tools/grow-list.csv` (name, type, acclimation_start, category).
2. Claude researches `price_ils` for each and fills it in.
3. When a plant's runway is up, it moves to the store catalog
   (`tools/store-catalog.csv`) and `python3 tools/build_store.py` publishes it.

Nothing here touches the live site until step 3, and only when Kat says go.
