# GSMG 5 BTC — First-Appearance Outside the Page ("outside-squares")

**Date:** 2026-11-12
**Approved by:** Hazrat ("apply it", 2026-11-12) — item (b) of think-like-creator §5.
**Script:** `~/workspace/gsmg_outside_squares.py`, log `gsmg-outside-squares.log`,
summary JSON `gsmg-outside-squares-summary.json`.
**Result: 0 hits on all four shapes.**

## The rule (proven by the control)

The Bifid square key DBIFHCEG is the first 8 distinct letters of the 91-token
prefix in first-appearance order (D0, B1, I3, F5, H7, C8, E11, G12, A16).
DBIFHCEG at period 570 decrypts the segment to a plaintext starting BTCSEED.
Wave 2 applied this rule to every token sequence ON the SalPhaseIon page
(18 squares, 0 hits); the null-letter wave closed the 'A' question (0 hits).
This wave applies the same rule to token sequences OUTSIDE the page.

Per sequence, three key variants: the full distinct-letter string, its first
8 letters, and the distinct letters BEFORE the first 'a' (null-letter
variant). J is dropped (Bifid merges I/J). Each square decrypts the Bifid
segment (570), the 91-token prefix, the 256-symbol object and Stream B at
periods 91, 285, 570 and full length. Every distinct output goes through
all four shapes: hash pages, neighbours (both address forms, incl. the
third-door oracle address), blob decryptions (SHA-256 + MD5 password hex,
both digests, all four blobs + both corrected blob2 readings), and each
derived key itself as a blob password (raw, hex-of-raw, SHA-256 hex).

## Harness certification (all PASS before the run)

- privkey-1 vectors, both forms: comp `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`,
  uncomp `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`.
- Known hash-page preimages reproduce: `hopeisthequintessentialhumandelusion`
  → c1780cbb…, `anstoo` → 21ef0533…, genesis string → 89727c59…, raw bytes of
  the genesis hash → f9719d6d….
- Bifid control: DBIFHCEG, period 570 → the known `BTCSEED…` plaintext exactly.
- 227-char concatenation verified: length 227, SHA-256
  `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`.
- Cosmic 1327-byte plaintext REPRODUCED from primary sources (floflo
  tested.md §11): XOR chain of the SHA-256 digests of `matrixsumlist,
  enter, lastwordsbeforearchichoice, thispassword, matrixsumlist,
  yourlastcommand, secondanswer` → `a795de11…0735`; those 32 raw bytes as
  the EVP_BytesToKey/MD5 password against blob3 → 1327 bytes, SHA-256
  `4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081`. The
  plaintext bytes are used here as a sequence for the first time.

## Sequences (36)

### Group 1 — hash pages' content (7 identified)

| # | Sequence | Source |
|---|----------|--------|
| 1 | `GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | genesis string, 89727c59 preimage |
| 2 | 1327-byte Cosmic plaintext (reproduced, see above) | 4f7a1e4e preimage |
| 3 | `ourfirsthintisyourlastcommand` | e24bd2c0 preimage |
| 4 | `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` | hex of the 32 raw bytes that are the f9719d6d preimage |
| 5 | `hopeisthequintessentialhumandelusion` | c1780cbb preimage |
| 6 | `humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness` | 10d6a2c5 preimage |
| 7 | `anstoo` | 21ef0533 preimage |
| 8 | `Hello :-)` | live site's 404 answer for hash paths — the only served content of a hash page ever observed |

**The 5 unknown pages (0b0f37ec, 673e3b1a, a2aefdbb, aca20ae7, c2eef34b)
contribute NO sequence here — they have no content on record.** Recorded
explicitly, not overlooked.

### Group 2 — Decentraland scene text (16)

| # | Sequence | Source |
|---|----------|--------|
| 9 | Full game.ts source (2,394 chars, decoded from the bundle's source map; saved as `~/workspace/gsmg-archive-scene/game.ts`) | `bin/game.js` |
| 10 | `GSMG.IO \n5 BTC PUZZLE CHALLENGE` | sign TextShape |
| 11 | Full scene.json text | `scene.json` |
| 12 | `GSMG.io Puzzle piece` | scene title |
| 13 | `gsmg.io magic puzzle piece` | estate name (on-chain) |
| 14 | `White Rabbits everywhere` | estate description (on-chain) |
| 15 | Estate name + description joined | on-chain metadata |
| 16 | `bin/game.js scene.json sounds/puzzlepiece.mp3` | filenames joined |
| 17 | `sounds/puzzlepiece.mp3` | audio filename |
| 18 | `QmRK2YoLei9wrxLvHUKisywobxEvczTicXepPxKLKzN51v` | entity id |
| 19 | The three content CIDs joined | bundle manifest |
| 20 | `Logic Pro X 10.4.1` | mp3 tag (only real text in the audio) |
| 21 | The three game.ts string literals joined | game.ts |
| 22 | `GSMG.io` | contact name |
| 23 | `spawn1` | spawn point name |
| 24 | `webrtc https://signalling-01.decentraland.org` | communications |

