# GSMG 5 BTC — Preimage attack: dedicated dictionary attack on the 5 unknown hash pages

**Date:** 2026-11-12
**Approved by:** Hazrat ("Yes, run the preimage attack").
**Result: 0 hits. None of the 5 unknown preimages is in this candidate universe.**

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

## Certification (mandatory, all three workers, before any real run)

Every worker proved the exact code path finds known preimages, and planted a
synthetic positive (`anstoo` in a test stream, flagged; decoy not flagged):

- `sha256('anstoo')` = `21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f` ✓
- `sha256('GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe')` = `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` ✓
- `sha256('hopeisthequintessentialhumandelusion')` = `c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046` ✓
- `sha256('causality')` = `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf` ✓

**Correction (found by hand-checking before dispatch, recorded in all three
workers' JSONs):** `sha256('causality')` = `eb3efb51…` is a pure
hash-function control only — 'causality' has **NO hash page among the 12**
and was NOT treated as a target. The brief's phrasing ("'causality' → its
page hash") was inaccurate; the control still proves the hashing path.

Worker 1's first launch failed on a harness assert (its S1 original for the
hope-phrase cleaned to `hopeitisthe…` instead of the canonical
`hopeisthe…`); it fixed the original and re-ran from scratch — certification
passed on the second run. One transient exec failure (exit 1) was recorded
during the triples worker's run; the worker completed and its JSON totals
were verified independently — no effect on the result.

## What was already covered (not re-run)

- Singles and same-source adjacent concatenations from every prior sweep
  (creator's 482 messages, the full 56,211-message non-creator room, Matrix
  trilogy, Mr. Robot, Fresco, Cosmic Duality book, Bitcoin whitepaper,
  literary canon, poster text, OP_RETURN payloads, Decentraland text) — every
  fragment from all of those was already hashed against these pages.
- The hash dictionary (`gsmg-hash-dictionary.md`): 30,652 cross-domain
  combinations (sets A 29 / B 26 / C 17 / D 16; pairs with separators
  {"", "-", "_", " "}; B×B×B triples with "" separator), 153,260 hashes,
  0 hits. This attack deduplicates against that exact set (regenerated from
  `gsmg_hash_dictionary.py` by all three workers; the dictionary's 30,652
  combinations were reproduced exactly).

## Candidate universe — NEW relative to the hash dictionary

### Element sets (measured, built deterministically from on-disk sources)

| Set | Size | Contents |
|---|---|---|
| S1 CORE | 34 | P91, D149 (149-digit string), thematrixhasyou, 3 riddle answers, causality, flower sentence, seed URL, 227-char digest `1a57c572…`, ARCH1, ARCH2, HALF/BHALF hex, yinyang/yingyang, dualite, salphaseion, meganigma, whiterabbit(s), gsmg/gsmgio, phase32/phase3, matrixsumlist, lastwordsbeforearchichoice, thispassword, ourfirsthintisyourlastcommand, anstoo, answertoo, 227/149/91 |
| S2 OP_RETURN | 37 | Distinct ASCII OP_RETURN payloads from `gsmg-archive/prize_txs.json` + `escrow2_txs.json`, cleaned 3–60 chars (incl. `causalitytranscended`, `fanstoo`, `entertherabbithole`, `matrixsumlistenterlastwordsbeforearchichoicethispassword`, `gsmgwitnessblk949653tx808f812f`) |
| S3 SCENE/POSTER | 25–26 | Decentraland CIDs + scene text, poster text, `GSMG MEGANIGMA \|\| 5 BTC`, estate contract, parcels −41,−16 / −41,−17, prize address, `enterprise@gsmg.io` |
| S4 CREATOR SENTENCES | 634 | Unique sentences from Jrk Bgrt's 482 Telegram messages (regenerated from the export, same logic as `gsmg_creator_words_sweep.py`) |
| S5 LINES | 2,645 | `gsmg_mrrobot_fresco_lines.txt` + `gsmg_literary_canon_lines.txt` after cleaning/dedup (the two files total 2,811 lines incl. comments — fewer than the ~5,737 estimated from fragment counts) |
| S6 CHAT SHORT | 20,000 | Short cleaned fragments (≤25 chars) from the full non-creator room, capped from 38,150 unique, ranked by frequency then alphabetically |

