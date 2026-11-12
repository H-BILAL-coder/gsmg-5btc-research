# GSMG — Wave 3: Geometric Reading (Dual Reading, wave 3)

**Date:** 2026-11-12
**Method:** Lux's "Dual Reading", wave 3 — a GEOMETRIC reading of the
puzzle's non-textual objects. No more strings from books or films; read
the objects themselves as geometry, derive numbers from their structure,
and test those against the three oracles.
**Result: 66 candidates, 0 hits.**

## 1. POSTER — `gsmg-repo/puzzle.png` (1048 x 1556)

Grid: 14x14 cells, pitch 75px (74.86 exact), full width.
Coloured cells (row, col), NEW as row/col positions (spiral indices were
already tested in waves 1-2):
- Blue (15): (0,5) (1,2) (1,10) (2,7) (3,4) (4,1) (6,3) (7,0) (8,5)
  (8,13) (9,2) (11,8) (12,1) (13,2) (13,10)
- Yellow (9): (0,13) (4,9) (5,6) (5,10) (6,11) (7,12) (9,6) (10,7) (12,9)
- Blue rows 0,1,2,3,4,6,7,8,9,11,12,13; blue cols 0,1,2,3,4,5,7,8,10,13.
- Yellow rows 0,4,5,6,7,9,10,12; yellow cols 6,7,9,10,11,12,13.

Rabbit (white pixel-art rabbit, centre of the grid):
- Bounding box: **x 495-689, y 450-644 — 195 x 195 px**, a square.
- Centre: **(592, 547)**. Grid cells: cols 6-9, rows 6-8.
- Black pixels inside white cells in that region: **6,975**.
- The rabbit is a thick-stroke line drawing (two ears, body, tail); its
  outline is drawn inside white cells, not cell-aligned, so it carries no
  cell-level code.

QR code (bottom left):
- Bounding box: **x 1-231, y 1289-1519 — 231 x 231 px**.
- Module pitch: **7 px** (dark runs 7/14/21/28 px; finder outer square
  49 px = 7 modules). **33 x 33 modules = QR version 4.**
- Decodes (already known) to the blockchain.com link for the prize address.

Red separator line: rows **1047-1061**, **15 px** thick, full width 1048.
Title block: "GSMG.IO 5 BTC PUZZLE CHALLENGE" with the blue hexagonal G
logo; prize address printed at the bottom right.

## 2. DECENTRALAND SCENE — `apple-repo/.../artifacts/audio_audit/game.js`

The scene code was fully decompiled (the minified bundle ends in an
`eval('...')` whose source map contains the original TypeScript,
`../src/game.ts`). The scene does NOTHING hidden: no movement, no
animation, no proximity trigger, no second audio. Behaviour:
- **cube** (the audio cube): position **Vector3(8, 1, 8)**, BoxShape,
  AudioClip `sounds/puzzlepiece.mp3`, AudioSource, **OnClick ->
  source.playOnce()**. This cube IS the camera target (8,1,8).
- **cube2-cube9** (8 more cubes, BoxShape only, no audio, no click):
  cube2 (8,7,9), cube3 (8,7.5,8), cube4 (8,7,7), cube5 (8,6,9.5),
  cube6 (8,6,6.75), cube7 (8,5,9), cube8 (8,4,8), cube9 (8,3,8).
- **Text entity** at Vector3(5,5,10): TextShape
  "GSMG.IO \n5 BTC PUZZLE CHALLENGE", fontSize 5, Color3.Blue(),
  font Arial/Helvetica.
- scene.json: parcels "-41,-16" / "-41,-17", base "-41,-17", spawn
  (0,0,0), cameraTarget (8,1,8), title "GSMG.io Puzzle piece",
  owner 0x5D801b2B0B216790A49898b322246282547b546b, webrtc, fly true,
  voice disabled, contentRating E.

