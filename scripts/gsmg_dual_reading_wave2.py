#!/usr/bin/env python3
"""LUX'S METHOD — "The Dual Reading" (wave 2): the EVEN stream + the 227 digest.

Wave 1 found a real gap while verifying the Bifid data. The puzzle's Bifid
step outputs 570 letters that split into TWO interleaved streams:
  - ODD stream (285 letters, contains O and I): removing I/O gives the
    256-symbol object over a 23-letter alphabet. TESTED as a password.
  - EVEN stream (285 letters, ONLY the letters B, C, D, E): NEVER tested
    as a password on its own. This is the other half of the yin-yang —
    the dual the method is built on. A 4-letter alphabet is a 2-bit
    encoding (24 possible letter-to-bit mappings).
Wave 2 tests:
  A. The even stream as a password (SHA-256 hex, MD5 hex, raw), reversed,
     and concatenated/XORed with the odd stream.
  B. The even stream decoded as 2-bit bytes under all 24 letter mappings
     (MSB-first), as passwords and as direct keys.
  C. The 227-char Phase 3 concatenation's SHA-256 digest
     (1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5,
     verified in apple-repo SOLUTION.md) as a blob password — the digest
     is the password per the creator's convention, and it was only ever
     tested as a private-key scalar / preimage, never as an AES password.
     Plus its raw bytes and recursive forms.
A valid PKCS7 padding alone is NOT a hit. A real hit requires the plaintext
to yield the prize key (4 readings) whose address matches a prize escrow.
"""
import base64, hashlib, itertools, re

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

# The two Bifid streams (from gsmg-esrever-test.md; lengths verified).
ODD285 = 'TSEDOMKAHSHKDSKVXPOHRIIQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSOWKYUWASWNMDAORPGQOGSNSLTSAPUSPRANKSDNEKKTLRNNCGLNUSGSINUFDAKNSSSRSBLIRVODCGSOVVDMPSGLIGAWYAPGNYBGLRBRGBMRNGTDNFLPNRBBNRRMLSALNQOHQGXGFUEIAIAOTNIGELELMKDBAMORMCMSGBOMTLMDMMPSNSYOOINSOIBBNNCUIECGOMEUNELLAPPMXXRGBMNRDCWAHTIQPOFHGXPIL'
EVEN285 = 'BCEDEECEDBCDBCDDBCCCCDCBEBDCDBCDCDCCECDCEBCDCCCEDECEDEDDCBCBBEBBEEEDBCBBCEBEEBBEDDDECCECCCCCBDCCCBEECEECCBBEEEDEDBCDBDECBEBBEDCBCEBEBBCECCCEDEDDDCCEEBECCCDBDDDECCDCBCCCDBBECEEEEDDDECBCDDBECCEEDCEDCDEEDEDEBCEBECCDECCCCDCCDDBCBBDBDBDEECEBEBCBCCEDCBCCDCEDBDEBBCCCDDDDCCDDDEDEDBDCCDEDDDDCE'
BIF570 = 'BTCSEEDDEOEMCKEADHBSCHDKBDCSDKDVBXCPCOCHCRDICIBQEEBDDBCNDSBDCPDGCPDNCNCSESCGDDCLENBMCUDUCQCACDELDZELCMEFDFESDODWCKBYCUBWBAESBWBNEMEDEADOBRCPBGBQCOEGBSENESBLBTESDADPDUESCPCREACNCKCSCDCNBEDKCKCTCLBRENENCCEGELCNCUBSBGESEIENDUEFDDBACKDNBSDSESCRBSEBBLBIERDVCOBDCCEGBSEOBVBVCDEMCPCSCGELDIEGDADWDYCACPEGENBYEBCGCLCRDBBRDGDBDMERCNCGDTCDBNCFCLCPDNBRBBEBCNEREREMELDSDADLENCQBOCHDQDGBXEGCFCUEEEIDACIEADOCTDNEIEGDEELDEELBMCKEDBBEACMCODREMCCCMCSCGDBCOCMDTDLBMCDBMBMDPBSDNBSDYEOEOCIENBSEOBICBBBCNCNECDUCIBECCCGDOCMEEDUBNDEELBLBACPCPCMDXDXDRDGCBCMDNDRDDECDWEADHBTDICQCPDOEFDHDGDXDPCIEL'
assert len(ODD285) == 285 and len(EVEN285) == 285 and len(BIF570) == 570
# verify the split: interleaving ODD and EVEN (odd first) must rebuild BIF570
def weave(*strs):
    out, i = [], 0
    while True:
        progressed = False
        for s in strs:
            if i < len(s):
                out.append(s[i]); progressed = True
        if not progressed:
            break
        i += 1
    return ''.join(out)
