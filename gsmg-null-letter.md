# GSMG 5 BTC — "The Null Letter + the Unfiltered Room"

**Date:** 2026-11-12
**Brief:** Hazrat's standing brief ("unlock by any way... work nonstop" — meaning research + testing new named hypotheses only). Coordinator + 4 workers, all harnesses certified first (privkey-1 vectors both forms, Architect preimage, synthetic Salted__ witness, Bifid control where relevant). A valid PKCS7 padding alone is NEVER a hit — only an address match counts (prize escrow `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`, second escrow `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, or third-door oracle `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9`). Corrected reader throughout: floflo readings(), both address forms, both escrows + third-door, 6 blob variants (blob1–4 + blob2A/blob2B corrected readings).
**Result: 0 hits on all three oracles.**

## 1. The open question

Wave 2 of "Think like the creator" found the Bifid square key `DBIFHCEG` is the first 8 distinct letters of the 91-token prefix in first-appearance order (D0, B1, I3, F5, H7, C8, E11, G12, A16 → "DBIFHCEGA"). The 9th distinct letter 'A' is excluded. Three hypotheses were on record:

- **(a)** the creator used only the first 8 distinct letters;
- **(b)** 'a' is the null/zero symbol in the page's own digit conventions (a=0 in the dbbi/faed section, a=1 in the o=0/a=1..i=9 section) and is excluded as a padding/zero letter;
- **(c)** the key is the distinct letters of the prefix BEFORE the first 'a' appears (position 16 — the first 16 tokens contain exactly D,B,I,F,H,C,E,G).

Part 1 tests all three. Part 2 sweeps the unfiltered Telegram room — the 46,133 non-creator messages the Four Archives did not sweep (no creator reference, no puzzle keyword).

## 2. Part 1a — hypothesis (c) + hypothesis (a) gaps + keys as passwords

Script `gsmg_null_letter_c.py`, log `gsmg-null-letter-part1a.log`, summary `gsmg-null-letter-part1a.json`. Certification PASS (privkey-1 both forms, Architect preimage, synthetic witness, Bifid control DBIFHCEG/570 → BIF570 exactly).

### (c) Distinct letters before the first 'a' — 0 hits

13 sources, 8 new squares run through the full pipeline (segment at periods 91/285/570, prefix91 at 91, OBJ256 at 256, STREAM_B at 285; every output through all four shapes):

| Source | K_c | Status |
|---|---|---|
| segment | `F` | new, tested |
| prefix91 | `DBIFHCEG` | **control verified exactly**, not re-tested |
| whole stream, no z | `DBIFHCEG` | skipped — already tested (control key) |
| whole stream, with z | `DBIFHCEG` | skipped — already tested (control key) |
| agda | (empty — first token is 'a') | skipped with note |
| cfob | `CFOBDHGI` | new, tested |
| chunk-3 | `SH` | new, tested |
| chunk-4 | (empty — first token is 'a') | skipped with note |
| matrixsumlist | `M` | new, tested |
| lastwordsbeforearchichoice | `L` | new, tested |
| thispassword | `THISP` | new, tested |
| shabefanstoo | `SH` | same square as chunk-3, outputs deduped — 0 new candidates |
| Dualite base64 | `UFSDGVKXTPBCLQNZHO` | new, tested |

Corroboration worth noting: the whole 1,075-token stream's distinct letters before its first 'a' are ALSO exactly `DBIFHCEG` — the control key is not an artefact of the prefix alone.

### (a) First-8 gaps — 0 hits

First-8 squares for sequences wave 2 did not cover with first-8: agda `AGDFOHEI`, chunk-3 `SHABEFOU`, chunk-4 `ABQVXTPB`, Dualite `UFSDGVKX` — all 4 new, all tested, 0 hits. (Whole-stream first-8s are `DBIFHCEG`, skipped; cfob first-8 `CFOBDHGI` was already covered in (c).)

