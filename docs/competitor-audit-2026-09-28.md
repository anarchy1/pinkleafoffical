# Pink Leaf against the best plant stores: audit, 28 September 2026

Asked for by Kat: research the biggest stores in the niche worldwide, find
where pinkleaf.co.il falls short, make the payment system actually work, and
compare the design with the most modern stores.

This file is public (the repo is public), so it names competitors and
features only. No prices beyond what the store shows, no suppliers, no
customers.

Sources were gathered through search results because the sandbox blocks most
store sites directly. Anything below marked "reported" is from a search
summary rather than the store's own page.

---

## 1. Who was compared

**Rare and collector stores, USA:** Steve's Leaves, Gabriella Plants,
NSE Tropicals, Ecuagenera USA, Logee's, Rare Plant Fairy.
**Mainstream plant stores, USA:** The Sill, Bloomscape, Hey Rooted.
**Europe:** GrowTropicals (UK, 2,900+ aroids), PLNTS.com (NL, has a RarePLNTS
line), Plant Circle (Berlin, the closest model to Pink Leaf: a small rare
boutique shipping EU-wide).
**Asia and marketplaces:** Aroid Market (Indonesia), Thai exporters,
Palmstreet (live auction app).
**Israel:** Ekzotica, PLANT IT, Little Planter, Deco Garden, Mashtelaonline.
None of them focus on rare aroids.

**The gap nobody in Israel fills:** a curated rare-aroid catalogue with a
real checkout. Globes reports that rare-plant trade in Israel runs mostly
through WhatsApp and Facebook groups. Pink Leaf is one working checkout away
from being the only proper store in that space.

---

## 2. What the best stores share, and where Pink Leaf stands

Ranked by impact for a boutique of about 80 plants.

| # | What the leaders do | Pink Leaf before today | Now |
| - | --- | --- | --- |
| 1 | Real checkout: card, Apple Pay, Google Pay, Bit | Plants: WhatsApp only. Card slot empty | **Built.** Plants and substrate in one checkout. Card goes live with one key (section 3) |
| 2 | Installments (תשלומים) on expensive items | None | Open. Invoice4U supports it (`Type: 2`); needs Kat's rule on when to offer |
| 3 | A written arrival guarantee with a claim window | Kat replaces dead plants in practice, but nothing is written | Open. Copy for Kat to approve |
| 4 | Exact-plant photos, or an honest "similar plant" label | Honest banner: photos show the mature variety, plant ships young | Keep the honesty. Next step is a real photo of the actual starter per listing |
| 5 | Heat and weather rules for shipping | Sunday/Monday dispatch, no Shabbat in transit | Already good. Worth saying on the product page, not only in the bag |
| 6 | Back-in-stock alerts | NOTIFY ME opens WhatsApp | Works. Lacks a list to message when a drop lands |
| 7 | Visible reviews | None | Open. Google reviews or screenshots of customer messages (with permission) |
| 8 | Size facts on every listing (pot, leaves, height) | Light and humidity percentages only | Open. Needs Kat's data |
| 9 | Care guide linked from each product | Encyclopedia exists but is not linked from products | Open. Small code job |
| 10 | Shipping cost shown before checkout | "Shipping quoted per order" | **Fixed.** ₪37 anywhere in Israel shown in the bag and checkout |
| 11 | Announced drops and limited releases | Instagram | Fine as is |
| 12 | Fast personal support | WhatsApp concierge | A real strength. Kept as the second button everywhere |
| 13 | Gift cards | None | Open. Easy once card checkout is live |
| 14 | Loyalty or club | None | Low priority |
| 15 | Filters by light, pets, difficulty | Category, price, search, sort | Open. Needs a pet-safety field per plant |

## 3. The payment system: what was wrong and what is built

**What was wrong.** A substrate-only checkout existed. Its card option read a
URL that was never filled in, so it never appeared. Plants, which are the
business, had no checkout at all: the bag could only open WhatsApp. Every sale
needed Kat to make a payment link by hand in Invoice4U.

**What is built now** (commit on this branch, not yet deployed):

1. One checkout for plants and substrate: order summary with photos, delivery
   (₪37 anywhere in Israel) or studio pickup, contact details, payment choice,
   and a clear total.
2. **Card payment through the account Kat already has.** Meshulam clears
   through Invoice4U today, and Invoice4U issues the receipt. A small server
   function (`netlify/functions/checkout.mjs`) asks Invoice4U for a hosted
   payment page for the exact order and sends the customer there.
   - Prices come from the store's own tables on the server. A price edited in
     the browser is ignored, and if a price changed while the customer was
     shopping, they are shown the new total before paying.
   - Plants that are not available, and "Mature Plant" from-prices, can never
     be charged online.
   - The receipt Invoice4U emails to Kat carries the order number, delivery
     address, phone and notes. That email is the order record, so nothing
     needs a database.
   - Card details never touch the site.
3. Bit and bank transfer still work as before: the order goes to the studio on
   WhatsApp with the payment instructions. Bit is offered first, per the
   standing rule.
