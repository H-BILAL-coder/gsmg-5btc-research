# GSMG 5 BTC — Fresh-eyes pass ("guess it with full power")

**Date:** 2026-11-12
**Brief:** Hazrat's word ("guess it with full power"). THINKING pass, not a
compute wave. No closed test re-run, no large sweep.
**Script:** `~/workspace/gsmg_fresh_eyes.py`, log via stdout, results
`~/workspace/gsmg-fresh-eyes-results.json`.
**Result: 2 of the 5 unknown hash-page preimages IDENTIFIED (verified
independently with sha256sum). Everything else in this pass: 0 hits.**

## 1. The headline — two preimages found

The idea: the Four Archives web worker hashed page TEXT fragments, never the
Wayback CDX URL strings themselves. This pass hashed all 414 unique CDX URLs
(full URL, path, bare path) as hash-page preimages. Two matched:

| Hash page | Preimage (cleaned) | Source URL | CDX capture |
|---|---|---|---|
| `0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32` | `hopeitisthequintessentialhumandelusion` | `https://gsmg.io/hopeitisthequintessentialhumandelusion` | 2026-03-10 08:33:30, 200, 12,262 bytes |
| `c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625` | `youmeizandself` | `https://gsmg.io/youmeizandself` | 2026-01-05 01:41:13, 200, 12,213 bytes |

Verified independently: `printf '%s' "hopeitisthequintessentialhumandelusion"
| sha256sum` = `0b0f37ec…`, and `printf '%s' "youmeizandself" | sha256sum` =
`c2eef34b…` — exact full-hash matches, not prefixes.

### What they are

- **`hopeitisthequintessentialhumandelusion`** — "hope it is the
  quintessential human delusion". A solver-probe variant of the Architect
  quote: the known page `c1780cbb…` is the same sentence WITHOUT "it"
  (`hopeisthequintessentialhumandelusion`, from the creator's own Telegram
  message). Captured 2026-03-10 in the same minute as the hash page itself
  (08:32:30) and the ARCH1/ARCH2 hash pages — a batch probing Architect-quote
  variants (`hopeisthe…`, `hopeitisthe…`, `hopeisthe…simultaneously…`,
  `humphhope…simultaneously…`). Solver probe, not a creator gate.
- **`youmeizandself`** — "you me iz and self". A NEW phrase, never seen
  before in any record. Captured 2026-01-05 in a one-minute batch that
  probed four variants of the same template: `youmeandself` (01:41:35),
  `youmeiandself` (01:40:59), `youmeisandself` (01:41:26),
  `youmeizandself` (01:41:13) — and then the hash page itself (01:42:27).
  The "iz" variant is the one whose SHA-256 was also probed, i.e. the
  solver brute-forced the middle word and "iz" is the one that matched a
  hash page. It reads like a fragment of the creator's self-theme ("Give
  yourself yourself…", "you, me, is, and self") but with "iz" — it is a
  solver's probe string, and its only verified meaning is that it is the
  preimage of `c2eef34b…`.

### What they are NOT

Both phrases went through all four shapes in this same run (they were CDX
path candidates): Oracle 2 (neighbours, both address forms, incl.
third-door) — no hit; Oracle 3 (blobs, 6 variants, both digests) — no
address match. Neither phrase is the blob password or a neighbour scalar.
Their PAGE CONTENTS are the interesting unknown: both pages served 200 with
~12.2 KB bodies (the SPA shell size), but the bodies were never fetched —
not in `cached_html_text.json` (34 entries: homepage history, choice page,
/Puzzle, /theseedisplanted only), not in the local `wayback_cache/bodies/`
(124 files, no match for either slug), and not retrievable now: the live
site returns **404** for both URLs, and the Wayback Machine returns
**403** for the archived captures. The contents are a genuine open item,
retrievable only if the archive becomes reachable again (or from a solver
who saved them).

### Remaining unknown preimages: 3 of 5

- `673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d`
  (hash page captured 2026-01-05 00:49:05)
- `a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1`
- `aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a`

None of the other 412 CDX URL paths hashes to any of these three. They are
not CDX URL paths.

## 2. What else this pass tested (all 0 hits)

