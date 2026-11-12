#!/usr/bin/env python3
"""GSMG: neighbors EC oracle + new stage values as hash-page preimages.

VERIFIED: the four neighbor addresses are 2P, P/2, P+G, P-G of the prize
public key P (04f4d1bb...33559). 2P, P+G, P-G confirmed by direct EC
computation; P/2 is the remaining address by elimination.
  2P  = 1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm
  P+G = 1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1
  P-G = 1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT
  P/2 = 16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs (by elimination)
  P   = 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe

The creator's convention (planted addresses): private key = SHA-256 of a
stage answer. So if the prize key k = SHA-256(X) for some stage answer X,
then SHA-256(X) gives P. If X is one off, SHA-256(X) gives P+G (k = s-1),
P-G (k = s+1), 2P (k = s/2) or P/2 (k = 2s). This script tests every
candidate X against all five addresses — a new, cheap, exact oracle.

Also tests the new stage values as hash-page preimages (four shapes):
  - the 149-digit string (Phase 3.2 plaintext)
  - the 91-letter phrase (whitepaper sentence, checkerboard output)
  - the Beaufort key "thematrixhasyou"
  - the raw 24 bytes of "gsmg.io/theseedisplanted" (+ zero-pad, + reversed)
"""
import base64, hashlib, re

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
TARGETS = {
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe': 'P (k)',
    '1KHMK2C8uBptRz67FbrXy43yHzhZG16Hbm': '2P (k = s/2)',
    '16eEXbSuKN8tvcos1iKjdju6dAaWWRBMEs': 'P/2 (k = 2s)',
    '1PhXF3xVQ8Sg9FomBcmRwRbvvGfm3Y2os1': 'P+G (k = s-1)',
    '1G1kRAFR68y6CUq1SAJMzHmjd6sEEgtVUT': 'P-G (k = s+1)',
}
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
print('self-checks PASS')

import base58, coincurve
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def addr_from_privkey_bytes(priv):
    pk = coincurve.PrivateKey(priv)
    pub = pk.public_key.format(compressed=False)
    h = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    return base58.b58encode_check(b'\x00' + h).decode()

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

# ---------- candidate list ----------
cands = {}
def add(s, src):
    s = str(s).strip()
    if s:
        cands.setdefault(s, src)

# stage answers (from the internal audit)
stage = [
    'causality', 'theflowerblossomsthroughwhatseemstobeaconcretesurface',
    'jacquefresco', 'giveitjustonesecond', 'heisenbergsuncertaintyprinciple',
    'theseedisplanted', 'gsmg.io/theseedisplanted',
    'ourfirsthintisyourlastcommand', 'yinyang',
    'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
    'Safenet', 'Luna', 'HSM', '11110',
    'SalPhaseIon', 'CosmicDuality', 'ALPHANOISES',
    'GSMG', 'Jrk Bgrt', 'SoWut', '@SoWut',
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa',
    '1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9', '3GSMG24TujqfMJG1kQoBX18DzJHQLeJYMK',
    'neighbors', 'half and double', 'neighborshalfanddouble',
    '227', '227 chars were correct', '227charswerecorrect',
    'thebetterhalf', 'thehalf', 'Half', 'Better Half', 'THE_HALF', 'THE_BETTER_HALF',
    'the warning', 'Logic', 'The Warning',
    'GSMG.io neighbors, half and double', 'Halving', 'Good job, Neo!',
    'GSMG.io: You are here because 227 chars were correct',
    'GSMG.io: phase3.2 pass OK', 'GSMG.io: are you sure?',
    'GSMG.io: part of the cipher', 'GSMG.io: do you beleive me you need it?',
    'GSMG.io: Right, this is causality',
    'thematrixhasyou', 'THEMATRIXHASYOU',
    '15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112',
    'commonsolutionistointroduecentralauthorityormintthatcheckseverytransactionfordoublespending',
    'the private keys belong to half and better half',
    'choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself',
    'choice is an illusion created between those with power and those without',
    'a very special dessert, i wrote it myself',
    'One for one, four for one',
    'esrever',
]
for s in stage:
    add(s, 'stage')
