#!/usr/bin/env python3
"""GSMG — audit saved decrypted outputs with the CORRECTED key reader
(2026-11-11). Pasted-ChatGPT plan step 1: re-examine previously
decrypted outputs using the corrected reader.

The corrected reader (floflo777 open-crypto-puzzles tools/oracle.py,
readings(), verified 2026-10-18 in that repo) accepts as a candidate key:
  sha256(plaintext), first32, last32, sha256(first64),
  64/128-char hex -> 32 bytes (and first/last 32 of 64-byte hex),
  WIF-shaped Base58Check tokens.
It does NOT judge a plaintext by how printable it looks. The kit's old
reader required >=90% printable (crack.py) / >=0.5 (screens), so any
correct password yielding raw key material was silently rejected.

Inputs (saved outputs only — no new brute force):
  big_hits.txt (242 lines, plaintext TRUNCATED to first 60 bytes by the
      screen that wrote it — noted per line), smart_screen_blob1.txt (1),
      smart_screen_blob2.txt (9).
For every plaintext we run all readings, derive BOTH compressed and
uncompressed Legacy P2PKH addresses, and compare to the prize address
1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe (and, secondarily, to the split-off
17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa). We also flag entirely-printable
plaintexts over 64 bytes (floflo tested.md open follow-up: a wrong
password gives that with probability ~(95/256)^64, so it is near-certain
evidence of the right password even with no address match).

Self-checks (must all PASS before any result is trusted):
  privkey-1 -> 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH (comp) /
              1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm (uncomp)
  the escrow's known on-chain pubkey (floflo oracle.py) hashes to the
  prize address.
"""
import ast, base64, hashlib, json, sys

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
KNOWN_PUBKEY_HEX = ('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                    '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')

try:
    from coincurve import PrivateKey as CCPriv
    def priv_to_addrs(priv: bytes):
        pk = CCPriv(priv)
        pub_c = pk.public_key.format(compressed=True)
        pub_u = pk.public_key.format(compressed=False)
        out = []
        for pub in (pub_c, pub_u):
            h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
            out.append(base58_b58check(b'\x00' + h))
        return out[0], out[1]
    FAST = True
except Exception as e:
    FAST = False
    print('coincurve unavailable:', e); sys.exit(1)

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def base58_b58check(payload: bytes) -> str:
    h = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    data = payload + h
    n = int.from_bytes(data, 'big')
    s = ''
    while n > 0:
        n, r = divmod(n, 58)
        s = B58[r] + s
    return '1' * (len(data) - len(data.lstrip(b'\x00'))) + s

def b58decode_check(s: str):
    import base58 as b58lib
    return b58lib.b58decode_check(s)

# ---- self-checks ----
print('self-checks:')
c1, u1 = priv_to_addrs(b'\x00' * 31 + b'\x01')
assert c1 == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH', c1
assert u1 == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', u1
print('  privkey-1 vectors: PASS')
pub = bytes.fromhex(KNOWN_PUBKEY_HEX)
h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
assert base58_b58check(b'\x00' + h) == TARGET
print('  known on-chain escrow pubkey -> prize address: PASS')

def readings(plain: bytes):
    """floflo oracle.py readings(), verbatim logic."""
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
            raw = b58decode_check(token.decode('ascii'))
            if raw[:1] == b'\x80' and len(raw) in (33, 34):
                out.append(('wif', raw[1:33]))
        except Exception:
            pass
    return out

def parse_line(line, fname):
    """big_hits: score \\t blob \\t pw_repr \\t pt_repr.
    smart_screen_*: score \\t pw_repr \\t pt_repr (blob from filename)."""
    parts = line.rstrip('\n').split('\t')
    if len(parts) == 4:
        blob = parts[1]
        pw_part, pt_part = parts[2], parts[3]
    elif len(parts) == 3:
        blob = 'blob1' if 'blob1' in fname else 'blob2'
        pw_part, pt_part = parts[1], parts[2]
    else:
        return None
    try:
        score = float(parts[0])
    except ValueError:
        return None
    try:
        pw = ast.literal_eval(pw_part)
    except Exception:
        pw = pw_part  # smart files store the password bare, unquoted
    try:
        pt = ast.literal_eval(pt_part)
    except Exception:
        return None
    if isinstance(pw, str):
        pw = pw.encode()
    if not isinstance(pt, (bytes, bytearray)):
        return None
    return score, blob, pw, bytes(pt)

results = []
long_printable = []
n_lines = n_readings = 0
hits = []
for fname in ('big_hits.txt', 'smart_screen_blob1.txt', 'smart_screen_blob2.txt'):
    for line in open(f'{KIT}/{fname}', encoding='utf-8', errors='replace'):
        parsed = parse_line(line, fname)
        if parsed is None:
            continue
        score, blob, pw, pt = parsed
        n_lines += 1
        # flag: entirely printable over 64+ bytes (near-certain right password)
        if len(pt) >= 64 and all(32 <= b < 127 or b in (10, 13, 9) for b in pt):
            long_printable.append((fname, blob, len(pt), pt[:120]))
        for name, key in readings(pt):
            if len(key) != 32:
                continue
            n_readings += 1
            try:
                comp, uncomp = priv_to_addrs(key)
            except Exception:
                continue
            for addr, form in ((comp, 'compressed'), (uncomp, 'uncompressed')):
                if addr in (TARGET, SECOND):
                    hits.append({'file': fname, 'blob': blob, 'score': score,
                                 'reading': name, 'form': form, 'address': addr,
                                 'priv_hex': key.hex(),
                                 'plaintext_preview': pt[:80].decode('utf-8', 'replace'),
                                 'password_preview': pw[:80].decode('utf-8', 'replace')})
                    print(f'  *** HIT *** {fname} {blob} {name} {form} {addr}')

print(f'\nlines audited: {n_lines} | key readings tested: {n_readings} | '
      f'address matches: {len(hits)}')
print(f'long entirely-printable plaintexts (>=64 bytes): {len(long_printable)}')
for fname, blob, ln, prev in long_printable:
    print(f'  LONG-PRINTABLE {fname} {blob} len={ln}: {prev!r}')
if not hits and not long_printable:
    print('No candidate key matches the prize (or split-off) address, and no '
          'long printable plaintext was found. The saved outputs contain no '
          'missed key under the corrected reader.')

json.dump({'lines': n_lines, 'readings': n_readings, 'hits': hits,
           'long_printable': [(f, b, ln, p.decode('utf-8', 'replace'))
                              for f, b, ln, p in long_printable]},
          open('/home/hatch/workspace/gsmg-audit-outputs.json', 'w'), indent=2)
print('record: gsmg-audit-outputs.json')