Harness certified first (privkey-1 both forms; `anstoo` → 21ef0533…,
genesis → 89727c59…, ARCH1 → c1780cbb…; synthetic Salted__ witness; the
phase-2 blob decrypts under sha256('causality') and contains "keymakers"
— via the separate phase-2 blob vector from `gsmg_dynamic_replay.py`, NOT
a kit blob; Bifid control DBIFHCEG/570 → BTCSEED… exactly). A valid
padding alone is never a hit — only an address match counts.

**Totals:** 1,114 distinct candidates; Oracle 1: 742 text + 2 bytes, 2 hits
(the two above); Oracle 2: 1,114 candidates, 0 hits; Oracle 3: 40,104
decryptions, 158 valid paddings (chance ~157), 0 address matches.

### A. Phase 3 parts standalone — 0 hits (but two recoveries)

A grep over `gsmg_preimage_pairs.py`, `gsmg_hash_dictionary.py`,
`gsmg_dynamic_replay.py`, `gsmg_closing_protocol.py` finds ZERO occurrences
of `safenet` / `luna` / `11110` / `HSM` — the seven parts were only ever
tested as the 227-char concatenation. Tested standalone (exact casing from
apple SOLUTION.md): `Safenet`, `Luna`, `HSM`, `11110`, case variants
(`safenet`, `SafeNet`, `SAFENET`, `luna`, `LUNA`, `hsm`, `Hsm`), joins
(`SafenetLunaHSM`, `SafeNet Luna HSM`, `Safenet Luna HSM`,
`SafeNetLunaHSM`, `SafenetLunaHSM11110`, `causalitySafenetLunaHSM11110`),
the FEN pre-move (`B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2
w - - 0 1`) and post-Rc6+ (`B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2
b - - 0 1`). All 0 hits on all four shapes.

**Recovery 1 — the main.cpp literal (part 6) is now on disk as a string.**
It was never stored as a standalone string before this pass. From
apple-repo README line 187:
`0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854`
(140 chars; hex-decodes to the genesis coinbase message reversed).
Tested standalone: 0 hits. (Note: the audit JSON
`seven_stage_passwords_intertwine_audit.json` carries a CORRUPT variant
missing `6E614A` ("naJ") — do not use that copy.)

