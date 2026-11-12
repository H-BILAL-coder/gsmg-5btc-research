#!/usr/bin/env python3
"""Test lukaszbanasiak/python-ciphers' menu (AtBash, Bacon, Bifid, Caesar,
Polybius) against the open GSMG objects, using the tool's own exact code
(ported faithfully to Python 3) and the corrected oracle (both digests,
floflo readings(), both address forms, prize + second escrow).

Objects: obj256, Bifid plaintext (570), streamA, streamB, dropped29,
prefix91 (from gsmg-esrever-results.json) + the 252 saved valid-padding
plaintexts from the kit (big_hits.txt + smart_screen_*).
"""
import ast, base64, hashlib, json, re, sys
from unicodedata import normalize
import base58 as b58lib
from coincurve import PrivateKey as CCPriv
from Crypto.Cipher import AES

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
INV2 = pow(2, -1, N_ORDER)
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# ---------- oracle (copied from gsmg_esrever.py, verified) ----------
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
    """If a transform output is exactly 32 bytes or 64 hex chars, check it as a key."""
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

# ---------- the tool's ciphers (lukaszbanasiak/python-ciphers, faithful port) ----------
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

# ---------- self-checks ----------
assert priv_to_addrs(bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000001'))[0] == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH'
assert priv_to_addrs(bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000001'))[1] == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
# tool Bifid reproduces the puzzle's confirmed Bifid decode
_res = json.load(open('/home/hatch/workspace/gsmg-esrever-results.json'))
assert bifid_decrypt(_res['segment'], poly_array('DBIFHCEG')) == _res['plaintext']
print('SELF-CHECKS PASS: privkey-1 vectors + tool Bifid == puzzle Bifid plaintext', flush=True)

# ---------- objects ----------
res = _res
objects = {
    'obj256': res['obj256'],
    'bifid_plaintext_570': res['plaintext'],
    'streamA': res['streamA'],
    'streamB': res['streamB'],
    'dropped29': res['dropped29'],
    'prefix91': res['prefix91'],
}
SQUARES = {'DBIFHCEG': poly_array('DBIFHCEG'), 'default': poly_array('')}

def test_output(label, s):
    """Test one transform output as a password and as a direct key."""
    b = s.encode('latin-1', 'replace') if isinstance(s, str) else s
    if not b:
        return
    try_password(b)
    check_direct_key_bytes(b, label)

n_out = 0
for oname, obj in objects.items():
    # Caesar shifts 1-25
    for sh in range(1, 26):
        test_output(f'{oname}|caesar+{sh}', caesar(obj, sh)); n_out += 1
    # AtBash
    test_output(f'{oname}|atbash', atbash(obj)); n_out += 1
    # Bacon encode (+ decode of the encoding is the original; skip)
    test_output(f'{oname}|bacon-enc', bacon_encode(obj)); n_out += 1
    # Polybius encode, both squares
    for sqname, arr in SQUARES.items():
        test_output(f'{oname}|poly-enc-{sqname}', poly_encode(obj, arr)); n_out += 1
    # Bifid encrypt + decrypt, both squares
    for sqname, arr in SQUARES.items():
        test_output(f'{oname}|bifid-enc-{sqname}', bifid_encrypt(obj, arr)); n_out += 1
        test_output(f'{oname}|bifid-dec-{sqname}', bifid_decrypt(obj, arr)); n_out += 1
print(f'string objects done: {n_out} outputs tested', flush=True)

# ---------- saved valid-padding plaintexts (audit parser) ----------
def parse_line(line, fname):
    parts = line.rstrip('\n').split('\t')
    if len(parts) == 4:
        blob = parts[1]; pw_part, pt_part = parts[2], parts[3]
    elif len(parts) == 3:
        blob = 'blob1' if 'blob1' in fname else 'blob2'
        pw_part, pt_part = parts[1], parts[2]
    else:
        return None
    try:
        pt = ast.literal_eval(pt_part)
    except Exception:
        return None
    if not isinstance(pt, (bytes, bytearray)):
        return None
    return bytes(pt)

n_pt = 0
for fname in ('big_hits.txt', 'smart_screen_blob1.txt', 'smart_screen_blob2.txt'):
    for line in open(f'{KIT}/{fname}', encoding='utf-8', errors='replace'):
        pt = parse_line(line, fname)
        if pt is None:
            continue
        n_pt += 1
        s = pt.decode('latin-1')
        for sh in range(1, 26):
            test_output(f'saved-pt#{n_pt}|caesar+{sh}', caesar(s, sh)); n_out += 1
        test_output(f'saved-pt#{n_pt}|atbash', atbash(s)); n_out += 1
        test_output(f'saved-pt#{n_pt}|bacon-enc', bacon_encode(s)); n_out += 1
        for sqname, arr in SQUARES.items():
            test_output(f'saved-pt#{n_pt}|poly-enc-{sqname}', poly_encode(s, arr)); n_out += 1
            test_output(f'saved-pt#{n_pt}|bifid-enc-{sqname}', bifid_encrypt(s, arr)); n_out += 1
            test_output(f'saved-pt#{n_pt}|bifid-dec-{sqname}', bifid_decrypt(s, arr)); n_out += 1
print(f'saved plaintexts done: {n_pt} plaintexts', flush=True)

print('TOTAL outputs tested:', n_out)
print('STATS:', stats)
print('HITS:', hits)
print('LONG-PRINTABLE:', long_printable)
json.dump({'outputs': n_out, 'saved_plaintexts': n_pt, 'stats': stats,
           'hits': hits, 'long_printable': long_printable},
          open('/home/hatch/workspace/gsmg-tool-menu-results.json', 'w'), indent=2)
print('RESULTS WRITTEN')