### Keys as blob passwords — 0 hits, and never tested before

Grep of all five prior scripts (`gsmg_think_like_creator_wave2.py`, `gsmg_dual_reading.py`, `gsmg_dual_reading_wave2.py`, `gsmg_closing_protocol.py`, `gsmg_archive_chain.py`): 9 occurrences of `DBIFHCEG`, all in the wave-2 script as Bifid-square keywords/comments/asserts; 0 in any password/blob context, 0 in the other four files. So both keys were tested here in forms [raw, hex-of-raw, sha256-hex] × digests (sha256, md5) × 6 blobs = 72 decryptions, 3 valid paddings (chance-level), 0 address matches.

### Part 1a totals

| Measure | Count |
|---|---|
| Distinct candidates | 66 |
| Hash-page checks (text shapes) | 66 |
| Hash-page checks (raw bytes) | 66 |
| Neighbour checks (scalar + direct first32/last32, both forms) | 396 |
| Blob decryptions | 2,448 (66×36 + 72) |
| Valid paddings (expected ~9.56 at 1/256) | 13 |
| Address matches | **0** |

Self-caught correction: the first run derived chunk-4's first-8 from the *unfiltered* first-appearance string, giving digit-contaminated `ABQVX0T8` (chunk-4 tokens include base64 fragments with digits/`+`/`/`). The worker fixed the script to reuse the replicated wave-2 values and re-ran the whole wave fresh; the corrected key `ABQVXTPB` was tested (6 new candidates, 0 hits). The erroneous first run also had 0 hits, so nothing was lost; only the corrected run's outputs are in the delivered log/JSON.

## 3. Part 1b — hypothesis (b): 'a' as zero/null

Script `gsmg_null_letter_b.py`, log `gsmg-null-letter-part1b.log`, summary `gsmg-null-letter-part1b.json`. Certification PASS (privkey-1 both forms, Architect preimage, synthetic witness, stream checks: even/odd 285 each, weave == BIF570, odd minus I/O == OBJ256; VIC positive control D149 → `INCASE…`). No pip reinstall needed.

### (i) Strip 'a' / 'a'→'0' — 0 hits

17 distinct candidates from 11 core units (P91, D149, `thematrixhasyou`, the three riddle answers, OBJ256, STREAM_B, BIF570, even/odd streams) × 2 variants, all four shapes. Dedupe notes: D149, R2 (`giveitjustonesecond`) and the even stream contain no 'a' (strip == zero-variant); odd-stream stripped/zeroed collide exactly with STREAM_B stripped/zeroed — the two differ only where one has 'A' and the other I/O. The single valid padding came from R1 strip-a (`jcquefresco`, raw password, sha256 digest, blob2B, 79-byte random-looking plaintext) — readings yielded no prize/escrow/third-door address.

### (ii) VIC checkerboard decode with 'a' as null — 0 hits

