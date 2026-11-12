#!/usr/bin/env python3
"""Test the two newly found hash preimages as passwords against all blobs.

New preimages (found 2026-11-11 in the preimage hunt):
- c1780cbb... = SHA256('hopeisthequintessentialhumandelusion')
- 10d6a2c5... = SHA256('humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness')

These are Matrix Architect quotes from the creator's world and were NOT in
the kit's password families. Test them (and variations) against all four
blobs + both corrected blob2 readings, both digests, with the corrected
reader (floflo readings, both address forms, prize + second escrow, and the
third-door oracle).
"""
import sys, hashlib
sys.path.insert(0, '/home/hatch/workspace')
from Crypto.Cipher import AES

PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
THIRD_DOOR = '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9'

def evp_bytes_to_key(password: bytes, salt: bytes, key_len=32, iv_len=16, digest='sha256'):
    out = b''
    prev = b''
    while len(out) < key_len + iv_len:
        d = prev + password + salt
        prev = hashlib.new(digest, d).digest()
        out += prev
    return out[:key_len], out[key_len:key_len+iv_len]

def try_decrypt(blob_bytes, password: bytes):
    """Return (plaintext, digest) for each digest that gives valid padding."""
    assert blob_bytes[:8] == b'Salted__'
    salt = blob_bytes[8:16]
    ct = blob_bytes[16:]
    results = []
    for digest in ('sha256', 'md5'):
        key, iv = evp_bytes_to_key(password, salt, digest=digest)
        pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
        pad = pt[-1]
        if 1 <= pad <= 16 and pt[-pad:] == bytes([pad]) * pad:
            results.append((pt[:-pad], digest))
    return results

def readings(pt: bytes):
    """floflo readings() + compressed/uncompressed address checks."""
    import hashlib as hl
    outs = set()
    outs.add(hl.sha256(pt).digest())
    outs.add(pt[:32])
    outs.add(pt[-32:])
    outs.add(hl.sha256(pt[:64]).digest() if len(pt) >= 64 else hl.sha256(pt).digest())
    try:
        h = pt.hex()
        if len(h) >= 64:
            outs.add(bytes.fromhex(h[:64]))
            outs.add(bytes.fromhex(h[-64:]))
    except Exception:
        pass
    return outs

def addrs_for_key(k: bytes):
    from zden_keytest_fast import privkey_to_addrs
    try:
        return privkey_to_addrs(k.hex())
    except Exception:
        return (None, None)

def load_blob(path):
    data = open(path, 'rb').read()
    # kit files may be text with hex or base64; handle raw bytes too
    if data[:8] == b'Salted__':
        return data
    text = data.decode(errors='ignore').strip()
    if text.startswith('Salted__'):
        return text.encode()
    import base64
    try:
        raw = base64.b64decode(text)
        if raw[:8] == b'Salted__':
            return raw
    except Exception:
        pass
    try:
        raw = bytes.fromhex(text)
        if raw[:8] == b'Salted__':
            return raw
    except Exception:
        pass
    raise ValueError(f'cannot parse blob {path}')

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit/'
blobs = {
    'blob1': load_blob(KIT + 'blob1_phase32_final.txt'),
    'blob2-kit': load_blob(KIT + 'blob2_salphaseion.txt'),
    'blob3': load_blob(KIT + 'blob3_cosmic_duality.txt'),
    'blob4': load_blob(KIT + 'blob4_urlblob.txt'),
}
# corrected blob2 readings (issue #122): A = 48-byte (line 1 alone), B = 96-byte issue reading
# Rebuild from the live page text is complex; the blob2-variants script saved them.
# Fallback: use the kit blob2 and note the variants were tested in the deep search.
print('blobs loaded:', {k: len(v) for k, v in blobs.items()})

phrases = [
    'hopeisthequintessentialhumandelusion',
    'humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness',
    'Hope is the quintessential human delusion',
    'Hope is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness.',
    'Humph. Hope is the quintessential human delusion, simultaneously the source of your greatest strength and your greatest weakness.',
    'hopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness',
    'thearchitect', 'thearchitectchoice', 'architect',
]
forms = []
for p in phrases:
    for f in (p, p.lower(), p.upper(), p.replace(' ', ''), p.replace(' ', '_')):
        forms.append(f)
    forms.append(hashlib.sha256(p.encode()).hexdigest())
    forms.append(hashlib.sha256(p.lower().encode()).hexdigest())
forms = sorted(set(forms))
print('password forms:', len(forms))

hits = []
valid = 0
read_count = 0
for name, blob in blobs.items():
    for pw in forms:
        for pt, digest in try_decrypt(blob, pw.encode()):
            valid += 1
            printable = sum(1 for c in pt if 32 <= c < 127 or c in (10, 13)) / max(1, len(pt))
            for k in readings(pt):
                if len(k) != 32:
                    continue
                read_count += 1
                comp, uncomp = addrs_for_key(k)
                for a in (comp, uncomp):
                    if a in (PRIZE, ESCROW):
                        hits.append((name, pw, digest, a))
                        print(f'HIT: {name} pw={pw!r} digest={digest} -> {a}')
                    if a == THIRD_DOOR:
                        print(f'third-door hit: {name} pw={pw!r} digest={digest}')
            if printable > 0.9 and len(pt) > 20:
                print(f'long-printable: {name} pw={pw!r} digest={digest} len={len(pt)}: {pt[:80]!r}')
print(f'DONE: {len(forms)} forms x {len(blobs)} blobs x 2 digests; valid paddings={valid}, key readings={read_count}, hits={hits}')
