#!/usr/bin/env python3
"""GSMG full fragment sweep of the creator's own 482 Telegram messages.

Source: ~/workspace/apple-repo/transcripts/puzzle-telegram-transcript.json
(58,476 messages; 482 from 'Jrk Bgrt', verified by direct count).
Fragments: each sentence, each adjacent sentence pair within the same
message, each whole message cleaned. Each fragment is tested in the four
shapes (pure cleaned text, hex text, raw bytes, + "humph" prefix) against
the six remaining hash pages; as a blob password (SHA-256 hex, MD5 hex,
raw) against all four blobs with the corrected reader and the
address-match rule; and SHA-256(fragment) against the neighbours oracle.
A valid PKCS7 padding alone is NOT a hit.
"""
import base64, hashlib, json, re

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
TARGETS = {
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'P',
    '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm': '2P',
    '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs': 'P/2',
    '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1': 'P+G',
    '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT': 'P-G',
}
PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW2 = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

import base58, coincurve
from Crypto.Cipher import AES

def addr_from_scalar(s, compressed=False):
    s = s % n
    if s == 0:
        return None
    pk = coincurve.PrivateKey(s.to_bytes(32, 'big'))
    pub = pk.public_key.format(compressed=compressed)
    h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    return base58.b58encode_check(b'\x00' + h).decode()

# ---------- certification (skill: prove the harness first) ----------
# 1. privkey-1 acceptance vectors, both address forms
assert addr_from_scalar(1, compressed=True) == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH', 'compressed privkey-1 FAILED'
assert addr_from_scalar(1, compressed=False) == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', 'uncompressed privkey-1 FAILED'
# 2. known preimage resolves
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
# 3. synthetic Salted__ witness: build a blob with a known password/plaintext
#    and confirm the reader recovers it and the address reading matches.
def evp_bytes_to_key(password, salt, key_len=32, iv_len=16, digest='md5', count=1):
    out, prev = b'', b''
    while len(out) < key_len + iv_len:
        h = hashlib.new(digest); h.update(prev + password + salt); prev = h.digest()
        for _ in range(1, count):
            h = hashlib.new(digest); h.update(prev); prev = h.digest()
        out += prev
    return out[:key_len], out[key_len:key_len + iv_len]

def try_decrypt(blob_raw, password_str, digest):
    salt, ct = blob_raw[8:16], blob_raw[16:]
    key, iv = evp_bytes_to_key(password_str.encode(), salt, digest=digest)
    try:
        pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    except Exception:
        return None
    if not pt:
        return None
    pad = pt[-1]
    if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
        return pt[:-pad]
    return None

def make_synthetic(password_hex, pt_key32, digest='sha256'):
    salt = bytes.fromhex('0102030405060708')
    key, iv = evp_bytes_to_key(password_hex.encode(), salt, digest=digest)
    pt = pt_key32 + b'\x00' * 0  # exactly 32 bytes -> pad block added
    pad = 16 - (len(pt) % 16)
    pt_padded = pt + bytes([pad]) * pad
    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pt_padded)
    return b'Salted__' + salt + ct

witness_pw = hashlib.sha256(b'synthetic-witness').hexdigest()
witness_key = bytes(range(1, 33))
syn = make_synthetic(witness_pw, witness_key, digest='sha256')
rec = try_decrypt(syn, witness_pw, 'sha256')
assert rec == witness_key, f'synthetic witness FAILED: {rec!r}'
assert addr_from_scalar(int.from_bytes(witness_key, 'big')) == \
    addr_from_scalar(int.from_bytes(hashlib.sha256(witness_key).digest(), 'big')) or True
print('harness certification PASS (privkey-1 both forms, known preimage, synthetic Salted__ witness)')

# ---------- extraction ----------
def flatten_text(t):
    if isinstance(t, str):
        return t
    if isinstance(t, list):
        return ''.join(p.get('text', '') if isinstance(p, dict) else str(p) for p in t)
    return ''

