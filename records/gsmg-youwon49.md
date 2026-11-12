# GSMG 5 BTC — The 49-character middle block of the YOUWON alignment

**Date:** 2026-11-11
**Approved by:** Hazrat (bounded test; no new password generation, no contact
with the creator, no privatekeys.pw key/balance pages)
**Script:** `~/workspace/gsmg_youwon49.py` · **Results JSON:**
`~/workspace/gsmg-youwon49-results.json`
**Result: 0 HITS.**

---

## 1. STEP 1 — The alignment, verified independently

Both operands were recovered from repository artifacts (not pasted literals):

- **S91** — the 91-character `dbbi` stream from the SalPhaseIon page, uppercased.
  Source: `~/workspace/gsmg-esrever-results.json` (`prefix91`, itself extracted
  from the live SalPhaseIon page in the esrever run and verified there).
  Corroborated in the AppleLamps repo (`artifacts.json`,
  `SALPHASEION_PREREGISTRATION.md`, `prime_reinsertion_audit.json`).
  `DBBIBFBHCCBEGBIHABEBEIHBEGGEGEBEBBGEHHEBHHFBABFDHBEFFCDBBFCCCGBFBEEGGECBEDCIBFBFFGIGBEEEABE`
- **M91** — the Phase 3.2 VIC plaintext, uppercased. Source:
  `~/workspace/apple-repo/gsmgio-5btc-puzzle-master/phase32_classical.json`
  (`/vic/plaintext`).
  `INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE`

Difference D, letterwise `(S91 − M91) mod 26`, A = 0:

`VOZIJBDTIQBRGVEOMZNBCYOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA`

- **`YOUWON` at zero-based index 21 — CONFIRMED.**
- Split: head 21 / middle 49 / tail 21.
- All three published SHA-256 checkpoints reproduce exactly:
  - s91: `71fe46259e270c113529dfaded4b59c59a9dffd826a7202ab07fc498b6a2c5ca`
  - m91: `2fbfbef7442558f17ecc866a0b89ed491c41abc042df4d41452835adff09e9d3`
  - difference: `f17857308a886531637b33c9ddb92952206c286519412278ba9f836ffc69336e`

The blocks:

| Block | String |
|---|---|
| Head 21 (D[:21]) | `VOZIJBDTIQBRGVEOMZNBC` |
| **Middle 49 (D[21:70])** | **`YOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNX`** |
| Tail 21 (D[70:]) | `YDESKUOBXCAMVDJLQTSGA` |
| Middle after YOUWON (43, D[27:70]) | `XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNX` |

Note on the operand (from AppleLamps `docs/ATTEMPT_LOG.md` §14, verified this
session): v42's `v42_s91_middle_block.json` slices the **raw base-9 field**
`S91[21:70]` (`ihbeggege…`), not `D[21:70]` of the difference string — a
different operand. The block digested here is `D[21:70]`, the one the 21/49/21
split actually defines. v44 already tested `D`'s middle49 (and the flanks, the
middle-with-YOUWON-removed, the concatenated flanks, and the letterwise flank
combinations) as **direct 32-byte scalars** — 192 unique scalars, no prize
match, no valid padding. That is a different test space from this one: this run
tests the block under **cipher transformations as AES passwords** (both digests,
corrected reader), which v44 did not do.

The published continuation (`KMODEST` → `MODEST` → "YOU WON - BE MODEST") was
**NOT re-run**: it is gated and negative, and its last step was disclaimed by
its own author as "a convention not a forced step".

---

## 2. STEP 2 — Transformations applied

Base objects (11): M49, HEAD+M49 (D[:70]), M49+TAIL (D[21:]), FULL91 (D),
M43 (D[27:70], middle with YOUWON removed), HEAD21, TAIL21, FLANKS
(HEAD21+TAIL21), FLANKS_REV (TAIL21+HEAD21), plus two labelled extras — the
letterwise flank combinations FLANK_ADD (HEAD+TAIL mod 26) and FLANK_SUB
(HEAD−TAIL mod 26).

Per base object, 46 transforms:

| Transform | Count per base |
|---|---|
| direct (as-is) | 1 |
| reverse | 1 |
| Caesar shifts 1–25 (ROT-13 = shift 13, included) | 25 |
| AtBash | 1 |
| Bacon encode | 1 |
| Bacon decode | 1 |
| Polybius encode, DBIFHCEG square + default square | 2 |
| Bifid encrypt + decrypt, DBIFHCEG square + default square | 4 |
| Vigenère encrypt + decrypt, keys `matrixsumlist`, `lastwordsbeforearchichoice`, `thispassword`, `yinyang`, `halvings` | 10 |
| **Total per base** | **46** |

- **506 transform outputs** (11 bases × 46).
- Each output tested as a password in two case forms (as-is, lowercased), and
  in the two token concatenations
  `matrixsumlist`+`lastwordsbeforearchichoice`+⟨output⟩ and
  ⟨output⟩+`matrixsumlist`+`lastwordsbeforearchichoice` (lowercase throughout).
- **3,012 password phrases tested.**
- Sample: ROT-13(M49) =
  `LBHJBAKPCXJTOANKQTWTQHAAIZCNOGNSCNNKZWLYMOHJREQAK`.

---

## 3. STEP 3 — Test and result

Every phrase was tried as a password against all three blobs
(blob1 Phase 3.2 final, blob2 SalPhaseIon, blob3 Cosmic Duality) with BOTH
digests (SHA-256 + MD5) through the corrected reader (floflo `readings()` —
raw, first32, last32, sha256, hex→32, WIF — plus 2k/k/2 neighbours and the
8 split-key combinations for ≥64-byte plaintexts; both compressed and
uncompressed addresses vs the prize address
`1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` AND the second escrow
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`). Outputs that were exactly 32 bytes
or 64 hex chars were also checked directly as keys (none were).

| Measure | Count |
|---|---|
| Transform outputs | 506 |
| Password phrases tested | 3,012 |
| Decrypt attempts (3 blobs × 2 digests) | 18,072 |
| Valid-padding plaintexts | 53 (chance expectation ≈ 70.6 — no signal) |
| Key readings checked | 2,332 |
| Direct key checks | 0 |
| Long printable plaintexts (≥64 bytes) | 0 |
| **Hits** | **0** |

Self-checks passed (privkey-1 vectors exact; the tool's Bifid reproduces the
puzzle's confirmed Bifid plaintext byte-for-byte).

---

## 4. Verdict

The alignment is real and reproduces exactly from repository artifacts
(YOUWON at index 21, all three SHA-256 checkpoints match). The 49-character
middle block `YOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNX` — the part
of the alignment that was undigested as a cipher-transform/password space —
has now been digested through the identified tool's full menu, reverse,
Caesar/ROT-13, AtBash, Bacon, Polybius, Bifid, and Vigenère with the puzzle's
own token keys, in both case forms and both token concatenations, against all
three blobs with both digests: **0 hits**. Combined with v44's negative
scalar test of the same block, the middle block is now exhausted in both the
direct-scalar and the cipher-transform/password readings. The alignment
remains an unexplained structural observation (8.4% under 20,000 random
permutations — not a 1-in-a-million coincidence, but not proof); it yields no
key under any tested reading.
