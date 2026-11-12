# GSMG 5 BTC — Phases 1–3: on-chain OP_RETURNs, audio metadata, manifestos

**Date:** 2026-11-11
**Approved by:** Hazrat (pasted three-phase plan; same standing "work nonstop"
brief).
**Result: 0 hits on the remaining six hashes in all three phases.**

## Phase 1 — Genesis / funding transaction hex

All 129 transactions of the prize address `1GSMG…` fetched from mempool.space.
**81 OP_RETURN outputs, 40 distinct payloads** (most duplicated 2–4×).
Script `~/workspace/gsmg_phases_123.py`; raw data `/tmp/gsmg_prize_txs.json`.
The pushed data was parsed properly (OP_RETURN opcode + push-length skipped),
so the spurious 'j' (0x6a) and length-byte prefixes are removed.

The payloads are **solver graffiti**, not creator content: stage answers
("yourlastcommand", "secondanswer", "matrixsumlistenterlastwordsbeforearchichoicethispassword",
"leavethematrix", "fourfirsthintisyourlastcommand", "fanstoo"), Matrix quotes
("THEMATRIXHASYOU", "There is no spoon", "If I were you, I'd hope we dont
meet again.", "happy xmas! Everything That Has A Beginning Has An End"),
claims ("hereismysecret" ×4, "isolveditwithanabacus", "iamtheone",
"Causality Transcended", "Turing Complete.", "The answer is women",
"#SOLUTION", "redpill", "entertherabbithole", "From Neo"), and one solver's
signature address `bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd` (standalone
and suffixed to three stage answers). Two hex-looking strings
("673b7b4b67571b1b4b-3.o", "844e86a69a04eea672049e0e0e8612") were also hashed.
The creator's known 2021-07-18 OP_RETURN ("GSMG.io neighbors, half and
double") is NOT among these 129 transactions — it was sent from a different
address, and was already verified in the audit.

## Phase 2 — Decentraland audio metadata

exiftool is not installed on this VM (wiped); `strings` was used instead.
Both copies of `puzzlepiece.mp3` (identical, 212,031 bytes) contain only
standard encoder metadata: **"Logic Pro X 10.4.1"** (encoder), "engiTunNORM"
and "engiTunSMPB" (iTunes normalisation data). No ID3 comments, no lyrics,
no hidden text blocks, no software-profile tags with keys.
`channel_difference.wav` has a minimal RIFF header (WAVEfmt, LIST, data) —
no extra metadata. The spectrogram PNGs carry no tEXt/iTXt/zTXt chunks.
There are no "alternate tracks" locally — only the one mp3 and the derived
difference WAV. All recovered strings were hashed: 0 hits.

## Phase 3 — Matrix "Source Code" manifestos

The archived What Is The Matrix site (1999 captures) is **Flash/image-based**:
the homepage and index2.html contain no recoverable text beyond "MATRIX" and
navigation button names. The red/blue pill text is not in the HTML captures.
The recoverable manifesto text is the **non-dialogue text of the IMSDb
Matrix (1999) script — 1,496 lines** (scene descriptions, on-screen text,
the opening trace program). The red/blue pill speech itself is Morpheus
dialogue and was already harvested in the earlier dialogue runs. All
non-dialogue lines were hashed in the four shapes: 0 hits.

## Totals

2,306 candidates → **6,855 text hashes + 2,306 byte hashes, 0 hits.**
The remaining six preimages (`0b0f37ec…`, `21ef0533…`, `673e3b1a…`,
`a2aefdbb…`, `aca20ae7…`, `c2eef34b…`) are not in the prize address's
on-chain messages, the Decentraland audio metadata, or the Matrix (1999)
non-dialogue text.
