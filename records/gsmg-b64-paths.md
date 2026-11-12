# GSMG 5 BTC — The two base64 URL paths from the CDX

**Date:** 2026-11-11
**Approved by:** Hazrat ("work nonstop"; "so we find what remaing").
**Result: both paths resolved. Neither is a new blob.**

Source: full Wayback CDX listing of `gsmg.io/*` (420 rows, fetched 2026-11-11;
saved `/tmp/gsmg_cdx.json` — ephemeral, re-fetchable). The two base64-ish paths
flagged unfetched in `gsmg-meaning-pass.md` §6 are:

## 1. Short path — the SalPhaseIon hash in base64

URL: `https://gsmg.io/iXJ8WYuc0c+Ic/J8twV/BQZF3banoVehECOawBUvajI=`

Base64-decodes to 32 bytes, hex
`89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32` —
exactly the SHA-256 of the genesis string, i.e. the SalPhaseIon hash.
It is the same hash page in base64 form instead of hex. One Wayback capture
(2026-01-05, HTTP 200, text/html) — the site's page, not new content.

## 2. Long path — 128 opaque bytes, most likely a solver probe

URL: `https://gsmg.io/k27RwIKbkYlwcerFhyUy_SpThDLmjxDDiAOBzqhbtFEj-0lg4HVQhrMqtPLWD0pE8_e7gplJIe87L7znhl6n-fW2RAMPY4jreE9rWxsp2AYJxBL6H9P9ARWZ9uUnXR9jVYOnV4L9MrUnhCGJ5D1GcpCh2V9b7UWfx1XDY2TZ0hs=`

URL-safe base64-decodes to 128 bytes:
`936ed1c0829b91897071eac5872532fd2a538432e68f10c3880381cea85bb451`
`23fb4960e0755086b32ab4f2d60f4a44f3f7bb82994921ef3b2fbce7865ea7f9`
`f5b644030f6388eb784f6b5b1b29d80609c412fa1fd3fd011599f6e5275d1f63`
`5583a75782fd32b527842189e43d467290a1d95f5bed459fc755c36364d9d21b`

- NOT an OpenSSL `Salted__` blob (no header), so it cannot be tested with the
  kit's password families (no salt/IV to derive from).
- SHA-256 of the 128 bytes: `99e384611c58a6ec3de64a642f13310e3c1439719c3f0e8d9effc624856ff3fd`
  — matches no known hash.
- None of the four 32-byte chunks matches anything in any local repo or file
  (grep for `936ed1c0`: 0 hits).
- Live URL returns HTTP 404, 9 bytes, `Hello :-)` — the site's 404 page.
- No Wayback capture exists for this URL at all.

Verdict: almost certainly a solver probe (the CDX is full of solver-requested
URLs, including long nonsense paths and test URLs). It never resolved to
content, live or archived. Closed as a lead unless new evidence appears.
If it were a raw AES ciphertext, there is no salt/IV and no key to try it
with beyond the kit families — and a 128-byte opaque value with no
provenance does not justify a new test run.
