#!/usr/bin/env python3
"""GSMG — corrected-oracle re-run of the kit's candidate families (2026-11-11).
Re-runs every candidate family the kit already tried, but with the two
holes fixed (per floflo777 open-crypto-puzzles, verified 2026-07-28 /
2026-10-18 in that repo):
  1. BOTH digests: the kit's screens used SHA-256 EVP_BytesToKey only.
     The small blobs' digest is unknown (try both); Cosmic Duality uses
     MD5 (verified against its published plaintext hash in that repo).
  2. CORRECTED reader: the kit required >=90% (crack.py) / >=0.5
     (screens) printable text, silently rejecting raw key material.
     Here a valid-padding decryption is reduced with floflo's readings()
     (sha256, first32, last32, sha256(first64), hex, WIF) and compared
     by ADDRESS (compressed + uncompressed, prize + split-off), never
     by how printable it looks. Entirely-printable plaintexts >64 bytes
     are also flagged (near-certain right password per that repo).
Candidate families (NO new brute-force spaces — re-run only):
  A. stored files: candidates.txt, smart_candidates.txt,
     gen_candidates.txt, long_ngrams.txt, dbbi_faed_cands.txt,
     with crack.py's password forms (as-is, lower, spaceless, sha256-hex).
  B. big_combine stream (2,332,800): YB x ML x YY x LW x 24 orders x
     5 seps x 3 forms, reproduced exactly from the kit's big_combine.py.
  C. wave2 stream (400,920): CORE x numbers x pre/post, from wave2.py.
Blobs: blob1, blob2 (80 bytes), blob3 Cosmic Duality (1328 bytes).
Padding is pre-checked on the last block only (exact for CBC), so blob3
costs the same per attempt as the small blobs; full decrypt runs only
on valid padding.
Bonus (cheap, exact offline oracle from floflo leads.md #1): the
unmessaged planted address 1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9 is
checked against sha256(X), bit-reversed sha256(X), and X padded to
32 bytes for every stored candidate X.
Progress is printed and logged; hits go to gsmg-rerun-hits.json.
"""
import base64, hashlib, itertools, json, sys, time

KIT = '/home/hatch/workspace/your_files/gsmg-puzzle-kit'
TARGET = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
SECOND = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
THIRD_DOOR = '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9'
LOG = '/home/hatch/workspace/gsmg-rerun.log'
HITS_JSON = '/home/hatch/workspace/gsmg-rerun-hits.json'

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
    return out  # (compressed, uncompressed)

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

N_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
INV2 = (N_ORDER + 1) // 2  # modular inverse of 2 mod n

def check_plain(plain, blob, digest, pw_preview, hits, long_printable, stats):
    stats['valid_padding'] += 1
    if len(plain) >= 64 and all(32 <= b < 127 or b in (10, 13, 9) for b in plain):
        long_printable.append({'blob': blob, 'digest': digest,
                               'pw': pw_preview, 'len': len(plain),
                               'text': plain[:200].decode('utf-8', 'replace')})
        print(f'  LONG-PRINTABLE {blob}/{digest} pw={pw_preview!r} len={len(plain)}', flush=True)

    def check_one_key(key: bytes, label: str):
        """Check one 32-byte key (both address forms, prize + split-off)."""
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
        # "neighbors, half and double" (creator's 2021-07-18 transaction pays
        # the addresses of 2P and P/2 of the prize key): if a reading yields a
        # key that is half or double the prize key, catch it here.
        k = int.from_bytes(key, 'big')
        if 1 <= k < N_ORDER:
            if check_one_key(((2 * k) % N_ORDER).to_bytes(32, 'big'), name + '+double'):
                return True
            if check_one_key(((k * INV2) % N_ORDER).to_bytes(32, 'big'), name + '+half'):
                return True
    # Split-key combinations: if the plaintext holds two 32-byte halves
    # ("the private keys belong to half and better half"), the prize key may
    # be their sum, difference, XOR, double or half.
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
    """Try one password (bytes) against all blobs x both digests."""
    pw_prev = pw[:60].decode('utf-8', 'replace')
    for digest in ('sha256', 'md5'):
        for bname, (salt, ct) in BLOBS.items():
            key, iv = evp(pw, salt, digest)
            # exact CBC padding pre-check on the last block only
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

