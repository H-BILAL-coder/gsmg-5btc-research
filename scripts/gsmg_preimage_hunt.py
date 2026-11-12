#!/usr/bin/env python3
"""Resolve the 8 unknown GSMG hash preimages (Part 2 of the pasted claims).

The paste claims the 8 unknown preimages are "variations, concatenated
strings, or hidden attributes directly embedded in the source formatting of
the very first landing page or the original Decentraland audio spectrogram
artifacts."

Method: gather candidate strings from those exact sources, generate
variations (case, spacing, reversal, pairwise concatenations, common
affixes), SHA-256 each, and compare against the 8 unknown hashes.

Sources:
- live gsmg.io homepage source (/tmp/gsmg_home.html)
- archived phase1verification.html (apple-repo/fresh-start/archives/)
- Decentraland audit JSON (apple-repo/.../decentraland_audio_audit.json)
- naddiseo decentraland.ipynb
- the known base set (stage answers, page names, known preimages)
"""
import hashlib, json, re, os, itertools

UNKNOWN = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '10d6a2c5320bfbd47d35f18dd67f177ae5a5f4b5d18a8a5127361c2941a92908',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
# sanity: known preimages hash to the known pages
KNOWN_TEXT = {
    'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe':
        '89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32',
    'ourfirsthintisyourlastcommand':
        'e24bd2c0fd454632f9fdd26cbdc210597f79e9fca9719c126a6d30cb41ef0238',
}
# f9719d6d... is SHA-256 of the RAW 32 BYTES of the SalPhaseIon hash, not of
# its hex text (correction to the meaning-pass wording, verified just now).
KNOWN_BYTES = {
    bytes.fromhex('89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32'):
        'f9719d6d531e6c3b5129644cd05da57bc6fdd075c9a61267c41d4b9627936096',
}
for s, h in KNOWN_TEXT.items():
    assert hashlib.sha256(s.encode()).hexdigest() == h, f'self-check failed for {s[:20]}'
for b, h in KNOWN_BYTES.items():
    assert hashlib.sha256(b).hexdigest() == h, 'self-check failed for raw hash bytes'
print('self-checks PASS (3 known preimages reproduce their pages)')

def extract_strings(path):
    """Extract candidate strings from a file: quoted strings, attribute
    values, visible text, comments, bare words of length>=3."""
    try:
        text = open(path, errors='ignore').read()
    except Exception as e:
        print(f'  skip {path}: {e}')
        return set()
    out = set()
    # quoted strings (single/double)
    for m in re.finditer(r'''["']([^"']{3,200})["']''', text):
        out.add(m.group(1))
    # HTML comments
    for m in re.finditer(r'<!--(.*?)-->', text, re.S):
        out.add(m.group(1).strip())
    # attribute values
    for m in re.finditer(r'''(?:href|src|content|id|class|name|title|alt|value|data-[a-z-]+)\s*=\s*["']([^"']{2,200})["']''', text):
        out.add(m.group(1))
    # visible text: strip tags, split into lines
    stripped = re.sub(r'<[^>]+>', ' ', text)
    stripped = re.sub(r'[{}();,]', ' ', stripped)
    for line in stripped.splitlines():
        line = line.strip()
        if 3 <= len(line) <= 200:
            out.add(line)
    # bare tokens (urls, hashes, ids)
    for m in re.finditer(r'[A-Za-z0-9_\-./]{4,200}', text):
        t = m.group(0)
        if any(c.isalpha() for c in t):
            out.add(t)
    return {s for s in out if s and not s.isspace()}

cands = set()
sources = [
    '/tmp/gsmg_home.html',
    '/home/hatch/workspace/apple-repo/fresh-start/archives/phase1verification.html',
    '/home/hatch/workspace/apple-repo/gsmgio-5btc-puzzle-master/decentraland_audio_audit.json',
    '/home/hatch/workspace/naddiseo-repo/decentraland.ipynb',
]
for src in sources:
    got = extract_strings(src)
    print(f'{src}: {len(got)} candidate strings')
    cands |= got

