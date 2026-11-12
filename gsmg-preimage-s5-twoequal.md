# GSMG 5 BTC — S5 two-equal preimage wave

**Date:** 2026-11-12
**Approved by:** Hazrat ("Yes, run the S5 two-equal set").
**Result: 0 hits. None of the 5 unknown preimages is an S5 two-equal triple.**

The one leftover class the leftovers wave (`gsmg-preimage-leftovers.md`)
deliberately did not run: two-equal triples over S5 (it exceeded that
wave's few-tens-of-millions cap). The main attack tested distinct-element
triples only; the leftovers wave tested all-same triples for every set,
bounded two-equal triples for S1–S4, and the full S5×S5 pairs. This wave
closes the S5 two-equal gap.

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

## Certification (mandatory, before any real run)

`gsmg_preimage_pairs.certify()` — all controls passed through the exact
code path used by the run:

- `sha256('anstoo')` = `21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f` ✓
- `sha256('GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')` = `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` ✓
- `sha256('hopeisthequintessentialhumandelusion')` = `c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046` ✓
- `sha256('causality')` = `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf` ✓ — pure hash-function control only; 'causality' has NO hash page among the 12.
- Synthetic positive: planted `'anstoo'` flagged as `21ef0533…`, decoy not flagged ✓
- Worker-path synthetic positive: a real S5 two-equal triple form
  (X+X+Y, `''`-separator) was planted, patched into the target set, run
  through the actual `work_batch` worker function, and flagged; after
  unpatching it was not flagged ✓

## Element set (verified exactly before running)

| Set | Size | Source |
|---|---|---|
| S5 LINES | 2,645 | `build_S5()` from `gsmg_preimage_pairs.py` (deduped cleaned lines from `gsmg_mrrobot_fresco_lines.txt` + `gsmg_literary_canon_lines.txt`) |

Cross-check: the two source line files hold 2,811 non-comment lines in
total; cleaned dedup collapses some lines, giving exactly 2,645 — the
same set the main attack and the leftovers wave used.

## Universe (verified exactly before running)

- Ordered pairs of distinct S5 elements (X, Y): 2,645 × 2,644 = 6,993,380.
- Three two-equal forms per pair (X+X+Y, X+Y+X, Y+X+X).
- **Expected triples: 3 × 2,645 × 2,644 = 20,980,140.** The earlier brief's
  20,980,740 was 600 high; the exact count is used here.
- Separators `{'', ' ', '-'}` × cases {lower, as-is}; S5 elements are
  cleaned-only, so cases collapse and each triple has exactly **3 distinct
  shape-A forms** — expected shape-A hashes 3 × 20,980,140 = **62,940,420**.
- Shape B (cleaned concatenation) always equals the `""`-separator lower
  A-form for this class, so it is skipped per the rules — expected 0,
  correct, not a bug.

## Results

| | Count |
|---|---|
| Triples tested | 20,980,140 |
| Shape-A hashes | 62,940,420 |
| Shape-B hashes | 0 |
| Dedup skipped (A-forms / triples) | 0 / 0 |
| Chunks (2-process Pool) | 2,099 |
| Runtime | 921.6 s (~15.4 min) |
| Coverage | 20,980,140 / 20,980,140 ✓ |

Dedup skipped: 0 (expected — the prior dictionary's B×B×B triples are
distinct-element only, so no two-equal cleaned form collides with it; and
the main attack never tested two-equal triples, so there is no overlap
with its tested classes either). No known-page refinds.

## Verdict per target — all NO HIT

- `0b0f37ec…96ee32` — NO HIT
- `673e3b1a…356b0d` — NO HIT
- `a2aefdbb…18b0b1` — NO HIT
- `aca20ae7…5ed9a` — NO HIT
- `c2eef34b…76625` — NO HIT

No hit occurred, so no blob/EC/third-door verification was triggered (the
script had the sha256sum-twice verification and four-shape follow-up wired
in for any hit). Boundaries held: no one contacted, nothing published, no
re-run of the main attack's or leftovers wave's tested classes.

## What this closes / does not close

**Closed:** S5 two-equal triples. Combined with the main attack and the
leftovers wave, every repeated-element triple class is now covered except
S6 two-equal, and every S5 pair/triple class is covered.

**Still NOT run:**
- **S6-TWO-EQUAL: 1,199,940,000 triples (~1.2B)** (3×20000×19999),
  ~2.4B hashes — far too large for this wave.
- **S6×S6 pairs: 400,000,000 pairs (20,000²)** — out of scope; Hazrat was
  told this is too large to finish sensibly.

Same caveat as the main attack: the 5 preimages may be solver probes with
random-ish preimages, or stage answers built from material outside these
corpora — in which case no dictionary of this kind can find them.

## Files

- Record: `gsmg-preimage-s5-twoequal.md` (this file)
- Script: `gsmg_preimage_s5_twoequal.py`
- Run totals: `gsmg-preimage-s5-twoequal.json`
- Log: `gsmg-preimage-s5-twoequal.log`
- Prior work: `gsmg-preimage-attack.md`, `gsmg-preimage-leftovers.md`,
  `gsmg-preimage-pairs.json`, `gsmg-preimage-triples.json`,
  `gsmg-preimage-wordlist.json`, `gsmg-preimage-leftovers-triples.json`,
  `gsmg-preimage-leftovers-s5pairs.json`
