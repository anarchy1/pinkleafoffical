# Deploy handoff, 28 September 2026

For a session running on Kat's Mac. A cloud session cannot deploy: the Netlify
connection it gets is read-only and every upload returns 403 from Netlify.
The Mac has the real credentials.

The previous handoff (26 Sep, branch `claude/find-order-lists-chat-yxu11j`) is
done: it was merged and deployed on 26 Sep.

## The commands

Run from the repo root. Adjust the path if the repo lives elsewhere.

```sh
cd ~/pinkleafoffical

git fetch origin
git checkout main
git pull origin main

# main was an ancestor of this branch when it was pushed, so this is a
# clean fast-forward unless main moved since.
git merge origin/claude/pinkleaf-audit-redesign-jixs5e
git push origin main

# THIS is what publishes. Pushing does not.
npx netlify-cli deploy --prod --dir .
```

If git refuses to commit or push, a stale lock is the usual cause:
`rm -f .git/index.lock`.

**New this time:** the deploy now includes a Netlify Function
(`netlify/functions/checkout.mjs`). The CLI bundles it automatically from
`netlify.toml`. The deploy summary should say "1 function deployed". If it
says none, the card checkout will stay hidden but nothing else breaks.

## Switching card payment on

Card payment stays hidden until Netlify has the Invoice4U API key.

1. Invoice4U: Settings, API. Copy the organisation API key. No API section?
   Ask Invoice4U support to enable API access for the Meshulam terminal.
2. Netlify: Project configuration, Environment variables. Add `I4U_API_KEY`.
3. Deploy again (environment variables apply on the next deploy).
4. Place one small real order, for example one bag of substrate, and check
   that the receipt email arrives with the order number and address.

## What a customer will notice

- **Plants can be checked out**, not only sent to WhatsApp. The bag's main
  button is now "Checkout", with WhatsApp as the second button.
- **Shipping ₪37 anywhere in Israel** is shown in the bag and added at
  checkout (the registry's rate). Studio pickup is free.
- Payment choices: Bit first, then card (once the key is in), then bank
  transfer if bank details are ever filled in.
- On inner pages the logo is smaller, so the store's first screen shows
  plants. The home page is unchanged.
- The checkout buttons are a deeper rose, for readability.
- Plant links shared on Instagram or WhatsApp open the plant again. They had
  been landing on the plain store.
- After using dark mode, the logo no longer turns invisible.

## Needs Kat's yes before or right after deploy

1. Which phone number takes Bit. The checkout tells customers to Bit the
   public WhatsApp number; the registry lists a different number for Bit.
2. The checkout line: "if a plant sold moments before your order, the studio
   refunds in full".
3. A short cancellation policy before card payment goes live.

## Verified before handoff

- All inline scripts pass `node --check`; all `ld+json` parses.
- Headless Chromium, phone and desktop: store, bag, checkout, Bit via
  WhatsApp, card handoff and return page, language switch. Zero page errors.
- Checkout function tested against the real `index.html` with Invoice4U
  mocked: server prices match the store, tampered totals are refused,
  unavailable plants and from-prices are refused, bad name, phone and email
  are refused, and provider errors return cleanly.
- Not tested against Invoice4U itself. No key exists in the sandbox. Step 4
  above is that test.
