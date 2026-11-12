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


# ================= NOTES + COSMIC DUALITY BOOK test (2026-11-11) =================
# Candidates are ONLY specific phrases supported by (a) the Cosmic Duality book
# itself (title, series, essay/chapter titles, opening line) and (b) the
# 2026-07-16 transcript thread (Anderson's youmeandself URL guesses).
# The NOTES phrases themselves (NOTE/NOTES/many NOTES/Give yourself...) were
# already tested by the repo's v61 audit (264 trials, 0 matches) and are NOT
# re-tested here.
import time
t0 = time.time()
CANDIDATES = [
    # --- Cosmic Duality book (Time-Life, 1991), verified MD5 c94862274a5616cc0ecf78b82ced757c ---
    ("book-title", "cosmicduality"),
    ("book-series", "mysteriesoftheunknown"),
    ("essay-unity-of-opposites", "theunityofopposites"),
    ("essay-unity-of-opposites-short", "unityofopposites"),
    ("ch1-dualities-as-old-as-time", "dualitiesasoldastime"),
    ("essay-dark-side-of-fairy-tales", "thedarksideoffairytales"),
    ("ch2-battle-of-the-sexes", "thebattleofthesexes"),
    ("essay-driving-the-devil-out", "drivingthedevilout"),
    ("ch3-grasp-of-ageless-evil", "inthegraspofagelessevil"),
    ("essay-paths-of-righteousness", "pathsofrighteousness"),
    ("ch4-triumph-of-good", "thetriumphofgood"),
    ("essay-hark-heavens-winged-host", "harkheavenswingedhost"),
    ("book-opening-genesis", "inthebeginninggodcreatedtheheavenandtheearth"),
    # --- 2026-07-16 transcript: Anderson's URL guesses from "Give yourself..." ---
    ("transcript-youmeandself", "youmeandself"),
    ("transcript-youmeiandself", "youmeiandself"),
    ("transcript-youmeisandself", "youmeisandself"),
    ("transcript-youmeizandself", "youmeizandself"),
]
# self-checks (same as esrever script)
c1, u1 = priv_to_addrs(b'\x00' * 31 + b'\x01')
assert c1 == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH' and u1 == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
KNOWN_PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                          '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
h = hashlib.new('ripemd160', hashlib.sha256(KNOWN_PUB).digest()).digest()
assert b58check(b'\x00' + h) == TARGET
print('self-checks PASS', flush=True)
n_forms = 0
for label, phrase in CANDIDATES:
    forms = crack_forms(phrase)
    n_forms += len(forms)
    print(f'{label}: {phrase!r} ({len(forms)} forms)', flush=True)
    for pw in forms:
        try_password(pw)
    third_door_check(phrase)
el = time.time() - t0
rec = {'candidates': [{'label': l, 'phrase': p} for l, p in CANDIDATES],
       'counts': {'phrases': len(CANDIDATES), 'password_forms': n_forms,
                  'valid_padding': stats['valid_padding'],
                  'key_readings': stats['readings'],
                  'third_door_checks': stats['third_door'],
                  'hits': len(hits), 'long_printable': len(long_printable),
                  'third_door_hits': len(hits_third), 'seconds': round(el, 1)},
       'hits': hits, 'hits_third': hits_third, 'long_printable': long_printable}
json.dump(rec, open('/home/hatch/workspace/gsmg-notes-cosmic-results.json', 'w'), indent=1)
print(f"\nDONE in {el:.1f}s: {len(CANDIDATES)} phrases, {n_forms} password forms, "
      f"valid-padding={stats['valid_padding']}, readings={stats['readings']}, "
      f"third_door={stats['third_door']}, HITS={len(hits)}, "
      f"LONG-PRINTABLE={len(long_printable)}, THIRD-DOOR-HITS={len(hits_third)}", flush=True)
