#!/usr/bin/env python3
"""GSMG — esrever + 29-dropped-letters + dbbi/faed balancing test (2026-11-11).
Bounded test approved by Hazrat. Reuses the corrected oracle from
gsmg_rerun.py (same code, same self-checks): both digests (SHA-256 + MD5),
floflo readings(), both address forms, prize + second escrow.
Also reads valid-padding plaintexts reversed and bit-reversed (the
"esrever" reading of the locks' plaintexts).

Step 1 reconstructs the 570-char Bifid segment from the LIVE SalPhaseIon
page (saved at ~/workspace/gsmg-salphaseion.html) and verifies it:
Bifid decode (keyed square DBIFHCEG, period 570, identity map a->A..i->I)
must start with BTCSEED; the 285-letter stream must drop exactly 29 I/O
to give the 256-symbol object over 23 letters.
"""
import base64, hashlib, json, re, sys, time
from Crypto.Cipher import AES
from coincurve import PrivateKey as CCPriv
import base58 as b58lib

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
THIRD_DOOR = '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9'
N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
INV2 = (N_ORDER + 1) // 2
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58check(payload: bytes) -> str:
    h = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    data = payload + h
    n = int.from_bytes(data, 'big')
    s = ''
    while n > 0:
        n, r = divmod(n, 58)
        s = B58[r] + s
    return '1' * (len(data) - len(data.lstrip(b'\x00'))) + s

def priv_to_addrs(priv: bytes):
    pk = CCPriv(priv)
    out = []
    for pub in (pk.public_key.format(compressed=True),
                pk.public_key.format(compressed=False)):
        h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
        out.append(b58check(b'\x00' + h))
    return out

def evp(pw: bytes, salt: bytes, md: str):
    H = hashlib.sha256 if md == 'sha256' else hashlib.md5
    out, prev = b'', b''
    while len(out) < 48:
        prev = H(prev + pw + salt).digest()
        out += prev
    return out[:32], out[32:48]

def load_blob(name):
    raw = base64.b64decode(open(f'{KIT}/{name}.txt').read().strip())
    return raw[8:16], raw[16:]
BLOBS = {'blob1': load_blob('blob1_phase32_final'),
         'blob2': load_blob('blob2_salphaseion'),
         'blob3': load_blob('blob3_cosmic_duality')}

def readings(plain: bytes):
    out = [('sha256(plaintext)', hashlib.sha256(plain).digest())]
    if len(plain) >= 32:
        out.append(('first32', plain[:32]))
        out.append(('last32', plain[-32:]))
    if len(plain) >= 64:
        out.append(('sha256(first64)', hashlib.sha256(plain[:64]).digest()))
    stripped = b''.join(plain.split())
    if stripped[:2] in (b'0x', b'0X'):
        stripped = stripped[2:]
    if len(stripped) in (64, 128) and all(c in b'0123456789abcdefABCDEF' for c in stripped):
        try:
            dec = bytes.fromhex(stripped.decode('ascii'))
            if len(dec) == 32:
                out.append(('hex->32', dec))
            elif len(dec) == 64:
                out.append(('hex->first32', dec[:32]))
                out.append(('hex->last32', dec[-32:]))
        except ValueError:
            pass
    token = b''.join(plain.split())
    if 50 <= len(token) <= 53:
        try:
            raw = b58lib.b58decode_check(token.decode('ascii'))
            if raw[:1] == b'\x80' and len(raw) in (33, 34):
                out.append(('wif', raw[1:33]))
        except Exception:
            pass
    return out

def bitrev(b: bytes) -> bytes:
    return bytes(int(f'{x:08b}'[::-1], 2) for x in b)

# ---- global result collectors ----
hits, long_printable = [], []
stats = {'valid_padding': 0, 'readings': 0, 'direct_keys': 0, 'third_door': 0}
hits_third = []