Geometric structure of the 9 cubes (all x=8, one vertical plane):
- y in creation order: **1, 7, 7.5, 7, 6, 6, 5, 4, 3**; sorted:
  1, 3, 4, 5, 6, 6, 7, 7, 7.5.
- z in creation order: **8, 9, 8, 7, 9.5, 6.75, 9, 8, 8**.
- Sums: y = **46.5**, z = **73.25**, all coords = **191.75**.
- Centroid: **(8, 5.167, 8.139)**.
- Bounding box: y 1-7.5 (height **6.5**), z 6.75-9.5 (width **2.75**).
- Distances from the audio cube (8,1,8): 0, 2, 3, 4.123, 5.154,
  5.220, 6.083, 6.083, 6.500.
- Shape as seen from spawn (0,0,0): a vertical stem at z=8
  (y=1,3,4) topped by a spreading triangle — apex (7.5,8), base
  y=6 spanning z=6.75-9.5 — i.e. a funnel/triangle on a stem.
  The cubes look hand-placed (7.5, 6.75, 9.5 are not computed values);
  the arrangement is a decorative stack, not a coded lattice.
- No animation, no state, no second object: the scene is 9 static
  cubes, one click-to-play sound, one blue sign.

## 3. SPECTROGRAM — `puzzlepiece.mp3` (5.198 s, 44.1 kHz stereo)

Re-computed from the audio (STFT + long FFT of the L-R channel
difference), not from the PNGs. Geometry:
- Fundamental: **f0 = 64.465 Hz** (least-squares fit from the strong
  harmonics 3,5,9,11,13,15,17,19). Close to but NOT C2 (65.41 Hz).
- Harmonic lines (L-R): **every odd harmonic 1..123 is present**
  (the 61-bit odd-harmonic bitstring is all 1s). Even harmonics are
  absent except a few weak ones (16, 22, 30, 32, 36, 40, 42, 44, 46,
  48, 50, 54, 56, 58, 60, 64, 68, 70, 72, 74, 78, 82, 84, 88, 92 —
  magnitudes 3-10x the floor vs hundreds for the odd ones; leakage).
  The presence bitstring (n=1..123) is 87 ones / 36 zeros and encodes
  nothing beyond "square-wave-like signal": it is the odd-harmonic
  signature, not a code.
- Harmonic amplitudes do NOT follow a clean 1/n square-wave decay
  (n=5 is stronger than n=3; n=7 is weak) — noted, not decoded.
- **Three broadband bursts** (high-band 5-20 kHz energy, >5x median):
  - Burst 1: 0.075-0.122 s, centre **0.099 s**, peak 137.8x.
  - Burst 2: 0.360-0.406 s, centre **0.383 s**, peak 167.2x.
  - Burst 3: 3.390-3.454 s, centre **3.422 s**, peak 177.6x.
  - Widths ~0.047 s each. Gaps: 0.284 s (1->2), 3.039 s (2->3).
  - The harmonic lines are continuous through the whole file
    (dropouts only at the 0.00 s start and 5.11-5.20 s end, i.e.
    edge effects) — there are no time-domain notches in the lines.
  - The vertical bars in the channel-difference spectrogram ARE these
    three bursts; they are broadband clicks, not text.
- The stereo spectrogram is otherwise noise (green/yellow static)
  with the low drone; the channel-difference spectrogram is the
  harmonic-line pattern plus the three bursts.

## 4. BOOK COVER — `cosmic-cover/page-001.png` (1488 x 1857)

Yin-yang artwork (measured, scan is dark so the stars are faint):
- Non-black disc extent: bbox **x 320-1169, y 641-1479 — 850 x 839 px**,
  centre **(744.5, 1060)**; inscribed radius ~**420 px**.
- Disc composition (r=420 around the centre): 94.1% dark, 2.6%
  blueish, 1.5% goldish. Blueish/dark = **0.027**;
  goldish/blueish = **0.581**.
