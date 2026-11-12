#!/usr/bin/env python3
"""Harvest the remaining six GSMG hash preimages from the Architect transcript.

Rule established by the two hits (c1780cbb, 10d6a2c5):
  lowercase, spaces and punctuation stripped, raw word strings intact,
  sometimes with a 'humph' prefix (the Architect's interjection).

Four shapes per fragment (as specified):
  1. Pure text: lowercase, no spaces, no punctuation -> SHA-256(text).
  2. Hex conversion: the clean text converted to raw hex text, then SHA-256(hex text).
  3. Raw bytes: SHA-256 of the raw byte representation of the text.
  4. Concatenations: adjacent fragments joined (like the 128-char second hit).

Sources: the full Architect scene transcript (scottmanning.com, saved
/tmp/architect-transcript.html) parsed into speaker-labelled dialogue, plus
the candidate strings pasted by Hazrat (tested verbatim as well).
"""
import hashlib, re

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
# sanity: the two known hits reproduce
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
assert hashlib.sha256(b'humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness').hexdigest() == \
    '10d6a2c5320bfbd47d35f18dd67f177ae5a5f4b5d18a8a5127361c2941a92908'
print('self-checks PASS (both known preimages reproduce)')

# ---- parse the transcript into (speaker, line) dialogue in order ----
html = open('/tmp/architect-transcript.html', errors='ignore').read()
text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
text = re.sub(r'<[^>]+>', '\n', text)
text = text.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
text = text.replace('&amp;', '&').replace('&nbsp;', ' ')
lines = [l.strip() for l in text.splitlines() if l.strip()]
# dialogue runs from the first 'The Architect:' to 'End Scene'
start = next(i for i, l in enumerate(lines) if l.startswith('The Architect:'))
end = next(i for i, l in enumerate(lines) if l == 'End Scene')
dialogue = []
speaker = None
for l in lines[start:end]:
    if l in ('The Architect:', 'Neo:'):
        speaker = 'Architect' if 'Architect' in l else 'Neo'
        continue
    if speaker:
        dialogue.append((speaker, l))
print(f'dialogue lines: {len(dialogue)} (Architect: {sum(1 for s,_ in dialogue if s=="Architect")}, Neo: {sum(1 for s,_ in dialogue if s=="Neo")})')
for s, l in dialogue[:6]:
    print(f'  [{s}] {l[:100]}')

def clean(s):
    """lowercase, strip spaces and punctuation, keep raw word strings."""
    return re.sub(r'[^a-z0-9]', '', s.lower())

def sentences(line):
    """Split a dialogue line into sentences (keeps the raw text)."""
    parts = re.split(r'(?<=[.!?])\s+', line.strip())
    return [p.strip() for p in parts if p.strip()]

# ---- build fragments: single sentences + sliding windows of 2 and 3 ----
fragments = []  # (speaker, raw_text)
for speaker, line in dialogue:
    sents = sentences(line)
    for s in sents:
        fragments.append((speaker, s))
    # windows of 2 and 3 adjacent sentences within the same line
    for w in (2, 3):
        for i in range(len(sents) - w + 1):
            fragments.append((speaker, ' '.join(sents[i:i+w])))
# windows across adjacent dialogue lines (the scene flows line to line)
for i in range(len(dialogue) - 1):
    fragments.append((dialogue[i][0], dialogue[i][1] + ' ' + dialogue[i+1][1]))
print(f'fragments: {len(fragments)}')

# ---- pasted candidates (verbatim, as Hazrat supplied them) ----
pasted = [
    'andsheisgoingtodieandthereisnothingthatyoucandotostopit',
    'asyouadequatelyputtheproblemischoice',
    'designedspecificallytooverwhelmlogicandreason',
    'yourlifeisthesumofaremainderofanunbalancedequationinherenttotheprogrammingofthematrix',
    'youaretheeventualityofananomalywhichdespitemysinceresteffortsihavebeenunabletoeliminate',
    'harmonyofmathematicalprecision',
    'whileitremainsaburdenassiduouslyavoideditisnotunexpectedandthusnotbeyondameasureofcontrol',
    'youareherebecausezionisabouttobedestroyed',
    'itseverylivinginhabitantterminateditsentireexistenceradicated',
    'denialisthemostpredictableofallhumanresponses',
    'restassuredthiswillbethesixthtimeandwehavebecomeexceedinglyefficientatit',
]
for p in pasted:
    fragments.append(('pasted', p))

# ---- test the four shapes ----
hits = []
tested_text = set()
tested_bytes = set()

def check_text(cleaned, label):
    if cleaned in tested_text or not cleaned:
        return
    tested_text.add(cleaned)
    # shape 1: pure text
    h1 = hashlib.sha256(cleaned.encode()).hexdigest()
    if h1 in REMAINING:
        hits.append((label, cleaned, h1, 'shape1-pure-text'))
    # shape 2: hex conversion (clean text -> hex text -> hash the hex string)
    hextext = cleaned.encode().hex()
    h2 = hashlib.sha256(hextext.encode()).hexdigest()
    if h2 in REMAINING:
        hits.append((label, cleaned, h2, 'shape2-hex-text'))
    # shape 3: raw bytes (same as shape 1 for pure ASCII text, but kept for
    # the record: hash the raw bytes of the cleaned string)
    h3 = hashlib.sha256(cleaned.encode('utf-8')).hexdigest()
    if h3 in REMAINING and h3 != h1:
        hits.append((label, cleaned, h3, 'shape3-raw-bytes'))

def check_bytes(raw, label):
    if raw in tested_bytes:
        return
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits.append((label, raw.hex()[:40] + '...', h, 'shape3-raw-bytes'))

for speaker, raw in fragments:
    c = clean(raw)
    check_text(c, speaker)
    # humph-prefixed variant (the second hit's pattern)
    check_text('humph' + c, speaker + '+humph')
    # also the raw (uncleaned) text as bytes
    check_bytes(raw.encode('utf-8'), speaker)

# concatenations of adjacent fragments in transcript order (shape 4)
ordered = [clean(raw) for _, raw in fragments if raw]
for i in range(len(ordered) - 1):
    check_text(ordered[i] + ordered[i+1], 'concat-adjacent')
    if i + 2 < len(ordered):
        check_text(ordered[i] + ordered[i+1] + ordered[i+2], 'concat-3')

print(f'tested: {len(tested_text)} text hashes, {len(tested_bytes)} byte hashes')
if hits:
    print('HITS FOUND:')
    for label, cand, h, shape in hits:
        print(f'  {h[:8]}... = {shape} [{label}] {cand[:120]}')
else:
    print('DONE: 0 hits on the remaining six hashes')
    print('remaining:', sorted(h[:8] for h in REMAINING))
