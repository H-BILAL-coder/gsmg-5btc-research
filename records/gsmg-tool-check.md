# GSMG 5 BTC — The single unnamed tool + the 11,473 outputs file

**Date:** 2026-11-11
**Approved by:** Hazrat ("check it"). Identification research, NOT brute force.
No new password lists generated; no contact with the creator; no
privatekeys.pw key/balance pages.
**Result: 0 HITS on everything tested.**

Sources: floflo777/open-crypto-puzzles `1-big-prizes/gsmg-io-5btc-puzzle/analysis/leads.md`
§4 (local clone `~/workspace/floflo-repo/`, HEAD 2026-11-10 14:54 UTC),
`analysis/tested.md` §§15–17, 466; the candidate tools' own source code (quoted
below); `~/workspace/gsmg-esrever-results.json` (the confirmed Bifid segment and
plaintext); `~/workspace/gsmg_tool_menu_test.py` and
`~/workspace/gsmg-tool-menu-results.json`.

---

## LEAD 1 — Identify the single unnamed tool

floflo §4 fingerprints: (a) the tool's Bifid implementation takes **no period
parameter** — it always uses a period equal to the full message length (exactly
the convention confirmed on the puzzle's own Bifid step, period 570 = full
message); (b) its available cipher list is **short** (fewer than a dozen
ciphers). The name is in floflo's private research, not the public docs.

### IDENTIFIED: lukaszbanasiak/python-ciphers

**https://github.com/lukaszbanasiak/python-ciphers** — "Simple ciphers
implementation in Python."

**Fingerprint (a) — no Bifid period parameter: MATCHES.** The Bifid CLI
options are only `-d` (decrypt), `-k` (key), `-V` (verbose), `-f` (file).
The whole transform is (`Bifid.py`, verbatim):

```python
def transform(data):
    data = re.sub(r'[\D]+', '', data)
    return data[::2] + data[1::2]

def transform_back(data):
    data = re.sub(r'[\D]+', '', data)
    numbers = ''
    a, b = (data[:len(data) / 2], data[len(data) / 2:])
    for i in range(len(a)):
        numbers += a[i] + b[i]
    return numbers
```

`transform` splits the coordinate digit string into evens + odds — the entire
message as one block. There is no period anywhere in the file.

**Fingerprint (b) — short cipher list: MATCHES.** The repo contains exactly
five ciphers — AtBash, Bacon, Bifid, Caesar, Polybius — plus CharFreq (frequency
analysis, not a cipher). Fewer than a dozen.

**Chronology: fits.** Created 2013-03-25, version 1.0 — six years before the
puzzle (2019-04-13). Python 2 CLI (Polish author, Łukasz Banasiak).