assert weave(EVEN285, ODD285) == BIF570, 'stream split FAIL'
print('stream split verified: weave(even, odd) == 570-letter Bifid output')
print('even-stream alphabet:', sorted(set(EVEN285)), '(4 letters — a 2-bit encoding)')

DIGEST227 = '1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5'

cands = {}
def add(s, label):
    if s and s not in cands:
        cands[s] = label

# ---- A. The even stream ----
add(EVEN285, 'even stream')
add(EVEN285[::-1], 'even stream reversed')
add(EVEN285 + ODD285, 'even+odd')
add(ODD285 + EVEN285, 'odd+even')
xor_eo = bytes(a ^ b for a, b in zip(EVEN285.encode(), ODD285.encode()))
add(xor_eo, 'even XOR odd (raw)')
add(xor_eo.hex(), 'even XOR odd (hex)')
add(hashlib.sha256(EVEN285.encode()).hexdigest(), 'sha256(even stream)')
add(hashlib.sha256(EVEN285.encode()).digest(), 'sha256(even stream) raw')

# ---- B. The even stream as 2-bit bytes (24 mappings) ----
for perm in itertools.permutations('BCDE'):
    bits = ''.join(f'{perm.index(ch):02b}' for ch in EVEN285)
    # take full bytes only (568 bits = 71 bytes)
    byts = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits) - 7, 8))
    mname = ''.join(perm)
    add(byts, 'even-as-2bit ' + mname)
    add(byts.hex(), 'even-as-2bit ' + mname + ' hex')

# ---- C. The 227-char digest as a password ----
add(DIGEST227, 'sha256(227-char Phase 3 concat)')
add(bytes.fromhex(DIGEST227), 'sha256(227-char) raw bytes')
add(hashlib.sha256(DIGEST227.encode()).hexdigest(), 'sha256hex(sha256(227))')
add(hashlib.sha256(DIGEST227.encode()).digest(), 'sha256raw(sha256(227))')
add(hashlib.md5(DIGEST227.encode()).hexdigest(), 'md5hex(sha256(227))')
add(hashlib.sha256(bytes.fromhex(DIGEST227)).hexdigest(), 'sha256hex(raw sha256(227))')
add(hashlib.sha256(bytes.fromhex(DIGEST227)).digest(), 'sha256raw(raw sha256(227))')

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
    c = re.sub(r'[^a-z0-9]', '', s.lower())
    if c and c not in tested_text:
        tested_text.add(c)
        for h, shape in ((hashlib.sha256(c.encode()).hexdigest(), 'text'),
                         (hashlib.sha256(c.encode().hex().encode()).hexdigest(), 'hex-text')):
            if h in REMAINING:
                hits1.append((label, h, shape))
print(f'Oracle 1 (hash pages): {len(tested_text)} text, {len(tested_bytes)} bytes -> hits: {hits1 if hits1 else "none"}')

# ---------- Oracle 2: neighbors (+ direct-key check for the 2-bit decodes) ----------
TARGETS = {'1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm',
           '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs', '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1',
           '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT'}
hits2 = []
for s, label in cands.items():
    raw = s if isinstance(s, bytes) else s.encode()
    # as a SHA-256 scalar
    addr = addr_from_scalar(int.from_bytes(hashlib.sha256(raw).digest(), 'big'))
    if addr in TARGETS:
        hits2.append((label, addr, 'sha256-scalar'))
    # as a direct 32-byte key (first32 / last32) when the candidate is bytes >= 32
    if isinstance(s, bytes) and len(s) >= 32:
        for part, priv in (('first32', s[:32]), ('last32', s[-32:])):
            addr2 = addr_from_scalar(int.from_bytes(priv, 'big'))
            if addr2 in TARGETS:
                hits2.append((label, addr2, f'direct-key {part}'))
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
