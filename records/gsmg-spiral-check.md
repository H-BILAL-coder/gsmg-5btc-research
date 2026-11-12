# GSMG spiral check — 2026-11-11

Claim (pasted ChatGPT text): the 14x14 Genesis Matrix has exactly 24 coloured
cells (15 blue, 9 yellow), and every coloured cell lands on a spiral position
where the spiral index is congruent to 5 (mod 8).

Method: `~/workspace/gsmg_spiral_check.py` reads `~/workspace/gsmg-repo/puzzle.png`
(1048x1556), samples each of the 14x14 cells (75px pitch, 9x9 majority vote around
the cell centre), classifies W/K/B/Y, walks the spiral counterclockwise from (0,0)
(down the left column first — the Phase 0 reading direction).

Results:
- Counts: 15 blue, 9 yellow, 24 coloured — VERIFIED exactly as claimed.
- Spiral self-check: the bitstream decodes to 'gsmg.io/theseedisplanted' EXACTLY,
  so the spiral direction and indexing are the verified ones.
- Coloured-cell spiral indices (0-based): 7, 15, 23, 31, 39, 47, 55, 63, 71, 79,
  87, 95, 103, 111, 119, 127, 135, 143, 151, 159, 167, 175, 183, 191.
- Residues: 0-based all 7 (mod 8); 1-based all 0 (mod 8). Row-major: no structure.

Verdict: the counts verify exactly, and the uniform-spacing structure verifies
exactly — one coloured cell per byte, always at the same bit position (the LSB of
each of the 24 message bytes). But the residue is 7 (0-based) / 0 (1-based) under
the verified spiral, NOT 5 as claimed. The claim as literally stated does not
match; the "5" is either a different indexing convention or an error. The
meaningful content (one coloured cell per byte, same bit position) is confirmed;
it is a property of the known message, not new information.