# kit candidate files (the generated families)
for f in ['/home/hatch/workspace/your_files/gsmg-puzzle-kit/smart_candidates.txt',
          '/home/hatch/workspace/your_files/gsmg-puzzle-kit/gen_candidates.txt',
          '/home/hatch/workspace/your_files/gsmg-puzzle-kit/candidates.txt',
          '/home/hatch/workspace/your_files/gsmg-puzzle-kit/long_ngrams.txt',
          '/home/hatch/workspace/your_files/gsmg-puzzle-kit/dbbi_faed_cands.txt']:
    try:
        for line in open(f, errors='ignore'):
            add(line.strip(), f.split('/')[-1])
    except Exception as e:
        print('  skip', f, e)
print(f'candidates: {len(cands)}')

# ---------- Part 1: hash-page preimages (four shapes) for the new values ----------
new_vals = {
    '149-digit': '15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112',
    '91-letter': 'commonsolutionistointroduecentralauthorityormintthatcheckseverytransactionfordoublespending',
    'beaufort-key': 'thematrixhasyou',
}
# raw 24 bytes of gsmg.io/theseedisplanted, zero-padded left to 32 bytes, + reversed
raw24 = b'gsmg.io/theseedisplanted'
assert len(raw24) == 24
padded = b'\x00' * 8 + raw24
reversed_bits = bytes(int('{:08b}'.format(b)[::-1], 2) for b in raw24[::-1])
hits = []
tested_text = set()
tested_bytes = set()
def check_text(c, label):
    if c in tested_text or not c:
        return
    tested_text.add(c)
    h1 = hashlib.sha256(c.encode()).hexdigest()
    if h1 in REMAINING:
        hits.append((label, c, h1, 'shape1-pure-text'))
    h2 = hashlib.sha256(c.encode().hex().encode()).hexdigest()
    if h2 in REMAINING:
        hits.append((label, c, h2, 'shape2-hex-text'))
def check_bytes(raw, label):
    if raw in tested_bytes:
        return
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits.append((label, raw[:60].decode(errors='ignore'), h, 'shape3-raw-bytes'))
for label, s in new_vals.items():
    c = clean(s)
    check_text(c, label)
    check_text('humph' + c, label + '+humph')
    check_bytes(s.encode(), label)
for label, b in [('seed24-padded', padded), ('seed24-reversed', reversed_bits),
                 ('seed24-raw', raw24)]:
    check_bytes(b, label)
    check_text(b.hex(), label + '-hex')
print(f'Part 1 (new values as preimages): {len(tested_text)} text, {len(tested_bytes)} bytes')
print('  hits:', hits if hits else 'none')

# ---------- Part 2: neighbors EC oracle ----------
# For each candidate X: s = SHA-256(X) as a scalar; also try s = SHA-256(raw bytes)
# and s = the raw bytes themselves when X is a hex string. Compute s*G address
# and compare against the five target addresses.
oracle_hits = []
tested = 0
for s, src in sorted(cands.items()):
    # form A: SHA-256 of the text
    for priv, form in [(hashlib.sha256(s.encode()).digest(), 'sha256(text)')]:
        if priv == b'\x00' * 32:
            continue
        try:
            addr = addr_from_privkey_bytes(priv)
        except Exception:
            continue
        tested += 1
        if addr in TARGETS:
            oracle_hits.append((s, src, form, addr, TARGETS[addr], priv.hex()))
    # form B: if the candidate is a 64-hex string, use its raw bytes as the key
    if re.fullmatch(r'[0-9a-f]{64}', s.lower()):
        try:
            addr = addr_from_privkey_bytes(bytes.fromhex(s.lower()))
        except Exception:
            continue
        tested += 1
        if addr in TARGETS:
            oracle_hits.append((s, src, 'raw-bytes', addr, TARGETS[addr], s.lower()))
print(f'Part 2 (neighbors oracle): {tested} scalar tests over {len(cands)} candidates')
if oracle_hits:
    print('ORACLE HITS:')
    for s, src, form, addr, meaning, priv in oracle_hits:
        print(f'  X={s[:80]!r} [{src}] form={form} -> {addr} = {meaning} ; priv={priv}')
else:
    print('  0 oracle hits — no candidate is the prize key or one of its neighbours')
print('DONE: remaining six still unknown:', sorted(h[:8] for h in REMAINING))