**Decisive test — the tool's exact code reproduces the puzzle's Bifid
byte-for-byte.** A faithful Python-3 port of the tool's `Polybius.generate_array`
+ `encode` + `transform_back` + `decode`, with key `DBIFHCEG`, applied to the
puzzle's 570-char segment, reproduces the confirmed plaintext exactly
(starts `BTCSEED`, identical to the esrever script's plaintext). The tool's
keyed-square construction (`alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'`, key
letters first, J skipped, row-major) is the same construction the puzzle's
Bifid uses.

**Caveat (recorded honestly):** the tool has **no Beaufort and no VIC**, yet
the puzzle's solved phases used Beaufort (key `THEMATRIXHASYOU`) and the VIC
straddling checkerboard. If the author used this one tool for *every* phase,
that is a contradiction — it cannot have built the Beaufort/VIC phases.
Possible readings: (i) floflo's identification is about the Bifid convention
specifically and the author used this tool for the Bifid/Polybius phases (and
other means for Beaufort/VIC); (ii) the match is a coincidence of a common
simple Bifid convention (many simple implementations omit the period); (iii)
the real tool is a different one with the same Bifid fingerprint plus
Beaufort/VIC — none was found in this search (see scorecard). The Bifid +
menu match is exact; the "same software for every phase" claim is in tension
with it, and that tension is unresolved.

### Menu test — the tool's own ciphers against the open objects: 0 HITS

Script `~/workspace/gsmg_tool_menu_test.py`, results
`~/workspace/gsmg-tool-menu-results.json`. Self-checks pass (privkey-1
vectors exact; tool Bifid == puzzle Bifid plaintext).

Method: the tool's five ciphers, ported faithfully, applied to the open
objects — the 256-symbol object, the Bifid plaintext (570), streamA, streamB,
the 29 dropped letters, the 91-letter prefix, plus the 252 saved
valid-padding plaintexts from the kit (`big_hits.txt` + `smart_screen_*`,
audit parser). Transforms per object: Caesar shifts 1–25, AtBash, Bacon
encode, Polybius encode (DBIFHCEG square + default square), Bifid encrypt +
decrypt (DBIFHCEG square + default square) = 33 outputs per object.
Every output was tested as a password against all three blobs with BOTH
digests (SHA-256 + MD5) through the corrected reader (floflo `readings()`,
both address forms, vs the prize address AND the second escrow), and checked
directly as a key when it was exactly 32 bytes or 64 hex chars.

| Measure | Count |
|---|---|
| Transform outputs tested as passwords | 8,514 (198 string objects + 8,316 saved-plaintext) |
| Valid-padding plaintexts | 217 (≈200 expected by chance: 8,514 × 6 / 256) |
| Key readings checked | 9,610 |
| Direct key checks (32-byte / 64-hex outputs) | 62 |
| Long entirely-printable plaintexts (≥64 bytes) | 0 |
| **Hits** | **0** |

Conclusion: the tool's menu, applied to the open objects, produces nothing.
If this is the tool, its menu is exhausted on these objects (as floflo §4
said would kill the identification's usefulness — every cipher on the menu
tested with no match on the currently open objects).

### Scorecard — every other candidate checked

| Candidate | Bifid period? | Cipher menu | Verdict |
|---|---|---|---|
| **lukaszbanasiak/python-ciphers** | **None** (only -d/-k/-V/-f; `data[::2]+data[1::2]`) | **5 ciphers** | **MATCHES BOTH** |
| cryptii (github.com/cryptii/cryptii, `src/Encoder/BifidCipher.js`) | None (only `key` setting; whole-message transpose) | 37 encoder bricks, ~14 classical ciphers | Fails (b) — menu not short |
| CyberChef (GCHQ; via ToolFactory) | None ("no separate period control") | Hundreds of operations | Fails (b) |
| Boxentriq | Has period control ("Optional. Leave blank to use the full message length") | Many tools | Fails (a) and (b) |
| CacheSleuth | Has period grouping ("leave it blank to use the full text length") | Many tools | Fails (a) and (b) |
| Practical Cryptography | Has `Period =` input | ~25 ciphers | Fails (a) and (b) |
| pycipher (jameslyons/pycipher, `bifid.py`) | Has period ("must be a positive integer") | ~25 ciphers | Fails (a) and (b) |
| ciphertool (SourceForge, `cipherProc configure -period n`) | Has `-period n` | Dozens of cipher types | Fails (a) and (b) |
| R `ciphertext` package | Has `period = 100` default | ~12 ciphers (borderline) | Fails (a) |
| dcode.fr | Has period field (`period" name="period" value="5"`) | Hundreds of tools | Fails (a) and (b) |
| Rumkin | Page describes full-message fractionation; tool form not confirmed | 48 cipher tool paths | Fails (b) |
| kit.forhosting.com | No period mentioned; full-message fractionation described | Huge tool site | Fails (b) |
| ZapadRo97/AnotherCipherProgram | No period seen (Affine + Bifid only) | 2 ciphers | **Ruled out on chronology** — created 2020-04-28, after the puzzle (2019) |
| ChrisJMurphy/cipher | Bifid-only project | No menu (single cipher) | Does not fit the "cipher list" fingerprint |

No other candidate matches both fingerprints. cryptii and CyberChef match
(a) but fail (b); every other named tool fails (a).

---

## LEAD 2 — Re-check the 11,473 outputs file

floflo `analysis/leads.md:44` and `analysis/tested.md:466`: 11,473
valid-padding plaintexts from sections 15–17, open follow-up (re-read through
the extended readings, flag any entirely-printable 64+ byte decrypt). The file
was in floflo's private research folder, NOT public as of the 2026-11-11 audit.

**Still NOT public.** Checked 2026-11-11:

| Where | Result |
|---|---|
| floflo777/open-crypto-puzzles (local clone, HEAD 2026-11-10 14:54 UTC; GSMG path last commit 2026-10-18) | `data/` holds only `pipeline-stages.json`, `planted-addresses.csv`, `stage-chain.json`. No outputs file. |
| SHEMZILLER/open-crypto-puzzles (fork, cloned 2026-11-11) | Older snapshot; `data/` holds only `pipeline-stages.json` + `stage-chain.json`. No outputs file; no "11473" anywhere in the GSMG folder. |
| puzzlehunt/gsmgio-5btc-puzzle (local clone, last commit 2021-05-25, 0 behind after fetch) | No outputs file; no "11473". |
| Naddiseo/gsmgio-5btc-puzzle (local clone, last commit 2026-09-29, 0 behind after fetch) | No outputs file; no "11473". |
| AppleLamps/puzle (local clone, last commit 2026-08-07, 0 behind after fetch) | No outputs file. The "11473" grep hits there are false positives — hex substrings inside SHA-256 hashes (e.g. `…6174691147362f51c…`), not the number 11,473. |
| NoobSilence/crypto-puzzle-lab (cloned 2026-11-11) | No "11473" anywhere; no valid-padding file. GSMG material is docs + `knowledge_base/gsmg.json` only. |
| Web search ("GSMG 11473 valid padding plaintexts") | Only floflo's own `leads.md` mentions the figure. No file, no mirror, no paste. |

**No audit was possible** — the file is not available anywhere public. The
count (11,473) is verified as a documented figure; the plaintexts themselves
remain in floflo's private research folder. The audit's own corrected-oracle
re-run (2,908,328 passwords, 64,157 valid-padding plaintexts, 1,283,140 key
readings, 0 hits) is the closest available substitute and is also negative.

---

## What remains

- The tool identification is the strongest lead of the two: a real,
  publicly available tool whose Bifid reproduces the puzzle's Bifid
  byte-for-byte and whose menu is exactly five ciphers. Its menu is now
  exhausted on the open objects (0 hits). The Beaufort/VIC tension is
  unresolved — either the author used more than one tool, or the Bifid match
  is a coincidence of a common simple convention.
- The 11,473 outputs file is still private. Nothing further can be done on
  that lead from public material.
- The July 12, 2026 hint (close friends / personal knowledge) remains the
  only substantive pointer for the meaning reconstruction.
