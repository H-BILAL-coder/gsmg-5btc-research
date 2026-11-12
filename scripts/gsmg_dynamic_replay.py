#!/usr/bin/env python3
"""GSMG item 1 — dynamic candidate replay (reconstructed).

FILTER AUDIT (verified in the record):
  floflo777 analysis/tested.md (2026-07-28 review) + analysis/leads.md lead #3:
  "an appearance-based acceptance filter used in about 46% of the folder's
  scripts (98 of 213) had been silently rejecting the correct answer shape
  for years, because it required decrypted plaintext to look like printable
  ASCII when the expected plaintext is raw key material."
  Row 8 already replayed 116,043 LITERAL strings harvested from 1,017
  archived scripts (0 match). The DYNAMIC patterns (concatenations,
  permutations, chained transforms built at run time) were never logged and
  never replayed. The 213 / 1,017 archived scripts are NOT on disk in this
  workspace (on-disk floflo-repo has only 3 tools/*.py files), so the replay
  below RECONSTRUCTS the dynamic pattern classes from the validated Phase 3
  inputs instead of re-running each script's own generation logic.

Reconstructed dynamic pipeline (new — avoids tested.md rows 15-19 and the
parent's 2,908,328-password re-run: kit Stream A stored files, Stream B
big_combine YB/ML/YY/LW, Stream C wave2 CORE x NUMS):
  Units: P91 (91-letter phrase), D149 (149-digit string), BK (thematrixhasyou),
         R1 (jacquefresco), R2 (giveitjustonesecond), R3 (heisenbergsuncertaintyprinciple)
  Class A: ordered k-tuples k=3..6 of the 6 units, seps {"","-","_"," ","/","."}
           (k=2 pairs EXCLUDED — floflo row 16 covered ordered pairs of stage answers)
  Class B: transformed-unit pairs (>=1 non-identity transform),
           transforms {reverse, ROT13, Atbash, Beaufort(BK), Vigenere(BK), hex, b64}
  Class C: chained double-transforms on single units
  Class D: the 256-symbol object / 285-letter stream / 570-letter Bifid output
           as BLOB PASSWORDS (rows 1-5 tested them as direct KEYS, not passwords)
  Class E: D149 special forms (reversed, "-" every 3 digits, pairs->bytes, hex)

Harness (corrected reader, no printability judgment):
  password forms {sha256 hex, md5 hex, raw} x digests {sha256, md5} x blobs
  {blob1, blob2, blob2A, blob2B, blob3, blob4}; last-block padding pre-check;
  valid padding -> full decrypt -> floflo readings() + 2k/k/2 neighbours +
  split-key combinations (>=64-byte plaintexts) -> both address forms, both escrows.
  A hit requires an address match, never padding alone.
"""
import base64, hashlib, itertools, json, re, time

# ---------------- certified harness self-checks ----------------
import base58, coincurve
from Crypto.Cipher import AES

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW2 = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'

def addr_from_scalar(s, compressed=False):
    s = s % N
    if s == 0:
        return None
    pk = coincurve.PrivateKey(s.to_bytes(32, 'big'))
    pub = pk.public_key.format(compressed=compressed)
    h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    return base58.b58encode_check(b'\x00' + h).decode()

# privkey-1 acceptance vectors (certified_derivation_testing skill)
assert addr_from_scalar(1, compressed=True) == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH', 'privkey-1 comp FAIL'
assert addr_from_scalar(1, compressed=False) == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', 'privkey-1 uncomp FAIL'
print('self-check 1 PASS: privkey-1 comp + uncomp reproduce')

# synthetic-witness key (fixed): its address is a match target ONLY for the
# WITNESS blob, so the harness can prove it catches a real hit.
WITNESS_PRIV = bytes.fromhex('11' * 32)
WITNESS_ADDR = addr_from_scalar(int.from_bytes(WITNESS_PRIV, 'big'), compressed=False)
print(f'witness address: {WITNESS_ADDR}')

# known preimages reproduce (hash-page sanity)
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
print('self-check 2 PASS: known hash preimage reproduces')