### Group 3 — adjacent outside-page sequences (12)

| # | Sequence | Source |
|---|----------|--------|
| 25 | `GSMG.IO 5 BTC PUZZLE CHALLENGE` | poster title band (same letters as the scene sign — deduplicated, one square) |
| 26 | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | prize address as printed |
| 27 | 227-char concatenation (verified above) | Phase 3 seven parts as one sequence |
| 28 | All 8 creator OP_RETURN payloads joined | vanity wallet `3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK` |
| 29–36 | Each OP_RETURN payload alone: `GSMG.io: Right, this is causality` / `GSMG.io: are you sure?` / `GSMG.io: You are here because 227 chars were correct` / `GSMG.io: phase3.2 pass OK` / `GSMG.io: part of the cipher` / `GSMG.io: do you beleive me you need it?` / `Halving` / `Good job, Neo!` | same |

## Derived square keys (78)

ANSTO, BING, BINGAME, BINGAMESCOUDPZL, C, CAUSLITY, CAUSLITYFENHMXBDKRP,
CBDF, CBDFA, DISPL, DISPLAYT, DISPLAYTEGMOUZCFVNWRXBHK, GODBNE, GSMCWTD,
GSMCWTDDF, GSMCWTDFAPXRBE, GSMIO, GSMIOACP, GSMIOACPUZLE,
GSMIOACPUZLEWHTRBVY, GSMIOARE, GSMIOAREYU, GSMIOBTC, GSMIOBTCPUZLEH,
GSMIOBTCPUZLEHAN, GSMIOBTCPUZLEHANWDFXR, GSMIODYU, GSMIODYUBELVNT,
GSMIOP, GSMIOPAR, GSMIOPARTFHEC, GSMIOPH, GSMIOPHA, GSMIOPHAEK, GSMIOPUZ,
GSMIOPUZLEC, GSMIORHT, GSMIORHTC, GSMIORHTCAULY, GSMIORHTCAULYEBWPKFDVN,
GSMIOYU, GSMIOYUA, GSMIOYUAREHBCWT, H, HALVING, HELO, HOPEISTQ, HOPEISTQUN,
HOPEISTQUNALMD, HUMPOEIS, HUMPOEISTQN, HUMPOEISTQNALDYRCFGWK, LOGICPRX,
OURFISTH, OURFISTHNYL, OURFISTHNYLACMD, QMCO, QMCOASKX,
QMCOASKXYNZDBRTGVFLEUPHWI, QMRKYOLE, QMRKYOLEIWXVHUSBCZTPN, SOUNDPZL,
SOUNDPZLEICM, SOUNDPZLEICMGBTH, SOUNDPZLEICMGBTHARVF, SP, SPAWN, SPAWNCUB,
SPAWNCUBEOTIYDRFMHVXGLZK, WEBRTCHP, WEBRTCHPSIGN, WEBRTCHPSIGNALDO,
WHITER, WHITERAB, WHITERABSVY, YVIPCMGX, YVIPCMGXRESUZBDKQLNF,
YVIPCMGXRESUZBDKQLNFAWTOH.

