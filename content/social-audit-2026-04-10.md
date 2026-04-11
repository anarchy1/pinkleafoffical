# Pink Leaf — Social Media Audit (2026-04-10, late night)

Comparison: what's actually been posted vs the content plan in `content/week-2026-04-10-social.md`.

---

## 🚨 CRITICAL BUG FOUND & FIXED

**The entire website was linking customers to the WRONG Instagram account.**

- ❌ WRONG: `@pinkleaf.store` — this handle belongs to "hey kash," an India-based beauty/cosmetic dropship business. Not you.
- ✅ CORRECT: `@pinkleaf.studio` — "Pink Leaf | Rare & Variegated Plants" — this is your real account (21 posts, 9 followers, Nurseries & Gardening Store category).

**Scope of the bug:** 35 files across the site were pointing to the wrong handle — every article footer, every encyclopedia entry, the homepage, the social config JS. Every visitor clicking "Instagram" on any Pink Leaf article was being redirected to a random beauty products store.

**Fix applied:** All 35 files updated in this session from `pinkleaf.store` → `pinkleaf.studio`. Needs deploy/commit to go live.

---

## 📱 INSTAGRAM (@pinkleaf.studio — the REAL one)

**Current state:**
- 21 posts total
- 9 followers
- 22 following
- Bio: "🌿 Rare & variegated plants · 🧬 Small-batch propagation & preservation"
- Category: Nurseries & Gardening Store

**Observation:** Instagram is actually your most active channel. 21 posts is meaningful volume. The content style visible in the grid includes:
- Plant photos (root development, variegation close-ups)
- TC/propagation photos (magenta grow light petri dishes)
- Aesthetic interior/lifestyle shots (plants in a room setting)
- Leaf macro shots

**Verdict:** Instagram is fine in terms of POSTING activity — Kat has been posting. The problem is that **nobody could find it** because the website was sending all traffic to the wrong handle. Fixing the link alone should improve follower growth.

**What the content plan (for week of 2026-04-10) needs you to post:**
1. ✅ TC myth-busting educational post
2. ⚠️ Alocasia Polly Pink Variegata product spotlight (₪350 high var, ₪199 regular)
3. ⚠️ BTS / 21-day hardening trust builder
4. ⚠️ "3 mistakes that kill TC plants" 5-slide carousel
5. ⚠️ Customer thank-you (3 plants sold this week)

None of this week's planned posts have been published yet based on the visible grid. The 5 drafts in `content/week-2026-04-10-social.md` are ready to go — you just need to copy/paste the Hebrew + English captions.

---

## 📱 FACEBOOK — Kat Dee personal profile (Pink Leaf brand)

**Current state:**
- Profile: Kat Dee (with Pink Leaf logo as profile picture)
- 746 followers · 131 following
- Category: Digital creator
- NOT a dedicated Pink Leaf business Page — this is the personal profile used as the brand's FB presence

**Posts found about Pink Leaf:**
1. **March 3, 2026** — "The wait is over. Welcome to Pink Leaf Botanical Studios. 🎀✨" — the launch announcement. Got 3 likes. Plant photo + Pink Leaf logo, with a snake coiled around the pot (artistic render).
2. **April 4, 2026** — Updated cover photo. 1 comment from "אבי מלכי" saying "תמונה מהממת" (stunning photo). Kat replied.

**That's it.**

One launch post + one cover photo update = the entire Pink Leaf Facebook presence over 5+ weeks.

**Verdict:** 🔴 **Facebook is dormant for Pink Leaf.** The plan calls for ~3-5 posts/week. Reality is 1 post in 5 weeks. Huge gap.

**Recommendation:**
- For now, continue using the Kat Dee personal profile (don't create a new Page — you'd lose the 746 existing followers and have to start from zero)
- Cross-post everything you post to Instagram onto this profile
- At minimum: repost the 5 drafts in `content/week-2026-04-10-social.md` this week

---

## 📋 WHATSAPP STATUS

Not audited this session (would need phone access). Based on the plan, WhatsApp Status should also mirror the weekly content. TBD when WhatsApp bot access is set up.

---

## 🎯 IMMEDIATE ACTIONS (for Kat tomorrow morning)

1. **Deploy the IG handle fix.** Commit the 35 file changes and push/deploy. Anyone who lands on an article today is being sent to a beauty store.
2. **Post this week's content.** The 5 drafts are fully written in Hebrew + English in `content/week-2026-04-10-social.md`. Copy-paste and publish to:
   - Instagram @pinkleaf.studio (feed + stories + reels)
   - Facebook Kat Dee profile (with Pink Leaf logo)
3. **Fix the bio on both accounts** to include the website `pinkleaf.co.il` prominently.
4. **Follow back the 22 accounts** you're already following on IG — that's easy mutual engagement and some of them probably would follow Pink Leaf back if pinged.

---

## 🔍 WHAT WE LEARNED

- The "no Google traffic" problem has a sibling: **no Instagram traffic either**, because every visitor trying to follow you was landing on the wrong account. It's a compounding zero-discovery problem.
- Instagram engagement exists (21 posts, someone's been working) — it just has zero inbound traffic from the site.
- Facebook on the other hand is genuinely under-posted.
- The content plan is solid and ready. The blocker is execution + the broken IG link.

---

*Audit generated 2026-04-10 ~12:55 AM local*
