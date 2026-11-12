#!/usr/bin/env python3
"""GSMG remaining-six preimage hunt: Phases 1-3 (on-chain, audio, manifestos).

Phase 1: OP_RETURN / scriptSig / witness ASCII from the prize address's 129
  transactions (mempool.space, saved /tmp/gsmg_prize_txs.json). The pushed
  data is parsed properly (OP_RETURN opcode + push-length skipped), so the
  spurious 'j' (0x6a) and length-byte prefixes are removed.
Phase 2: Decentraland audio metadata — ID3/encoder strings from puzzlepiece.mp3
  (both copies), channel_difference.wav header strings, and PNG text chunks
  from the spectrogram images.
Phase 3: Non-dialogue text from the IMSDb Matrix (1999) script (opening trace
  program, on-screen text, scene descriptions) + the recoverable text of the
  archived What Is The Matrix site (Flash/image-based; almost no text).

All candidates are tested in the four shapes (pure text, hex text, raw bytes,
adjacent concatenations) + 'humph' prefix against the six remaining hashes.
"""
import hashlib, json, re, struct

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
assert hashlib.sha256(b'humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness').hexdigest() == \
    '10d6a2c5320bfbd47d35f18dd67f177ae5a5f4b5d18a8a5127361c2941a92908'
print('self-checks PASS')

cands = {}  # string -> source label

def add(s, src):
    s = s.strip()
    if len(s) >= 3 and len(s) <= 300:
        cands.setdefault(s, src)

# ---------- Phase 1: OP_RETURN data, parsed properly ----------
data = json.load(open('/tmp/gsmg_prize_txs.json'))
def parse_push(script_hex):
    """Parse a script; return the list of pushed data blobs."""
    try:
        b = bytes.fromhex(script_hex)
    except Exception:
        return []
    out = []
    i = 0
    while i < len(b):
        op = b[i]
        i += 1
        if op == 0x6a:  # OP_RETURN
            continue
        if 0x01 <= op <= 0x4b:
            n = op
        elif op == 0x4c and i < len(b):
            n = b[i]; i += 1
        elif op == 0x4d and i + 1 < len(b):
            n = struct.unpack('<H', b[i:i+2])[0]; i += 2
        elif op == 0x4e and i + 3 < len(b):
            n = struct.unpack('<I', b[i:i+4])[0]; i += 4
        else:
            continue
        if i + n <= len(b):
            out.append(b[i:i+n])
            i += n
        else:
            break
    return out

op_n = 0
for txid, sp in data['opreturns']:
    for blob in parse_push(sp):
        try:
            txt = blob.decode('utf-8')
        except Exception:
            continue
        if all(32 <= c < 127 or c in (10, 13) for c in blob):
            add(txt, f'opreturn:{txid[:8]}')
            op_n += 1
print(f'Phase 1: {len(data["opreturns"])} OP_RETURN outputs -> {op_n} text payloads')
# also the other ASCII strings found in scriptsig/witness (already decoded)
for s in data['strings']:
    add(s, 'tx-ascii')

# ---------- Phase 2: audio metadata ----------
def strings_in_file(path, minlen=4):
    raw = open(path, 'rb').read()
    out, cur = [], bytearray()
    for byte in raw:
        if 32 <= byte < 127:
            cur.append(byte)
        else:
            if len(cur) >= minlen:
                out.append(bytes(cur).decode())
            cur = bytearray()
    if len(cur) >= minlen:
        out.append(bytes(cur).decode())
    return out

audio_files = [
    '/home/hatch/workspace/naddiseo-repo/decentraland-assets/puzzlepiece.mp3',
    '/home/hatch/workspace/apple-repo/gsmgio-5btc-puzzle-master/artifacts/audio_audit/channel_difference.wav',
]
for f in audio_files:
    for s in strings_in_file(f):
        # keep only human-plausible strings (letters, not binary noise)
        if re.search(r'[A-Za-z]{3,}', s) and len(s) <= 120:
            add(s, 'audio:' + f.split('/')[-1])