Notes on the variants: `anstoo` starts with 'a', so its before-first-a
variant is empty; 8 sequences contain no 'a' at all (404 page, scene
title, audio filename, entity id, mp3 tag, contact name, OP_RETURN 6,
OP_RETURN 8), so no before-first-a variant exists for them. The 227-char
sequence's before-first-a variant is the single letter `C` (its second
character is 'a').

## Results

| Measure | Count |
|---|---|
| Sequences | 36 |
| Derived square keys | 78 |
| Distinct decryption outputs | 592 (78 keys × ~11 decryptions, deduplicated; periods ≥ target length coincide) |
| Control reproducers (a square decrypting the segment at period 570 to `BTCSEED…`) | **none** besides DBIFHCEG itself (not in this wave) |
| Oracle 1 — hash pages | 592 texts × 3 shapes = 1,776 comparisons — **0 hits** |
| Oracle 2 — neighbours (both address forms, incl. third-door `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9`) | 592 × 2 = 1,184 scalar tests — **0 hits** |
| Oracle 3 — blobs, outputs | 14,208 decryptions, 49 valid paddings (expected ~55.5 at 1/256) — **0 address matches** |
| Keys themselves as blob passwords (raw, hex-of-raw, SHA-256 hex × both digests × 6 blobs) | 2,808 decryptions, 8 valid paddings (expected ~11) — **0 address matches** |
| **Total blob decryptions** | **17,016**, 57 valid paddings vs ~66.5 expected at chance — **0 address matches** |
| **Real hits** | **0** |

Prior-use verification for the keys as blob passwords: a grep over all
`gsmg_*.py` scripts finds NO prior occurrence of any key of 4+ letters —
the long keys were genuinely never used as passwords before. The only
hits are trivial: the 1-letter keys `C` and `H` and the 2-letter key `SP`
appear as substrings inside other scripts' code (any file containing
those letters), and `ANSTO` appears in the null-letter scripts as part of
the `anstoo` fragment handling (lowercase `anstoo` itself was tested as a
password in the Four Archives, 0 hits; the uppercase 5-letter square-key
form is new here). The grep check is therefore meaningful only for keys
of 4+ letters, and for those it is clean.

## Per-group verdicts

- **Group 1 (hash pages' content): 0 hits.** No square derived from any
  identified hash page's content — including the reproduced 1327-byte
  Cosmic plaintext — decrypts anything to a password, a neighbour scalar,
  or a hash-page preimage.
- **Group 2 (Decentraland scene): 0 hits.** No square from the scene's
  source, sign, metadata, filenames, CIDs or tags does either. The
  scene's text is exhausted as a square source.
- **Group 3 (adjacent sequences): 0 hits.** The 227-char concatenation,
  the prize address as printed, the poster title, and every creator
  OP_RETURN payload — alone and joined — give nothing.

## What this closes

The first-appearance rule, applied to token sequences outside the
SalPhaseIon page, is now closed in full: the other hash pages' content,
the Decentraland scene's text, and the adjacent outside-page sequences
all yield squares whose decryptions are 0 hits on all four shapes. With
wave 2 (sequences on the page) and the null-letter wave (the 'A'
question), the derived-squares family is now exhausted everywhere the
rule can be applied from the puzzle's own material.

## What remains

The insight/meaning (now with no untested place left to apply the
first-appearance rule); a new creator message (12h watch live); the 5
unknown hash preimages; the literal 213 floflo scripts (not held here);
cosmic_A; the 'tiny hint'; publication for fresh eyes (staged, awaiting
Hazrat's word). No contact made, nothing published, no closed tests
re-run.
