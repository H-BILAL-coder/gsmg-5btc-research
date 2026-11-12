# GSMG 5 BTC — StudyX "explanation" check

**Date:** 2026-11-11
**Approved by:** Hazrat ("check it", with the pasted StudyX text + links).
**Result: the paste is mostly wrong. Its one testable idea was tested: 0 hits.**

Source pasted by Hazrat: a StudyX AI homework answer claiming the puzzle is a
16x16 grid (256 pixels) mapping directly to a 256-bit private key, with
Blue/Yellow as modifiers, and that the address "currently holds no funds"
because the puzzles were "promotional stunts" with no solvable key.
Links pasted alongside: puzzlehunt issue #84, the StudyX page, a broken
"puzzlebalance" URL, Bitcointalk topic 5532424.

## Verdicts

1. **Grid is 14x14 (196 cells), NOT 16x16 (256). — FALSE.**
   Verified from the file just now (`gsmg_studyx_2bit.py`): white 85, black 87,
   blue 15, yellow 9 = 196 cells. The paste's whole premise (256 cells = 256
   bits) is wrong. The paste's own cited source contradicts it: issue #84's
   body says "Decoded the 14x14 image spiral → gsmg.io/theseedisplanted".

2. **The image does not contain the private key. — FALSE.**
   The 1-bit spiral reading (black/blue=1, white/yellow=0) decodes to the URL
   `gsmg.io/theseedisplanted` — the front door, not a key. Re-verified in the
   same run. The key sits behind the final yinyang gate; the image gives the
   door, the theme, the colour hint and the prize address, nothing more.

3. **"The address currently holds no funds" — FALSE.**
   Live mempool.space check 2026-11-11 ~20:03 CST: prize address
   `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` funded 876,003,172 sats, spent
   750,353,498 sats, balance **125,649,674 sats = 1.25649674 BTC**, 129 txs.
   Second escrow `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` = 3.75055856 BTC
   (verified this morning; the retry just now returned an empty response —
   mempool.space flaky, not a balance change). Total ~5.007 BTC, untouched
   since the creator's own halvings. Nothing was "moved" or "simulated".

4. **"Promotional stunts… no solvable, valid private key" — OPINION, not evidence.**
   The prize is real and on-chain. Issue #84 (2026-03-02, "why I believe it's
   unsolvable", 2 comments) is one solver's opinion after reaching the same
   dead end — it documents the chain4 route as exhausted, not a scam.
   Bitcointalk topic 5532424 ("Need help Puzzle GSMG.IO 5BTC", since
   2025-02-18) is a community discussion thread; no new claim surfaced in
   today's deep search. The broken "puzzlebalance" link is just a malformed URL.

5. **The 2-bit colour mapping (White=00, Black=01, Blue=10, Yellow=11) — TESTED, 0 hits.**
   Even though the premise is wrong, the idea was tested in every order it
   could mean (script `~/workspace/gsmg_studyx_2bit.py`): spiral + row-major
   orders; 2-bit streams (392 bits each); first 256 bits, last 256 bits,
   SHA-256 of the full stream; ink+colour and colour+ink concatenations.
   **18 candidate keys, checked against the prize address AND the second
   escrow, both address forms: 0 hits.** The colour distinction does not
   encode a second key layer — the coloured cells sit at the LSB position of
   each byte of the known URL, i.e. they are part of the 1-bit reading, not
   a separate channel.