4. After paying, the customer lands on a thank-you page with the order number.
   The copy follows the registry rule: payment closes the order and holds the
   plants, and the shipment leaves on Sunday or Monday.

**To switch card payment on, Kat does three things:**

1. In Invoice4U: Settings, API. Copy the organisation API key. If there is no
   API section, ask Invoice4U support to enable API access for the Meshulam
   terminal.
2. In Netlify: Project configuration, Environment variables. Add
   `I4U_API_KEY` with that key. For a first test, also add
   `I4U_QA_MODE` = `true` if Invoice4U gives a test account, otherwise skip it.
3. Deploy from the Mac as usual (`npx netlify-cli deploy --prod --dir .`).
   The deploy now also uploads the checkout function. Then place one real
   small order (for example one bag of substrate) end to end and check the
   receipt email.

Until step 2 is done the card option simply does not appear. Nothing breaks.

**Also available but not built:** Bit, Apple Pay and Google Pay inside the
same Meshulam page (Invoice4U flags `IsBitPayment`, `IsApplePay`,
`IsGooglePay`, which must be enabled on the terminal). Going direct to Grow's
own API is possible too, but it needs separate credentials, a Grow review of
the integration, and a separate receipt setup, so Invoice4U is the shorter
road.

---

## 4. Design against the most modern stores

What the best stores do in 2025 and 2026 (Baymard Institute, Nielsen Norman
Group, web.dev), and how Pink Leaf compares.

**Already good:** clean product grid, category tabs generated from the
catalogue, search, price filter, sort, result count, honest availability
badges, bilingual RTL/LTR, a strong restrained palette, dark mode, an
accessibility menu, self-hosted Tailwind.

**Fixed today:**

- **The first screen on a phone was all header.** The full logo sat on every
  page, so on the store the first plant appeared only after scrolling. Inner
  pages now show the whole logo at a smaller size (never cropped).
- **Floating buttons covered the bag.** The dark mode, accessibility and
  WhatsApp buttons sat on top of the bag title and its main button. They step
  aside while the bag is open.
- **The main buttons failed contrast.** White on the brand pink measured about
  2:1 (WCAG AA needs 4.5:1). The two buttons that move money are now a deeper
  rose from the same family.
- **Mixed languages in one sentence.** The bag showed English headings over
  Hebrew text. It now speaks one language at a time and follows the HE/EN
  switch.

**Still open, in order of impact** (all customer visible, so Kat decides):

1. **Hebrew has no web font.** The site loads Cinzel and Inter, neither of
   which has Hebrew letters, so Hebrew falls back to whatever the phone has.
   `assets/pinkleaf-enhancements.css` names Heebo as a fallback, but nothing
   loads it, so it only works on the rare device that has it installed.
   The modern Hebrew stores use Heebo, Assistant or Rubik for text, and Frank
   Ruhl Libre as a serif. This is the single biggest visual upgrade available.
2. **Size options as buttons, not a dropdown**, with the price updating on the
   button. This is Baymard's clearest product-page finding.
3. **A sticky add-to-bag bar on mobile product pages** that shows price and
   size once the main button scrolls away.
4. **Care icons plus a link to the encyclopedia entry** on every product page.
5. **Filters on mobile as one "Filter and sort" button** that opens a panel,
   instead of three stacked controls.
6. **A second photo on hover** (desktop) and swipe (phone), once there is a
   second photo per plant.
7. **Letter-spacing on Hebrew.** The Cinzel style spaces letters widely, which
   suits Latin capitals and hurts Hebrew. Partly fixed on the checkout
   buttons; the navigation still has it.
8. **Photos in WebP.** 221 WebP versions already exist in `plants/`, but the
   store grid loads the JPG versions.
9. **Firebase loads on every page** for the Lab quiz leaderboard. It could
   load only when the Lab opens.

---

## 5. Things found that need Kat, not code

1. **The Bit number on the site is not the one the registry lists for Bit.**
   The checkout tells customers to send Bit to the studio's public WhatsApp
   number. The Operations Registry records a different number for Bit and
   PayBox. If Bit is not registered on the WhatsApp number, customers' Bit
   payments fail. Kat to confirm which number takes Bit. The private number
   is not written into this public file.
2. **Oversize shipping.** The registry says a plant over 40x40 cm ships at
   double the fee. The online total charges the single ₪37 and says the studio
   confirms oversize with the customer. Kat can instead name which plants are
   oversize, and the checkout will charge the right fee.
3. **The crawlable text version of the store is stale.** The fallback block
   that search engines read lists one plant under "Available Plants", with
   prices that no longer match, while the store shows that plant as coming
   soon.
4. **Cancellation policy.** Israeli consumer law requires one for online
   sales, and whether live plants count as perishable is a question for a
   lawyer. The store should publish a short policy before card payment goes
   live.
5. **Refund wording at checkout.** The checkout says that if a plant sold
   moments before an order, the studio refunds in full. That is Kat's promise
   to make, so it needs her yes.
