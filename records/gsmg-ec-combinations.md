# GSMG 5 BTC — EC key-combination test

**Date:** 2026-11-12 (early hours)
**Approved by:** Hazrat (pasted pivot plan; same standing "work nonstop" brief).
**Result: 0 hits.**

## The test

The "neighbors, half and double" hint may mean the prize key k is formed by
COMBINING existing solved keys with elliptic-curve math, not by hashing one
password. Script `~/workspace/gsmg_ec_combinations.py`.

44 known scalars collected: the Half and Better Half keys; SHA-256 of every
stage answer (causality, flower, the three riddles, theseedisplanted,
ourfirsthint, yinyang, genesis string, thematrixhasyou, the 149-digit string,
the 91-letter phrase, the nine creator OP_RETURN messages); the six known
page hashes as scalars; the four blob salts (zero-padded to 32 bytes); four
file SHA-256s.

Operations (all mod n, secp256k1 order):
- single-key: double (2a), half (a/2), plus1 (a+1), minus1 (a-1)
- pairwise: add (a+b), sub (a-b, b-a), xor (a^b)

Each result's UNCOMPRESSED address was compared against P and its four
neighbours (2P, P/2, P+G, P-G). **3,960 scalar combinations tested, 0 hits.**

Certified: privkey-1 uncompressed reproduces `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`.

## What this means

The prize key is not a sum, difference, XOR, double, half, or ±1 of any pair
of known keys. Combined with the neighbors oracle (no single candidate is k
or a neighbour), the EC-combination route on known keys is exhausted. The
"neighbors" hint therefore does not point to a combination of the keys
already in hand — it points to a value not yet identified, or it is a
structural description of the key's derivation rather than a recipe.

Note on the paste's "Cosmic Duality" premise: the Cosmic Duality PDF is the
1991 Time-Life survey book, verified byte-for-byte — it is not the creator's
own writing, and the creator never says "Cosmic" or "Duality" in Telegram.
The creator's own words are the Telegram messages (482 verified) and the
2020 OP_RETURNs, not that book.