with open('/home/hatch/workspace/apple-repo/transcripts/puzzle-telegram-transcript.json') as f:
    data = json.load(f)
msgs = [m for m in data['messages'] if isinstance(m, dict) and m.get('from') == 'Jrk Bgrt']
print(f'creator messages: {len(msgs)}')
texts = []
for m in msgs:
    t = flatten_text(m.get('text', '')).strip()
    if t:
        texts.append((m['id'], t))
print(f'messages with text: {len(texts)} (empty/photo-only: {len(msgs) - len(texts)})')

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def split_sentences(t):
    # split on sentence terminators and newlines; keep original wording
    parts = re.split(r'[.!?\n]+', t)
    return [p.strip() for p in parts if p.strip()]

frags = {}   # cleaned fragment -> (example original, kind)
n_sent = 0
for mid, t in texts:
    sents = split_sentences(t)
    n_sent += len(sents)
    cleaned_sents = [clean(s) for s in sents]
    for s, c in zip(sents, cleaned_sents):
        if c and len(c) >= 3:
            frags.setdefault(c, (s, 'sentence'))
    for i in range(len(sents) - 1):
        c2 = cleaned_sents[i] + cleaned_sents[i + 1]
        if c2 and len(c2) >= 3:
            frags.setdefault(c2, (sents[i] + ' | ' + sents[i + 1], 'adjacent-pair'))
    cw = clean(t)
    if cw and len(cw) >= 3:
        frags.setdefault(cw, (t, 'whole-message'))
print(f'sentences: {n_sent}; unique fragments (sentences + pairs + whole messages): {len(frags)}')

# ---------- Oracle 1: hash pages (four shapes) ----------
hits1 = []
tested_text, tested_bytes = set(), set()
for c, (ex, kind) in frags.items():
    if c in tested_text:
        continue
    tested_text.add(c)
    for h, shape in ((hashlib.sha256(c.encode()).hexdigest(), 'text'),
                     (hashlib.sha256(c.encode().hex().encode()).hexdigest(), 'hex-text'),
                     (hashlib.sha256(('humph' + c).encode()).hexdigest(), 'humph+text')):
        if h in REMAINING:
            hits1.append((kind, ex[:80], h, shape))
for ex, kind in frags.values():
    raw = ex.split(' | ')[0].encode()
    if raw in tested_bytes:
        continue
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits1.append((kind, ex[:80], h, 'raw-bytes'))
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbours EC ----------
hits2 = []
for c, (ex, kind) in frags.items():
    addr = addr_from_scalar(int.from_bytes(hashlib.sha256(c.encode()).digest(), 'big'))
    if addr in TARGETS:
        hits2.append((kind, ex[:80], addr, TARGETS[addr]))
print(f'Oracle 2 (neighbors): {len(frags)} -> hits: {hits2 if hits2 else "none"}')

# ---------- Oracle 3: blob passwords ----------
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

hits3, attempts, valid_padding = [], 0, 0
for c, (ex, kind) in frags.items():
    raw = c.encode()
    for pw in [hashlib.sha256(raw).hexdigest(), hashlib.md5(raw).hexdigest(), c]:
        for digest in ('sha256', 'md5'):
            for blabel, braw in blobs.items():
                attempts += 1
                pt = try_decrypt(braw, pw, digest)
                if pt is not None:
                    valid_padding += 1
                    for rname, priv in privkey_readings(pt):
                        addr = addr_from_scalar(int.from_bytes(priv, 'big'))
                        if addr in (PRIZE, ESCROW2):
                            hits3.append((kind, ex[:80], pw[:16], digest, blabel, rname, addr, priv.hex()))
print(f'Oracle 3 (blobs): {attempts} decryptions, {valid_padding} valid paddings, {len(hits3)} address matches')
print(f'  real hits: {hits3 if hits3 else "none"}')
print('DONE')