**Recovery 2 — the 227-char concatenation reconstructed exactly.**
`causalitySafenetLunaHSM11110` + part 6 + FEN-post = 227 chars,
SHA-256 = `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`
— verified in-script. This CONFIRMS the FEN post-Rc6+ reconstruction
(`2R5`, side `b`, ending `0 1`). The full 227-char string itself as a blob
password was never tested before (dual-reading wave 1 skipped it — "not on
disk"; wave 2 tested only its digest). Tested now: 0 hits.

### B. Final objects RAW as preimages + neighbour scalars — 0 hits

OBJ256, STR285 (odd stream with I/O), EVEN285, BIF570. They were only ever
tested as BLOB PASSWORDS (dynamic replay Class D) and in transformed forms
(VIC-encode, base-23/25) — never raw through Oracles 1–2. Tested raw now:
0 hits. Also the 29 dropped I/O letters of the odd stream in order (29
chars) — 0 hits.

### C. CDX URL strings — 2 hits (see §1), everything else 0

414 unique URLs (full URL, path, bare path) through all four shapes. Only
the two §1 paths matched anything. The 5 unknown pages' own URLs
(`gsmg.io/<hash>`, `/<hash>`) as preimages: 0 hits.

### D. New Bifid squares — 0 hits, none reproduces the control

Three squares never used before, each decrypting the segment @570, the
prefix @91, OBJ256 @256, STREAM_B @285 (12 outputs through all shapes):
- **VIC checkerboard alphabet as a square key**
  (`FUBCDORALETHINGKYMVPSJQZXW`, J dropped by the square builder): segment
  → `UBAIRWFWHZHWAQRZBQBDBYBHFXAIBHTE…` — NOT the BTCSEED plaintext.
- **P91 first-appearance as a square key** (`COMNSLUTIRDEAHKVYGPBF`):
  segment → `FAEHAUACWMWOAIATANPDMNFBDCEHFBAK…`.
- **MEGANIGMA as a square key**: segment → `IYEQMBBTMOMKGIMDCQIXCHCIBSEQCIKA…`.
No square reproduces the BTCSEED control; all 12 outputs 0 hits.

### E. Colour-split poster spiral indices — 0 hits

Recomputed from `gsmg-repo/puzzle.png` (grid origin 37,37, pitch 75;
spiral counterclockwise from top-left). The 24 coloured-cell AP
(7,15,…,191) was tested whole; the splits are new:
- Blue (15): `[7, 15, 23, 31, 47, 55, 63, 87, 95, 103, 111, 127, 135, 159, 183]`
- Yellow (9): `[39, 71, 79, 119, 143, 151, 167, 175, 191]`
Union verified = the AP. Each split tested as comma-joined, concatenated,
and as bytes: 0 hits.

### F. Audio click times — 0 hits

`0993833422`, `993833422`, `2843039`, `0.0990.3833.422` (clicks at 0.099s /
0.383s / 3.422s): 0 hits.

### G. 2026 site banner phrases — 0 hits

`The lights are off`, `Nine years of chaos ended`, `One mystery remains`,
`Follow the white rabbit`, full banner string: 0 hits.

## 3. Leads that died on inspection (checked, not tested)

- **Creator's photo-only Telegram messages.** 3 carry a `photo` field
  (2020-01-04, no text; 2020-02-20, "😎"; 2026-07-16, "Nice"). The image
  files are NOT on disk (only `photos/photo_…jpg` references in the
  export) — untestable from here. The one puzzle-related photo on disk,
  `apple-repo/gsmgio-5btc-puzzle-master/photo_2020-04-26_09-24-30.jpg`,
  is a Decentraland screenshot of the already-fully-decompiled scene
  (white question-mark cubes, the "GSMG.IO 5 BTC PUZZLE CHALLENGE" sign,
  parcel −41,−17) — nothing new in it.
- **July 2026 hint image** (`gsmg-july2026-hint.png`) is just a screenshot
  of the already-recorded "close friends" message — nothing new.
- **Transaction IDs as preimages** — already tested (archive chain worker:
  every txid hex + raw bytes). Closed, not re-run.
- **BIF570 raw as a blob password** — already tested (dynamic replay
  Class D). Closed; only its Oracle 1/2 use was new (§2B).

## 4. What remains

- **3 unknown preimages** (`673e3b1a…`, `a2aefdbb…`, `aca20ae7…`) — not
  CDX URL paths, not in any tested candidate universe.
- **The contents of the two newly-identified pages** (`/youmeizandself`,
  `/hopeitisthequintessentialhumandelusion`) — live 404, archive 403 at
  time of checking; a saved copy from a solver, or archive access
  returning, is the only route.
- **The remaining probe families in CDX**: the 2026-01-05 batch also
  probed blob material as URLs (hex `Salted__…` paths, a base64 path
  `iXJ8WYuc0c+Ic/J8twV/BQZF3banoVehECOawBUvajI=`) and the 2026-03-10
  batch probed the Architect variants — all hashed here, no further
  matches. **Closed after this record was written:** all 9,192 unique
  strings from the site's JS bundle (`apple-repo/sources/GSMG _
  GSMG_files/app.js.download`, quoted strings + path-like tokens) hashed
  against the 3 remaining targets — 0 hits. The JS-route extension of the
  URL-slug idea is now closed too.
- Everything previously open stands: the literal 213 floflo scripts,
  cosmic_A, the 'tiny hint', a new creator message (12h watch live),
  fresh eyes on the published repo.

## 5. Correction to the record (harness)

The rescan script's docstring says its harness was certified with "phase-2
blob under sha256('causality')" — that check does NOT exist in its code,
and it does NOT hold for any kit blob: no form of 'causality' (raw, SHA-256
hex, SHA-256 raw bytes, MD5 hex) opens any of the six kit blob variants
under either digest (verified directly). The phase-2 blob is a SEPARATE
blob (the Phase 2 page's blob, `PHASE2_B64` in `gsmg_dynamic_replay.py`),
which does decrypt under sha256('causality') and contains "keymakers".
This pass certifies against that vector instead. No prior result is
affected — all prior waves used the kit blobs only as targets, and their
certifications (privkey-1, known preimages, synthetic witness, Bifid
control) are independent of this.
