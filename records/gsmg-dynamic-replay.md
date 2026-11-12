# GSMG 5 BTC — Dynamic candidate replay (reconstructed)

**Date:** 2026-11-12
**Approved by:** Hazrat (pasted plan, items 1–2; item 3 already running as the 12h watch).
**Result: 0 real hits. Harness certified by a planted synthetic witness.**

## 1(a). Filter audit — the claim HOLDS in the record, but the scripts are not here

- The claim is verified in the primary source on disk:
  `floflo-repo/1-big-prizes/gsmg-io-5btc-puzzle/analysis/tested.md` (2026-07-28
  review, lines 5–8): "an appearance-based acceptance filter used in about
  46% of the folder's scripts (98 of 213) had been silently rejecting the
  correct answer shape for years, because it required decrypted plaintext to
  look like printable ASCII when the expected plaintext is raw key material."
  Confirmed in `analysis/leads.md` lead #3, which ranks the dynamic replay
  first precisely because row 8's literal replay is partial.
- The bug, exactly: an acceptance filter that judged a decryption by whether
  its plaintext looked like printable ASCII. The expected plaintext is raw
  32-byte key material, so a correct password whose decryption yielded binary
  key bytes was silently discarded.
- **Limitation, stated plainly:** the 213 scripts and the 1,017 archived
  scripts live in floflo777's private research folder. They are NOT on disk
  in this workspace — the on-disk floflo-repo has only 3 `.py` files
  (`tools/fig_pipeline.py`, `fig_stages.py`, `oracle.py`). So the scripts'
  own generation logic could not be inspected line-by-line or re-run
  literally. What IS verifiable on disk: the shipped `tools/oracle.py` now
  has the fix (`readings()` — sha256(pt), first32, last32, sha256(first64),
  hex→32/first32/last32, WIF — tries both digests, no printability judgment),
  and its `--selftest` passes all 5 checks (on-chain pubkey HASH160, phase-2
  blob under sha256("causality"), wrong-password rejection, MD5-fails-on-phase-2,
  blob shape). The same bug pattern (printable-ratio thresholds) is visible in
  on-disk audit scripts (`apple-repo/scripts/second_door_yellow_red_audit.py`
  "structured" = printable_ratio ≥ 0.85; `second_door_yinyang_joint_audit.py`
  printable ≥ 0.75), but those are audits, not the 213 scripts.
- Row 8 already replayed 116,043 literal strings harvested from the archive
  (0 match). This replay therefore RECONSTRUCTS the dynamic pattern classes
  leads.md names — "token concatenations, permutations of decoded fragments,
  and chained transforms (for example, applying a Vigenere step and then a
  substitution step in sequence)" — from the validated Phase 3 inputs.

## 1(b). Reconstructed pipeline (script `~/workspace/gsmg_dynamic_replay.py`)

Units: P91 (91-letter phrase), D149 (149-digit string), BK (thematrixhasyou),
R1 (jacquefresco), R2 (giveitjustonesecond), R3 (heisenbergsuncertaintyprinciple).
P91 and D149 do not appear in any kit stored file (grep count 0), so even the
units themselves were never in the kit's Stream A.

| Class | Pattern | Count |
|---|---|---|
| A | Ordered k-tuples k=3..6 of the 6 units, seps {"","-","_"," ","/","."} (k=2 pairs EXCLUDED — floflo row 16 covered ordered pairs of stage answers) | 11,520 |
| B | Transformed-unit pairs (≥1 non-identity transform): reverse, ROT13, Atbash, Beaufort(BK), Vigenere(BK), hex, base64; seps {"","-"} | 3,724 |
| C | Chained double-transforms on single units | 198 |
| D | The 256-symbol object / 285-letter stream / 570-letter Bifid output as BLOB PASSWORDS (whole + first/last 32/64/128 + reversed + 20 spatial reading orders of the 16×16 grid) — floflo rows 1–5 tested these as direct KEYS, never as passwords | 38 |
| E | D149 special forms (reversed, "-" every 3 digits, digit-pairs→bytes, hex, 1→I/0→O) | 3 (2 of the 5 forms already present under an earlier class label) |
| **Total unique candidates** | | **15,483** |

## 1(c). Feasibility gate

15,483 candidates ≪ 50,000,000. Gate passed. Full test run.

## Test (corrected reader, no printability judgment)

- Password forms {SHA-256 hex, MD5 hex, raw} × digests {SHA-256, MD5} ×
  blobs {blob1, blob2, blob2A, blob2B, blob3, blob4} (both blob2 readings,
  issue #122). Last-block PKCS7 pre-check, full decrypt on valid padding,
  then floflo `readings()` + 2k/k/2 neighbours + split-key combinations
  (a+b, a−b, b−a, a XOR b, 2a, a/2, 2b, b/2) for ≥64-byte plaintexts, both
  address forms, both escrows. A hit requires an address match, never
  padding alone.
- **650,286 decryptions, 2,583 valid paddings (0.397% — the expected
  ~1/256 chance rate), 0 real hits.** Runtime 116.3 s.
- **Certification (witness):** a synthetic Salted__ blob was encrypted with
  a known password from class A (P91+BK+R1, "" separator) and a known
  32-byte key (0x11×32), and run through the exact same code path. The
  harness recovered it (2 readings: first32 and last32). Without that
  witness the negative would be uncertified per the repo house rules; with
  it, the negative is certified. The first run of this script had a witness
  bug (the witness address was never a match target, so it could not be
  found) — it was fixed before the reported run, and the fix is recorded
  here so the earlier 0-hit run is not cited as certified.
- Harness self-checks that passed before the run: privkey-1 compressed
  `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` and uncompressed
  `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`; known hash preimage
  `hopeisthequintessentialhumandelusion` reproduces; all 6 blobs load as
  `Salted__`; phase-2 blob decrypts under sha256("causality") and contains
  "keymakers"; floflo `tools/oracle.py --selftest` OK (5/5).
- Hits record: `~/workspace/gsmg-dynamic-replay-hits.json`
  (candidates 15,483; attempts 650,286; valid_padding 2,583;
  witness_found true; real_hits []).

## Conclusion

The reconstructed dynamic patterns — multi-unit concatenations, transformed
pairs, chained transforms, and the final-page objects as passwords — contain
no key to any of the four blobs under either digest. The dynamic-replay lead
as reconstructed here is closed. What it does NOT close: the literal
generation logic of the 213 archived scripts themselves, which remain in a
private folder this workspace does not hold.
