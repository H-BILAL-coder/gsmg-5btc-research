#!/usr/bin/env python3
"""GSMG: 1991 Time-Life Cosmic Duality cover audit -> candidates, three oracles.

Cover (verified by direct inspection of gsmg-cosmic-duality.pdf p.1):
- Series "MYSTERIES OF THE UNKNOWN", title "Cosmic Duality"
- Artwork: a YIN-YANG (taijitu) formed by two interlocking star-field shapes
  on black — upper half dark with a bright BLUE-WHITE star, lower half blue
  with a bright GOLDEN-YELLOW star — inside a thin silver square border.
- That is the "scary specific": the cover IS a yin-yang (the next phase's
  name) in the puzzle's two colours (blue + yellow/gold), with two stars
  (the two halves). The puzzle's poster grid is 15 blue + 9 yellow squares;
  the "Half and Better Half" are two halves; the blob is "Dualite".

Bibliographic (from the PDF text layer, copyright p.):
- Cosmic Duality, by the Editors of Time-Life Books, Time-Life Books,
  Alexandria, Virginia. Series: Mysteries of the Unknown.
- (c) 1991 Time-Life Books. Second printing 1993. Printed in USA.
- ISBN 0-8094-6516-7 (trade), ISBN 0-8094-6517-5 (library).
- LC: BFI999C6975 1991, 147'.4-dc20, 90-28806.
- Chapters: The Unity of Opposites; Dualities As Old As Time; The Dark Side
  of Fairy Tales; The Battle of the Sexes; Driving the Devil Out; Grasp of
  Ageless Evil; Paths of Righteousness; The Triumph of Good; Hark! Heaven's
  Winged Host.

Each candidate is tested against THREE oracles:
  1. the six remaining hash pages (four shapes)
  2. the four blobs as AES password (SHA-256 + MD5, both blob2 readings)
  3. the neighbors EC oracle (SHA-256 -> address vs P and 4 neighbours)
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
TARGETS = {
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'P (k)',
    '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm': '2P (k = s/2)',
    '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs': 'P/2 (k = 2s)',
    '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1': 'P+G (k = s-1)',
    '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT': 'P-G (k = s+1)',
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

cands = [
    # cover artwork
    'yinyang', 'yinandyang', 'taijitu', 'theyinyang', 'yinyangstar',
    'bluestar', 'goldstar', 'yellowstar', 'blueandgold', 'blueandgoldstar',
    'twostars', 'twocontrastingstars', 'thetwostars',
    'mysteriesoftheunknown', 'Mysteries of the Unknown',
    'cosmicduality', 'Cosmic Duality', 'cosmicduality1991',
    # bibliographic
    '0809465167', '0-8094-6516-7', '0809465175', '0-8094-6517-5',
    'BFI999C6975', '9028806', '1991', '1993', 'secondprinting1993',
    'timelifebooks', 'Time-Life Books', 'alexandriavirginia',
    # chapters / essays
    'theunityofopposites', 'The Unity of Opposites',
    'dualitiesasoldastime', 'Dualities As Old As Time',
    'thedarksideoffairytales', 'The Dark Side of Fairy Tales',
    'thebattleofthesexes', 'The Battle of the Sexes',
    'drivingthedevilout', 'Driving the Devil Out',
    'graspofagelessevil', 'Grasp of Ageless Evil',
    'pathsofrighteousness', 'Paths of Righteousness',
    'thetriumphofgood', 'The Triumph of Good',
    'harkheavenswingedhost', "Hark! Heaven's Winged Host",
    # cross-reference: cover vs poster
    'blueandyellow', 'yellowandblue', 'yellowblue', 'blueyellow',
    'fifteenblue', 'nineyellow', '15blue9yellow', 'blue15yellow9',
    'halfandbetterhalf', 'twohalves', 'thetwohalves',
    'dualite', 'Dualite', 'duality', 'cosmicdualityblob',
    # combinations
    'cosmicdualityyinyang', 'yinyangcosmicduality',
    'mysteriesoftheunknowncosmicduality',
    '0809465167cosmicduality', 'cosmicduality0809465167',
]
print(f'candidates: {len(cands)}')

# ---------- Oracle 1: hash pages ----------
hits1 = []
tested_text = set()
tested_bytes = set()
def check_text(c, label):
    if c in tested_text or not c:
        return
    tested_text.add(c)
    h1 = hashlib.sha256(c.encode()).hexdigest()
    if h1 in REMAINING:
        hits1.append((label, c, h1, 'shape1-pure-text'))
    h2 = hashlib.sha256(c.encode().hex().encode()).hexdigest()
    if h2 in REMAINING:
        hits1.append((label, c, h2, 'shape2-hex-text'))
def check_bytes(raw, label):
    if raw in tested_bytes:
        return
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits1.append((label, raw[:60].decode(errors='ignore'), h, 'shape3-raw-bytes'))
for s in cands:
    c = clean(s)
    check_text(c, 'cover')
    check_text('humph' + c, 'cover+humph')
    check_bytes(s.encode(), 'cover')
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbors ----------
hits2 = []
for s in cands:
    priv = hashlib.sha256(s.encode()).digest()
    addr = addr_from_scalar(int.from_bytes(priv, 'big'))
    if addr in TARGETS:
        hits2.append((s, addr, TARGETS[addr], priv.hex()))
print(f'Oracle 2 (neighbors): {len(cands)} candidates -> hits: {hits2 if hits2 else "none"}')

# ---------- Oracle 3: blobs ----------
def evp_bytes_to_key(password, salt, key_len=32, iv_len=16, digest='md5', count=1):
    out = b''
    prev = b''
    while len(out) < key_len + iv_len:
        h = hashlib.new(digest)
        h.update(prev + password + salt)
        prev = h.digest()
        for _ in range(1, count):
            h = hashlib.new(digest)
            h.update(prev)
            prev = h.digest()
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

kit = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
blobs = {}
for fname, label in [('blob1_phase32_final.txt', 'blob1'),
                     ('blob2_salphaseion.txt', 'blob2'),
                     ('blob3_cosmic_duality.txt', 'blob3'),
                     ('blob4_urlblob.txt', 'blob4')]:
    b64 = open(f'{kit}/{fname}').read().strip()
    blobs[label] = base64.b64decode(b64)
line1 = 'U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z'
line2 = 'QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
blobs['blob2A'] = base64.b64decode(line1)
blobs['blob2B'] = base64.b64decode(line1 + line2)

def privkey_readings(pt):
    out = [('sha256(pt)', hashlib.sha256(pt).digest())]
    if len(pt) >= 32:
        out.append(('first32', pt[:32]))
        out.append(('last32', pt[-32:]))
    if len(pt) >= 64:
        out.append(('sha256(first64)', hashlib.sha256(pt[:64]).digest()))
    return out
PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW2 = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
hits3 = []
attempts = 0
valid_padding = 0
for s in cands:
    for pw in [hashlib.sha256(s.encode()).hexdigest(), hashlib.md5(s.encode()).hexdigest(), s]:
        for digest in ('sha256', 'md5'):
            for label, raw in blobs.items():
                attempts += 1
                pt = try_decrypt(raw, pw, digest)
                if pt is not None:
                    valid_padding += 1
                    for rname, priv in privkey_readings(pt):
                        addr = addr_from_scalar(int.from_bytes(priv, 'big'))
                        if addr in (PRIZE, ESCROW2):
                            hits3.append((s, pw[:16], digest, label, rname, addr, priv.hex()))
print(f'Oracle 3 (blobs): {attempts} decryptions, {valid_padding} valid paddings, {len(hits3)} address matches')
print(f'  real hits: {hits3 if hits3 else "none"}')
print('DONE')
