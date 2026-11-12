# GSMG 5 BTC — Internal mechanics audit + 2021 creator address

**Date:** 2026-11-12 (early hours)
**Approved by:** Hazrat (pasted pivot plan; same standing "work nonstop" brief).
**Result: 0 hits on the remaining six hashes.**

## The 2021 creator address — full audit

`3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK` has only **30 transactions** in total.
All 18 OP_RETURN payloads recovered (mempool.space, saved
`/tmp/gsmg_creator_2021_txs.json`). The creator's own verified messages
(2020–2021, from his vanity wallet):

- 2021-07-18 — "GSMG.io neighbors, half and double" (tx a82052a2…)
- 2020-05-10 — "Halving"
- 2020-04-12 — "Good job, Neo!" (×2)
- 2020-04-18 — "GSMG.io: You are here because 227 chars were correct"
- 2020-04-18 — "GSMG.io: phase3.2 pass OK"
- 2020-04-18 — "GSMG.io: are you sure?"
- 2020-04-18 — "GSMG.io: part of the cipher"
- 2020-04-18 — "GSMG.io: do you beleive me you need it?" ("beleive" misspelled)
- 2020-04-18 — "GSMG.io: Right, this is causality"

The 2025 messages on the same address are solver graffiti ("I thought choice
was an illusion?", "Happy late mothers day!", "Yes", "BULLSHIT", a Neo wallet
address). The neighbors tx spends 21,048 sats from the vanity wallet and pays
5,000 sats each to four addresses — `1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT`,
`16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs`, `1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm`,
`1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1` (the uncompressed 2P, P/2, P+G, P-G
addresses). All nine creator messages, their no-prefix variants, the four
neighbor addresses, the txids and the input/output addresses were hashed in
all four shapes: 0 hits.

## Internal artifacts hashed

Script `~/workspace/gsmg_internal_audit.py` — 276 text + 84 byte candidates,
**568 text hashes + 360 byte hashes, 0 hits**:

- **Solved stage keys** (causality, theflower…, the three riddles, theseedisplanted,
  ourfirsthintisyourlastcommand, yinyang, the genesis string, Phase 3 components)
  and the SHA-256 of each in text / raw / hex-of-hex shapes.
- **Known pages, recursive**: all six identified pages (incl. the two Architect
  quotes) hashed as hex text, uppercase hex, raw bytes and hex-of-hex.
  f9719d6d verified by computation: SHA-256 of the raw bytes of the SalPhaseIon
  hash = `f9719d6d531e6c3b5129644cd05da57bc6fdd075c9a61267c41d4b9627936096`.
- **Half / Better Half keys**: hex, raw bytes, WIF (comp + uncomp), addresses
  (comp + uncomp), XOR, concatenations.
- **Blob salts and ciphertexts** (all four blobs): salt hex/raw, base64 text,
  raw blob, ciphertext raw/hex, SHA-256 of ciphertext and of whole blob.
- **File checksums**: SHA-256 (hex + raw) and MD5 of the poster, puzzle.png,
  theseedisplanted.png, phase2.png, phase3.png, the 2020 photo, the Cosmic
  Duality PDF, the Bitcoin whitepaper PDF and puzzlepiece.mp3
  (mp3 SHA-256 `ef17a96dce37b4dd7cbf79f210c5cbaf37fcae60e5faf8004de4e0832bd0dfee`).

## What this means

The remaining six preimages (`0b0f37ec…`, `21ef0533…`, `673e3b1a…`,
`a2aefdbb…`, `aca20ae7…`, `c2eef34b…`) are not the creator's verified on-chain
messages, not the solved stage keys or their hashes, not the known pages
hashed again, not the Half keys, not the blob salts/ciphertexts, and not the
puzzle files' checksums. The creator's "227 chars were correct" message is
new to the record — 227 characters is a specific count, but it is a message
about a stage, not a preimage. The literary canon (Neuromancer, Snow Crash,
Ghost in the Shell, Alice in Wonderland, Cypherpunk Manifesto) remains
untested and low-yield by the plan's own assessment.