# ---- resume support (after a machine replacement kills the run) ----
# --skip-a: skip stream A + third-door (already done in a killed run)
# --resume-b N: skip the first N passwords of stream B (already tried)
# --hits-file F: write the JSON record to F instead of the default
import sys as _sys
SKIP_A = '--skip-a' in _sys.argv
RESUME_B = 0
HITS_FILE = HITS_JSON
for _i, _a in enumerate(_sys.argv):
    if _a == '--resume-b' and _i + 1 < len(_sys.argv):
        RESUME_B = int(_sys.argv[_i + 1])
    if _a == '--hits-file' and _i + 1 < len(_sys.argv):
        HITS_FILE = _sys.argv[_i + 1]
if SKIP_A or RESUME_B:
    print(f'resume mode: SKIP_A={SKIP_A} RESUME_B={RESUME_B} HITS_FILE={HITS_FILE}', flush=True)

# ---- self-checks ----
c1, u1 = priv_to_addrs(b'\x00' * 31 + b'\x01')
assert c1 == '1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH' and u1 == '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm'
KNOWN_PUB = bytes.fromhex('04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464'
                          '9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559')
h = hashlib.new('ripemd160', hashlib.sha256(KNOWN_PUB).digest()).digest()
assert b58check(b'\x00' + h) == TARGET
print('self-checks PASS (privkey-1 vectors + escrow pubkey -> prize address)', flush=True)

hits, long_printable = [], []
stats = {'valid_padding': 0, 'readings': 0}
t0 = time.time()
n_pw = 0

def log_progress(tag):
    el = time.time() - t0
    print(f'  [{tag}] {n_pw:,} passwords, {el:.0f}s, '
          f'{n_pw/max(el,1):,.0f}/s, valid-padding={stats["valid_padding"]}, '
          f'readings={stats["readings"]}, hits={len(hits)}', flush=True)

# ---- Stream A: stored candidate files ----
stored = []
for fn in ('candidates.txt', 'smart_candidates.txt', 'gen_candidates.txt',
           'long_ngrams.txt', 'dbbi_faed_cands.txt'):
    for line in open(f'{KIT}/{fn}', encoding='utf-8', errors='replace'):
        line = line.strip()
        if line and not line.startswith('#'):
            stored.append(line)
stored = list(dict.fromkeys(stored))
if SKIP_A:
    stored = []  # resume: stream A + third-door already done in the killed run
print(f'stream A: {len(stored):,} unique stored phrases', flush=True)
for phrase in stored:
    for pw in crack_forms(phrase):
        try_password(pw, hits, long_printable, stats)
        n_pw += 1
    if n_pw % 100000 < 10:
        log_progress('A')
log_progress('A done')

# ---- third-door bonus check (stored candidates only) ----
td_hits = 0
for phrase in stored:
    for cand in (hashlib.sha256(phrase.encode()).digest(),
                 hashlib.sha256(phrase.encode()).digest()[::-1]):
        try:
            comp, uncomp = priv_to_addrs(cand)
        except Exception:
            continue
        if THIRD_DOOR in (comp, uncomp):
            td_hits += 1
            print(f'  *** THIRD-DOOR HIT *** phrase={phrase!r} priv={cand.hex()}', flush=True)
    if len(phrase.encode()) <= 32:
        padded = phrase.encode().ljust(32, b'\x00')
        try:
            comp, uncomp = priv_to_addrs(padded)
            if THIRD_DOOR in (comp, uncomp):
                td_hits += 1
                print(f'  *** THIRD-DOOR HIT (padded) *** phrase={phrase!r}', flush=True)
        except Exception:
            pass
