# LUX'S METHOD — "The Dual Reading" (my own method, built from everything learned)

**Date:** 2026-11-12
**Asked for by:** Hazrat ("make your own method on the basis of this by which it can be solve it").
**Result: wave 1 + wave 2 both 0 hits — but the method found two real gaps and closed them.**

## The method

Three principles, each from something verified in this puzzle:

1. **DERIVE, DON'T GUESS.** Every solved stage's answer was the OUTPUT of a
   transformation applied to that stage's own artifacts — never a phrase
   guessed from a book or a film. The final answer X is likewise an output,
   not an input. So stop generating phrases; generate transformations of
   the puzzle's own material.
2. **THE RULE IS NON-TEXTUAL.** floflo's difficulty note (puzzle.json):
   "what would open the third door is a rule of the creator's from early
   2020 read on a non-textual object." The input is a non-textual object —
   the poster grid, the book cover, the Decentraland scene, the audio —
   and the rule is read off its STRUCTURE (positions, counts, geometry),
   not its text.
3. **THE OPERATION IS DUALITY.** Everything in the puzzle comes in pairs
   (two blobs, two escrows, two parcels, two stars, two colours, Half +
   Better Half, two Architect preimages, two Bifid streams). The answer's
   construction is a pairing operation — and the pairing operation never
   tested against ALL FOUR blobs was INTERLEAVING: weaving the two halves
   together, the way a yin-yang is drawn (two halves interlocked, not
   placed side by side).

## Wave 1 (script `~/workspace/gsmg_dual_reading.py`) — 259 candidates, 0 hits

- A. Interleavings (char-by-char weave) of all 11 core units in pairs, plus
  3-way weaves of the five core artifacts, plus half-interleaves.
- B. Non-textual readings as numbers: the poster grid's coloured-cell
  spiral indices (7,15,23,...,191 — an arithmetic progression, step 8),
  the counts (15 blue, 9 yellow, 24), the parcel coordinates (-41,-16 /
  -41,-17), the scene spawn/camera (0,0,0 / 8,1,8), the cover's two halves'
  centres (measured: upper ~(932,655), lower ~(1100,1593)), the audio
  (C2, 65 Hz, 5.198 s).
- C. The puzzle's own keys as passwords: the four blob salts (hex + raw),
  the six known page hashes (hex + raw 32 bytes), recursive hashing
  (SHA-256 of the raw SHA-256 of each stage answer).
- D. The 227-char Phase 3 concatenation as a blob password — SKIPPED in
  wave 1 (the literal string was not on disk); recovered in wave 2 via its
  verified digest (see below).
- Results: hash pages 0, neighbours 0, blobs 9,324 decryptions, 36 valid
  paddings (exactly the ~1/256 chance rate), 0 address matches.

## Wave 2 (script `~/workspace/gsmg_dual_reading_wave2.py`) — 63 candidates, 0 hits

While verifying the Bifid data, the method found a real gap. The puzzle's
Bifid step outputs 570 letters that split into TWO interleaved streams:
- ODD stream (285 letters, contains O and I): removing I/O gives the
  256-symbol object over a 23-letter alphabet. Already tested.
- EVEN stream (285 letters, ONLY the letters B, C, D, E): NEVER tested as
  a password on its own. The split was verified by computation:
  weave(even, odd) == the 570-letter Bifid output exactly. A 4-letter
  alphabet is a 2-bit encoding.
- Wave 2 tested: the even stream as a password (SHA-256 hex, MD5 hex,
  raw), reversed, concatenated/XORed with the odd stream, decoded as
  2-bit bytes under all 24 letter mappings (as passwords AND as direct
  32-byte keys via first32/last32), and the 227-char digest.
- The 227-char Phase 3 concatenation's SHA-256 digest is
  `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`
  (verified in apple-repo SOLUTION.md: the seven parts are causality,
  Safenet, Luna, HSM, 11110, main.cpp line 1616 raw hex literal, and the
  FEN position after the non-mating move Rc6+). Tested as a blob password
  in hex, raw-bytes, and recursive forms — it had only ever been tested
  as a private-key scalar / preimage before, never as an AES password.
- Results: hash pages 0, neighbours 0 (incl. direct-key checks), blobs
  2,268 decryptions, 6 valid paddings, 0 address matches.

## What the method establishes

- The even stream (the Bifid output's other half) is now tested and closed
  as a password, a direct key, and a 2-bit decoding.
- The 227-char digest is now tested as an AES password and closed.
- The interleaving operation, the non-textual numeric readings, and the
  puzzle's own keys as passwords are all closed.
- What the method does NOT close: the literal rule "read on a non-textual
  object" — if the rule is a reading of the Decentraland scene's 3D space
  or the poster's geometry that no one has yet stated, it is still out
  there. The method's next wave would be a geometric reading of the scene
  and the poster, not more strings.
