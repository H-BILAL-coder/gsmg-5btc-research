#!/usr/bin/env python3
"""GSMG — meaning-reconstruction candidate test (2026-11-11).
Tests a SMALL named set of password phrases derived from the creator's own
words and the puzzle's structure (see gsmg-meaning-pass.md), against all FOUR
blobs with BOTH digests and the corrected reader. No new word lists, no brute
force. Every phrase here was verified NOT to be an exact line in any kit
candidate file (candidates/gen/smart/long_ngrams/dbbi_faed) — i.e. not already
tested against all four blobs by the audit re-run / blob4 test.
Oracle: floflo readings() + 2k/k/2 neighbours + split-key combos, both
address forms, prize + second escrow, plus the third-door check.
"""
import base64, hashlib, json, time

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
THIRD_DOOR = '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9'

from Crypto.Cipher import AES
from coincurve import PrivateKey as CCPriv
import base58 as b58lib

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
         'blob3': load_blob('blob3_cosmic_duality'),
         'blob4': load_blob('blob4_urlblob')}

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
    for token in plain.split():
        if 50 <= len(token) <= 53:
            try:
                raw = b58lib.b58decode_check(token.decode('ascii'))
                if raw[:1] == b'\x80' and len(raw) in (33, 34):
                    out.append(('wif', raw[1:33]))
            except Exception:
                pass
    return out

N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
INV2 = (N_ORDER + 1) // 2

def check_plain(plain, blob, digest, pw_preview, hits, long_printable, stats):
    stats['valid_padding'] += 1
    if len(plain) >= 64 and all(32 <= b < 127 or b in (10, 13, 9) for b in plain):
        long_printable.append({'blob': blob, 'digest': digest,
                               'pw': pw_preview, 'len': len(plain),
                               'text': plain[:200].decode('utf-8', 'replace')})
        print(f'  LONG-PRINTABLE {blob}/{digest} pw={pw_preview!r} len={len(plain)}', flush=True)

    def check_one_key(key: bytes, label: str):
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
                       'form': form, 'address': addr, 'priv_hex': key.hex(),
                       'pw': pw_preview,
                       'plaintext': plain[:120].decode('utf-8', 'replace')}
                hits.append(hit)
                print(f'  *** HIT *** {hit}', flush=True)
                return True
        return False

    for name, key in readings(plain):
        if len(key) != 32:
            continue
        if check_one_key(key, name):
            return True
        k = int.from_bytes(key, 'big')
        if 1 <= k < N_ORDER:
            if check_one_key(((2 * k) % N_ORDER).to_bytes(32, 'big'), name + '+double'):
                return True
            if check_one_key(((k * INV2) % N_ORDER).to_bytes(32, 'big'), name + '+half'):
                return True
    if len(plain) >= 64:
        a = int.from_bytes(plain[:32], 'big')
        b = int.from_bytes(plain[-32:], 'big')
        combos = {
            'halves a+b': (a + b) % N_ORDER,
            'halves a-b': (a - b) % N_ORDER,
            'halves b-a': (b - a) % N_ORDER,
            'halves a^b': a ^ b,
            'halves 2a': (2 * a) % N_ORDER,
            'halves a/2': (a * INV2) % N_ORDER,
            'halves 2b': (2 * b) % N_ORDER,
            'halves b/2': (b * INV2) % N_ORDER,
        }
        for label, v in combos.items():
            if 1 <= v < N_ORDER:
                if check_one_key(v.to_bytes(32, 'big'), label):
                    return True
    return False

def try_password(pw: bytes, hits, long_printable, stats):
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
            check_plain(pt, bname, digest, pw_prev, hits, long_printable, stats)

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