def evp_bytes_to_key(password, salt, key_len=32, iv_len=16, digest='md5', count=1):
    out, prev = b'', b''
    while len(out) < key_len + iv_len:
        h = hashlib.new(digest); h.update(prev + password + salt); prev = h.digest()
        for _ in range(1, count):
            h = hashlib.new(digest); h.update(prev); prev = h.digest()
        out += prev
    return out[:key_len], out[key_len:key_len + iv_len]

def last_block_padding_ok(key, iv, ct):
    """CBC: decrypt only the last block, check PKCS7. Exact pre-check."""
    if len(ct) < 32:
        return False
    last = ct[-16:]
    prev = ct[-32:-16]
    dec = AES.new(key, AES.MODE_ECB).decrypt(last)
    pt_last = bytes(a ^ b for a, b in zip(dec, prev))
    pad = pt_last[-1]
    return 1 <= pad <= 16 and pt_last[-pad:] == bytes([pad]) * pad

def full_decrypt(key, iv, ct):
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    pad = pt[-1]
    if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
        return pt[:-pad]
    return None

def readings(pt):
    out = [('sha256(pt)', hashlib.sha256(pt).digest())]
    if len(pt) >= 32:
        out += [('first32', pt[:32]), ('last32', pt[-32:])]
    if len(pt) >= 64:
        out.append(('sha256(first64)', hashlib.sha256(pt[:64]).digest()))
    stripped = b''.join(pt.split())
    if stripped[:2] in (b'0x', b'0X'):
        stripped = stripped[2:]
    if len(stripped) in (64, 128) and all(c in b'0123456789abcdefABCDEF' for c in stripped):
        try:
            dec = bytes.fromhex(stripped.decode('ascii'))
            if len(dec) == 32:
                out.append(('hex->32', dec))
            elif len(dec) == 64:
                out += [('hex->first32', dec[:32]), ('hex->last32', dec[-32:])]
        except ValueError:
            pass
    token = b''.join(pt.split())
    if 50 <= len(token) <= 53:
        try:
            raw = base58.b58decode_check(token.decode('ascii'))
            if raw[:1] == b'\x80' and len(raw) in (33, 34):
                out.append(('wif', raw[1:33]))
        except Exception:
            pass
    return out