print(f'Phase 2: audio strings collected (total candidates so far: {len(cands)})')

def png_text_chunks(path):
    """Return tEXt/iTXt/zTXt chunk contents from a PNG."""
    raw = open(path, 'rb').read()
    out = []
    i = 8
    while i + 8 <= len(raw):
        length = struct.unpack('>I', raw[i:i+4])[0]
        ctype = raw[i+4:i+8].decode('latin1', errors='ignore')
        chunk = raw[i+8:i+8+length]
        if ctype in ('tEXt', 'iTXt', 'zTXt'):
            out.append(chunk.decode('latin1', errors='ignore'))
        i += 12 + length
    return out

import glob
for png in glob.glob('/home/hatch/workspace/apple-repo/gsmgio-5btc-puzzle-master/artifacts/audio_audit/*.png'):
    for s in png_text_chunks(png):
        add(s, 'png:' + png.split('/')[-1])
print(f'Phase 2 done (total candidates: {len(cands)})')

# ---------- Phase 3: non-dialogue text from the IMSDb 1999 script ----------
lines = []
html = open('/tmp/matrix1999-imsdb.html', errors='ignore').read()
text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
text = re.sub(r'<[^>]+>', '\n', text)
raw_lines = [l.strip() for l in text.splitlines() if l.strip()]
names = {'ORACLE', 'NEO', 'MORPHEUS', 'SMITH', 'AGENT SMITH', 'TRINITY',
         'CYPHER', 'TANK', 'DOZER', 'APOC', 'SWITCH', 'MOUSE', 'RHINEHEART'}
speaker = None
for l in raw_lines:
    if l in names:
        speaker = l
        continue
    if re.match(r'^(INT\.|EXT\.|CUT TO|FADE|DISSOLVE)', l):
        speaker = None
        lines.append(('scene', l))
        continue
    if speaker is None:
        # non-dialogue: scene description / on-screen text / trace output
        lines.append(('nondialogue', l))
for _, l in lines:
    add(l, 'imsdb-nondialogue')
print(f'Phase 3: {len(lines)} non-dialogue lines from IMSDb 1999 script')
# What Is The Matrix site recoverable text
for s in ['MATRIX', 'The Matrix', 'regular', 'enhanced', 'getflash', 'short',
          'community', 'soundtrack', 'red pill', 'blue pill', 'Red Pill',
          'Blue Pill', 'Follow the white rabbit', 'Knock, knock, Neo',
          'Wake up, Neo', 'The Matrix has you']:
    add(s, 'whatisthematrix')
print(f'total candidates: {len(cands)}')

# ---------- hash runner: four shapes + humph + concatenations ----------
def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

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

ordered = []
for s, src in sorted(cands.items()):
    c = clean(s)
    check_text(c, src)
    check_text('humph' + c, src + '+humph')
    check_bytes(s.encode('utf-8'), src)
    ordered.append(c)
for i in range(len(ordered) - 1):
    check_text(ordered[i] + ordered[i+1], 'concat-adjacent')

print(f'tested: {len(tested_text)} text hashes, {len(tested_bytes)} byte hashes')
if hits:
    print('HITS FOUND:')
    for label, cand, h, shape in hits:
        print(f'  {h[:8]}... = {shape} [{label}] {cand[:140]}')
else:
    print('DONE: 0 hits on the remaining six hashes')
    print('remaining:', sorted(h[:8] for h in REMAINING))
# show the most interesting Phase 1 strings for the record
print('--- notable OP_RETURN payloads (first 40):')
shown = 0
for txid, sp in data['opreturns']:
    for blob in parse_push(sp):
        try:
            txt = blob.decode('utf-8')
        except Exception:
            continue
        if all(32 <= c < 127 for c in blob) and len(txt) >= 4:
            print(f'  {txid[:10]}: {txt[:100]}')
            shown += 1
            if shown >= 40:
                break
    if shown >= 40:
        break
