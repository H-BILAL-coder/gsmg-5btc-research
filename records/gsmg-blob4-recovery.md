# GSMG 5 BTC — 4th blob (urlblob) recovery attempt

**Date:** 2026-11-11
**Approved by:** Hazrat ("do it" — both next steps; this is the blob-recovery half).
**Script:** `~/workspace/gsmg_blob4_test.py` (retargeted copy of `gsmg_rerun.py`) ·
**Results JSON:** `~/workspace/gsmg-blob4-hits.json` ·
**Blob saved to kit:** `~/workspace/your_files/gsmg-puzzle-kit/blob4_urlblob.txt`

---

## 1. STEP 1 — The exact target

The "4th blob" is the **urlblob**: an orphaned, independent OpenSSL `Salted__`
AES-256-CBC container, **salt `74c974e3f92e64b5`, 96 bytes of ciphertext**
(112 bytes total decoded).

**Exact source URL path** (reconstructed and verified from the blob bytes —
see §2):
`gsmg.io/53616c7465645f5f74c974e3f92e64b59f7ea22a50dcb0d4289d176d4ce9dba7f99a695b8d0797b5c7791e65a8d2b68a5879f5d31ae5e8a2635205de31b851cf43b2534f58765696d3c2a01f7f3a41f7284fbbcc836517cbf7ba613c43a919d9dc669e4824baba6a5caeb77dfc3e0607`
(224 hex chars; prefix `53616c7465645f5f` is ASCII `Salted__`; ends `0607`.)

**Provenance** (Hosterjack attempt `urlblob-4th-orphaned-blob-salt-74c974e3`,
2026-02-07, in `content/attempts.js` of
`hosterjackagv/gsmg-5btc-puzzle`): "A hex-encoded Salted__ blob found as a
literal gsmg.io URL path in the CDX: gsmg.io/53616c7465645f5f74c974e3f92e64b5…0607
(captured 2026-02-07, returns the SPA shell). Decoded to urlblob.bin (112 bytes
total) = magic 'Salted__' + salt 74c974e3f92e64b5 + 96-byte ciphertext (6 AES
blocks)." Method: "Spotted a long hex string used as a URL path in the Wayback
CDX, recognized its prefix 53616c7465645f5f as ASCII 'Salted__' (the OpenSSL
enc magic), and hex-decoded it to recover a complete fourth AES-256-CBC blob
with its own random salt." It is orphaned — provenance is only a
community-posted URL path (the page itself returns the empty SPA shell) — and
structural analysis confirms it shares no ciphertext blocks with the other
three blobs: an independent container, not a fragment of cosmic.

**Why it was recorded "unrecoverable":** on 2026-11-01 the Wayback Machine was
offline when Lux tried to fetch it, so it was never recovered then. The blob
itself was already public in the Hosterjack repo's `ciphertexts/urlblob.txt`
since 2026-02-07 — the "unrecoverable" status was stale; the repo copy was
simply never checked.

**The other three blobs for reference** (from the same Hosterjack provenance
line): cosmic salt `2d3f6fe0`, salph_inner `3ab58534`, p32_trailing `b45a5e3d`.

**Prior sweep (Hosterjack, recorded in the same entry):** "76 tests → 0 valid
padding, 0 readable hits" under their byte-exact harness. That was a small
key set only — the kit's full candidate families had never been run against
urlblob before this attempt.

---

## 2. STEP 2 — Recovery

**Recovered — from the public Hosterjack repo, NOT from the Wayback Machine.**

- `https://raw.githubusercontent.com/HosterjackAGV/gsmg-5btc-puzzle/main/ciphertexts/urlblob.txt`
  (152 bytes) — fetched 2026-11-11.
- Base64: `U2FsdGVkX190yXTj+S5ktZ9+oipQ3LDUKJ0XbUzp26f5mmlbjQeXtcd5HmWo0raKWHn10xrl6KJjUgXeMbhRz0OyU09YdlaW08KgH386QfcoT7vMg2UXy/e6YTxDqRnZ3GaeSCS6umpcrrd9/D4GBw==`
- Decodes to 112 bytes: header `Salted__`, salt `74c974e3f92e64b5` (EXACT
  match to the recorded salt), 96 bytes ciphertext (EXACT match to the
  recorded size).
- The full hex URL path reconstructed from the recovered bytes starts with
  `53616c7465645f5f74c974e3f92e64b5` and ends with `0607`, matching the
  truncated path in the Hosterjack entry exactly.
- Saved to the kit as `blob4_urlblob.txt` (verified: salt + 96-byte ct).

**Archive attempts:**
- **Wayback Machine CDX API** — tried 3 times 2026-11-11: first attempt
  returned the "Internet Archive: Temporarily Offline" page; a retry then
  returned live results for a general `gsmg.io/*` query (first captures
  visible, e.g. `https://www.gsmg.io/` 2019-04-22); a prefix query for the
  exact hex path then returned "Temporarily Offline" again. The CDX API is
  flaky right now (intermittently offline). The exact-URL query
  (`url=gsmg.io/53616c7465645f5f74c974e3f92e64b5`, exact match on the
  truncated prefix) returned `[]` — not a real negative, since the full path
  is 224 hex chars and the query was a prefix. No CDX verification of the
  2026-02-07 capture was possible in this session; the recovery does not
  depend on it (the blob bytes themselves verify against the recorded salt
  and size, and the reconstructed hex path matches the entry's truncated
  path).
- **gsmg-archive.org** — the archive site linked from the Hosterjack footer
  ("gsmg.io archive (original pages)") returns HTTP 200 and is online now
  (it was the site recorded offline on 2026-11-01). It was not needed for
  the recovery, since the blob was already in the public repo.
- **archive.today / Common Crawl / web search for the filename** — not
  needed; the blob was recovered from the primary public source
  (Hosterjack repo) before reaching those steps.

---

## 3. STEP 3 — Testing the kit's candidate families against blob4

**Status: RUNNING at time of writing** — `gsmg_blob4_test.py` (exact copy of
the audit's `gsmg_rerun.py` oracle, retargeted to blob4 only): streams A
(stored files), B (big_combine 2,332,800), C (wave2 400,920); both digests
(SHA-256 + MD5); corrected reader (floflo readings() + 2k/k/2 neighbours +
8 split-key combinations); both address forms; vs the prize address
`1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` AND the second escrow
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`; third-door check included.
Self-checks PASS (privkey-1 vectors + escrow pubkey → prize address).

**Result: COMPLETE, 0 HITS** (2026-11-11, ~625 s).

| Measure | Count |
|---|---|
| Passwords (streams A + B + C) | 2,908,328 |
| Decrypt attempts (× 2 digests) | 5,816,656 |
| Valid-padding plaintexts | 22,825 (chance: 2,908,328 × 2 / 256 ≈ 22,721 — exactly chance) |
| Key readings checked | 456,500 |
| Third-door checks | 0 hits |
| Long-printable plaintexts (≥64 bytes) | 0 |
| **Hits** | **0** |

Stream A alone: 174,608 passwords, 1,408 valid paddings, 28,160 readings,
0 hits. No candidate family in the kit opens urlblob under either digest,
in any tested reading or split-key combination. Combined with Hosterjack's
own 76-test null, urlblob is now swept null by the kit's full families too.

**Conclusion:** the 4th blob is recovered, verified genuine, and tested —
it contains no key reachable from any kit candidate family. Its recovery
closes the "unrecoverable" status, but it does not advance the solve: like
the other three blobs, it needs the same missing password. The blob is now
in the kit as `blob4_urlblob.txt` for any future candidate family.