def check_key_bytes(kb, label, hits):
    """All address checks for one 32-byte key: both forms, both escrows,
    plus 2k and k/2 neighbours (creator's 'half and double' motif)."""
    k = int.from_bytes(kb, 'big') % N
    if k == 0:
        return
    for kk, klab in ((k, ''), ((2 * k) % N, '2k'), ((k * ((N + 1) // 2)) % N, 'k/2')):
        for comp in (False, True):
            addr = addr_from_scalar(kk, compressed=comp)
            if addr in (PRIZE, ESCROW2) or (addr == WITNESS_ADDR and 'WITNESS' in label):
                hits.append((label, klab, 'comp' if comp else 'uncomp', addr, kk.to_bytes(32, 'big').hex()))

def check_plaintext(pt, label, hits):
    for rname, kb in readings(pt):
        check_key_bytes(kb, f'{label}:{rname}', hits)
    if len(pt) >= 64:
        a, b = pt[:32], pt[-32:]
        ai, bi = int.from_bytes(a, 'big'), int.from_bytes(b, 'big')
        for name, val in (('a+b', (ai + bi) % N), ('a-b', (ai - bi) % N),
                          ('b-a', (bi - ai) % N), ('a^b', ai ^ bi),
                          ('2a', (2 * ai) % N), ('a/2', (ai * ((N + 1) // 2)) % N),
                          ('2b', (2 * bi) % N), ('b/2', (bi * ((N + 1) // 2)) % N)):
            check_key_bytes(val.to_bytes(32, 'big'), f'{label}:split-{name}', hits)

# ---------------- blobs ----------------
KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
blobs = {}
for fname, label in [('blob1_phase32_final.txt', 'blob1'),
                     ('blob2_salphaseion.txt', 'blob2'),
                     ('blob3_cosmic_duality.txt', 'blob3'),
                     ('blob4_urlblob.txt', 'blob4')]:
    blobs[label] = base64.b64decode(open(f'{KIT}/{fname}').read().strip())
line1 = 'U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z'
line2 = 'QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ'
blobs['blob2A'] = base64.b64decode(line1)
blobs['blob2B'] = base64.b64decode(line1 + line2)
for lab, raw in blobs.items():
    assert raw[:8] == b'Salted__', lab
print(f'self-check 3 PASS: {len(blobs)} blobs load, all Salted__')

# phase-2 known vector through MY decrypt (real puzzle material, not self-made)
PHASE2_B64 = ("U2FsdGVkX18GKGYS1D7X7VjxWz6uUyPFszr8dVvtOIrJqioWHgT69JJnzJGDVOvF"
 "QYWh5BEZxFPXmMq1cbyy3dVVDgLhF050xlDy2J5grtKw9jUOO4oFNRgoD+1dlukX"
 "pd8ccg++kkXgE9mGBP6lQbukDiSjY4mnR2Mv6ydIncrRqacQNVEmEgM4fGTi1ANz"
 "nHsGn7mP+P3UyrJCRbuFmpZJc4CNdPj6YuxwR4HkHkqcfxh0L5CaEu4VbY70+fmk"
 "qgZQyMJqiUlaV9KC4UPuRVj0r7MYbVRazkhsjeIcogmdJGEeBwD47lEB7X9PNKWm"
 "ojTvRZg6R+sZzRZE26VLaF+s9cpTo4Y8PZUxKvQ86HXC8QIavUgDfw7HxIxkTatv"
 "CW2yq3ZOXl5naR6oSNxdX9alyhTzB+/2623oGdlWev5Oo8xHJqUi7QjVP+mNC8BA"
 "+Cg0DJwcOFGO5K7g8Rm06+sLogwntdIgTo70X3FegAtipHboeUNKefiAguvkDoIf"
 "8iMPc+83PygvlZPDNQCOKugwDEUimhHwQrMsmalRNoFEQEb+ZIC+na15cPoRAlOD"
 "NJfXIJ96ihAy9wWis39mQW6JFqZmUags4xoP3lJ35bCrXsNOPFZ4WH+f4YC/Ov8C"
 "QW5bjtxno8GG4b/wBWevhcRVMK6KmRJj8NBCssnrlz0sQ70rMNkiN2wiSPcwX3Ad"
 "JgLs8vQAUM59x9fkKFFzD4+Sc1sJztUTB7CMGGfpZOA8W33VZnEdmGcoaHlDsR8G"
 "vAkZ+jg+QJs9ZNHqWE1+1zgm/6NsWWgWH8OI2PPCfXHxDbfDk8uD/Zibr/yjSKvu"
 "Sb8OecflOT2hw37WL49uADgeWgnp2bzkfGIq7EYS7OImjZZwY5h4sfcPfhvQ9kOV")
raw2 = base64.b64decode(PHASE2_B64)
pw2 = hashlib.sha256(b'causality').hexdigest()
k2, iv2 = evp_bytes_to_key(pw2.encode(), raw2[8:16], digest='sha256')
pt2 = full_decrypt(k2, iv2, raw2[16:])
assert pt2 is not None and b'keymakers' in pt2, 'phase-2 vector FAIL'
print('self-check 4 PASS: phase-2 blob decrypts under sha256("causality"), contains "keymakers"')

# ---------------- candidate generation ----------------
P91 = 'commonsolutionistointroduecentralauthorityormintthatcheckseverytransactionfordoublespending'
D149 = '15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112'
BK = 'thematrixhasyou'
R1, R2, R3 = 'jacquefresco', 'giveitjustonesecond', 'heisenbergsuncertaintyprinciple'
UNITS = [P91, D149, BK, R1, R2, R3]
assert len(P91) == 91 and len(D149) == 149
SEPS = ['', '-', '_', ' ', '/', '.']

def rot13(s):
    return s.translate(str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'))

def atbash(s):
    return s.translate(str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA'))

def beaufort(text, key):
    out, ki = [], 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[ki % len(key)].lower()) - 97
            p = ord(ch.lower()) - 97
            out.append(chr((k - p) % 26 + 97))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere(text, key):
    out, ki = [], 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[ki % len(key)].lower()) - 97
            p = ord(ch.lower()) - 97
            out.append(chr((p + k) % 26 + 97))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

TRANSFORMS = {
    'id': lambda s: s,
    'rev': lambda s: s[::-1],
    'rot13': rot13,
    'atbash': atbash,
    'beaufort': lambda s: beaufort(s, BK),
    'vigenere': lambda s: vigenere(s, BK),
    'hex': lambda s: s.encode().hex(),
    'b64': lambda s: base64.b64encode(s.encode()).decode(),
}

pool = {}  # candidate -> class label
def add(c, cls):
    if c and c not in pool:
        pool[c] = cls

# Class A: ordered k-tuples k=3..6
for k in (3, 4, 5, 6):
    for tup in itertools.permutations(UNITS, k):
        for sep in SEPS:
            add(sep.join(tup), f'A{k}')
print(f'Class A (k=3..6 tuples): {sum(1 for v in pool.values() if v.startswith("A"))}')

# Class B: transformed-unit pairs, >=1 non-identity transform
tunits = []  # (unit_idx, transform_name, value)
for i, u in enumerate(UNITS):
    for tname, tf in TRANSFORMS.items():
        v = tf(u)
        if v != u or tname == 'id':
            tunits.append((i, tname, v))
# dedupe by value, keep first label
seen_val = {}
for i, tname, v in tunits:
    seen_val.setdefault(v, (i, tname))
tunits = [(i, t, v) for v, (i, t) in seen_val.items()]
for (i1, t1, v1), (i2, t2, v2) in itertools.permutations(tunits, 2):
    if t1 == 'id' and t2 == 'id':
        continue  # plain pairs covered by floflo row 16
    for sep in ('', '-'):
        add(sep.join((v1, v2)), 'B')
print(f'Class B (transformed pairs): {sum(1 for v in pool.values() if v == "B")}')

# Class C: chained double-transforms on single units
for u in UNITS:
    for t1, t2 in itertools.permutations([t for t in TRANSFORMS if t != 'id'], 2):
        add(TRANSFORMS[t2](TRANSFORMS[t1](u)), 'C')
print(f'Class C (chained transforms): {sum(1 for v in pool.values() if v == "C")}')

# Class D: 256-symbol object / 285-letter stream / 570-letter Bifid output as passwords
OBJ256 = 'TSEDMKAHSHKDSKVXPHRQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSWKYUWASWNMDARPGQGSNSLTSAPUSPRANKSDNEKKTLRNNCGLNUSGSNUFDAKNSSSRSBLRVDCGSVVDMPSGLGAWYAPGNYBGLRBRGBMRNGTDNFLPNRBBNRRMLSALNQHQGXGFUEAATNGELELMKDBAMRMCMSGBMTLMDMMPSNSYNSBBNNCUECGMEUNELLAPPMXXRGBMNRDCWAHTQPFHGXPL'
STR285 = 'TSEDOMKAHSHKDSKVXPOHRIIQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSOWKYUWASWNMDAORPGQOGSNSLTSAPUSPRANKSDNEKKTLRNNCGLNUSGSINUFDAKNSSSRSBLIRVODCGSOVVDMPSGLIGAWYAPGNYBGLRBRGBMRNGTDNFLPNRBBNRRMLSALNQOHQGXGFUEIAIAOTNIGELELMKDBAMORMCMSGBOMTLMDMMPSNSYOOINSOIBBNNCUIECGOMEUNELLAPPMXXRGBMNRDCWAHTIQPOFHGXPIL'
BIF570 = 'BTCSEEDDEOEMCKEADHBSCHDKBDCSDKDVBXCPCOCHCRDICIBQEEBDDBCNDSBDCPDGCPDNCNCSESCGDDCLENBMCUDUCQCACDELDZELCMEFDFESDODWCKBYCUBWBAESBWBNEMEDEADOBRCPBGBQCOEGBSENESBLBTESDADPDUESCPCREACNCKCSCDCNBEDKCKCTCLBRENENCCEGELCNCUBSBGESEIENDUEFDDBACKDNBSDSESCRBSEBBLBIERDVCOBDCCEGBSEOBVBVCDEMCPCSCGELDIEGDADWDYCACPEGENBYEBCGCLCRDBBRDGDBDMERCNCGDTCDBNCFCLCPDNBRBBEBCNEREREMELDSDADLENCQBOCHDQDGBXEGCFCUEEEIDACIEADOCTDNEIEGDEELDEELBMCKEDBBEACMCODREMCCCMCSCGDBCOCMDTDLBMCDBMBMDPBSDNBSDYEOEOCIENBSEOBICBBBCNCNECDUCIBECCCGDOCMEEDUBNDEELBLBACPCPCMDXDXDRDGCBCMDNDRDDECDWEADHBTDICQCPDOEFDHDGDXDPCIEL'
assert len(OBJ256) == 256 and len(STR285) == 285 and len(BIF570) == 570, 'object lengths FAIL'
for obj in (OBJ256, STR285, BIF570):
    add(obj, 'D')
    for n in (32, 64, 128):
        add(obj[:n], 'D'); add(obj[-n:], 'D')
    add(obj[::-1], 'D')
# 256-symbol object under 20 spatial reading orders (16x16 grid)
def grid_orders(s):
    n = 16
    g = [list(s[i*n:(i+1)*n]) for i in range(n)]
    orders = {}
    orders['row'] = ''.join(''.join(r) for r in g)
    orders['row-rev'] = orders['row'][::-1]
    orders['col'] = ''.join(''.join(g[r][c] for r in range(n)) for c in range(n))
    orders['col-rev'] = orders['col'][::-1]
    orders['boust-row'] = ''.join(''.join(r if i % 2 == 0 else r[::-1]) for i, r in enumerate(g))
    orders['boust-row-rev'] = orders['boust-row'][::-1]
    orders['boust-col'] = ''.join(''.join(g[r][c] if c % 2 == 0 else g[n-1-r][c] for r in range(n)) for c in range(n))
    orders['boust-col-rev'] = orders['boust-col'][::-1]
    orders['transpose'] = ''.join(''.join(g[c][r] for c in range(n)) for r in range(n))
    orders['transpose-rev'] = orders['transpose'][::-1]
    # spiral clockwise from top-left, and counter-clockwise
    def spiral(gg, cw=True):
        out, top, bot, left, right = [], 0, n-1, 0, n-1
        while top <= bot and left <= right:
            if cw:
                for c in range(left, right+1): out.append(gg[top][c])
                top += 1
                for r in range(top, bot+1): out.append(gg[r][right])
                right -= 1
                if top <= bot:
                    for c in range(right, left-1, -1): out.append(gg[bot][c])
                    bot -= 1
                if left <= right:
                    for r in range(bot, top-1, -1): out.append(gg[r][left])
                    left += 1
            else:
                for r in range(top, bot+1): out.append(gg[r][left])
                left += 1
                for c in range(left, right+1): out.append(gg[bot][c])
                bot -= 1
                if left <= right:
                    for r in range(bot, top-1, -1): out.append(gg[r][right])
                    right -= 1
                if top <= bot:
                    for c in range(right, left-1, -1): out.append(gg[top][c])
                    top += 1
        return ''.join(out)
    orders['spiral-cw'] = spiral(g)
    orders['spiral-cw-rev'] = orders['spiral-cw'][::-1]
    orders['spiral-ccw'] = spiral(g, cw=False)
    orders['spiral-ccw-rev'] = orders['spiral-ccw'][::-1]
    # diagonals
    orders['diag'] = ''.join(g[r][c] for d in range(2*n-1) for r in range(n) for c in range(n) if r+c == d)
    orders['diag-rev'] = orders['diag'][::-1]
    orders['diag2'] = ''.join(g[r][c] for d in range(-n+1, n) for r in range(n) for c in range(n) if r-c == d)
    orders['diag2-rev'] = orders['diag2'][::-1]
    orders['anti-transpose'] = ''.join(''.join(g[n-1-c][n-1-r] for c in range(n)) for r in range(n))
    orders['anti-transpose-rev'] = orders['anti-transpose'][::-1]
    return orders
for name, s in grid_orders(OBJ256).items():
    add(s, 'D')
print(f'Class D (256/285/570 objects as passwords): {sum(1 for v in pool.values() if v == "D")}')

# Class E: D149 special forms
add(D149[::-1], 'E')
add('-'.join(D149[i:i+3] for i in range(0, len(D149), 3)), 'E')
add(bytes(int(D149[i:i+2]) for i in range(0, 148, 2)).decode('latin1'), 'E')
add(D149.encode().hex(), 'E')
add(D149.replace('1', 'I').replace('0', 'O'), 'E')
print(f'Class E (D149 forms): {sum(1 for v in pool.values() if v == "E")}')

cands = sorted(pool.keys())
print(f'TOTAL unique candidates: {len(cands)}')
# FEASIBILITY GATE: 50M
assert len(cands) < 50_000_000, 'pool exceeds feasibility gate'
print(f'FEASIBILITY GATE PASS: {len(cands)} candidates << 50,000,000')

# ---------------- synthetic witness (harness must catch a planted hit) ----------------
# Build a synthetic blob with a KNOWN password from class A, known 32-byte key plaintext.
witness_cand = SEPS[0].join((P91, BK, R1))  # class A triple, '' separator
assert witness_cand in pool and pool[witness_cand].startswith('A')
witness_priv = WITNESS_PRIV
witness_pt = witness_priv + bytes([16]) * 16  # 48 bytes -> PKCS7 pad to 64? no: 32+16=48, pad 16 -> 64
# encrypt with the SAME convention: password = sha256 hex, EVP sha256, AES-256-CBC
wpw = hashlib.sha256(witness_cand.encode()).hexdigest()
wsalt = bytes.fromhex('0102030405060708')
wk, wiv = evp_bytes_to_key(wpw.encode(), wsalt, digest='sha256')
wct = AES.new(wk, AES.MODE_CBC, wiv).encrypt(witness_pt)
# run the witness through the exact test path below (as a blob entry)
blobs['WITNESS'] = b'Salted__' + wsalt + wct
print(f'synthetic witness planted: candidate={witness_cand[:60]}... priv=0x11*32')
print(f'  witness address (uncomp) = {addr_from_scalar(int.from_bytes(witness_priv, "big"), compressed=False)}')

# ---------------- run ----------------
t0 = time.time()
hits = []
valid_padding = 0
attempts = 0
for idx, cand in enumerate(cands):
    for pw in (hashlib.sha256(cand.encode()).hexdigest(),
               hashlib.md5(cand.encode()).hexdigest(),
               cand):
        for digest in ('sha256', 'md5'):
            for label, raw in blobs.items():
                salt, ct = raw[8:16], raw[16:]
                key, iv = evp_bytes_to_key(pw.encode(), salt, digest=digest)
                attempts += 1
                if not last_block_padding_ok(key, iv, ct):
                    continue
                pt = full_decrypt(key, iv, ct)
                if pt is None:
                    continue
                valid_padding += 1
                check_plaintext(pt, f'{cand[:40]}|{label}', hits)
    if (idx + 1) % 2000 == 0:
        print(f'  ... {idx+1}/{len(cands)} candidates, {attempts} decryptions, {valid_padding} valid paddings, {len(hits)} hits, {time.time()-t0:.0f}s', flush=True)

elapsed = time.time() - t0
print(f'DONE: {len(cands)} candidates, {attempts} decryptions, {valid_padding} valid paddings, {len(hits)} hits, {elapsed:.1f}s')
# the witness must be among the hits (proves the harness catches a real hit)
witness_found = any('WITNESS' in h[0] for h in hits)
print(f'WITNESS recovered: {witness_found}')
real_hits = [h for h in hits if 'WITNESS' not in h[0]]
print(f'REAL hits (excluding witness): {real_hits if real_hits else "none"}')
with open('/home/hatch/workspace/gsmg-dynamic-replay-hits.json', 'w') as f:
    json.dump({'candidates': len(cands), 'attempts': attempts, 'valid_padding': valid_padding,
               'elapsed_s': round(elapsed, 1), 'witness_found': witness_found,
               'real_hits': real_hits}, f, indent=1)
