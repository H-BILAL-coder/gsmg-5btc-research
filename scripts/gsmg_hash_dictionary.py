#!/usr/bin/env python3
"""GSMG item 2 — cryptographic preimage checks on the six remaining hash pages.

Builds COMBINATIONS not previously tested. Singles and same-source adjacent
concatenations are already covered (Architect harvest: 200 fragments, 4 shapes;
Oracle/Smith/Merovingian: 10,050 fragments; trilogy: 9,939 fragments;
close reading: 84; cover audit: 68; footprint: 22; floflo rows 18-19:
substrings + third-door constructions). This script combines ACROSS domains:
  A: Architect scene phrases (verified film dialogue)
  B: internal puzzle terminology (stage names, keys, riddle answers)
  C: 1991 Time-Life Cosmic Duality metadata (ISBNs, chapter titles, series)
  D: creator's own phrases (verified Telegram / footprint)
Ordered pairs A x B, A x C, A x D, B x C, B x D, C x D, B x B, C x C
(A x A excluded — adjacent concatenations covered by the Architect harvest)
with separators {"", "-", "_", " "}, plus B x B x B triples ("" separator).
Shapes per combination: pure text, hex text, raw bytes, "humph" prefix,
and sha256(ripemd160(x)) chained. RIPEMD-160 alone is 40 hex and cannot
equal a 64-hex SHA-256 page hash; it is computed and reported as
not-applicable, and only the chained form is compared.
"""
import hashlib, itertools, json, re

REMAINING = {
    '0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32',
    '21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f',
    '673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d',
    'a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1',
    'aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a',
    'c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625',
}
# self-checks: both known preimages reproduce
assert hashlib.sha256(b'hopeisthequintessentialhumandelusion').hexdigest() == \
    'c1780cbbaa105784949cd6a2924e1f51a947b4258a0655defd0cd2e6f6544046'
assert hashlib.sha256(b'humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness').hexdigest() == \
    '10d6a2c5320bfbd47d35f18dd67f177ae5a5f4b5d18a8a5127361c2941a92908'
print('self-checks PASS: both known preimages reproduce')