- Brightest upper spot: **(589, 642)**, grey 224, RGB (223,225,224)
  — a near-white point in the upper half (the blue-white star's
  brightest pixel; its core is only ~2 px at the 70% threshold, so
  the star is small/faint in this scan).
- Brightest lower spot: (546, 1433), grey 137 — a broad blue-ish
  region (402 px core), not a compact star.
- The silver square border is too faint in this scan to measure by
  threshold; the disc bbox above is the reliable extent.
- Cover audit (prior wave) already established: the artwork IS a
  yin-yang of two interlocking star-field shapes, upper half dark
  with a bright blue-white star, lower half blue with a bright
  golden-yellow star, in a silver square border.

## 5. CANDIDATES TESTED (66)

From the poster: rabbit bbox/centre/count/cells, QR size/position,
red-line rows/thickness, poster size, blue/yellow cell row,col lists,
counts 15,9,24, coloured spiral indices.
From the scene: audio-cube position, cube count 9, cube y/z sequences
(creation order and sorted, joined and comma forms), sums 46.5 / 73.25 /
191.75, centroid, bounding height 6.5 / width 2.75, distances from the
audio cube, text position (5,5,10) and fontSize 5, the scene text, spawn,
all nine cube positions joined.
From the spectrogram: f0 64.465, burst centres/onsets/offsets/width,
three bursts, the 123-bit harmonic-presence bitstring (as text, as
16 raw bytes, as hex), the 61-bit odd-harmonic bitstring.
From the cover: disc bbox 850x839, centre (744.5,1060), radius 420,
brightest upper spot (589,642), blueish/dark 0.027, goldish/blueish 0.581.
Cross-object: rabbit+QR+f0 joined, cubes+f0+rabbit+QR, audio cube +
text position.

## 6. TESTS AND RESULTS

Harness certified before the run (per the certified_derivation_testing
skill): privkey-1 uncompressed reproduces
1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm (PASS); all four kit blobs parse as
Salted__ with the recorded salts (blob1 b45a5e3d827593ca, blob2
3ab585348552415d, blob3 2d3f6fe06dc950e6, blob4 74c974e3f92e64b5).
Script: `~/workspace/gsmg_geometric_test.py`.

- **Oracle 1 — six remaining hash pages** (0b0f37ec…, 21ef0533…,
  673e3b1a…, a2aefdbb…, aca20ae7…, c2eef34b…): 59 text candidates in
  the four shapes (pure cleaned text, hex text, raw bytes, humph
  prefix) + 1 byte candidate. **0 hits.**
- **Oracle 2 — neighbours** (SHA-256 of each candidate as a scalar vs
  P, 2P, P/2, P+G, P-G; direct 32-byte key checks for byte candidates):
  66 candidates. **0 hits.**
- **Oracle 3 — the four blobs** (SHA-256 and MD5 key derivation, both
  blob2 readings A/B, both escrows, address-match rule — a valid
  PKCS7 padding alone is NOT a hit): **2,376 decryptions, 11 valid
  paddings** (exactly the ~1/256 chance rate; expected ~9.3), **0
  address matches. 0 real hits.**

**Verdict: the geometric reading of the poster, the scene, the
spectrogram and the cover yields no key.** The measurements are now
on record; the three objects' geometry is exhausted as a source of
the blob password. What the wave establishes positively:
- The Decentraland scene is fully decompiled and is 9 static cubes +
  one click-to-play sound + one blue sign — no hidden behaviour, no
  animation, no second trigger. The "rule read on a non-textual
  object" is not in the scene's behaviour.
- The spectrogram's structure is a ~64.5 Hz odd-harmonic signal with
  three broadband clicks (0.099 / 0.383 / 3.422 s) — no time-domain
  notches, no hidden text, no coded harmonic pattern beyond the
  square-wave signature.
- The poster's rabbit is a 195x195 px drawing (not a code), the QR is
  version 4 (33x33, 7 px/module), the red line is 15 px.
- The cover's yin-yang disc is 850x839 px centred (744.5, 1060).