The exact wave-1 implementation was reused (exec of the file's own `vic_encode`/`vic_decode`, PREFIX91, mapping) — no reconstruction needed. Control reproduced: plain decode starts `PUAUDURBBUCOUARECUCARU…` (84 chars). PREFIX91 has only 3 'a's; variant A (remove 'a' tokens before mapping) and variant B (skip the 'a' digit in the digit stream) coincide exactly — each letter contributes one digit under the ord-96 mapping — giving one distinct output (`PUAUDURBBUCOUARUCUCARU…`, 84 chars, differing from the control at only a few positions). Both outputs tested in all four shapes: 2 candidates, 0 hits.

### (iii) OBJ256 as a base-23 number with 'a'=0 / 'a' skipped — 0 hits (new variant only)

ALPH23 + `base_n_to_bytes` reused verbatim from wave-1 section A. **Key finding: variant (1) [digit('a')=0, others 1–22 alphabetical] is numerically identical to the wave-1 control** (A is already 0 in the ALPH23 index mapping), so per instructions it was verified as control only, not re-tested as new. Control value: 145 bytes, 1158 bits, sha256 `35cd8be6…`. Variant (2) — skip all 15 A's → 241-digit string, 1090-bit integer, 137 bytes; tested as BE bytes, LE bytes, BE hex, LE hex: 4 candidates, 0 hits. (Caveat: wave-1 printed no standalone base-23 integer/bytes value, so the control could only be verified against the identical reused code path, not an independent published value.)

### Part 1b totals

| Measure | Count |
|---|---|
| Distinct candidates | 23 |
| Hash-page checks (text shapes) | 63 |
| Hash-page checks (raw bytes) | 23 |
| Neighbour checks (46 scalar + 64 direct) | 110 |
| Blob decryptions | 828 |
| Valid paddings (expected ~3.23 at 1/256) | 1 |
| Address matches | **0** |

Blob note (confirmed independently by both Part 1 workers): `blob2` (kit file) ≠ `blob2B` (corrected line1+line2) as raw bytes — the corrected readings genuinely differ from the file, so all six blob variants were distinct inputs as specified.

## 4. Part 2 — the unfiltered room (all 46,133 messages)

Source: `~/workspace/apple-repo/transcripts/puzzle-telegram-transcript.json` (58,476 messages, ONE chat). The Four Archives swept only the 10,078 filtered non-creator messages; this part sweeps the remainder with the same four-shape pipeline (`gsmg_archive_chat.py` functions reused). Remainder computed independently by BOTH workers from the same deterministic rule — counts matched exactly on both sides.

### Slice verification (both workers agree)

| Metric | Count | Expected |
|---|---|---|
| Total messages | 58,476 | 58,476 |
| Non-creator type='message' | 56,211 | 56,211 |
| Filter (a) creator-quote/mention/reply | 2,258 | — |
| Filter (b) keyword union | 8,626 | — |
| Swept (a)\|(b) | 10,078 | 10,078 |
| **Remainder total** | **46,133** | 46,133 |
| First half (worker A, ids 2–34,894) | 23,066 | 23,066/23,067 |
| Second half (worker B, ids 34,896–68,054) | 23,067 | 23,066/23,067 |

Messages with text: A 21,601 / B 21,318 (1,465 + 1,749 empty/photo-only skipped). Sentences: A 35,519 / B 32,958.

### Part 2a totals (first half)

Script `gsmg_null_letter_room_a.py`, log `gsmg-null-letter-room-a.log`, summary `gsmg-null-letter-room-a.json`. Runtime 111.2 s. Certification PASS.

| Measure | Count |
|---|---|
| Unique fragments (deduped within slice) | 43,752 |
| Hash-page checks (text shapes) | 43,752 |
| Hash-page checks (raw bytes) | 29,985 |
| Neighbour checks (both forms) | 43,752 |
| Blob decryptions | 1,575,072 |
| Valid paddings (expected ~6,153 at 1/256) | 6,151 |
| Address matches | **0** |

Known-only notes: the identified `21ef0533…` = SHA-256('anstoo') appeared twice ("AnsToo", sentence, mid 10724; "anstoo | a =1", adjacent pair, raw-bytes, mid 12782) — recorded as known, not hits.

### Part 2b totals (second half)

Script `gsmg_null_letter_room_b.py`, log `gsmg-null-letter-room-b.log`, summary `gsmg-null-letter-room-b.json`. Runtime 130.9 s. Certification PASS.

| Measure | Count |
|---|---|
| Unique fragments (deduped within slice) | 38,710 |
| Hash-page checks (text shapes) | 38,710 |
| Hash-page checks (raw bytes) | 29,302 |
| Neighbour checks (both forms) | 38,710 |
| Blob decryptions | 1,393,560 |
| Valid paddings (expected ~5,444 at 1/256) | 5,530 |
| Address matches | **0** |

Known-only note: fragment "anstoo" (mid 37005) matched `21ef0533…` in both text and raw-bytes shapes — already identified, recorded as known, not a hit.

Process note: worker B's first launch crashed ~0.5 s in on a `log(..., flush=True)` call (its `log()` helper takes no kwargs); the single call was fixed and the run relaunched — no data lost, the rerun recomputed everything from scratch. Slices are disjoint by construction (sorted remainder ids, split at len//2), so no overlap.

Caveat (both workers): fragments may overlap the already-swept filtered set (that set's fragment list was not saved to disk, so cross-set dedup was not possible); dedup is within each slice only.

## 5. Grand totals

| Oracle | Part 1a | Part 1b | Part 2a | Part 2b | **Total** |
|---|---|---|---|---|---|
| Candidates / fragments | 66 | 23 | 43,752 | 38,710 | **82,551** |
| Hash-page checks (text shapes) | 66 | 63 | 43,752 | 38,710 | **82,591** |
| Hash-page checks (raw bytes) | 66 | 23 | 29,985 | 29,302 | **59,376** |
| Neighbour checks | 396 | 110 | 43,752 | 38,710 | **82,968** |
| Blob decryptions | 2,448 | 828 | 1,575,072 | 1,393,560 | **2,971,908** |
| Valid paddings (expected ~11,609 at 1/256) | 13 | 1 | 6,151 | 5,530 | **11,695** |
| Address matches (real hits) | 0 | 0 | 0 | 0 | **0** |

Valid paddings overall: 11,695 observed vs ~11,609 expected at the 1/256 chance rate (ratio 1.007) — exactly chance-level noise. Every valid padding was fully decrypted and run through the floflo readings in both address forms against both escrows + the third-door oracle: **0 address matches**.

## 6. Verdicts

- **Hypothesis (c) — CLOSED.** The "before the first 'a'" rule gives 8 new squares (plus the control, which it reproduces exactly); all decryptions tested, 0 hits. The rule is real for the prefix (it yields the known key) but yields nothing new anywhere else it can be applied.
- **Hypothesis (a) — CLOSED for the gaps.** The only first-8 squares wave 2 had not covered are now tested (4 new), 0 hits. Combined with wave 2, every first-8 square derivable from the page's token sequences is now tested.
- **Hypothesis (b) — CLOSED, with one correction to the record.** Stripping 'a' / 'a'→'0' from every core unit, the VIC decode with 'a' as null, and the base-23 skip-a reading are all 0 hits. And the 'a'=0 base-23 variant is NOT a new test at all — it is numerically identical to the wave-1 standard mapping (A is already digit 0), so that reading was already covered by wave 1.
- **The unfiltered room — CLOSED.** All 46,133 remaining non-creator messages are now swept (82,462 fragments across both halves). No sentence, sentence pair, or whole message in the entire non-creator room — filtered or unfiltered — is the final blob password, a neighbours scalar, or a hash-page preimage, except the already-known `anstoo`. Combined with the Four Archives, **the whole non-creator chat (56,211 messages) has now been swept in full.**
- **DBIFHCEG / DBIFHCEGA as passwords — CLOSED.** They had never been tested as blob passwords before this wave; now tested, 0 hits.

## 7. What this closes, and what remains

**Closed by this wave:** why 'A' is excluded from the Bifid key — all three recorded hypotheses are now tested and negative; the exclusion is a property of the creator's rule with no exploitable reading found. The entire non-creator Telegram room. The Bifid keys as passwords.

**Still open (unchanged from before):** the insight/meaning; the first-appearance rule applied to token sequences OUTSIDE the SalPhaseIon page (other hash pages' content, the Decentraland scene's text — named in think-like-creator §5 but not tried); a new creator message (12h watch live); the 5 unknown hash preimages; the literal 213 archived scripts; cosmic_A; the 'tiny hint' (ambiguous); publication for fresh eyes (staged, awaiting Hazrat's word); the honest fallback that part of the answer may be personal knowledge of the creator.
