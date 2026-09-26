# Pink Leaf - Content System

The point of this file: posting should not depend on Kat remembering to post,
or on Kat inventing the idea that day. The ideas already exist. This is the
machine that turns them into a schedule.

Set up 2026-09-21.

---

## The problem this solves

20 encyclopedia entries exist. 5 have ever had a post written. 15 do not.
That is roughly four months of educational content already researched, already
bilingual, already paid for, that never reached an audience because the
pipeline ran on memory.

## The cadence

Three posts a week, on the Israeli week.

| Day | Slot | Source | Who drafts |
|---|---|---|---|
| Sunday | Education | One encyclopedia entry | Claude |
| Tuesday | Plant spotlight | One plant care-guide entry or one SKU | Claude |
| Thursday | Studio / freestyle | Kat's own material: a plant that just landed, a repot, a customer photo, whatever she feels like | Kat |

Sunday and Tuesday are the floor. They come out of the bank below and require
no new ideas from anyone. Thursday is Kat's, and it is the slot where the
spontaneous stuff lives.

**Kat's freestyle always wins.** If she wants to post something on a Sunday,
it goes out and the queued entry slides one week. The queue exists so that a
week with no inspiration still has three posts, not so that a week with
inspiration gets fewer.

## The bank

Education entries with no post yet, in queue order:

1. `water-quality-ph-aroids` - Water quality and pH, why tap water is not neutral
2. `engineered-substrates` - Engineered substrate, why potting soil kills
3. `leaf-symptom-diagnosis` - Reading leaf symptoms
4. `variegation-types` - Types of variegation, the genetics
5. `atmospheric-data-vpd-ppfd` - VPD and PPFD
6. `semi-hydro-leca-guide` - Semi-hydro LECA
7. `plant-health-indicators` - 5 signs a plant is thriving
8. `post-flask-sterilization` - Post-flask sterilization
9. `repotting-tc-plant` - Repotting a TC plant
10. `investment-variegation-stability` - Buying correctly, genetic stability

Plant spotlight entries with no post yet:

1. `plant-monstera-albo-variegata` - Monstera Albo
2. `plant-alocasia-polly-pink-variegata` - Alocasia Polly Pink
3. `plant-philodendron-jose-buono` - Philodendron Jose Buono
4. `plant-alocasia-heart-balloon` - Alocasia Heart Balloon
5. `plant-alocasia-macrorrhiza-variegata` - Alocasia Macrorrhiza Variegata

That is 10 Sundays and 5 Tuesdays of content that needs zero new thinking.

## The schedule

| Week of | Sunday (education) | Tuesday (spotlight) |
|---|---|---|
| 2026-09-27 | water-quality-ph-aroids | plant-monstera-albo-variegata |
| 2026-10-04 | engineered-substrates | plant-alocasia-polly-pink-variegata |
| 2026-10-11 | leaf-symptom-diagnosis | plant-philodendron-jose-buono |
| 2026-10-18 | variegation-types | plant-alocasia-heart-balloon |
| 2026-10-25 | atmospheric-data-vpd-ppfd | plant-alocasia-macrorrhiza-variegata |
| 2026-11-01 | semi-hydro-leca-guide | (SKU spotlight, Kat picks) |
| 2026-11-08 | plant-health-indicators | (SKU spotlight, Kat picks) |
| 2026-11-15 | post-flask-sterilization | (SKU spotlight, Kat picks) |
| 2026-11-22 | repotting-tc-plant | (SKU spotlight, Kat picks) |
| 2026-11-29 | investment-variegation-stability | (SKU spotlight, Kat picks) |

Already written and unposted, use these first or slot them anywhere:
`fertilizing-rare-aroids`, `pests-thrips-mites-quarantine`,
`alocasia-corm-propagation` (see `content/encyclopedia-posts-2026-09-19.md`),
`choosing-your-substrate`, `first-48-hours-new-plant`
(see `content/posts-2026-09-23.md`), and `are-aroids-toxic-pets-children`,
`how-much-light-israeli-apartment`, `growing-aroids-outdoors-israel`,
`is-it-really-rare-buying-check` (see `content/posts-2026-09-24.md`).

Run `choosing-your-substrate` first. The substrate store now has a working
checkout behind it, so it is the first post a reader can act on without
opening WhatsApp.

## The job

Any session, when asked for content, does this without being told how:

1. Read this file. Find the next week with no drafted post.
2. Draft the Sunday and Tuesday posts for the next 2 to 4 weeks, one file per
   batch in `content/`, named `posts-YYYY-MM-DD.md`.
3. Each post: Hebrew and English, both paste ready, plus platform, visual
   suggestion, goal, and the link to the entry page.
4. Mark the rows below as drafted, and commit.

Standing rule from CLAUDE.md still applies: a new encyclopedia entry gets its
post in the same commit as the entry, and it goes to the front of the queue.

## Drafted log

| Batch file | Covers | Drafted |
|---|---|---|
| `content/week-2026-04-10-social.md` | tissue-culture, 21-day-hardening-sop, Polly Pink spotlight | 2026-04-10 |
| `content/encyclopedia-posts-2026-09-19.md` | fertilizing, pests, corms | 2026-09-19 |
| `content/posts-2026-09-23.md` | choosing a substrate, first 48 hours | 2026-09-23 |
| `content/posts-2026-09-24.md` | toxicity, light, outdoors in Israel, is it really rare | 2026-09-24 |

## What is still manual, and honestly

Claude cannot publish to Instagram. It drafts, Kat posts. If that becomes the
bottleneck, the next step is a scheduler (Meta Business Suite handles Instagram
and Facebook scheduling for free), and the batch above is written far enough
ahead to load a month at a time.