def clean(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

# (cleaned, original) pairs; original keeps spaces/punctuation for the raw-bytes shape
A = [
    ('helloneo', 'Hello, Neo.'),
    ('iamthearchitecticreatedthematrix', 'I am the Architect. I created the Matrix.'),
    ('youaretheeventualityofanomaly', 'You are the eventuality of an anomaly.'),
    ('theproblemischoice', 'The problem is choice.'),
    ('itwasdesignedspecificallytooverwhelmlogicandreason', 'It was designed specifically to overwhelm logic and reason.'),
    ('thiswillbethesixthtimewehavedestroyedit', 'This will be the sixth time we have destroyed it.'),
    ('thefunctionoftheoneisnowtoreturntothesource', 'The function of the One is now to return to the Source.'),
    ('therearetwodoors', 'There are two doors.'),
    ('thedoortoyourrightleadstothesourceandthesalvationofzion', 'The door to your right leads to the Source, and the salvation of Zion.'),
    ('thedoortoyourleftleadsbacktothematrix', 'The door to your left leads back to the Matrix.'),
    ('failuretocomplywiththisprocesswillresultinacataclysmicsystemcrash', 'Failure to comply with this process will result in a cataclysmic system crash.'),
    ('afterwhichyouwillberequiredtoselectfromthematrix23individuals16female7male', 'After which, you will be required to select from the Matrix 23 individuals, 16 female, 7 male.'),
    ('hopeisthequintessentialhumandelusion', 'Hope, it is the quintessential human delusion.'),
    ('hopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness', 'Hope, it is the quintessential human delusion, simultaneously the source of your greatest strength, and your greatest weakness.'),
    ('thematrixisolderthanyouknow', 'The Matrix is older than you know.'),
    ('therearelevelsofsurvivalwearepreparedtoaccept', 'There are levels of survival we are prepared to accept.'),
    ('ifiamthefatherofthematrixshewouldundoubtedlybeitsmother', 'If I am the father of the Matrix, she would undoubtedly be its mother.'),
    ('theanomalyissystemiccreatingfluctuationsineventhemostsimplisticequations', 'The anomaly is systemic, creating fluctuations in even the most simplistic equations.'),
    ('whileitremainsaburdenassiduouslyavoideditisnotunexpected', 'While it remains a burden assiduously avoided, it is not unexpected.'),
    ('whichbringsusatlasttothemomentoftruth', 'Which brings us at last to the moment of truth.'),
    ('oneoftheseliveshasafuturetheotherdoesnot', 'One of these lives has a future, the other does not.'),
    ('wewont', "We won't."),
    ('please', 'Please.'),
    ('concordantly', 'Concordantly.'),
    ('ergo', 'Ergo.'),
    ('thesource', 'The Source.'),
    ('zion', 'Zion.'),
    ('theone', 'The One.'),
    ('anomaly', 'Anomaly.'),
]
B = [
    ('yinyang', 'yinyang'), ('yingyang', 'yingyang'), ('dualite', 'Dualite'),
    ('cosmicduality', 'Cosmic Duality'), ('salphaseion', 'SalPhaseIon'),
    ('thematrixhasyou', 'thematrixhasyou'), ('causality', 'causality'),
    ('jacquefresco', 'jacquefresco'), ('giveitjustonesecond', 'giveitjustonesecond'),
    ('heisenbergsuncertaintyprinciple', 'heisenbergsuncertaintyprinciple'),
    ('theseedisplanted', 'theseedisplanted'),
    ('theflowerblossomsthroughwhatseemstobeaconcretesurface', 'theflowerblossomsthroughwhatseemstobeaconcretesurface'),
    ('whiterabbit', 'white rabbit'), ('whiterabbitseverywhere', 'White Rabbits everywhere'),
    ('gsmgiomagicpuzzlepiece', 'gsmg.io magic puzzle piece'),
    ('half', 'half'), ('betterhalf', 'better half'), ('neighbors', 'neighbors'),
    ('phase32', 'phase 3.2'), ('phase3', 'phase 3'),
    ('matrixsumlist', 'matrixsumlist'), ('lastwordsbeforearchichoice', 'lastwordsbeforearchichoice'),
    ('ourfirsthintisyourlastcommand', 'ourfirsthintisyourlastcommand'),
    ('227', '227'), ('149', '149'), ('91', '91'),
]
C = [
    ('0809465167', '0-8094-6516-7'), ('0809465175', '0-8094-6517-5'),
    ('mysteriesoftheunknown', 'Mysteries of the Unknown'),
    ('timelifebooks', 'Time-Life Books'),
    ('theunityofopposites', 'The Unity of Opposites'),
    ('dualitiesasoldastime', 'Dualities As Old As Time'),
    ('thedarksideoffairytales', 'The Dark Side of Fairy Tales'),
    ('thebattleofthesexes', 'The Battle of the Sexes'),
    ('drivingthedevilout', 'Driving the Devil Out'),
    ('graspofagelessevil', 'Grasp of Ageless Evil'),
    ('pathsofrighteousness', 'Paths of Righteousness'),
    ('thetriumphofgood', 'The Triumph of Good'),
    ('harkheavenswingedhost', "Hark! Heaven's Winged Host"),
    ('1991', '1991'), ('1993', '1993'),
    ('bfi999c6975', 'BFI999C6975'), ('alexandriavirginia', 'Alexandria, Virginia'),
]
D = [
    ('makethebestofeverything', 'Make the best of everything.'),
    ('giveyourselfyourselfandyourselfwillbegivenyourself', 'Give yourself yourself and yourself will be given yourself.'),
    ('geestveruimend', 'geestveruimend'),
    ('latetly', 'Latetly, I\'m working with many NOTES.'),
    ('myclosefriendshavethebestchance', 'My close friends have the best chance.'),
    ('nevergonnagiveyouup', 'Never gonna give you up.'),
    ('freewill', 'free will'), ('nohintsonlyfreewill', 'No hints, only free will.'),
    ('hiddenlaptop', 'hidden laptop'),
    ('ihaveahiddenlaptopwhichihaventtouchedinyears', "I have a hidden laptop which I haven't touched in years."),
    ('somealreadyfoundit', 'Some already found it.'),
    ('the5btcwasnevertheactualprize', 'The "5" btc was never the actual prize.'),
    ('ifyouguysgot1microstepfurther', 'If you guys got 1 microstep further.'),
    ('areyoureallylookingforjustthebtc', 'Are you really looking for just the btc?'),
    ('itismeanttobesolved', 'It is meant to be solved.'),
    ('whenyingyangisreached2hoursmax', 'when yingyang is reached, 2 hours max'),
]

# ---- build combinations ----
combos = set()  # (cleaned_joined, raw_joined, label)
SEPS = ['', '-', '_', ' ']
def add_pair(s1, s2, label):
    for sep in SEPS:
        combos.add((s1[0] + sep + s2[0], s1[1] + sep + s2[1], label))

for s1, s2, label in (
    [(a, b, 'AxB') for a in A for b in B] +
    [(a, c, 'AxC') for a in A for c in C] +
    [(a, d, 'AxD') for a in A for d in D] +
    [(b, c, 'BxC') for b in B for c in C] +
    [(b, d, 'BxD') for b in B for d in D] +
    [(c, d, 'CxD') for c in C for d in D] +
    [(b1, b2, 'BxB') for b1 in B for b2 in B if b1 is not b2] +
    [(c1, c2, 'CxC') for c1 in C for c2 in C if c1 is not c2]):
    add_pair(s1, s2, label)
# triples B x B x B, '' separator only
for b1, b2, b3 in itertools.permutations(B, 3):
    combos.add((b1[0] + b2[0] + b3[0], b1[1] + b2[1] + b3[1], 'BxBxB'))

print(f'combinations: {len(combos)}')
from collections import Counter
print('  by class:', dict(Counter(l for _, _, l in combos)))

# ---- test shapes ----
hits = []
n_text = n_hex = n_bytes = n_humph = n_chain = 0
for cleaned, raw, label in sorted(combos):
    # 1. pure text
    h = hashlib.sha256(cleaned.encode()).hexdigest()
    n_text += 1
    if h in REMAINING:
        hits.append((cleaned, h, 'pure-text', label))
    # 2. hex text
    h = hashlib.sha256(cleaned.encode().hex().encode()).hexdigest()
    n_hex += 1
    if h in REMAINING:
        hits.append((cleaned, h, 'hex-text', label))
    # 3. raw bytes (original spacing/punctuation)
    h = hashlib.sha256(raw.encode()).hexdigest()
    n_bytes += 1
    if h in REMAINING:
        hits.append((raw, h, 'raw-bytes', label))
    # 4. humph prefix
    h = hashlib.sha256(('humph' + cleaned).encode()).hexdigest()
    n_humph += 1
    if h in REMAINING:
        hits.append((cleaned, h, 'humph-prefix', label))
    # 5. chained: sha256(ripemd160(cleaned))
    r = hashlib.new('ripemd160', cleaned.encode()).digest()
    h = hashlib.sha256(r).hexdigest()
    n_chain += 1
    if h in REMAINING:
        hits.append((cleaned, h, 'sha256(ripemd160)', label))

total = n_text + n_hex + n_bytes + n_humph + n_chain
print(f'hashes computed: text={n_text} hex={n_hex} bytes={n_bytes} humph={n_humph} chained={n_chain} total={total}')
print(f'RIPEMD-160 alone: 40 hex, cannot equal a 64-hex SHA-256 page hash — not compared directly; only the chained sha256(ripemd160(x)) form was compared.')
print(f'HITS: {hits if hits else "none — the six remaining preimages are not cross-domain combinations of these elements in any of the five shapes"}')
with open('/home/hatch/workspace/gsmg-hash-dictionary-hits.json', 'w') as f:
    json.dump({'combinations': len(combos), 'hashes': total,
               'shapes': {'text': n_text, 'hex': n_hex, 'bytes': n_bytes,
                          'humph': n_humph, 'chained': n_chain},
               'hits': hits}, f, indent=1)