# ---- named candidate set (see gsmg-meaning-pass.md for the evidence) ----
CANDIDATES = [
    # R1 hash-chain preimages (SalPhaseIon page directives)
    'shabefourfirsthintisyourlastcommand', 'shabefanstoo',
    # R2 Architect Choice (non-literal)
    'trinity', 'theleftdoor', 'leftdoor', 'doorleft', 'choosetrinity',
    'trinitysdoor', 'thesource', 'zion',
    # R3 Mr. Robot last scene ("Hello, Elliot.")
    'helloelliot', 'hello elliot', 'elliot', 'darlene', 'lastscene',
    'the last scene', 'eps3.4', 'eps34', 'runtimeerror', 'runtime-error',
    'mrrobot', 'mr robot', 'eps3.4_runtime-error.r00',
    # R4 Neo's passport expiry (the only date he gives away)
    '11092001', '1192001', '11-09-2001', '110901', 'september112001',
    '11september2001', '09112001', '20010911',
    # R5 "The theory of everything is a hint" (2023-01-12)
    'theoryofeverything', 'thetheoryofeverything', 'theory of everything',
    # R6 Jacque / Venus / Zeitgeist
    'venusproject', 'thevenusproject', 'resourcebasedeconomy', 'zeitgeist',
    'jacquesideas',
    # R7 his own identifiers
    'sowut', 'so wut', 'sowhat', 'bgrt', 'jrkbgrt', 'jrk bgrt',
    # R8 "Give yourself yourself..."
    'giveyourself', 'giveyourselfyourself',
    # R9 page names
    'finalstage', 'thearchitectchoice', 'architectchoice',
    # R10 other untested words from his world
    'betterhalf', 'yin yang', 'ying yang', 'dualite', 'whiterose',
    'passport', 'france', 'ibiza', 'littleones', 'obstacle',
    'geestveruimend', 'rickroll', 'freewill', 'thewarning', 'bankingwar',
    'digi', 'lockio', 'n-you',
]

# ---- self-checks ----
c1, u1 = priv_to_addrs(b'\x00' * 31 + b'\x01')
assert c1 == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH' and u1 == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
KNOWN_PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                          '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
h = hashlib.new('ripemd160', hashlib.sha256(KNOWN_PUB).digest()).digest()
assert b58check(b'\x00' + h) == TARGET
print('self-checks PASS (privkey-1 vectors + escrow pubkey -> prize address)', flush=True)

hits, long_printable = [], []
stats = {'valid_padding': 0, 'readings': 0, 'third_door': 0}
t0 = time.time()
n_forms = 0
third_hits = []

def inv_bytes(s: bytes) -> bytes:
    return bytes(int(f'{b:08b}'[::-1], 2) for b in s)

for phrase in CANDIDATES:
    # third-door check: sha256(phrase), bit-reversed sha256, phrase padded to 32
    for cand in (hashlib.sha256(phrase.encode()).digest(),
                 inv_bytes(hashlib.sha256(phrase.encode()).digest())):
        k = int.from_bytes(cand, 'big')
        if 1 <= k < N_ORDER:
            stats['third_door'] += 1
            comp, uncomp = priv_to_addrs(cand)
            if THIRD_DOOR in (comp, uncomp):
                third_hits.append({'phrase': phrase, 'priv': cand.hex()})
                print(f'  *** THIRD-DOOR HIT *** {phrase!r}', flush=True)
    if len(phrase.encode()) <= 32:
        cand = phrase.encode().ljust(32, b'\x00')
        k = int.from_bytes(cand, 'big')
        if 1 <= k < N_ORDER:
            stats['third_door'] += 1
            comp, uncomp = priv_to_addrs(cand)
            if THIRD_DOOR in (comp, uncomp):
                third_hits.append({'phrase': phrase + ' (padded)', 'priv': cand.hex()})
                print(f'  *** THIRD-DOOR HIT (padded) *** {phrase!r}', flush=True)
    for pw in crack_forms(phrase):
        n_forms += 1
        try_password(pw, hits, long_printable, stats)

el = time.time() - t0
out = {
    'candidates': len(CANDIDATES),
    'password_forms': n_forms,
    'decrypt_attempts': n_forms * 2 * 4,
    'valid_padding': stats['valid_padding'],
    'readings': stats['readings'],
    'third_door_checks': stats['third_door'],
    'third_door_hits': third_hits,
    'long_printable': long_printable,
    'hits': hits,
    'elapsed_s': round(el, 1),
}
json.dump(out, open('/home/hatch/workspace/gsmg-meaning-results.json', 'w'), indent=1)
print(f"DONE: {len(CANDIDATES)} phrases, {n_forms} password forms, "
      f"{n_forms * 2 * 4:,} decrypt attempts, valid_padding={stats['valid_padding']} "
      f"(chance ~{n_forms * 2 * 4 / 256:.1f}), readings={stats['readings']}, "
      f"third_door={stats['third_door']}, long_printable={len(long_printable)}, "
      f"hits={len(hits)}, {el:.1f}s")