### Layer 1 — ordered pairs (Worker 1, `gsmg-preimage-pairs.json`)

Ordered cross-corpus pairs, separators {"", "-", "_", " ", ".", "/"} × case
{lower, as-is} for the small sets, {"", " ", "-"} for S4/S5, {"", " "} for
S6. Shapes: (A) joined string as written, UTF-8; (B) cleaned lowercase
alphanumeric-only joined form (skipped when identical to A).

| Class | Pairs | Hash A | Hash B | Dedup skipped |
|---|---|---|---|---|
| S1×S2 | 1,258 | 11,352 | 627 | 546 |
| S1×S3 | 850 | 8,010 | 537 | 451 |
| S2×S3 | 925 | 9,732 | 691 | 52 |
| S2×S2 | 1,369 | 14,004 | 840 | 26 |
| S3×S3 | 625 | 6,750 | 523 | 26 |
| S1×S1 | 1,156 | 6,042 | 258 | 3,897 |
| S4×S1 | 21,556 | 77,982 | 4,438 | 0 |
| S4×S2 | 23,458 | 102,708 | 8,876 | 0 |
| S4×S3 | 15,850 | 74,178 | 9,510 | 0 |
| S4×S4 | 401,956 | 1,205,868 | 0* | 237 |
| S5×S1 | 89,930 | 325,263 | 18,511 | 93 |
| S5×S2 | 97,865 | 428,478 | 37,030 | 14 |
| S5×S3 | 66,125 | 309,456 | 39,673 | 11 |
| S6×S1 | 680,000 | 1,358,822 | 139,890 | 1,767 |
| S6×S2 | 740,000 | 1,479,892 | 280,000 | 162 |
| **Total** | **2,142,923** | **5,418,537** | **541,404** | **7,282** |

\* S4×S4 shape B = 0: S4 originals are already cleaned lowercase, so shape B
is always identical to the `""`-separator shape-A form and is skipped per the
rules — correct, not a bug. 126 chunks, 61.6s, 0 truncations.

### Layer 2 — ordered triples (Worker 2, `gsmg-preimage-triples.json`)

Ordered triples of distinct elements (permutations, matching the prior
B×B×B convention). Shapes A/B as above.

| Class | Candidates | Hash A | Hash B | Dedup skipped |
|---|---|---|---|---|
| S1×S1×S1 (seps `"","-"," "`, lower + as-is) | 83,772 | 83,772 | 55,848 | 23,940 |
| S1×S1×S2 | 244,524 | 244,524 | 169,386 | 4,560 |
| S1×S2×S2 | 271,500 | 271,500 | 220,002 | 228 |
| S1×S1×S3 | 170,146 | 170,146 | 139,852 | 4,886 |
| S1×S3×S3 | 132,270 | 132,270 | 124,926 | 330 |
| S1×S2×S3 (all 6 orderings) | 391,552 | 391,552 | 349,324 | 944 |
| S4×S1×S1 (sentence first/middle/last) | 8,145,720 | 8,145,720 | 8,011,080 | 0 |
| **Total** | **9,439,484** | **9,439,484** | **9,070,418** | **34,888** |

~2.5 min, 0 truncations. Dedup note: the prior B×B×B set was fully excluded
(all 7,980 ordered triples drawn from the 21 B∩S1 elements × 3 separators =
23,940 skips).

### Layer 3 — wordlist + structured (Worker 3, `gsmg-preimage-wordlist.json`)

Shapes: (A) as written, (B) cleaned lowercase, (C) hex of cleaned.

| Layer | Count |
|---|---|
| L1 generic wordlist (184 common passwords + 138 puzzle-relevant English words) | 320 |
| L2 puzzle vocab singles + suffixes (45 bases × 17 suffixes × seps {"", "-", "_"} + singles) | 2,339 |
| L3 dates 2017-01-01–2026-12-31 (3,652 days; YYYYMMDD, YYYY-MM-DD, DDMMYYYY, DD-MM-YYYY, MonthYYYY, YYYYMM, MMYYYY) | 14,968 |
| L4 gsmg + 2/3/4-digit (11,100) + gsmgio/yinyang/dualite/meganigma + 2-digit (400) + plain 0–99999 (100,000) | 111,500 |
| L5 D149 windows (8/16/32/64 + full; length verified 149) + P91 windows (8/16/32; length 91), each also reversed | 1,396 |
| L6 years/counts (25 base strings prefixed/suffixed with gsmg/yinyang/dualite) | 175 |
| **Total unique candidates** | **130,562** |

