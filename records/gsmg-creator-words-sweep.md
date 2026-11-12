# GSMG 5 BTC — Full fragment sweep of the creator's own 482 Telegram messages

**Date:** 2026-11-12
**Approved by:** Hazrat ("find it by applying all your power").
**Result: 0 hits on all three oracles.**

## Why this was a genuine gap

Prior work tested 84 hand-picked candidates from his words
(`gsmg-close-reading.md`) and cross-domain combinations
(`gsmg-hash-dictionary.md`), but never every sentence of every message as
a fragment. This sweep closes that gap.

## Source

The full Telegram export on disk:
`~/workspace/apple-repo/transcripts/puzzle-telegram-transcript.json`
(58,476 messages). **482 messages are from `Jrk Bgrt`** (verified by
direct count, matching the profile). 466 of them carry text; 16 are
empty/photo-only (photos, stickers, GIFs — no text to test). No scraping,
no contact with anyone.

## What was tested

Extraction: every message's text flattened (13 messages store text as
entity lists — mentions, links, bot commands — flattened to plain text),
split on sentence boundaries (`.`, `!`, `?`, newlines), original wording
kept.

- Sentences: 725 total, **634 unique** (cleaned, ≥3 alphanumerics).
- Adjacent sentence pairs within the same message: **259 unique**.
- Whole messages cleaned: **412 unique**.
- **Total unique fragments: 937.**

Each fragment was tested (script `~/workspace/gsmg_creator_words_sweep.py`,
log `gsmg_creator_words_sweep.log`):

1. **Oracle 1 — hash pages** (four shapes: pure cleaned text, hex text,
   raw bytes, + "humph" prefix): 937 text + 698 byte hashes — **0 hits**.
2. **Oracle 2 — neighbours EC** (SHA-256 of fragment → uncompressed
   address vs P and the four neighbours): 937 — **0 hits**.
3. **Oracle 3 — blob passwords** (SHA-256 hex, MD5 hex, raw × SHA-256/MD5
   EVP × 4 blobs + both corrected blob2 readings): **33,732 decryptions,
   114 valid paddings** (expected ~132 at the 1/256 chance rate — within
   chance), **0 address matches** — 0 real hits.

## Harness certification (before trusting the negative)

- privkey-1 acceptance vectors, **both** address forms: compressed
  `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH` ✓, uncompressed
  `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm` ✓.
- Known preimage resolves: SHA-256 of
  `hopeisthequintessentialhumandelusion` = `c1780cbb…` ✓.
- Synthetic Salted__ witness: a blob built with a known password and
  known 32-byte key was recovered exactly by the reader ✓.

Note: the run first failed with `ModuleNotFoundError: No module named
'base58'` — a VM replacement had wiped the pip packages again. Fixed with
`pip install --break-system-packages pynacl bip_utils==2.12.3 base58
coincurve pycryptodome`; imports verified before the run.

## What this closes

No sentence, sentence pair, or whole message the creator ever typed in
Telegram — including the riddle-like July 16 line, the only self-declared
hint, the "tiny hint" promise, the yinyang lines, the hidden-laptop line,
and the "some already found it" line — is the final password, a hash-page
preimage, or a neighbours scalar, in any of the four shapes. Combined with
the close reading (84 hand-picked candidates) and the hash dictionary
(cross-domain combinations), **his own words are now exhaustively
swept as fragments**. If the answer is in his words at all, it is not a
sentence he typed — it would have to be a combination, a transformation,
or something he never said in that chat.
