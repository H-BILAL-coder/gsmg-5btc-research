#!/usr/bin/env python3
"""Digest the 49-char middle block of the GSMG YOUWON alignment (D[21:70])
and test the results as passwords.

STEP 1 (verified in-run): S91 (91-char dbbi stream, from repo artifacts) minus
the Phase 3.2 VIC plaintext, letterwise mod 26, spells YOUWON at index 21.
D = 'VOZIJBDTIQBRGVEOMZNBCYOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCAMVDJLQTSGA'
Middle 49 (D[21:70]) = 'YOUWONXCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNX'

Transformations (per brief): the identified tool's menu
(lukaszbanasiak/python-ciphers — AtBash, Bacon, Bifid key DBIFHCEG, Caesar
1-25, Polybius DBIFHCEG + default), reverse, ROT-13 (= Caesar 13, included),
Vigenere with the puzzle's own token keys, direct password; plus the
concatenations matrixsumlist+lastwordsbeforearchichoice+<result> and
<result>+matrixsumlist+lastwordsbeforearchichoice.
Extra (labelled): the two letterwise flank combinations (HEAD+TAIL, HEAD-TAIL
mod 26) as additional base objects.
Testing: every candidate as a password against all three blobs, both digests
(SHA-256 + MD5), corrected reader (floflo readings(), both address forms,
prize + second escrow). Reuses the verified oracle from gsmg_tool_menu_test.py.
"""
import base64, hashlib, json, re
import base58 as b58lib
from coincurve import PrivateKey as CCPriv
from Crypto.Cipher import AES

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
INV2 = pow(2, -1, N_ORDER)
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# ---------- oracle (verbatim from gsmg_tool_menu_test.py, verified) ----------
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

hits, long_printable = [], []
stats = {'valid_padding': 0, 'readings': 0, 'passwords': 0, 'direct_keys': 0}

def check_key(key: bytes, label: str, blob='', digest='', pw=''):
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
                               'len': len(plain)})
    for variant, prefix in ((plain, ''), (plain[::-1], 'rev:'), (bitrev(plain), 'bitrev:')):
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
        for label, v in {'halves a+b': (a + b) % N_ORDER, 'halves a-b': (a - b) % N_ORDER,
                         'halves b-a': (b - a) % N_ORDER, 'halves a^b': a ^ b,
                         'halves 2a': (2 * a) % N_ORDER, 'halves a/2': (a * INV2) % N_ORDER,
                         'halves 2b': (2 * b) % N_ORDER, 'halves b/2': (b * INV2) % N_ORDER}.items():
            if 1 <= v < N_ORDER:
                if check_key(v.to_bytes(32, 'big'), label, blob, digest, pw_preview):
                    return True
    return False

def try_password(pw: bytes):
    stats['passwords'] += 1
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

def check_direct_key_bytes(b: bytes, label: str):
    if len(b) == 32:
        stats['direct_keys'] += 1
        check_key(b, label + '|direct32')
    s = b.strip()
    if len(s) == 64 and all(c in b'0123456789abcdefABCDEF' for c in s):
        try:
            stats['direct_keys'] += 1
            check_key(bytes.fromhex(s.decode('ascii')), label + '|direct-hex64')
        except ValueError:
            pass

# ---------- tool ciphers (lukaszbanasiak/python-ciphers, faithful port) ----------
EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caesar(words, shift):
    out = ''
    for ch in words:
        if ch.upper() not in EN:
            out += ch
        elif ch.islower():
            out += EN[(EN.index(ch.upper()) + shift) % 26].lower()
        else:
            out += EN[(EN.index(ch) + shift) % 26]
    return out

def atbash(words):
    out = ''
    for ch in words:
        if ch.upper() not in EN:
            out += ch
        elif ch.islower():
            out += EN[25 - EN.index(ch.upper())].lower()
        else:
            out += EN[25 - EN.index(ch)]
    return out

def bacon_encode(words):
    d = {}
    for i in range(26):
        t = bin(i)[2:].zfill(5).replace('0', 'a').replace('1', 'b')
        d[chr(65 + i)] = t
    words = re.sub(r'[^A-Z]+', '', words.upper())
    return ''.join(d.get(c, '') for c in words).upper()

