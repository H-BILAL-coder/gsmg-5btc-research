# GSMG 5 BTC — Preimage leftovers: repeated-element triples + S5×S5 pairs

**Date:** 2026-11-12
**Approved by:** Hazrat ("Yes, run the leftover pairs and triples").
**Result: 0 hits. None of the 5 unknown preimages is in this candidate universe.**

The two gaps the main preimage attack (`gsmg-preimage-attack.md`) explicitly left open:
repeated-element triples (it tested distinct-element triples only) and S5×S5
ordered pairs (out of scope as too large at the time). S6×S6 pairs remain out
of scope and were not started.

## Targets (SHA-256, the 5 still-unknown of the 12 hash-named Wayback pages)

- `0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32`
- `673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d`
- `a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1`
- `aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a`
- `c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625`

The other 7 of 12 are identified (genesis string → `89727c59…`, 1327-byte Cosmic
plaintext → `4f7a1e4e…`, `ourfirsthintisyourlastcommand` → `e24bd2c0…`,
SalPhaseIon raw bytes → `f9719d6d…`, ARCH1 → `c1780cbb…`, ARCH2 →
`10d6a2c5…`, `anstoo` → `21ef0533…`).

## Certification (mandatory, both workers, before any real run)

Both workers called the main attack's `certify()` (from
`gsmg_preimage_pairs.py`) and all controls passed:

- `sha256('anstoo')` = `21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f` ✓
- `sha256('GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')` = `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` ✓
- `sha256('hopeisthequintessentialhumandelusion')` = `c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046` ✓
- `sha256('causality')` = `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf` ✓ — pure hash-function control only; 'causality' has NO hash page among the 12.
- Synthetic positive: planted `'anstoo'` flagged as `21ef0533…`, decoy not flagged ✓ (the triples worker additionally tested it through the actual worker path with a patched target set).

## Element sets (reused exactly from the main attack, verified before running)

| Set | Size | Source |
|---|---|---|
| S1 CORE | 34 | `build_S1()` from `gsmg_preimage_pairs.py` |
| S2 OP_RETURN | 37 | `build_S2()` from `gsmg_preimage_pairs.py` |
| S3 SCENE/POSTER (union) | 35 | Union of the pairs worker's `build_S3()` (25) and the triples worker's `S3_ORIGINALS` (26), deduplicated by cleaned form — 10 new from the triples list. The main attack's two workers had built S3 slightly differently; the union is used here and recorded. |
| S4 CREATOR SENTENCES | 634 | `build_S4_S6()` from `gsmg_preimage_pairs.py` |
| S5 LINES | 2,645 | `build_S5()` from `gsmg_preimage_pairs.py` |
| S6 CHAT SHORT | 20,000 | `build_S4_S6()` from `gsmg_preimage_pairs.py` (38,150 unique before cap) |

