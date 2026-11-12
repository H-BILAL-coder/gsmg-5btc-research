# GSMG 5 BTC — 1991 Time-Life Cosmic Duality cover audit

**Date:** 2026-11-12 (early hours)
**Approved by:** Hazrat (pasted pivot plan; same standing "work nonstop" brief).
**Result: the cover's "scary specific" is identified visually; its strings open nothing.**

## The cover (direct inspection of gsmg-cosmic-duality.pdf p.1)

- Series **"MYSTERIES OF THE UNKNOWN"**, title **"Cosmic Duality"**.
- Artwork: a **YIN-YANG (taijitu)** formed by two interlocking star-field
  shapes on a black background — the upper half dark with a bright
  **BLUE-WHITE star**, the lower half blue with a bright **GOLDEN-YELLOW
  star** — inside a thin silver square border.
- That is the "scary specific": the cover IS a yin-yang (the next phase's
  name) rendered in the puzzle's two colours (blue + yellow/gold), with two
  stars (the two halves). The GSMG poster grid is 15 blue + 9 yellow squares;
  "Half and Better Half" are two halves; the large blob is titled "Dualite".
  The creator chose the book because its cover literally depicts the puzzle's
  core symbol in its core colours. Pages 2–4 of the scan are blank.

## Bibliographic (PDF text layer, copyright page)

- Cosmic Duality, by the Editors of Time-Life Books, Time-Life Books,
  Alexandria, Virginia. Series: Mysteries of the Unknown. 152 pages.
- (c) 1991 Time-Life Books. Second printing 1993. Printed in USA.
- ISBN 0-8094-6516-7 (trade), ISBN 0-8094-6517-5 (library).
- LC: BFI999C6975 1991, 147'.4-dc20, 90-28806.
- Chapters: The Unity of Opposites; Dualities As Old As Time; The Dark Side
  of Fairy Tales; The Battle of the Sexes; Driving the Devil Out; Grasp of
  Ageless Evil; Paths of Righteousness; The Triumph of Good; Hark! Heaven's
  Winged Host.

## Candidates tested (three oracles)

Script `~/workspace/gsmg_cover_audit.py` — 68 candidates (yin-yang,
taijitu, blue/gold stars, the series and title, both ISBNs, the LC number,
all nine chapter/essay titles, the blue/yellow cross-references, "dualite",
and combinations):
- Oracle 1 (hash pages): 106 text + 68 byte hashes — 0 hits.
- Oracle 2 (neighbors EC): 68 candidates — 0 hits.
- Oracle 3 (blobs): 2,448 decryptions, 8 valid paddings (expected ~1/256),
  0 address matches — 0 real hits.

The cover's strings do not open anything directly. Its value is the visual
match: it confirms the yin-yang is the next phase's symbol and that blue +
yellow/gold are the puzzle's colours — which the poster grid already showed.
The cover is a depiction, not a key.