def check_key(key: bytes, label: str, blob='', digest='', pw=''):
    """Check one 32-byte key, both address forms, prize + second escrow."""
    if len(key) != 32:
        return False
    k = int.from_bytes(key, 'big')
    if not (1 <= k < N_ORDER):
        return False
    stats['readings'] += 1
    try:
        comp, uncomp = priv_to_addrs(key)
    except Exception:
        return False
    for addr, form in ((comp, 'compressed'), (uncomp, 'uncompressed')):
        if addr in (TARGET, SECOND):
            hit = {'blob': blob, 'digest': digest, 'reading': label,
                   'form': form, 'address': addr, 'priv_hex': key.hex(), 'pw': pw}
            hits.append(hit)
            print(f'  *** HIT *** {hit}', flush=True)
            return True
    return False

def check_plain(plain, blob, digest, pw_preview):
    stats['valid_padding'] += 1
    if len(plain) >= 64 and all(32 <= b < 127 or b in (10, 13, 9) for b in plain):
        long_printable.append({'blob': blob, 'digest': digest, 'pw': pw_preview,
                               'len': len(plain),
                               'text': plain[:200].decode('utf-8', 'replace')})
        print(f'  LONG-PRINTABLE {blob}/{digest} pw={pw_preview!r} len={len(plain)}', flush=True)
    # readings on the plaintext, its reverse, and its bit-reverse
    variants = [(plain, ''), (plain[::-1], 'rev:'), (bitrev(plain), 'bitrev:')]
    for variant, prefix in variants:
        for name, key in readings(variant):
            if len(key) != 32:
                continue
            if check_key(key, prefix + name, blob, digest, pw_preview):
                return True
            k = int.from_bytes(key, 'big')
            if 1 <= k < N_ORDER:
                if check_key(((2 * k) % N_ORDER).to_bytes(32, 'big'),
                             prefix + name + '+double', blob, digest, pw_preview):
                    return True
                if check_key(((k * INV2) % N_ORDER).to_bytes(32, 'big'),
                             prefix + name + '+half', blob, digest, pw_preview):
                    return True
    if len(plain) >= 64:
        a = int.from_bytes(plain[:32], 'big')
        b = int.from_bytes(plain[-32:], 'big')
        combos = {'halves a+b': (a + b) % N_ORDER, 'halves a-b': (a - b) % N_ORDER,
                  'halves b-a': (b - a) % N_ORDER, 'halves a^b': a ^ b,
                  'halves 2a': (2 * a) % N_ORDER, 'halves a/2': (a * INV2) % N_ORDER,
                  'halves 2b': (2 * b) % N_ORDER, 'halves b/2': (b * INV2) % N_ORDER}
        for label, v in combos.items():
            if 1 <= v < N_ORDER:
                if check_key(v.to_bytes(32, 'big'), label, blob, digest, pw_preview):
                    return True
    return False

def try_password(pw: bytes):
    pw_prev = pw[:60].decode('utf-8', 'replace')
    for digest in ('sha256', 'md5'):
        for bname, (salt, ct) in BLOBS.items():
            key, iv = evp(pw, salt, digest)
            last = ct[-16:]
            prev_block = ct[-32:-16] if len(ct) > 16 else iv
            dec_last = AES.new(key, AES.MODE_ECB).decrypt(last)
            pt_last = bytes(a ^ b for a, b in zip(dec_last, prev_block))
            pad = pt_last[-1]
            if not (1 <= pad <= 16) or pt_last[-pad:] != bytes([pad]) * pad:
                continue
            pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
            pt = pt[:-pad]
            if not pt:
                continue
            check_plain(pt, bname, digest, pw_prev)

def crack_forms(phrase: str):
    forms = set()
    variants = {phrase, phrase.lower(), phrase.replace(' ', ''),
                phrase.lower().replace(' ', '')}
    for v in variants:
        if not v:
            continue
        forms.add(v.encode('utf-8'))
        forms.add(hashlib.sha256(v.encode('utf-8')).hexdigest().encode('ascii'))
    return forms

