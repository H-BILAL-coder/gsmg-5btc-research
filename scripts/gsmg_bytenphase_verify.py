#!/usr/bin/env python3
"""Verify puzzlehunt issue #115 (BYTENPHASE) end-to-end from the published S570,
and cross-check S570 against the esrever-reconstructed segment from the live page."""
import json

S570 = (
"FAEDGGEEDFCBDABHHGGCADCFEDDGFDGBGIGAAEDGGIAFAECGHGGCDAIHE"
"HAHBAHIGCEIFGBFGEFGAIFABIFAGAEGEACGBBEAGFGGEEGGAFBACGFCDB"
"EIFFAAFCIDAHGDEEFGHHCGGAEGDEBHHEGEGHCEGADFBDIAGEFCICGGIFD"
"CGAAGGFBIGAICFBHECAECBCEIAICEBGBGIECDEGGFGEGAEDGGFIICIIIF"
"IFHGGCGFGDCDGGEFCBEEIGEFIBGIBGGGHHFBCGIFDEHEDFDAGICDBHICG"
"AIEDAEHAHGHHCIHDGHFHBIICECBIICHIHIIIGIDDGEHHDFDCHCBAFGFBH"
"AHEAGEGECAFEHGCFGGGGCAGFHHGHBAIHIDIEHHFDEGGDGCIHGGGGGHADA"
"HIGIGBGECGEDFCDGGACCDEHIICIGFBFFHGGAEIDBBEIBBEIIFDGFDHIEE"
"EIEEECIFDGDAHDIGGFHEGFIAFFIGGBCBCEHCEABFBEDBIIBFBFDEDEEHG"
"IGFAAIGGAGBEIICHIEDIFBEHGBCCAHHBIIBIBBIBDCBAHAIDHFAHIIHIC"
)
print('S570 len:', len(S570), 'starts:', S570[:4])
assert len(S570) == 570 and S570.startswith('FAED')

# step 2: remove FAE, 63 groups of 9, A=1..I=9, sum mod 26, 0=A
s = S570[3:]
assert len(s) == 567
vals = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9}
out63 = ''
for i in range(0, 567, 9):
    g = s[i:i+9]
    out63 += chr(ord('A') + (sum(vals[c] for c in g) % 26))
print('63-letter:', out63)
print('matches published:', out63 == 'RPRRUAVBQMTOLVAZUUVXKNXXPIPDEZSSIEELUSODWOCXFSBYOGZAETLSEOKNAIJ')

# step 3: Vigenere subtract key THEPROBLEMIS (A=0)
key = 'THEPROBLEMIS'
vig = ''.join(chr(ord('A') + ((ord(c)-65) - (ord(key[i % len(key)])-65)) % 26)
              for i, c in enumerate(out63))
print('Vigenere:', vig)
print('matches published:', vig == 'YINCDMUQMALWSOWKDGUMGBPFWBLONLRHESWTBLKOFABMBGTGVZVLNFKHACCVHBF')
print('starts YIN:', vig.startswith('YIN'))

# step 4-5: drop YIN, alternate streams, XOR 5-bit values
rest = vig[3:]
assert len(rest) == 60
A = rest[0::2]; B = rest[1::2]
print('stream A:', A)
print('stream B:', B)
print('streams match published:', A == 'CMQAWOKGMBFBOLHSTLOAMGGZLFHCVB' and B == 'DUMLSWDUGPWLNREWBKFBBTVVNKACHF')
xor = [(ord(a)-65) ^ (ord(b)-65) for a, b in zip(A, B)]
print('xor values:', xor)
B32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
disp = ''.join(B32[v] for v in xor)
print('display:', disp)

# step 6: 6x5 matrix row-major, inward spiral from upper-left (down, right, up, left)
rows = [list(disp[i*5:(i+1)*5]) for i in range(6)]
for r in rows: print('  ', ''.join(r))
# spiral
res = []
top, bottom, left, right = 0, 5, 0, 4
while top <= bottom and left <= right:
    for r in range(top, bottom+1): res.append(rows[r][left])
    left += 1
    if left > right: break
    for c in range(left, right+1): res.append(rows[bottom][c])
    bottom -= 1
    if top > bottom: break
    for r in range(bottom, top-1, -1): res.append(rows[r][right])
    right -= 1
    if left > right: break
    for c in range(right, left-1, -1): res.append(rows[top][c])
    top += 1
spiral = ''.join(res)
print('spiral:', spiral)
print('matches published BYTENPHASE...:', spiral == 'BYTENPHASEGBDOEL4YJKSVTML2KSDB')
print('prefix BYTENPHASE:', spiral.startswith('BYTENPHASE'))

# cross-check S570 against the esrever-reconstructed segment
try:
    ej = json.load(open('/home/hatch/workspace/gsmg-esrever-results.json'))
    print('esrever json keys:', list(ej.keys()))
    for k, v in ej.items():
        if isinstance(v, str) and len(v) >= 500:
            print(f'field {k}: len {len(v)}, == S570: {v == S570}, startswith FAED: {v.startswith("FAED")}')
            if v != S570:
                diffs = [i for i in range(min(len(v), 570)) if v[i] != S570[i]]
                print('  first diffs at:', diffs[:10], 'count:', len(diffs))
except Exception as e:
    print('esrever cross-check error:', e)

json.dump({'s570_len': len(S570), 'out63_match': out63 == 'RPRRUAVBQMTOLVAZUUVXKNXXPIPDEZSSIEELUSODWOCXFSBYOGZAETLSEOKNAIJ',
           'vig_match': vig == 'YINCDMUQMALWSOWKDGUMGBPFWBLONLRHESWTBLKOFABMBGTGVZVLNFKHACCVHBF',
           'spiral': spiral, 'spiral_match': spiral == 'BYTENPHASEGBDOEL4YJKSVTML2KSDB',
           'xor_values': xor},
          open('/home/hatch/workspace/gsmg-bytenphase-verify.json', 'w'), indent=2)
print('record: gsmg-bytenphase-verify.json')