# base set: known strings, stage answers, page names, clue words
base = [
    'GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe',
    'ourfirsthintisyourlastcommand', 'shabefourfirsthintisyourlastcommand',
    'shabefanstoo', 'HASHTHETEXT', 'hashthetext',
    'theflowerblossomsthroughwhatseemstobeaconcretesurface',
    'causality', 'Safenet', 'Luna', 'HSM', '11110',
    'jacquefresco', 'giveitjustonesecond', 'heisenbergsuncertaintyprinciple',
    'matrixsumlist', 'lastwordsbeforearchichoice', 'thispassword', 'enter',
    'yourlastcommand', 'secondanswer',
    'TheArchitectChoice', 'final_stage', 'banking-war', 'merovingian',
    'eps3.4_runtime-error.r00', 'followthewhiterabbit', 'lock-io', 'n-you',
    'hopeisthequintessentialhumandelusion', 'digitallogiccryptography',
    'cryptogic', 'door.png', 'theseedisplanted', 'phase1verification',
    'yinyang', 'yingyang', 'thearchitectchoice', 'finalstage',
    '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe', '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa',
    'QmRK2YoLei9wrxLvHUKisywobxEvczTicXepPxKLKzN51v',
    'QmeRy5MjmEZ2W6J3DwhQfht5HKBKXBFpoGzSkzmjeGKiDK',
    'QmdESuCguQMVXRKYwcXRJLdNcEcfi3ZXxTGPLEE3NC8czC',
    'QmcoAs6kCXynZksyNDB7RTgVYfTkxyrLb8nEU2RJepbhoE',
    '-41,-17', '-41 -17', '41,-17',
    'puzzlepiece.mp3', 'sounds/puzzlepiece.mp3', 'GSMG.io Puzzle piece',
    'ef17a96dce37b4dd7cbf79f210c5cbaf37fcae60e5faf8004de4e0832bd0dfee',
    '2c2897dc3168dd6ea3e87c56584f8b7743dae967702357d8c3f19a8647a7d29d',
]
cands |= set(base)
print('total base candidates:', len(cands))

def variations(s):
    yield s
    yield s.lower()
    yield s.upper()
    yield s.replace(' ', '')
    yield s.replace(' ', '_')
    yield s.replace('-', '')
    yield s[::-1]
    yield s.strip()
    for aff in ('gsmg', 'GSMG', 'gsmg.io', 'GSMG.IO', 'gsmgio', '5btc', '5BTC'):
        yield aff + s
        yield s + aff
        yield aff + '/' + s
        yield aff + '-' + s

# single-string variations
tested = set()
hits = []
def check(s):
    if s in tested or not s:
        return
    tested.add(s)
    h = hashlib.sha256(s.encode()).hexdigest()
    if h in UNKNOWN:
        hits.append((s, h))
        print(f'  HIT: {s!r} -> {h}')

for c in list(cands):
    for v in variations(c):
        check(v)
print(f'after single-string variations: {len(tested)} hashes, hits={len(hits)}')

# pairwise concatenations of the most salient strings (bounded)
salient = [c for c in cands if 3 <= len(c) <= 60 and re.search(r'[a-zA-Z]', c)]
salient = sorted(set(salient))[:400]
print(f'pairwise concatenations over {len(salient)} salient strings...')
for a, b in itertools.permutations(salient, 2):
    for sep in ('', '-', '_', '/', ' '):
        check(a + sep + b)
print(f'after pairwise: {len(tested)} hashes total, hits={len(hits)}')

# also: concatenations of the 4 known-preimage strings with each other and with base
known_strs = list(KNOWN_TEXT.keys())
for a in known_strs:
    for b in base:
        check(a + b)
        check(b + a)
print(f'after known-string combos: {len(tested)} hashes total, hits={len(hits)}')

# byte-string candidates: raw bytes of known hashes, the blobs, the 128-byte
# base64 path (the 4th identified preimage was raw bytes, not text, so the
# unknown ones may be too).
import base64
byte_cands = []
for h in ['89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32',
          '4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081',
          'e24bd2c0fd454632f9fdd26cbdc210597f79e9fca9719c126a6d30cb41ef0238']:
    byte_cands.append(bytes.fromhex(h))
byte_cands.append(base64.urlsafe_b64decode(
    'k27RwIKbkYlwcerFhyUy_SpThDLmjxDDiAOBzqhbtFEj-0lg4HVQhrMqtPLWD0pE8_e7gplJIe87L7znhl6n-fW2RAMPY4jreE9rWxsp2AYJxBL6H9P9ARWZ9uUnXR9jVYOnV4L9MrUnhCGJ5D1GcpCh2V9b7UWfx1XDY2TZ0hs='))
for blob in ['blob1_phase32_final.txt', 'blob2_salphaseion.txt',
            'blob3_cosmic_duality.txt', 'blob4_urlblob.txt']:
    try:
        byte_cands.append(open('/home/hatch/workspace/your_files/gsmg-puzzle-kit/' + blob, 'rb').read())
    except Exception as e:
        print('  skip blob', blob, e)
byte_hits = 0
for b in byte_cands:
    h = hashlib.sha256(b).hexdigest()
    if h in UNKNOWN:
        print(f'  BYTE HIT: {len(b)} bytes -> {h}')
        byte_hits += 1
    # also SHA-256 of the hex encoding of the bytes
    h2 = hashlib.sha256(b.hex().encode()).hexdigest()
    if h2 in UNKNOWN:
        print(f'  BYTE-HEX HIT: {len(b)} bytes -> {h2}')
        byte_hits += 1
print(f'after byte candidates: {len(tested)} text hashes + {len(byte_cands)} byte hashes, hits={len(hits) + byte_hits}')

if hits:
    print('HITS FOUND:')
    for s, h in hits:
        print(f'  {h[:8]}... = SHA256({s!r})')
else:
    print('DONE: 0 matches across', len(tested), 'candidate hashes vs 8 unknown pages')
    print('remaining unknown:', sorted(h[:8] for h in UNKNOWN))
