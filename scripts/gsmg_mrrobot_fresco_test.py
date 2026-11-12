#!/usr/bin/env python3
"""GSMG Mr. Robot + Jacque Fresco harvest — test the dialogue lines vs 3 oracles.

Source file: ~/workspace/gsmg_mrrobot_fresco_lines.txt
  - 2,427 Mr. Robot dialogue sentences (Wikiquote, S1–S4, incl. the finale
    and eps3.5_kill-process.inc), gathered by the harvest subagent.
  - 80 Jacque Fresco sentences (Wikiquote: Designing the Future 2007,
    The Best That Money Can't Buy 2002, Zeitgeist: Moving Forward 2011,
    Larry King 1974), added by Lux.
  Analysis input only (copyrighted transcripts). NOT for any repo.

Method (same as the Matrix trilogy sweep): each line is a fragment; adjacent
line pairs are also fragments. Each fragment is tested in four shapes
(pure cleaned text, hex text, raw bytes, + "humph" prefix) against the six
remaining hash pages; as a blob password (SHA-256 hex, MD5 hex, raw) against
all four blobs with the corrected reader (address match, not printability);
and SHA-256(fragment) against the neighbours oracle.
A valid PKCS7 padding alone is NOT a hit.
"""
import base64, hashlib, re

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
print('self-checks PASS')

import base58, coincurve
from Crypto.Cipher import AES

def addr_from_scalar(s):
    s = s % n
    if s == 0:
        return None
    pk = coincurve.PrivateKey(s.to_bytes(32, 'big'))
    pub = pk.public_key.format(compressed=False)
    h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    return base58.b58encode_check(b'\x00' + h).decode()

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

# ---- load lines, build fragments ----
lines = []
for raw in open('/home/hatch/workspace/gsmg_mrrobot_fresco_lines.txt', errors='ignore'):
    raw = raw.strip()
    if not raw or raw.startswith('#'):
        continue
    lines.append(raw)
print(f'lines: {len(lines)}')
frags = {}  # cleaned -> example original
for i, ln in enumerate(lines):
    c = clean(ln)
    if c and len(c) >= 3:
        frags.setdefault(c, ln)
    if i + 1 < len(lines):
        c2 = clean(ln + ' ' + lines[i + 1])
        if c2 and len(c2) >= 3:
            frags.setdefault(c2, ln + ' | ' + lines[i + 1])
print(f'fragments (lines + adjacent pairs): {len(frags)}')

# ---------- Oracle 1: hash pages ----------
hits1 = []
tested_text, tested_bytes = set(), set()
for c, ex in frags.items():
    if c in tested_text:
        continue
    tested_text.add(c)
    for h, shape in ((hashlib.sha256(c.encode()).hexdigest(), 'text'),
                     (hashlib.sha256(c.encode().hex().encode()).hexdigest(), 'hex-text')):
        if h in REMAINING:
            hits1.append((ex[:80], h, shape))
    h3 = hashlib.sha256(('humph' + c).encode()).hexdigest()
    if h3 in REMAINING:
        hits1.append((ex[:80], h3, 'humph+text'))
for ex in frags.values():
    raw = ex.split(' | ')[0].encode()
    if raw in tested_bytes:
        continue
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits1.append((ex[:80], h, 'raw-bytes'))
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbors ----------
TARGETS = {'1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm',
           '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs', '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1',
           '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT'}
hits2 = []
for c, ex in frags.items():
    addr = addr_from_scalar(int.from_bytes(hashlib.sha256(c.encode()).digest(), 'big'))
    if addr in TARGETS:
        hits2.append((ex[:80], addr))
print(f'Oracle 2 (neighbors): {len(frags)} -> hits: {hits2 if hits2 else "none"}')

# ---------- Oracle 3: blobs ----------
def evp_bytes_to_key(password, salt, key_len=32, iv_len=16, digest='md5', count=1):
    out, prev = b'', b''
    while len(out) < key_len + iv_len:
        h = hashlib.new(digest); h.update(prev + password + salt); prev = h.digest()
        for _ in range(1, count):
            h = hashlib.new(digest); h.update(prev); prev = h.digest()
        out += prev
    return out[:key_len], out[key_len:key_len + iv_len]

def try_decrypt(raw, pw, digest):
    salt, ct = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(pw, salt, digest=digest)
    try:
        pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    except Exception:
        return None
    if not pt:
        return None
    pad = pt[-1]
    return pt[:-pad] if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad else None

kit = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
blobs = {}
for fname, label in [('blob1_phase32_final.txt', 'blob1'),
                     ('blob2_salphaseion.txt', 'blob2'),
                     ('blob3_cosmic_duality.txt', 'blob3'),
                     ('blob4_urlblob.txt', 'blob4')]:
    blobs[label] = base64.b64decode(open(f'{kit}/{fname}').read().strip())
line1 = 'U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z'
line2 = 'QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
blobs['blob2A'] = base64.b64decode(line1)
blobs['blob2B'] = base64.b64decode(line1 + line2)

def privkey_readings(pt):
    out = [('sha256(pt)', hashlib.sha256(pt).digest())]
    if len(pt) >= 32:
        out += [('first32', pt[:32]), ('last32', pt[-32:])]
    if len(pt) >= 64:
        out.append(('sha256(first64)', hashlib.sha256(pt[:64]).digest()))
    return out
PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW2 = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
hits3, attempts, valid_padding = [], 0, 0
for c, ex in frags.items():
    raw = c.encode()
    for pw in [hashlib.sha256(raw).hexdigest().encode(), hashlib.md5(raw).hexdigest().encode(), raw]:
        for digest in ('sha256', 'md5'):
            for blabel, braw in blobs.items():
                attempts += 1
                pt = try_decrypt(braw, pw, digest)
                if pt is not None:
                    valid_padding += 1
                    for rname, priv in privkey_readings(pt):
                        addr = addr_from_scalar(int.from_bytes(priv, 'big'))
                        if addr in (PRIZE, ESCROW2):
                            hits3.append((ex[:80], pw[:16], digest, blabel, rname, addr, priv.hex()))
print(f'Oracle 3 (blobs): {attempts} decryptions, {valid_padding} valid paddings, {len(hits3)} address matches')
print(f'  real hits: {hits3 if hits3 else "none"}')
print('DONE')