def third_door_check(phrase: str):
    """Exact offline oracle (floflo leads #1): sha256(X), bit-reversed
    sha256(X), X padded to 32 bytes, vs the unmessaged planted address."""
    xb = phrase.encode('utf-8')
    cands = [('sha256', hashlib.sha256(xb).digest()),
             ('bitrev-sha256', bitrev(hashlib.sha256(xb).digest()))]
    if len(xb) >= 32:
        cands.append(('first32', xb[:32]))
        cands.append(('last32', xb[-32:]))
    else:
        cands.append(('lpad32', b'\x00' * (32 - len(xb)) + xb))
        cands.append(('rpad32', xb + b'\x00' * (32 - len(xb))))
    for label, key in cands:
        stats['third_door'] += 1
        k = int.from_bytes(key, 'big')
        if not (1 <= k < N_ORDER):
            continue
        try:
            comp, uncomp = priv_to_addrs(key)
        except Exception:
            continue
        for addr, form in ((comp, 'compressed'), (uncomp, 'uncompressed')):
            if addr == THIRD_DOOR:
                hits_third.append({'phrase': phrase[:80], 'reading': label,
                                   'form': form, 'priv_hex': key.hex()})
                print(f'  *** THIRD-DOOR HIT *** {hits_third[-1]}', flush=True)

# ---- self-checks ----
c1, u1 = priv_to_addrs(b'\x00' * 31 + b'\x01')
assert c1 == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH' and u1 == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
KNOWN_PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                          '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
h = hashlib.new('ripemd160', hashlib.sha256(KNOWN_PUB).digest()).digest()
assert b58check(b'\x00' + h) == TARGET
print('self-checks PASS (privkey-1 vectors + escrow pubkey -> prize address)', flush=True)

# ================= STEP 1: reconstruct from the live page =================
html = open('/home/hatch/workspace/gsmg-salphaseion.html').read()
toks = re.search(r'<textarea[^>]*>(.*?)</textarea>', html, re.S).group(1).split()
assert len(toks) == 1075, len(toks)
c0 = toks[:765]
prefix91 = ''.join(c0[:91])
binrun = ''.join('0' if t == 'a' else '1' for t in c0[91:195])
matrixsumlist = ''.join(chr(int(binrun[i:i+8], 2)) for i in range(0, 104, 8))
assert matrixsumlist == 'matrixsumlist', matrixsumlist
segment = ''.join(c0[195:765])
assert len(segment) == 570
# agda / cfob: letters o=0,a=1..i=9 -> decimal integer -> bytes
mp = {'o': '0', 'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9'}
def dec_int(tokens):
    d = ''.join(mp[t] for t in tokens)
    n = int(d)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('ascii')
lastwords = dec_int(toks[766:829])
thispassword = dec_int(toks[830:859])
assert lastwords == 'lastwordsbeforearchichoice', lastwords
assert thispassword == 'thispassword', thispassword

# Bifid decode of the segment
key = "DBIFHCEG"
alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
sq = []
for ch in key + alpha:
    if ch not in sq:
        sq.append(ch)
