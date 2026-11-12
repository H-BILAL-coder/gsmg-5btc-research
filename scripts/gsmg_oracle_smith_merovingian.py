#!/usr/bin/env python3
"""Harvest the remaining six GSMG hash preimages from Oracle / Smith /
Merovingian dialogue.

Same rule as the two hits (c1780cbb, 10d6a2c5): lowercase, spaces and
punctuation stripped, raw word strings intact, sometimes with a 'humph'
prefix. Four shapes per fragment: (1) pure text, (2) hex text, (3) raw
bytes, (4) concatenations of adjacent fragments.

Sources (all fetched 2026-11-11):
- scottmanning.com Merovingian restaurant transcript (Reloaded)
- scottmanning.com Neo-Oracle transcript (Reloaded bench scene)
- scottmanning.com Smith interrogates Morpheus transcript (film 1)
- scottmanning.com The Matrix Revolutions page (Smith rain battle)
- IMSDb The Matrix (1999) full script (Oracle kitchen scene, Smith)
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
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
assert hashlib.sha256(b'humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness').hexdigest() == \
    '10d6a2c5320bfbd47d35f18dd67f177ae5a5f4b5d18a8a5127361c2941a92908'
print('self-checks PASS')

def html_to_lines(path):
    html = open(path, errors='ignore').read()
    text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = (text.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
                .replace('&amp;', '&').replace('&nbsp;', ' ').replace('&#8211;', '-')
                .replace('&#8212;', '-').replace('&quot;', '"').replace('&#39;', "'"))
    return [l.strip() for l in text.splitlines() if l.strip()]

def parse_scottmanning(path, speakers):
    """Speaker labels are 'Name:' on their own line; dialogue follows.
    Labels may be multi-word ('Agent Smith:')."""
    lines = html_to_lines(path)
    out = []
    speaker = None
    for l in lines:
        if re.match(r'^[A-Z][A-Za-z ]+:$', l) and l[:-1] in speakers:
            speaker = l[:-1]
            continue
        if l in ('End Scene', 'Further Reading'):
            break
        if speaker:
            out.append((speaker, l))
    return out

def parse_imsdb(path):
    """Screenplay format: ALL-CAPS character name line, then dialogue lines."""
    lines = html_to_lines(path)
    names = {'ORACLE', 'NEO', 'MORPHEUS', 'SMITH', 'AGENT SMITH', 'TRINITY',
             'CYPHER', 'TANK', 'DOZER', 'APOC', 'SWITCH', 'MOUSE', 'RHINEHEART'}
    out = []
    speaker = None
    for l in lines:
        if l in names:
            speaker = l.title()
            continue
        if re.match(r'^(INT\.|EXT\.|CUT TO|FADE|DISSOLVE)', l):
            speaker = None
            continue
        if speaker and len(l) > 2 and not l.startswith('('):
            # skip stage directions in parens and page numbers
            if re.match(r'^\d+\.$', l):
                continue
            out.append((speaker, l))
    return out

dialogue = []
for path, speakers in [
    ('/tmp/merovingian-transcript.html', {'Merovingian', 'Neo', 'Morpheus', 'Persephone', 'Trinity'}),
    ('/tmp/neo-oracle-matrix-reloaded-transcript.html', {'Oracle', 'Neo', 'Architect', 'Seraph', 'Sati'}),
    ('/tmp/smith-interrogates-morpheus-transcript.html', {'Smith', 'Morpheus', 'Neo', 'Agent Smith', 'Agent Brown', 'Agent Jones'}),
    ('/tmp/the-matrix-revolutions.html', {'Smith', 'Neo', 'Oracle', 'Architect'}),
]:
    got = parse_scottmanning(path, speakers)
    print(f'{path.split("/")[-1]}: {len(got)} lines')
    dialogue += got

ims = parse_imsdb('/tmp/matrix1999-imsdb.html')
print(f'imsdb1999: {len(ims)} lines')
# keep only the Oracle kitchen + Smith scenes from the 1999 script (the whole
# script is parsed; it is all in-scope dialogue)
dialogue += ims

def parse_stockq(path):
    """Subtitle-style script: spoken lines separated by <br>, no speaker
    labels. Return each line as a fragment with speaker 'stockq'."""
    html = open(path, errors='ignore').read()
    text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '\n', text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # drop obvious navigation / metadata lines
    out = []
    for l in lines:
        if len(l) < 3:
            continue
        if l.lower().startswith(('matrix revolutions', 'the matrix', 'movie script',
                                 'home', 'search', 'copyright', 'all rights')):
            continue
        out.append(('stockq', l))
    return out

# Revolutions rain battle: StockQ full script (subtitle-style, no labels)
rev = parse_stockq('/tmp/stockq-revolutions.html')
print(f'stockq-revolutions: {len(rev)} lines')
dialogue += rev

from collections import Counter
print('total dialogue lines:', len(dialogue), Counter(s for s, _ in dialogue))

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def sentences(line):
    parts = re.split(r'(?<=[.!?])\s+', line.strip())
    return [p.strip() for p in parts if p.strip()]

fragments = []
for speaker, line in dialogue:
    sents = sentences(line)
    for s in sents:
        fragments.append((speaker, s))
    for w in (2, 3):
        for i in range(len(sents) - w + 1):
            fragments.append((speaker, ' '.join(sents[i:i+w])))
for i in range(len(dialogue) - 1):
    fragments.append((dialogue[i][0], dialogue[i][1] + ' ' + dialogue[i+1][1]))
print(f'fragments: {len(fragments)}')

# the paste's key lines, verbatim (some already tested in earlier hunts, but
# re-tested here in all four shapes for completeness)
pasted = [
    'You have already made the choice, now you have to understand it',
    'youvealreadymadethechoicenowyouhavetounderstandit',
    'causalitythereisnoescapefromit',
    'Causality, there is no escape from it.',
    'choiceisanillusioncreatedbetweenthosewithpowerandthosewithout',
    'why mr anderson why do you persist',
    'Why, Mr. Anderson? Why do you persist?',
    'itsthesmell',
    "It's the smell, if there is such a thing.",
    'human beings are a disease a cancer of this planet',
    'you are a plague and we are the cure',
    'freedomisadelusion',
    'cookiesneedlovelikeeverythingdoes',
    'no one can see beyond a choice they dont understand',
    'temetnosce',
    'knowyourself',
]
for p in pasted:
    fragments.append(('pasted', p))

hits = []
tested_text = set()
tested_bytes = set()

def check_text(cleaned, label):
    if cleaned in tested_text or not cleaned:
        return
    tested_text.add(cleaned)
    h1 = hashlib.sha256(cleaned.encode()).hexdigest()
    if h1 in REMAINING:
        hits.append((label, cleaned, h1, 'shape1-pure-text'))
    h2 = hashlib.sha256(cleaned.encode().hex().encode()).hexdigest()
    if h2 in REMAINING:
        hits.append((label, cleaned, h2, 'shape2-hex-text'))

def check_bytes(raw, label):
    if raw in tested_bytes:
        return
    tested_bytes.add(raw)
    h = hashlib.sha256(raw).hexdigest()
    if h in REMAINING:
        hits.append((label, raw[:60].decode(errors='ignore'), h, 'shape3-raw-bytes'))

for speaker, raw in fragments:
    c = clean(raw)
    check_text(c, speaker)
    check_text('humph' + c, speaker + '+humph')
    check_bytes(raw.encode('utf-8'), speaker)

ordered = [clean(raw) for _, raw in fragments if raw]
for i in range(len(ordered) - 1):
    check_text(ordered[i] + ordered[i+1], 'concat-adjacent')
    if i + 2 < len(ordered):
        check_text(ordered[i] + ordered[i+1] + ordered[i+2], 'concat-3')

print(f'tested: {len(tested_text)} text hashes, {len(tested_bytes)} byte hashes')
if hits:
    print('HITS FOUND:')
    for label, cand, h, shape in hits:
        print(f'  {h[:8]}... = {shape} [{label}] {cand[:140]}')
else:
    print('DONE: 0 hits on the remaining six hashes')
    print('remaining:', sorted(h[:8] for h in REMAINING))
