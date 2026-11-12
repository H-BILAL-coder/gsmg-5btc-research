# GSMG 5 BTC — Hash dictionary: cross-domain combinations (six remaining pages)

**Date:** 2026-11-12
**Approved by:** Hazrat (pasted plan, item 2).
**Result: 0 hits. The six remaining preimages are not cross-domain combinations
of these elements in any of the five shapes.**

## What was already covered (not re-run)

Singles and same-source adjacent concatenations: Architect harvest (200
fragments, 4 shapes), Oracle/Smith/Merovingian (10,050 fragments), trilogy
(9,939 fragments), phases 1–3 (2,306), internal audit (568), close reading
(84), cover audit (68), footprint (22), floflo rows 18–19 (substrings +
third-door constructions). This script tests only COMBINATIONS ACROSS
domains, which none of those covered.

## Element sets (script `~/workspace/gsmg_hash_dictionary.py`)

- **A — Architect scene phrases (29):** verified film dialogue, cleaned +
  original forms, incl. both known preimages as elements
  ("hopeisthequintessentialhumandelusion",
  "hopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness").
- **B — internal puzzle terminology (26):** yinyang, yingyang, dualite,
  cosmicduality, salphaseion, thematrixhasyou, causality, jacquefresco,
  giveitjustonesecond, heisenbergsuncertaintyprinciple, theseedisplanted,
  theflowerblossomsthroughwhatseemstobeaconcretesurface, whiterabbit,
  whiterabbitseverywhere, gsmgiomagicpuzzlepiece, half, betterhalf,
  neighbors, phase32, phase3, matrixsumlist, lastwordsbeforearchichoice,
  ourfirsthintisyourlastcommand, 227, 149, 91.
- **C — 1991 Time-Life Cosmic Duality metadata (17):** ISBNs 0809465167 /
  0809465175, mysteriesoftheunknown, timelifebooks, theunityofopposites,
  dualitiesasoldastime, thedarksideoffairytales, thebattleofthesexes,
  drivingthedevilout, graspofagelessevil, pathsofrighteousness,
  thetriumphofgood, harkheavenswingedhost, 1991, 1993, bfi999c6975,
  alexandriavirginia.
- **D — creator's own phrases (16):** makethebestofeverything,
  giveyourselfyourselfandyourselfwillbegivenyourself, geestveruimend,
  latetly, myclosefriendshavethebestchance, nevergonnagiveyouup, freewill,
  nohintsonlyfreewill, hiddenlaptop,
  ihaveahiddenlaptopwhichihaventtouchedinyears, somealreadyfoundit,
  the5btcwasnevertheactualprize, ifyouguysgot1microstepfurther,
  areyoureallylookingforjustthebtc, itismeanttobesolved,
  whenyingyangisreached2hoursmax.

## Combinations

| Class | Count |
|---|---|
| A×B / A×C / A×D / B×C / B×D / C×D / B×B / C×C ordered pairs, seps {"","-","_"," "} (A×A excluded — adjacent concatenations covered by the Architect harvest) | 15,052 |
| B×B×B triples, "" separator | 15,600 |
| **Total unique combinations** | **30,652** |

Caveat: B×B pairs of pure stage answers may partly overlap floflo row 16
(ordered pairs of stage answers); pairs involving the non-answer terms
(yinyang, dualite, salphaseion, matrixsumlist, whiterabbit, half, neighbors,
etc.) are new, and all cross-domain classes are new.

## Shapes (5 per combination — 153,260 hashes)

1. Pure text: SHA-256(cleaned).
2. Hex text: SHA-256(hex(cleaned)).
3. Raw bytes: SHA-256(original spaced/punctuated form).
4. "humph" prefix: SHA-256("humph" + cleaned).
5. Chained: SHA-256(RIPEMD-160(cleaned)).
   RIPEMD-160 alone is 40 hex and cannot equal a 64-hex SHA-256 page hash,
   so it was computed but not compared directly; only the chained form was
   compared.

Self-checks: both known preimages reproduce before the run.

## Result

**0 hits.** The six remaining preimages
(0b0f37ec…, 21ef0533…, 673e3b1a…, a2aefdbb…, aca20ae7…, c2eef34b…) are not
cross-domain combinations of Architect phrasing, internal terminology,
Cosmic Duality metadata, or the creator's own phrases in any of the five
shapes. Hits record: `~/workspace/gsmg-hash-dictionary-hits.json`
(combinations 30,652; hashes 153,260; hits []).