Conventions (mirroring the main attack's triples/pairs workers): a candidate is
(a_string, b_or_None); shape A hashes a_string as-written; shape B hashes the
cleaned concatenation unless it equals an A form; dedup key = b if not None
else clean(a), skipped if in the prior hash-dictionary dedup set
(`build_dedup()`, 30,652 combos regenerated). Separators/cases by set class:
small sets (S1/S2/S3) `{'', '-', '_', ' ', '.', '/'}` × {lower, as-is};
S4/S5 `{'', ' ', '-'}` × {lower, as-is}; S6 `{'', ' '}` × {lower} only.
S4/S5/S6 elements are cleaned-only, so for those classes shape B always
equals the `""`-separator lower A-form and is skipped per the rules — correct,
not a bug.

## Part A — repeated-element triples (Worker 1)

| Class | Triples | Shape A | Shape B | Coverage |
|---|---|---|---|---|
| S1-ALL-SAME | 34 | 246 | 7 | 34/34 |
| S2-ALL-SAME | 37 | 324 | 14 | 37/37 |
| S3-ALL-SAME | 35 | 336 | 21 | 35/35 |
| S4-ALL-SAME | 634 | 1,902 | 0 | 634/634 |
| S5-ALL-SAME | 2,645 | 7,935 | 0 | 2,645/2,645 |
| S6-ALL-SAME | 20,000 | 40,000 | 0 | 20,000/20,000 |
| S1-TWO-EQUAL | 3,366 | 27,756 | 1,260 | 3,366/3,366 |
| S2-TWO-EQUAL | 3,996 | 41,112 | 2,478 | 3,996/3,996 |
| S3-TWO-EQUAL | 3,570 | 39,564 | 3,024 | 3,570/3,570 |
| S4-TWO-EQUAL | 1,203,966 | 3,611,898 | 0 | 1,203,966/1,203,966 |
| **Total** | **1,238,283** | **3,771,073** | **6,804** | |

Dedup skipped: 0 (expected — the prior dictionary's B×B×B triples are
distinct-element only, so no repeated-element cleaned form collides with it).
143 chunks, 2-process Pool, 55.4s, exit 0. Totals re-verified independently
from the JSON after the run.

## Part B — S5×S5 ordered pairs, distinct elements (Worker 2)

- Ordered pairs (X≠Y): **6,993,380** = 2645×2644, exactly as expected.
- Shape A: **20,980,140 hashes** (exactly 3 distinct forms per pair —
  separators `{'', ' ', '-'}` × cases {lower, as-is} collapse because S5
  elements are cleaned lowercase-only). Shape B: **0** (always identical to
  the `""`-separator shape-A form, skipped per the rules — correct, not a
  bug). Actual workload was ~21M hashes, not the ~49M estimated in the brief
  (which assumed distinct case forms).
- Dedup skipped: **0** — no S5×S5 form collided with the prior-dictionary
  dedup set.
- 16 chunks, 2-process Pool, 197.8s, 0 truncations. No known-page refinds.
- Dedup note: the main attack never tested S5×S5, so this class is new; a few
  pair strings may coincide with strings the main attack tested in S5×S1/S2/S3
  where an S5 element equals an S1/S2/S3 element — harmless re-hashing, not a
  gap (a hit there would already have been found).

## Grand totals

| | Candidates | Hashes (A + B) | Dedup skipped |
|---|---|---|---|
| Part A — repeated-element triples | 1,238,283 | 3,777,877 | 0 |
| Part B — S5×S5 pairs | 6,993,380 | 20,980,140 | 0 |
| **Total** | **8,231,663** | **24,758,017** | **0** |

## Verdict per target — all NO HIT

- `0b0f37ec…96ee32` — NO HIT
- `673e3b1a…356b0d` — NO HIT
- `a2aefdbb…18b0b1` — NO HIT
- `aca20ae7…5ed9a` — NO HIT
- `c2eef34b…76625` — NO HIT

No hit occurred, so no blob/EC/third-door verification was triggered (both
workers had the sha256sum-twice verification and four-shape follow-up wired in
for any hit). Boundaries held: no one contacted, nothing published, no re-run
of the main attack's tested classes.

## Explicitly NOT run

- **S5-TWO-EQUAL: 20,980,140 triples** (3×2645×2644) — ~~not run~~ **RUN
  2026-11-12 at Hazrat's word ("Yes, run the S5 two-equal set") — see
  `gsmg-preimage-s5-twoequal.md`: 20,980,140 triples, 62,940,420 hashes,
  0 hits.** (It had exceeded this wave's few-tens-of-millions cap.)
- **S6-TWO-EQUAL: 1,199,940,000 triples (~1.2B)** (3×20000×19999) — not run,
  ~2.4B hashes, far exceeding the cap.
- **S6×S6 pairs: 400,000,000 pairs (20,000²)** — not run, out of scope;
  Hazrat was told this is too large to finish sensibly.

## Correction to the brief (flagged by Worker 1, verified)

The dispatch brief stated S5 two-equal as **20,980,740** triples. The exact
product is **20,980,140** (2645×2644 = 6,993,380, ×3) — the brief figure was
600 high. The exact count is used above and in the JSONs. Related: the
brief's "~147M hashes" estimate for S5 two-equal assumed 7 hashes per triple,
but for cleaned-only S5 the distinct A-forms are 3 per triple, so the true
figure is ~62.9M — still over the cap, so the not-run decision is unaffected.

## What this does NOT close

The three not-run items above, and the same caveat as the main attack: the 5
preimages may be solver probes with random-ish preimages, or stage answers
built from material outside these corpora — in which case no dictionary of
this kind can find them.

## Files

- Record: `gsmg-preimage-leftovers.md` (this file)
- Triples: `gsmg-preimage-leftovers-triples.json`, `gsmg-preimage-leftovers-triples.log`, `gsmg-preimage-leftovers-triples-state.json`, `gsmg_preimage_leftovers_triples.py`
- S5 pairs: `gsmg-preimage-leftovers-s5pairs.json`, `gsmg-preimage-leftovers-s5pairs.log`, `gsmg_preimage_leftovers_s5pairs.py`
- Prior work: `gsmg-preimage-attack.md`, `gsmg-preimage-pairs.json`, `gsmg-preimage-triples.json`, `gsmg-preimage-wordlist.json`, `gsmg_hash_dictionary.py`

## Addendum 2026-11-12 — S5 two-equal now run

The S5-TWO-EQUAL item struck from the "Explicitly NOT run" list above was
run the same day at Hazrat's word. Record: `gsmg-preimage-s5-twoequal.md`
(script `gsmg_preimage_s5_twoequal.py`, totals
`gsmg-preimage-s5-twoequal.json`): 20,980,140 triples, 62,940,420
shape-A hashes, 0 shape-B, 0 dedup skipped, 921.6 s, **0 hits** on all 5
targets. The only preimage items still not run are S6-TWO-EQUAL (~1.2B
triples) and S6×S6 pairs (400M).
