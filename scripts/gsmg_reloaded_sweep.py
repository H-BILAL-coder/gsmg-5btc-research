#!/usr/bin/env python3
"""GSMG remaining-six preimage hunt: FULL Matrix Reloaded script sweep.

The creator's verified 2020 OP_RETURNs quote Reloaded beyond the Architect
scene ("Right, this is causality" = Merovingian; "do you beleive me you need
it?" ~ Morpheus). So the remaining six may be Merovingian / Morpheus / Oracle
lines from anywhere in Reloaded, not just the two scenes already harvested.

Sources: StockQ full Reloaded script (subtitle-style, no speaker labels) +
DocLecture Reloaded script (second source for the same film).
Plus the targeted lines from the paste (Merovingian causality block, Morpheus
"Do you believe" lines, Trainman / Rama-Kandra karma lines from Revolutions,
already covered by the StockQ Revolutions harvest — re-tested here verbatim).
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

def stockq_lines(path):
    html = open(path, errors='ignore').read()
    text = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.S)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '\n', text)
    return [l.strip() for l in text.splitlines() if l.strip() and len(l.strip()) >= 3]

dialogue = []
for path in ['/tmp/stockq-reloaded.html', '/tmp/doclecture-reloaded.html']:
    lines = stockq_lines(path)
    print(f'{path.split("/")[-1]}: {len(lines)} lines')
    dialogue += [('reloaded', l) for l in lines]

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def sentences(line):
    parts = re.split(r'(?<=[.!?])\s+', line.strip())
    return [p.strip() for p in parts if p.strip()]

fragments = []
for _, line in dialogue:
    sents = sentences(line)
    for s in sents:
        fragments.append(s)
    for w in (2, 3):
        for i in range(len(sents) - w + 1):
            fragments.append(' '.join(sents[i:i+w]))
for i in range(len(dialogue) - 1):
    fragments.append(dialogue[i][1] + ' ' + dialogue[i+1][1])
    if i + 2 < len(dialogue):
        fragments.append(dialogue[i][1] + ' ' + dialogue[i+1][1] + ' ' + dialogue[i+2][1])

# targeted lines from the paste, verbatim + cleaned variants
targeted = [
    'Right, this is causality',
    'Causality. There is no escape from it.',
    'Choice is an illusion, created between those with power and those without.',
    'Do you believe that my being stronger or faster has anything to do with my muscles in this place?',
    "You're here because you know something. What you know you can't explain, but you feel it.",
    'You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.',
    'Karma is a word. Like love. A way of saying what I mean.',
    'Every life that is born into this world comes with a purpose.',
    'What is the purpose of life? To end.',
    'I love my wife and my daughter.',
    'There is no spoon.',
    'Free your mind.',
    'The Matrix has you.',
    'Follow the white rabbit.',
    'Knock, knock, Neo.',
    'Wake up, Neo.',
    'do you beleive me you need it',
    'Do you beleive me you need it?',
    'do you believe me you need it',
    'You are here because 227 chars were correct',
    'GSMG.io neighbors, half and double',
]
for t in targeted:
    fragments.append(t)

print(f'fragments: {len(fragments)}')

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

for raw in fragments:
    c = clean(raw)
    check_text(c, 'reloaded')
    check_text('humph' + c, 'reloaded+humph')
    check_bytes(raw.encode('utf-8'), 'reloaded')
ordered = [clean(f) for f in fragments]
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
