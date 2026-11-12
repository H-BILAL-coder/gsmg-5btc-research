#!/usr/bin/env python3
"""GSMG wave 3 — Geometric reading: test the measured geometry vs 3 oracles.

Measurements (all new in wave 3; wave 1-2 values NOT re-tested):
  POSTER (puzzle.png 1048x1556): rabbit bbox 195x195, centre (592,547),
    cols 6-9 rows 6-8, 6975 black px; QR 231x231 at (1,1289); red line
    15px rows 1047-1061; coloured cells row/col positions (see record).
  SCENE (game.js decompiled): 9 cubes, all x=8; y (creation order)
    1,7,7.5,7,6,6,5,4,3; z 8,9,8,7,9.5,6.75,9,8,8; audio cube (8,1,8)
    = camera target; text (5,5,10) fontSize 5 blue; spawn (0,0,0).
  SPECTROGRAM (puzzlepiece.mp3, L-R): f0=64.465 Hz; odd harmonics 1..123
    present; three broadband bursts centred 0.099s, 0.383s, 3.422s,
    each ~0.047s wide (onsets 0.075, 0.360, 3.390).
  COVER (page-001.png): yin-yang disc bbox 850x839, centre (744.5,1060),
    radius ~420; brightest upper spot (589,642); blueish/dark 0.027.

Each candidate is tested in the four shapes (pure cleaned text, hex text,
raw bytes, + "humph" prefix) against the six remaining hash pages; as a
blob password (SHA-256 hex, MD5 hex, raw) against all four blobs with the
corrected reader (address match, not printability); and SHA-256(candidate)
against the neighbours oracle.
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

# ---- harmonic presence bitstring (L-R, n=1..123, f0=64.465) ----
present_h = [1,3,5,7,9,11,13,15,16,17,19,21,22,23,25,27,29,30,31,32,33,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,51,53,54,55,56,57,58,59,60,61,63,64,65,67,68,69,70,71,72,73,74,75,77,78,79,81,82,83,84,85,87,88,89,91,92,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123]
present_set = set(present_h)
bits = ''.join('1' if i in present_set else '0' for i in range(1, 124))
print('harmonic bitstring (n=1..123):', bits)
print('bitstring len:', len(bits), 'ones:', bits.count('1'), 'zeros:', bits.count('0'))
# the bitstring as bytes (123 bits -> pad to 128 bits / 16 bytes)
bits_padded = bits + '0' * (128 - len(bits))
bits_bytes = bytes(int(bits_padded[i:i+8], 2) for i in range(0, 128, 8))
# odd-harmonic-only bitstring (n odd 1..123): which odd harmonics are present
odd_bits = ''.join('1' if i in present_set else '0' for i in range(1, 124, 2))
print('odd-harmonic bitstring (61 bits):', odd_bits)

cands = {}
def add(s, label):
    if s and s not in cands:
        cands[s] = label

# ---- POSTER ----
add('195x195', 'rabbit bbox 195x195')
add('195,195', 'rabbit bbox 195,195')
add('592,547', 'rabbit centre')
add('592547', 'rabbit centre joined')
add('6975', 'rabbit black px count')
add('6-9', 'rabbit grid cols 6-9')
add('6,7,8', 'rabbit grid rows 6-8')
add('231x231', 'QR size 231x231')
add('231,231', 'QR size 231,231')
add('1,1289', 'QR position')
add('1047,1061', 'red line rows')
add('15', 'red line thickness 15')
add('1048x1556', 'poster size')
add('10481556', 'poster size joined')
# coloured cells row/col as strings
add('0,5;1,2;1,10;2,7;3,4;4,1;6,3;7,0;8,5;8,13;9,2;11,8;12,1;13,2;13,10', 'blue cells row,col')
add('0,13;4,9;5,6;5,10;6,11;7,12;9,6;10,7;12,9', 'yellow cells row,col')
add('15,9,24', 'blue/yellow/total counts')
add('7,15,23,31,39,47,55,63,71,79,87,95,103,111,119,127,135,143,151,159,167,175,183,191', 'coloured spiral indices')
# ---- SCENE ----
add('8,1,8', 'audio cube / camera target')
add('818', 'audio cube joined')
add('9', 'cube count 9')
add('1,7,7.5,7,6,6,5,4,3', 'cube y creation order')
add('1777566543', 'cube y creation order joined')
add('8,9,8,7,9.5,6.75,9,8,8', 'cube z creation order')
add('898795675988', 'cube z creation order joined')
add('1,3,4,5,6,6,7,7,7.5', 'cube y sorted')
add('46.5', 'sum of cube y')
add('73.25', 'sum of cube z')
add('191.75', 'sum of all cube coords')
add('8,5.167,8.139', 'cube centroid')
add('6.5', 'cube bounding height')
add('2.75', 'cube bounding width')
add('0,2,3,4.123,5.154,5.22,6.083,6.083,6.5', 'distances from audio cube')
add('5,5,10', 'text position')
add('5510', 'text position joined')
add('5', 'text fontSize 5')
add('GSMG.IO 5 BTC PUZZLE CHALLENGE', 'scene text')
add('gsmgio5btcpuzzlechallenge', 'scene text cleaned')
add('0,0,0', 'scene spawn')
add('8,1,8', 'scene camera target (dup of audio cube)')
# cube positions concatenated
add('818879878879568675859848838', 'all cube positions joined')
add('(8,1,8)(8,7,9)(8,7.5,8)(8,7,7)(8,6,9.5)(8,6,6.75)(8,5,9)(8,4,8)(8,3,8)', 'all cube positions')
# ---- SPECTROGRAM ----
add('64.465', 'spectrogram f0 64.465 Hz')
add('64465', 'f0 in mHz')
add('0.099,0.383,3.422', 'burst centres')
add('99,383,3422', 'burst centres ms')
add('0.075,0.360,3.390', 'burst onsets')
add('0.122,0.406,3.454', 'burst offsets')
add('0.047', 'burst width')
add('0.099', 'burst 1 centre')
add('0.383', 'burst 2 centre')
add('3.422', 'burst 3 centre')
add('3', 'three bursts')
add(bits, 'harmonic presence bitstring 1..123')
add(bits_bytes, 'harmonic bitstring as bytes')
add(bits_bytes.hex(), 'harmonic bitstring as hex')
add(odd_bits, 'odd-harmonic presence bitstring')
# ---- COVER ----
add('850x839', 'cover disc bbox')
add('744.5,1060', 'cover disc centre')
add('7441060', 'cover disc centre joined')
add('420', 'cover disc radius')
add('589,642', 'cover brightest upper spot')
add('0.027', 'cover blueish/dark ratio')
add('0.581', 'cover goldish/blueish ratio')
# ---- cross-object combinations ----
add('19523164465', 'rabbit+QR+f0 joined')
add('9,64.465,195,231', 'cubes, f0, rabbit, QR')
add('8,1,8,5,5,10', 'audio cube + text position')
print(f'candidates: {len(cands)}')

# ---------- Oracle 1: hash pages ----------
hits1 = []
tested_text, tested_bytes = set(), set()
for s, label in cands.items():
    if isinstance(s, bytes):
        if s in tested_bytes:
            continue
        tested_bytes.add(s)
        h = hashlib.sha256(s).hexdigest()
        if h in REMAINING:
            hits1.append((label, h, 'raw-bytes'))
        continue
    c = clean(s)
    if c and c not in tested_text:
        tested_text.add(c)
        for h, shape in ((hashlib.sha256(c.encode()).hexdigest(), 'text'),
                         (hashlib.sha256(c.encode().hex().encode()).hexdigest(), 'hex-text')):
            if h in REMAINING:
                hits1.append((label, h, shape))
        h3 = hashlib.sha256(('humph' + c).encode()).hexdigest()
        if h3 in REMAINING:
            hits1.append((label, h3, 'humph+text'))
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbors ----------
TARGETS = {'1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm',
           '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs', '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1',
           '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT'}
hits2 = []
for s, label in cands.items():
    raw = s if isinstance(s, bytes) else s.encode()
    addr = addr_from_scalar(int.from_bytes(hashlib.sha256(raw).digest(), 'big'))
    if addr in TARGETS:
        hits2.append((label, addr))
    # direct 32-byte key check for byte candidates
    if isinstance(s, bytes) and len(s) >= 32:
        for part, priv in (('first32', s[:32]), ('last32', s[-32:])):
            addr2 = addr_from_scalar(int.from_bytes(priv, 'big'))
            if addr2 in TARGETS:
                hits2.append((label, addr2, 'direct-key ' + part))
print(f'Oracle 2 (neighbors): {len(cands)} -> hits: {hits2 if hits2 else "none"}')

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
for s, label in cands.items():
    raw = s if isinstance(s, bytes) else s.encode()
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
                            hits3.append((label, pw[:16], digest, blabel, rname, addr, priv.hex()))
print(f'Oracle 3 (blobs): {attempts} decryptions, {valid_padding} valid paddings, {len(hits3)} address matches')
print(f'  real hits: {hits3 if hits3 else "none"}')
print('DONE')
