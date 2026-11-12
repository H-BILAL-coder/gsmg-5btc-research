# GSMG 5 BTC — XOR Triangle + 8 unknown hash preimages

**Date:** 2026-11-11
**Approved by:** Hazrat ("do it", on the pasted two-part synthesis).
**Result: Part 1 is already tested and negative in the public record.
Part 2 found TWO NEW hash preimages. Neither is the blob password.**

## Part 1 — The "XOR Triangle" — NOT new, already tested, 0 hits

The paste claims a "community consensus" to think triangular and build an XOR
triangle, with cosmic_A or the 98 buggy scripts' data as vertices/layers.
Checked against the local repos (AppleLamps `docs/ATTEMPT_LOG.md`,
`VERIFICATION_REPORT.md`):

- Exact serialized eight-row missing-node recurrence
  (`parent[j] = child[j] XOR child[j+1]`) — independently rerun over
  **18,432 layouts: zero internally consistent survivors.**
- Clue-bounded XOR-triangle, Cosmic-formula, Pascal/Witteveen and
  T5/HILLONE trail families — **8,771 unique scalars: 0 matches.**
- v75 second-door composition (six poster operands incl. the lower/upper
  91-cell triangle bit streams × four anchors × four rules) — 96 compositions
  → 2,304 AES + 192 scalar gates: **0 prize.**
- The phrase "XOR triangle" itself has **no formula** in the public record
  (earliest immutable comment 2025-12-25, puzzlehunt PR #68).
- The paste's two inputs do not exist: cosmic_A was never published, and the
  98 buggy scripts' dynamic candidates were never logged.

Verdict: the triangle was already tested in every exact form the community
could define, and all of them failed. The paste adds no new construction.
Closed unless someone publishes an actual formula with actual inputs.

## Part 2 — The 8 unknown hash preimages — TWO FOUND

Method (script `~/workspace/gsmg_preimage_hunt.py`): the full 64-hex hashes
were pulled from the Wayback CDX listing (13 paths; 12 hash pages + the
urlblob hex path). Candidate strings were extracted from the exact sources
the paste names — the live gsmg.io homepage source, the archived
`phase1verification.html`, the Decentraland audio audit JSON, and the
`decentraland.ipynb` — plus a base set of stage answers, page names and clue
words. Variations (case, spacing, reversal, affixes) and pairwise
concatenations were hashed and compared: **~1,784,285 candidate hashes, plus
8 byte-string candidates.**

### NEW — 2 of the 8 unknown preimages identified

- **`c1780cbb…` = SHA-256(`hopeisthequintessentialhumandelusion`)** —
  the Architect's "Hope is the quintessential human delusion" (short form).
- **`10d6a2c5…` = SHA-256(`humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness`)** —
  the full quote with the Architect's "Humph" prefix. (Found by testing the
  longer CDX page-name variants after the first hit.)

Pattern confirmed: the hash pages are SHA-256 of meaningful strings from the
creator's world — Matrix Architect quotes in these two cases. 6 of 12 hash
pages are now identified (89727c59, 4f7a1e4e, e24bd2c0, f9719d6d, c1780cbb,
10d6a2c5).

### Still unknown — 6 preimages

`0b0f37ec…`, `21ef0533…`, `673e3b1a…`, `a2aefdbb…`, `aca20ae7…`,
`c2eef34b…`. A further 581 Matrix-quote variants (other Architect lines,
Merovingian, Oracle, "choice is an illusion" forms, "humph" prefixes) were
tested against them: 0 more hits. The remaining six are not in that set.

### Correction to the record

`f9719d6d…` is the SHA-256 of the **raw 32 bytes** of the SalPhaseIon hash,
not of its hex text (verified directly: SHA-256 of the hex string gives
`db14474e…`). The meaning-pass wording ("SHA-256 of the SalPhaseIon hash
hex") was imprecise. This matters: preimages can be byte strings, not only
text — the hunt tested byte candidates too (raw hash bytes, the 128-byte
base64 path, the blob files): 0 hits.

### Are the two new quotes the blob password? NO — tested, 0 hits

Script `~/workspace/gsmg_architect_pw_test.py` (+ a follow-up for the blob2
variants): both quotes and their variations (39 forms vs the four blobs,
23 forms vs both corrected blob2 readings) with both digests, corrected
reader, both address forms, prize + second escrow + third-door check:
**0 valid paddings, 0 key readings, 0 hits.** The quotes are new words
from the creator's world and they confirm the hash-page pattern — but they
do not open any box.
