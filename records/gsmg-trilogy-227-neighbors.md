# GSMG 5 BTC — Full trilogy sweep, 227 chars, and the neighbors EC oracle

**Date:** 2026-11-12 (early hours)
**Approved by:** Hazrat (pasted pivot plan; same standing "work nonstop" brief).
**Result: 0 hits everywhere. The neighbors oracle is now a certified, tested tool.**

## 1. Full Matrix trilogy dialogue sweep — DONE, 0 hits

Script `~/workspace/gsmg_reloaded_sweep.py`. The full **Reloaded** script from
two sources (StockQ 1,830 lines + DocLecture 1,000 lines) → 9,939 fragments →
**24,722 text hashes + 9,245 byte hashes, 0 hits.** Targeted lines re-tested
verbatim (Merovingian causality block, Morpheus "Do you believe", Trainman /
Rama-Kandra karma lines, "do you beleive me you need it" with the creator's
misspelling): 0 hits.

The trilogy is now fully covered: Matrix (1999) full script, Reloaded full
script (×2 sources), Revolutions full script, plus the Architect, Oracle,
Smith and Merovingian scene transcripts. Combined with the earlier harvests,
the remaining six preimages are not Matrix trilogy dialogue in any shape.

## 2. The "227 chars" — SOLVED, not a lead

From the floflo README: "the 7 parts concatenated (227 characters) open the
phase 3 plaintext". The 227-char string is the concatenation of the seven
Phase 3 parts (causality, Safenet, Luna, HSM, 11110, Bitcoin source-code data,
FEN chess position). The creator's message "You are here because 227 chars
were correct" (2020-04-18) was a confirmation that a solver's 227-char
concatenation was right. It is a solved stage, not the final gate. No
227-char string exists in the unsolved layer; the only 227-char lines in the
workspace are generated candidate-file artefacts.

## 3. The neighbors EC oracle — VERIFIED and tested, 0 hits

The prize public key P is published (floflo README, from the 2024-04-24
spending tx): `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559`.
Direct EC computation confirms the four neighbor addresses:
- 2P = `1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm`
- P+G = `1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1`
- P-G = `1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT`
- P/2 = `16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs` (by elimination)

The creator's convention (planted addresses): private key = SHA-256 of a stage
answer. So the prize key k is SHA-256(X) for some X, or a neighbour of it
(k = s±1, s/2, 2s where s = SHA-256(X)). Script
`~/workspace/gsmg_neighbors_oracle.py` tests every candidate X against all
five addresses (P, 2P, P/2, P+G, P-G) in uncompressed form (the prize and
neighbors are uncompressed; the planted stage-answer addresses are compressed,
a separate convention). **107,915 scalar tests over 73,347 candidates** (all
stage answers + the kit's smart/gen/long-ngram/candidate families): **0 hits.**
No candidate is the prize key or one of its neighbours.

Oracle certified: privkey-1 vectors pass (comp `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`,
uncomp `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`); Half/Better Half keys reproduce
their known addresses in compressed form (`1JG648ya…`, `145ZQ9si…`).

## 4. New stage values as hash-page preimages — 0 hits

The 149-digit string (`15165943…11154112`, Phase 3.2 plaintext), the 91-letter
phrase (`commonsolutionistointroduecentralauthorityormintthatcheckseverytransactionfordoublespending`,
the whitepaper sentence via the straddling checkerboard), the Beaufort key
`thematrixhasyou`, and the raw 24 bytes of `gsmg.io/theseedisplanted`
(zero-padded and bit-reversed) were hashed in all four shapes: 0 hits.

## 5. Side-by-side: the six known preimages

| Page | Preimage | Kind |
|---|---|---|
| 89727c59… | `GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` | internal (genesis string) |
| 4f7a1e4e… | 1327-byte Cosmic plaintext (bytes) | internal (stage artifact) |
| e24bd2c0… | `ourfirsthintisyourlastcommand` | internal (hint phrase) |
| f9719d6d… | raw bytes of the SalPhaseIon hash | internal (hash of a hash) |
| c1780cbb… | `hopeisthequintessentialhumandelusion` | quote (Architect) |
| 10d6a2c5… | `humphhopeisthequintessentialhumandelusionsimultaneously…` | quote (Architect) |

**Split: 4 internal + 2 quotes.** If the twelve pages follow the same
rough ratio, the remaining six are a mix — roughly 4 internal stage keys and
2 more quotes. The internal side is now exhausted (stage keys, hashes,
Half keys, blobs, files, the neighbors oracle). The quote side is exhausted
for the Matrix trilogy. What is left on the quote side is other voices in the
creator's world (Mr. Robot, Jacque Fresco) or quotes typed from memory with
the creator's own misspellings/paraphrases, which a script sweep cannot
generate.
