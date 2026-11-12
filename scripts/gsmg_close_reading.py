#!/usr/bin/env python3
"""GSMG close reading: creator's own words as candidates, three oracles.

From the creator's verified words (gsmg-creator-profile.md, 482 messages):
- New Year message: "Happy new year! Make the best of everything. Oh, and
  here's a 'tiny hint' <3." -> makethebestofeverything
- July 16 (his last messages): "Give yourself yourself and yourself will be
  given yourself." / "Latetly, I'm working with many NOTES." / "geestveruimend"
- Rickroll origin: "The rickroll effect inspired me to make an actual puzzle"
  -> nevergonnagiveyouup
- The only date he gives away: Neo's passport expiry (11-09-2001, film prop)
- "No hints, only free will." / "strugle" / Mr. Robot last scene / salphation
  / "zeroed out" / hidden laptop / close friends / "Some already found it"
  / "The 5 btc was never the actual prize" / "one microstep further"

Each candidate is tested against THREE oracles:
  1. the six remaining hash pages (four shapes)
  2. the four blobs as AES password (SHA-256 + MD5 key derivation, both
     blob2 readings, corrected reader)
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
    # New Year "tiny hint"
    'makethebestofeverything', 'Make the best of everything',
    'happynewyear', 'Happy new year! Make the best of everything.',
    # July 16
    'giveyourselfyourselfandyourselfwillbegivenyourself',
    'Give yourself yourself and yourself will be given yourself.',
    'latetly', 'Latetly, I\'m working with many NOTES.', 'latetlyimworkingwithmanynotes',
    'geestveruimend', 'mind-expanding', 'mindexpanding',
    'hidden in a room with a hidden door', 'hiddenlaptop',
    'I have a hidden laptop which I haven\'t touched in years',
    # rickroll origin
    'nevergonnagiveyouup', 'Never Gonna Give You Up', 'rickroll', 'therickrolleffect',
    # Neo passport date (the only date he gives away)
    '11092001', '11-09-2001', '1192001', 'september112001', '11september2001',
    'expirydateofneospassport', 'theexpirydateofneospassport',
    # free will / determinism
    'freewill', 'nohintsonlyfreewill', 'No hints, only free will.', 'strugle',
    # Mr. Robot
    'mrrobot', 'thelastsceneofmrrobot', 'the last scene of mr. robot',
    # salphation / prime / zeroed out
    'salphation', 'breakingsalphation', 'thefeelingofthephasesname',
    'zeroedout', 'somecharactersneedtobe zeroedout', 'primenumbers',
    'primepart', 'youareattheprimepartalready',
    # close friends (the only self-declared hint)
    'myclosefriendshavethebestchance', 'closefriends', 'myclosefriends',
    'somealreadyfoundit', 'understoodnottoriskit', 'somealreadyfounditandunderstoodnottoriskit',
    # the secret / prize
    'thesecretinmyhead', 'sharewiththeplanet', 'the5btcwasnevertheactualprize',
    'onlyatinyfraction', 'itismeanttobesolved', 'itcanbesolved',
    'onemicrostepfurther', '1microstep', 'thehardestpartisdone',
    'areyoureallylookingforjustthebtc', 'themostobviousreason',
    # first piece / doors
    'rosesarewhitebutoftenred', 'yellowhasanumberandsodoesblue',
    'gobacktothefirstpuzzlepiece', 'therabbitsnestmaycontainawholelotmore',
    'thereisanotherdoor', 'anotherdoor', 'hushhush',
    # misc creator phrases
    'thequickestbraindiditwithin2hours', 'withintwohours', '2hoursmax',
    'whenyingyangisreached2hoursmax', 'itsthenextphase',
    'ionlyneedtolookattheaddress', 'thepriceistakeninnotime',
    'inthatmatrixcypherkindawayilikeit', 'matrixcypher',
    'quiteegocentric', 'lifeenjoyingproject',
    'mostofyouknowthepuzzlewaybetterthanme', 'ihaveahiddenlaptop',
    'someofyoucanfindme', 'quiteafewinthischatalreadymetme',
    'beforeyoubegin', 'thefinalhint', 'tinyhint', 'atinyhint',
]
print(f'candidates: {len(cands)}')

# ---------- Oracle 1: hash pages (four shapes) ----------
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
    check_text(c, 'close-reading')
    check_text('humph' + c, 'close-reading+humph')
    check_bytes(s.encode(), 'close-reading')
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbors EC ----------
hits2 = []
for s in cands:
    priv = hashlib.sha256(s.encode()).digest()
    addr = addr_from_scalar(int.from_bytes(priv, 'big'))
    if addr in TARGETS:
        hits2.append((s, addr, TARGETS[addr], priv.hex()))
print(f'Oracle 2 (neighbors): {len(cands)} candidates -> hits: {hits2 if hits2 else "none"}')

# ---------- Oracle 3: blob passwords ----------
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
# corrected blob2 readings (issue #122): A = 48-byte line-1-only, B = 96-byte line1+line2
line1 = 'U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z'
line2 = 'QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
blobs['blob2A'] = base64.b64decode(line1)
blobs['blob2B'] = base64.b64decode(line1 + line2)

hits3 = []
attempts = 0
valid_padding = 0
def privkey_readings(pt):
    """The oracle's 4 standard readings of a plaintext as a 32-byte key."""
    out = []
    out.append(('sha256(pt)', hashlib.sha256(pt).digest()))
    if len(pt) >= 32:
        out.append(('first32', pt[:32]))
        out.append(('last32', pt[-32:]))
    if len(pt) >= 64:
        out.append(('sha256(first64)', hashlib.sha256(pt[:64]).digest()))
    return out
PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW2 = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
for s in cands:
    # password forms: SHA-256 hex and MD5 hex of the candidate (creator's convention)
    for pw in [hashlib.sha256(s.encode()).hexdigest(), hashlib.md5(s.encode()).hexdigest(), s]:
        for digest in ('sha256', 'md5'):
            for label, raw in blobs.items():
                attempts += 1
                pt = try_decrypt(raw, pw, digest)
                if pt is not None:
                    valid_padding += 1
                    # a real hit requires the plaintext to yield the prize key
                    for rname, priv in privkey_readings(pt):
                        addr = addr_from_scalar(int.from_bytes(priv, 'big'))
                        if addr in (PRIZE, ESCROW2):
                            hits3.append((s, pw[:16], digest, label, rname, addr, priv.hex()))
print(f'Oracle 3 (blobs): {attempts} decryptions, {valid_padding} valid paddings (expected ~1/256 by chance), {len(hits3)} address matches')
print(f'  real hits: {hits3 if hits3 else "none — the valid paddings are random-padding false positives, their plaintexts are garbage"}')
print('DONE')