Hashes: A 130,546 + B 8,835 + C 130,546 = **269,927**. Dedup skipped: 16.
(B is low because most candidates are already lowercase-alphanumeric, so A≡B
and the identical shape was skipped per spec.)

## Grand totals

| | Candidates | Hashes | Dedup skipped |
|---|---|---|---|
| Pairs | 2,142,923 | 5,959,941 | 7,282 |
| Triples | 9,439,484 | 18,509,902 | 34,888 |
| Wordlist + structured | 130,562 | 269,927 | 16 |
| **Total** | **11,712,969** | **24,739,770** | **42,186** |

## Verdict per target — all NO HIT

- `0b0f37ec…96ee32` — NO HIT
- `673e3b1a…356b0d` — NO HIT
- `a2aefdbb…18b0b1` — NO HIT
- `aca20ae7…5ed9a` — NO HIT
- `c2eef34b…76625` — NO HIT

No hit occurred, so no blob/EC/third-door verification was triggered.
Boundaries held: no one contacted, nothing published.

## Caveats / what this does NOT close

- Triples use distinct elements only (permutations) — triples with a
  repeated element (e.g. `yinyang+yinyang+yinyang`) were not tested; a small
  add-on (~34 extra per class pattern) if ever wanted.
- Minor cross-class overlap exists where element sets intersect (e.g.
  `salphaseion`, `thematrixhasyou` in both S1 and S2), so a few identical
  pairs were hashed in two classes; this only slightly inflates the hash
  total, it cannot hide a hit.
- S5×S5 pairs and S6×S6 pairs were out of scope (too large); S6 pairs were
  limited to S6×S1 and S6×S2.
- The 5 preimages may be solver probes with random-ish preimages, or stage
  answers built from material not in these corpora — in which case no
  dictionary of this kind can find them.

## Files

- Record: `gsmg-preimage-attack.md` (this file)
- Pairs: `gsmg-preimage-pairs.json`, `gsmg-preimage-pairs.log`, `gsmg_preimage_pairs.py`
- Triples: `gsmg-preimage-triples.json`, `gsmg-preimage-triples.log`, `gsmg_preimage_triples.py`, `gsmg-preimage-triples-state.json`
- Wordlist: `gsmg-preimage-wordlist.json`, `gsmg-preimage-wordlist.log`, `gsmg_preimage_wordlist.py`
- Prior work: `gsmg-hash-dictionary.md`, `gsmg_hash_dictionary.py`

## Addendum 2026-11-12 — two preimages identified (fresh-eyes pass)

The fresh-eyes pass (`gsmg-fresh-eyes.md`, script `gsmg_fresh_eyes.py`)
hashed all 414 unique Wayback CDX URL strings as preimages and identified
2 of the 5:

- `0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32` =
  SHA-256(`hopeitisthequintessentialhumandelusion`) — a solver-probe
  variant of the Architect quote (the known `c1780cbb…` page drops the
  "it"); word-slug URL captured 2026-03-10. Verified with sha256sum.
- `c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625` =
  SHA-256(`youmeizandself`) — a new phrase, never seen before; word-slug
  URL captured 2026-01-05 in a batch probing `youme{and,i,is,iz}andself`.
  Verified with sha256sum.

Both phrases were run through all four shapes in the same pass (neighbours
both forms incl. third-door; blobs, 6 variants, both digests): 0 hits.
Neither is the blob password or a neighbour scalar. Their page contents
were never fetched and are currently unretrievable (live 404, archive 403).

Still unknown: `673e3b1a…`, `a2aefdbb…`, `aca20ae7…` — not any CDX URL path,
and not any of 9,192 strings from the site's JS bundle (`app.js.download`),
also hashed in the same pass.
