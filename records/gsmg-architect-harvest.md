# GSMG 5 BTC — Architect transcript harvest (remaining six preimages)

**Date:** 2026-11-11
**Approved by:** Hazrat ("do this", on the pasted battle plan).
**Result: 0 hits. The remaining six preimages are NOT Architect scene
sentences in any of the four shapes.**

## Method

Script `~/workspace/gsmg_architect_harvest.py`. The full Architect scene
transcript was fetched from scottmanning.com
(`/tmp/architect-transcript.html`, HTTP 200) and parsed into speaker-labelled
dialogue in order: **38 lines (24 Architect, 14 Neo)**, from "Hello, Neo."
to "We won't." before "End Scene". Fragments built: single sentences,
sliding windows of 2–3 sentences within a line, and concatenations of
adjacent dialogue lines — **200 fragments**, plus the 11 candidate strings
pasted by Hazrat (tested verbatim).

Four shapes per fragment (as specified):
1. Pure text: lowercase, no spaces, no punctuation → SHA-256.
2. Hex conversion: clean text → raw hex text → SHA-256 of the hex string.
3. Raw bytes: SHA-256 of the raw byte representation.
4. Concatenations: adjacent fragments joined (like the 128-char second hit).
Plus the 'humph' prefix variant (the second hit's pattern).

**Tested: 736 text hashes + 211 byte hashes against the six remaining
hashes. 0 hits.**

## Notes

- The pasted candidates match the real transcript in most cases, but two
  are paraphrases, not the real lines: the paste's
  "designedspecificallytooverwhelmlogicandreason" drops the real "It was"
  ("itwasdesignedspecificallytooverwhelmlogicandreason"), and the paste's
  "restassuredthiswillbethesixthtimeandwehavebecomeexceedinglyefficientatit"
  drops "we have destroyed it". Both the pasted and the real versions were
  tested. Neither hits.
- Self-checks pass: both known preimages reproduce exactly.
- Neo's lines (14) were included in the fragments and tested too. 0 hits.

## What this means

The remaining six preimages (`0b0f37ec…`, `21ef0533…`, `673e3b1a…`,
`a2aefdbb…`, `aca20ae7…`, `c2eef34b…`) are not single sentences, sentence
pairs/triples, or adjacent-line concatenations from the Architect scene, in
any of the four shapes, with or without 'humph'. They are either from other
dialogue (Oracle, Morpheus, Merovingian, other Matrix scenes), from other
sources in the creator's world (Mr. Robot, Jacque Fresco), byte strings, or
concatenations of non-adjacent fragments. The paste's "outlier page" idea
(one page being a different character's line) cannot be checked until more
preimages fall.