def bacon_decode(words):
    d = {}
    for i in range(26):
        t = bin(i)[2:].zfill(5).replace('0', 'a').replace('1', 'b')
        d[t] = chr(65 + i)
    words = re.sub(r'[^ab]+', '', words.lower())
    return ''.join(d.get(words[i*5:i*5+5], ' ') for i in range(len(words) // 5))

def poly_array(key=''):
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = re.sub(r'[^a-zA-Z]+', '', key).upper()
    if key:
        for k in key:
            alphabet = alphabet.replace(k, '')
        alphabet = key + alphabet
    return [[alphabet[5*y+x] for x in range(5)] for y in range(5)]

def poly_encode(words, array):
    cipher = ''
    for word in words.upper():
        for i in range(len(array)):
            if word in array[i]:
                cipher += str(i+1) + str(array[i].index(word)+1)
    return cipher

def poly_decode(numbers, array):
    numbers = re.sub(r'[\D]+', '', numbers)
    text = ''
    for n in range(0, len(numbers), 2):
        try:
            text += array[int(numbers[n])-1][int(numbers[n+1])-1]
        except IndexError:
            pass
    return text

def bifid_transform(data):
    data = re.sub(r'[\D]+', '', data)
    return data[::2] + data[1::2]

def bifid_transform_back(data):
    data = re.sub(r'[\D]+', '', data)
    n = len(data) // 2
    a, b = data[:n], data[n:]
    return ''.join(a[i] + b[i] for i in range(len(a)))

def bifid_encrypt(words, array):
    return poly_decode(bifid_transform(poly_encode(words, array)), array)

def bifid_decrypt(words, array):
    return poly_decode(bifid_transform_back(poly_encode(words, array)), array)

def vigenere_enc(words, key):
    key = re.sub(r'[^A-Z]+', '', key.upper())
    if not key:
        return words
    out, ki = '', 0
    for ch in words:
        if ch.upper() in EN:
            s = (EN.index(ch.upper()) + EN.index(key[ki % len(key)])) % 26
            out += EN[s] if ch.isupper() else EN[s].lower()
            ki += 1
        else:
            out += ch
    return out

def vigenere_dec(words, key):
    key = re.sub(r'[^A-Z]+', '', key.upper())
    if not key:
        return words
    out, ki = '', 0
    for ch in words:
        if ch.upper() in EN:
            s = (EN.index(ch.upper()) - EN.index(key[ki % len(key)])) % 26
            out += EN[s] if ch.isupper() else EN[s].lower()
            ki += 1
        else:
            out += ch
    return out

# ---------- self-checks ----------
assert priv_to_addrs(bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000001'))[0] == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH'
assert priv_to_addrs(bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000001'))[1] == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
_res = json.load(open('/home/hatch/workspace/gsmg-esrever-results.json'))
assert bifid_decrypt(_res['segment'], poly_array('DBIFHCEG')) == _res['plaintext']
print('SELF-CHECKS PASS: privkey-1 vectors + tool Bifid == puzzle Bifid plaintext', flush=True)

# ---------- STEP 1: verify the alignment ----------
S91 = _res['prefix91'].upper()
M91 = json.load(open('/home/hatch/workspace/apple-repo/gsmgio-5btc-puzzle-master/phase32_classical.json'))['vic']['plaintext'].upper()
assert len(S91) == 91 and len(M91) == 91, (len(S91), len(M91))
D = ''.join(chr((ord(a) - ord(b)) % 26 + ord('A')) for a, b in zip(S91, M91))
assert D.find('YOUWON') == 21, D
assert hashlib.sha256(S91.lower().encode()).hexdigest() == '71fe46259e270c113529dfaded4b59c59a9dffd826a7202ab07fc498b6a2c5ca'
assert hashlib.sha256(M91.lower().encode()).hexdigest() == '2fbfbef7442558f17ecc866a0b89ed491c41abc042df4d41452835adff09e9d3'
assert hashlib.sha256(D.encode()).hexdigest() == 'f17857308a886531637b33c9ddb92952206c286519412278ba9f836ffc69336e'
print('ALIGNMENT VERIFIED: YOUWON at index 21; all three SHA-256 checkpoints match', flush=True)

M49 = D[21:70]
HEAD21 = D[:21]
TAIL21 = D[70:]
M43 = D[27:70]
print('M49 :', M49)
print('HEAD:', HEAD21)
print('TAIL:', TAIL21)
print('M43 :', M43)

# ---------- STEP 2: candidate generation ----------
SQUARES = {'DBIFHCEG': poly_array('DBIFHCEG'), 'default': poly_array('')}
VIG_KEYS = ['matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword',
            'yinyang', 'halvings']
TOKENS = 'matrixsumlist' + 'lastwordsbeforearchichoice'

def letterwise(a, b, op):
    out = ''
    for x, y in zip(a, b):
        va, vb = EN.index(x), EN.index(y)
        out += EN[(va + vb) % 26] if op == '+' else EN[(va - vb) % 26]
    return out

bases = {
    'M49': M49,
    'HEAD+M49': HEAD21 + M49,
    'M49+TAIL': M49 + TAIL21,
    'FULL91': D,
    'M43': M43,
    'HEAD21': HEAD21,
    'TAIL21': TAIL21,
    'FLANKS': HEAD21 + TAIL21,
    'FLANKS_REV': TAIL21 + HEAD21,
    # labelled extra: letterwise flank combinations (v44 tested these only as scalars)
    'FLANK_ADD': letterwise(HEAD21, TAIL21, '+'),
    'FLANK_SUB': letterwise(HEAD21, TAIL21, '-'),
}

def transforms(name, s):
    """Yield (label, output) for every reading of base string s."""
    yield (f'{name}|direct', s)
    yield (f'{name}|reverse', s[::-1])
    for sh in range(1, 26):
        yield (f'{name}|caesar+{sh}', caesar(s, sh))
    yield (f'{name}|atbash', atbash(s))
    yield (f'{name}|bacon-enc', bacon_encode(s))
    yield (f'{name}|bacon-dec', bacon_decode(s))
    for sqname, arr in SQUARES.items():
        yield (f'{name}|poly-enc-{sqname}', poly_encode(s, arr))
        yield (f'{name}|bifid-enc-{sqname}', bifid_encrypt(s, arr))
        yield (f'{name}|bifid-dec-{sqname}', bifid_decrypt(s, arr))
    for k in VIG_KEYS:
        yield (f'{name}|vig-enc-{k}', vigenere_enc(s, k))
        yield (f'{name}|vig-dec-{k}', vigenere_dec(s, k))

outputs = []  # (label, string)
for bname, bstr in bases.items():
    for label, out in transforms(bname, bstr):
        outputs.append((label, out))
print(f'transform outputs: {len(outputs)}', flush=True)

# ---------- STEP 3: test ----------
def test_phrase(label, s):
    b = s.encode('latin-1', 'replace') if isinstance(s, str) else s
    if not b:
        return
    try_password(b)
    check_direct_key_bytes(b, label)

n_phrases = 0
seen = set()
for label, out in outputs:
    for form, s in (('asis', out), ('lower', out.lower())):
        key = (label, form, s)
        if key in seen or not s:
            continue
        seen.add(key)
        test_phrase(f'{label}|{form}', s)
        n_phrases += 1
        # concatenations with the puzzle tokens (lowercase throughout)
        low = s.lower()
        test_phrase(f'{label}|{form}|tok+pre', TOKENS + low)
        n_phrases += 1
        test_phrase(f'{label}|{form}|tok+post', low + TOKENS)
        n_phrases += 1
print(f'phrases tested: {n_phrases}', flush=True)
print(f'stats: {stats}', flush=True)
print(f'valid-padding plaintexts: {stats["valid_padding"]}', flush=True)
print(f'key readings checked: {stats["readings"]}', flush=True)
print(f'direct key checks: {stats["direct_keys"]}', flush=True)
print(f'long printable plaintexts: {len(long_printable)}', flush=True)
print(f'HITS: {len(hits)}', flush=True)
for h in hits:
    print('HIT:', h)

result = {
    'alignment_verified': True,
    's91': S91, 'm91': M91, 'difference': D,
    'youwon_index': 21,
    'middle49': M49, 'head21': HEAD21, 'tail21': TAIL21, 'middle43': M43,
    'transform_outputs': len(outputs),
    'phrases_tested': n_phrases,
    'stats': stats,
    'long_printable': long_printable,
    'hits': hits,
}
json.dump(result, open('/home/hatch/workspace/gsmg-youwon49-results.json', 'w'), indent=2)
print('results written to ~/workspace/gsmg-youwon49-results.json', flush=True)
