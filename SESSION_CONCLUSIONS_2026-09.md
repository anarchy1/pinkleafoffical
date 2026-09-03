# Pink Leaf , standing decisions & open items (Sept 2026)

Durable record so Kat never re-explains. Operational notes; financial/client
data stays in Notion, not here.

## PV numbering system (store plant IDs)
- Store plants use IDs like `PVxx`. 61 plants live; highest PV in use = **207**.
- The past mismatches (photo not matching plant) were NOT caused by the PV scheme.
  They were data-entry errors (a `plants/PVxx.jpg` file holding the wrong plant).
  Switching to a numeral system would NOT fix that; it just renumbers everything
  and risks new breakage.
- DECISION: keep PV. Fix correctness with ONE verified source of truth (the
  manifest: PV -> name -> photo), checked against Kat's folder. New plants get the
  next free numbers: PV208, PV209, ...

## Picture audit (the "do everything match" job)
- No old registration doc exists in the repo. Source of truth = Kat's computer
  folder (PV numbers + correct pictures) + the live store.
- Method: the PV manifest (pv_manifest.csv) lists every store plant, its name, and
  the photo file it uses. Kat compares it to her folder; flags wrong ones by PV ID;
  Claude swaps the exact `plants/PVxx.jpg`. All 61 currently HAVE a photo (none
  missing); the question is whether each is the RIGHT one.
- History note: store photos were mapped/corrected July 20-22, 2026 and untouched
  since. So current photos = that July state; wrong ones slipped that pass.

## Plant losses by supplier (Kat to calculate)
- Goal: attribute each dead plant to its supplier. Hypothesis: most losses came
  from Minhui's TC. If losses cluster on Minhui -> their TC quality is the problem
  and future orders with them are riskier. BUT the shipment before was perfect, so
  it could be the shipment, not the lab. Need the data to tell.
- Tracking: LOSSES_LOG gets a Supplier column. Kat fills it; we see the pattern.

## Website , open work
- SEO: goal was 5 keyword-strong articles per week. NOT happening; slacking.
  Restart: turn each care/knowledge post into a site article. Claude can draft them.
- Ordering system: shipping is now solid (plants arrive fine). BUT the site has no
  real checkout, people can't select a plant from photos and order. Currently routes
  to WhatsApp. Needs a proper "select plant -> pay" flow with the payment provider.
- Add new plants: pull from the new/supplier catalog (has plants the store lacks),
  assign PV208+, add names + prices + photos. Photos from Kat's folder or clean
  supplier images.

## Growing , Cuprea slow growth
- Cuprea is inherently slow, but the levers, in order: 1) bottom HEAT (25-28C, heat
  mat) = biggest accelerator; 2) stronger light, ~12h; 3) humidity 60-80%; 4)
  consistent light moisture in airy mix; 5) light regular feeding; 6) stop
  disturbing them. Suspect weak lamps + no bottom heat + cool space.

## Content
- Posting plants is random but views/likes are climbing. Ride the wave.
- What works: short plant reels, single hero shots, comparison carousels (Cuprea
  lineup, Watsoniana lineup). See CONTENT_PLAN.md.
- Value story: say it as VALUE (what you get: acclimated, selected, choose-your-own),
  not a price apology. TC price anchors retail buyers wrong; keep TC catalog for
  group-order growers only.
- IG stats: Claude cannot see Instagram (no connection). A connector (~$20/mo) would
  let Claude analyze stats. Until then Kat reports what's working.

## Positioning
- Pink Leaf is CHEAPER than comparable studios for a finished, acclimated,
  choose-your-own plant. State it (without naming competitors): "collector plants,
  acclimated and chosen by you, at honest prices."