pos = {ch: (i // 5 + 1, i % 5 + 1) for i, ch in enumerate(sq)}
grid = [[sq[r * 5 + c] for c in range(5)] for r in range(5)]
def bifid_decrypt(ct):
    ct = ct.upper()
    n = len(ct)
    u = [pos[ch][0] for ch in ct]
    v = [pos[ch][1] for ch in ct]
    T = []
    for i in range(n):
        T.append(u[i]); T.append(v[i])
    return ''.join(grid[T[i] - 1][T[i + n] - 1] for i in range(n))
plaintext = bifid_decrypt(segment)
assert plaintext.startswith('BTCSEED'), plaintext[:20]
streamA = plaintext[0::2]   # 1-based odd positions: 285 chars over {B,C,D,E}
streamB = plaintext[1::2]   # 1-based even positions: 285-letter stream
assert len(streamA) == 285 and len(streamB) == 285
assert sorted(set(streamA)) == ['B', 'C', 'D', 'E']
dropped = ''.join(ch for ch in streamB if ch in 'IO')
assert len(dropped) == 29, len(dropped)
obj256 = ''.join(ch for ch in streamB if ch not in 'IO')
assert len(obj256) == 256 and len(set(obj256)) == 23
print('STEP 1 VERIFIED: segment 570, plaintext starts BTCSEED, '
      f'streamB 285 -> 29 dropped -> 256-object over 23 letters', flush=True)
print('  29 dropped letters:', dropped, flush=True)

# ================= candidate phrases =================
cands = []  # (label, phrase)
def add(label, phrase):
    cands.append((label, phrase))

# ---- STEP 2: esrever ----
add('E1 256-object reversed', obj256[::-1])
add('E2 segment reversed', segment[::-1])
add('E3 streamB(285) reversed', streamB[::-1])
add('E4 streamA(BCDE) reversed', streamA[::-1])
add('E5 Bifid plaintext(570) reversed', plaintext[::-1])
add('E6 91-prefix reversed', prefix91[::-1])
add('E7 256-object forward', obj256)
add('E8 segment forward', segment)
add('E9 streamB forward', streamB)
add('E10 streamA forward', streamA)
add('E11 Bifid plaintext forward', plaintext)
add('E12 91-prefix forward', prefix91)
# Dualite / small-blob base64 and ciphertext reversed (as passwords)
b3b64 = open(f'{KIT}/blob3_cosmic_duality.txt').read().strip()
b1b64 = open(f'{KIT}/blob1_phase32_final.txt').read().strip()
b2b64 = open(f'{KIT}/blob2_salphaseion.txt').read().strip()
add('E13 Dualite blob base64 reversed', b3b64[::-1])
add('E14 Dualite blob ciphertext hex reversed',
    base64.b64decode(b3b64)[16:].hex()[::-1])
add('E15 blob1 base64 reversed', b1b64[::-1])
add('E16 blob2 base64 reversed', b2b64[::-1])

# ---- STEP 3: the 29 dropped letters ----
S1 = dropped
S2 = dropped[::-1]
add('S1 29 dropped letters', S1)
add('S2 29 dropped letters reversed', S2)
# direct key checks for the 29 letters (not passwords)
direct_keys = []
sb = S1.encode('ascii')
direct_keys.append(('29-letters sha256', hashlib.sha256(sb).digest()))
direct_keys.append(('29-letters lpad32', b'\x00' * 3 + sb))
direct_keys.append(('29-letters rpad32', sb + b'\x00' * 3))
for name, s in (('S1', S1), ('S2', S2)):
    for oname, one, zero in (('I=1,O=0', '1', '0'), ('O=1,I=0', '0', '1')):
        bits = ''.join(one if ch == 'I' else zero for ch in s)
        v = int(bits, 2)
        direct_keys.append((f'{name} bits {oname} as key', v.to_bytes(32, 'big')))

# ---- ADDITION: dbbi / faed balancing ----
dbbi = prefix91            # 91 chars, lowercase a-i (canonical)
faed = segment             # 570 chars, lowercase a-i (canonical)
assert len(dbbi) == 91 and len(faed) == 570
def digits(s):
    return [ord(c) - ord('a') for c in s]  # a=0..i=8
def to_letters(ds):
    return ''.join(chr(97 + d) for d in ds)
def to_digits0(ds):
    return ''.join(str(d) for d in ds)
def to_digits1(ds):
    return ''.join(str(d + 1) for d in ds)
alignments = {
    'A1 prefix91': (dbbi, faed[:91]),
    'A2 tiled570': ((dbbi * 7)[:570], faed),
    'A3 padded570': (dbbi + 'a' * (570 - 91), faed),
}
dbbi_faed_results = []  # (label, letters-string)
for aname, (dstr, fstr) in alignments.items():
    dx, fx = digits(dstr), digits(fstr)
    L = len(dx)
    assert len(fx) == L
    ops = {
        'add-mod9': [(x + y) % 9 for x, y in zip(dx, fx)],
        'sub-dbbi-faed-mod9': [(x - y) % 9 for x, y in zip(dx, fx)],
        'sub-faed-dbbi-mod9': [(y - x) % 9 for x, y in zip(dx, fx)],
        'xor-mod9': [(x ^ y) % 9 for x, y in zip(dx, fx)],
        'interleave': [v for pair in zip(dx, fx) for v in pair],
        'concat-dbbi+faed': dx + fx,
        'concat-faed+dbbi': fx + dx,
    }
    xor_hex = ''.join(format(x ^ y, 'x') for x, y in zip(dx, fx))
    for opname, ds in ops.items():
        letters = to_letters(ds)
        label = f'{aname} {opname}'
        dbbi_faed_results.append((label, letters))
        add(f'DF {label} letters', letters)
        add(f'DF {label} digits0', to_digits0(ds))
        add(f'DF {label} digits1', to_digits1(ds))
        add(f'DF {label} letters reversed', letters[::-1])
        add(f'DF {label} digits0 reversed', to_digits0(ds)[::-1])
        add(f'DF {label} digits1 reversed', to_digits1(ds)[::-1])
        # concatenation with the two decoded phrases
        add(f'DF concat-phrase {label}',
            matrixsumlist + lastwords + letters)
    add(f'DF {aname} xor-hex', xor_hex)
    add(f'DF {aname} xor-hex reversed', xor_hex[::-1])

# ================= run =================
t0 = time.time()
n_forms = 0
n_attempts = 0
for label, phrase in cands:
    forms = crack_forms(phrase)
    n_forms += len(forms)
    for pw in forms:
        n_attempts += 1
        try_password(pw)
    third_door_check(phrase)
for label, key in direct_keys:
    stats['direct_keys'] += 1
    check_key(key, label, blob='direct', digest='-', pw=label)
el = time.time() - t0

# ================= record =================
rec = {
    'segment': segment, 'plaintext': plaintext, 'streamA': streamA,
    'streamB': streamB, 'dropped29': dropped, 'obj256': obj256,
    'prefix91': prefix91, 'matrixsumlist': matrixsumlist,
    'lastwords': lastwords, 'thispassword': thispassword,
    'dbbi_faed_results': [{'label': l, 'letters': s}
                          for l, s in dbbi_faed_results],
    'counts': {'phrases': len(cands), 'password_forms': n_forms,
               'decrypt_attempts': n_attempts * 6,
               'valid_padding': stats['valid_padding'],
               'key_readings': stats['readings'],
               'direct_keys': stats['direct_keys'],
               'third_door_checks': stats['third_door'],
               'hits': len(hits), 'long_printable': len(long_printable),
               'third_door_hits': len(hits_third),
               'seconds': round(el, 1)},
    'hits': hits, 'hits_third': hits_third,
    'long_printable': long_printable,
}
json.dump(rec, open('/home/hatch/workspace/gsmg-esrever-results.json', 'w'), indent=1)
print(f"\nDONE in {el:.1f}s: {len(cands)} phrases, {n_forms} password forms, "
      f"{n_attempts * 6:,} decrypt attempts (3 blobs x 2 digests), "
      f"valid-padding={stats['valid_padding']}, readings={stats['readings']}, "
      f"direct_keys={stats['direct_keys']}, third_door={stats['third_door']}, "
      f"HITS={len(hits)}, LONG-PRINTABLE={len(long_printable)}, "
      f"THIRD-DOOR-HITS={len(hits_third)}", flush=True)