print(f'third-door check done: {td_hits} hits', flush=True)

# ---- Stream B: big_combine stream ----
def inv_bytes(s: str) -> bytes:
    b = s.encode()
    return bytes(int(f'{x:08b}'[::-1], 2) for x in b)[::-1]
ROWS = '610876654997879'; COLS = '8108108736759668'
YB = ['2347', '2357', 'yellowblueprimes', '23711131723', '519',
      '23711131723519', '51923711131723', '237519', 'yellowblue',
      'blueyellowprimes', 'yellow_blue_primes', 'yblueprimes']
ML = [ROWS + COLS, COLS + ROWS, 'matrixsumlist',
      (ROWS + COLS)[::-1], ROWS, COLS,
      '61,08,76,65,49,97,87,9', '81,08,10,87,36,75,96,68',
      '6108766549978798108108736759668'[::-1][:20]]
YY = ['95101', '10195', '9510110195', '1019595101', 'yinyang', 'yingyang',
      'ying_yang', 'halfandbetterhalf', 'cosmicduality', 'bellaciao']
LW = ['lastwordsbeforearchichoice', 'ivebeenwaitingforyou',
      'raisingthestakeswithoutextrachancesofwinning', 'oneforonefourforone',
      'youremainirrevocablyhuman', 'wakeupyou']
SEPS = ['', '+', '_', ' ', '.']
ORDERS = list(itertools.permutations([0, 1, 2, 3]))
def gen_big():
    for yb, ml, yy, lw in itertools.product(YB, ML, YY, LW):
        ing = (yb, ml, yy, lw)
        for order in ORDERS:
            parts = [ing[i] for i in order]
            for sep in SEPS:
                j = sep.join(parts)
                jb = j.encode()
                yield jb
                yield hashlib.sha256(jb).hexdigest().encode()
                yield inv_bytes(j)
print('stream B: big_combine (2,332,800) starting', flush=True)
for i_b, pw in enumerate(gen_big()):
    if i_b < RESUME_B:
        continue  # resume: already tried in the killed run
    try_password(pw, hits, long_printable, stats)
    n_pw += 1
    if n_pw % 250000 == 0:
        log_progress('B')
log_progress('B done')

# ---- Stream C: wave2 stream ----
CORE = ['yellowblueprimes', 'matrixsumlist', 'yinyang', 'yingyang',
        'lastwordsbeforearchichoice', '2347', '95101', '10195',
        'wewontgiveawaythepassword', 'itsinfrontofyoureyesbutyourenotseeingit',
        'verylaststepisatruegiveaway', 'promised', 'enterthispassword',
        'salvation', 'thematrixhasyou', 'gsmg', 'cosmicduality',
        '6108766549978798108108736759668', 'halfandbetterhalf', 'bellaciao']
NUMS = [str(i) for i in range(10000)] + [str(y) for y in range(2009, 2027)] + ['140', '101', '95', '7', '23']
print('stream C: wave2 (400,920) starting', flush=True)
for c in CORE:
    cb = c.encode()
    for num in NUMS:
        nb = num.encode()
        for pw in (cb + nb, nb + cb):
            try_password(pw, hits, long_printable, stats)
            n_pw += 1
    log_progress('C')
log_progress('C done')

print(f'\nDONE: {n_pw:,} passwords in {time.time()-t0:.0f}s | '
      f'valid-padding plaintexts: {stats["valid_padding"]} | '
      f'key readings: {stats["readings"]} | hits: {len(hits)} | '
      f'third-door hits: {td_hits} | long-printable: {len(long_printable)}', flush=True)
json.dump({'passwords': n_pw, 'valid_padding': stats['valid_padding'],
           'readings': stats['readings'], 'hits': hits,
           'third_door_hits': td_hits, 'long_printable': long_printable},
          open(HITS_FILE, 'w'), indent=2)
print('record:', HITS_FILE, flush=True)
