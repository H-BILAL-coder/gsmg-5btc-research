# GSMG 5 BTC — Close reading of the creator's own words

**Date:** 2026-11-12 (early hours)
**Approved by:** Hazrat (pasted pivot plan; same standing "work nonstop" brief).
**Result: 0 hits on all three oracles.**

## What was tested

84 candidates drawn from the creator's verified words (gsmg-creator-profile.md,
482 Telegram messages + the 2020 OP_RETURNs), each run against THREE oracles
(script `~/workspace/gsmg_close_reading.py`):

1. **Hash pages** (four shapes): 152 text + 84 byte hashes — 0 hits.
2. **Neighbors EC oracle** (SHA-256 → address vs P and 4 neighbours): 84 — 0 hits.
3. **Blob passwords** (SHA-256 hex, MD5 hex, raw string × SHA-256/MD5 EVP ×
   4 blobs + both corrected blob2 readings): 3,024 decryptions — 9 valid
   paddings, exactly the expected ~1/256 chance rate, **0 address matches**.
   The 9 paddings are random-padding false positives (plaintexts are garbage);
   a real hit requires the plaintext to yield the prize key, and none did.

Candidates included: "makethebestofeverything" (New Year "tiny hint"),
"giveyourselfyourselfandyourselfwillbegivenyourself" (July 16),
"geestveruimend" and "latetly" (July 16, his spellings),
"nevergonnagiveyouup" (the rickroll origin), "11092001" (Neo's passport
expiry — the only date he gives away), "freewill" / "strugle",
"thelastsceneofmrrobot", "salphation", "zeroedout", "hiddenlaptop",
"myclosefriendshavethebestchance", "somealreadyfoundit",
"the5btcwasnevertheactualprize", "onemicrostepfurther", "therabbitsnest…",
"thereisanotherdoor", "2hoursmax", "thefinalhint", "tinyhint".

## Close-reading notes (creator's words only)

- **The "tiny hint"**: 2019-05-18 he promised "a tiny hint at the start of
  2020, that will be the final hint"; the New Year message says "here's a
  'tiny hint'". The phrase recurs, but its content ("Make the best of
  everything") hits nothing.
- **"Give yourself yourself and yourself will be given yourself."**
  (2026-07-16, id 66961) — the most riddle-like line he ever wrote. Tested
  in all three oracles: nothing.
- **The hidden laptop** (2026-07-12, id 66568): "I have a hidden laptop
  which I haven't touched in years. On that thing... is the actual answer."
  Read plainly, the answer lives on a machine he no longer touches — which
  is consistent with the public material not containing it.
- **Close friends** (2026-07-12, ids 66573–66574, the only self-declared
  hint): "My close friends have the best chance of solving it (a few tried).
  But they don't have the skills some of you do." The answer needs personal
  knowledge of him, not just puzzle skill.
- **He no longer understands his own puzzle** (2026-07-12, id 66561): "I
  have these moment where I get into a frenzy and zone in with 800%. A day
  later I can hardly understand what I have done. And that is not a joke."
  And id 66568: "Most of you know the puzzle WAAAY better than me."
- **"Some already found it. And understood not to risk it..."**
  (2026-07-12, id 66600) — he does not say what "it" is.
- **"The '5' btc was never the actual prize. That was only a tiny fraction."**
  (2026-07-12, id 66593) — the BTC is a fraction of something bigger; the
  secret he "seriously wanted to share with the planet" (id 66592).
- **Correction to the plan's premise**: the Cosmic Duality PDF is the 1991
  Time-Life survey book, verified byte-for-byte — it is NOT the creator's own
  writing, and he never says "Cosmic" or "Duality" in Telegram. What he DID
  say about the book cover (2022-12-11): ".... That is very specific" /
  "If the puzzle is solved you'll see how scary specific that is". The book
  matters as an object, not as his text.
- **"humph"**: he typed the Architect quote himself in Telegram on
  2020-04-08 (id 3390), WITH "Humph." at the start — that is why the
  transcript scrapers missed it. The remaining six are likely typed the same
  way, from memory, with his quirks — which is why no script sweep can
  generate them.
