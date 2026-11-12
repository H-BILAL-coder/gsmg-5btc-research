#!/usr/bin/env python3
"""Test the StudyX claim: the 14x14 grid as a 2-bit-per-cell key reading.

StudyX says the grid is 16x16 (256 cells) with White=00, Black=01, Blue=10,
Yellow=11, reading top-left to bottom-right into a 256-bit private key.
Verified facts it gets wrong: the grid is 14x14 = 196 cells (not 16x16),
and the 1-bit spiral reading decodes to 'gsmg.io/theseedisplanted' (not a key).

This script tests the 2-bit idea anyway, in every order the claim could mean:
- spiral order and row-major order
- 2-bit values (White=00, Black=01, Blue=10, Yellow=11)
- first 256 bits, last 256 bits, SHA-256 of the full bitstream
- the 1-bit ink stream + the colour stream concatenated (both orders)
Each candidate key is checked against the prize address AND the second
escrow, both address forms, via the certified fast tester.
"""
import sys, hashlib
sys.path.insert(0, '/home/hatch/workspace')
import numpy as np
from PIL import Image
from zden_keytest_fast import privkey_to_addrs

PRIZE = '1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe'
ESCROW = '17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa'
TARGETS = {PRIZE, ESCROW}

img = np.array(Image.open('/home/hatch/workspace/gsmg-repo/puzzle.png').convert('RGB'))
# grid: top 1047x1047, 14x14 cells, 75px pitch, sample at (37+75c, 37+75r), 9x9 majority vote
# colours: black (0,0,0), white (255,255,255), blue (63,72,204), yellow (255,242,0)
def cell_colour(r, c):
    y, x = 37 + 75 * r, 37 + 75 * c
    patch = img[y-4:y+5, x-4:x+5].reshape(-1, 3)
    # nearest of the four known colours by mean distance
    known = {'black': (0,0,0), 'white': (255,255,255), 'blue': (63,72,204), 'yellow': (255,242,0)}
    mean = patch.mean(axis=0)
    best, bestd = None, 1e18
    for name, rgb in known.items():
        d = sum((float(mean[i]) - rgb[i]) ** 2 for i in range(3))
        if d < bestd:
            bestd, best = d, name
    return best

grid = [[cell_colour(r, c) for c in range(14)] for r in range(14)]
counts = {}
for row in grid:
    for cell in row:
        counts[cell] = counts.get(cell, 0) + 1
print('grid colours:', counts, '(total', sum(counts.values()), ')')
assert sum(counts.values()) == 196

# spiral order: counterclockwise from (0,0), down the left column first
def spiral_order(n=14):
    order = []
    top, bottom, left, right = 0, n-1, 0, n-1
    while top <= bottom and left <= right:
        for r in range(top, bottom+1): order.append((r, left))
        left += 1
        for c in range(left, right+1): order.append((bottom, c))
        bottom -= 1
        if left <= right:
            for r in range(bottom, top-1, -1): order.append((r, right))
            right -= 1
        if top <= bottom:
            for c in range(right, left-1, -1): order.append((top, c))
            top += 1
    return order

spiral = spiral_order()
rowmajor = [(r, c) for r in range(14) for c in range(14)]

# 1-bit sanity check: black/blue=1, white/yellow=0 in spiral order
bits1 = ''.join('1' if grid[r][c] in ('black', 'blue') else '0' for r, c in spiral)
url = bytes(int(bits1[i:i+8], 2) for i in range(0, 192, 8)).decode()
print('1-bit spiral decodes to:', url)
assert url == 'gsmg.io/theseedisplanted'

# 2-bit values per StudyX: White=00, Black=01, Blue=10, Yellow=11
val = {'white': '00', 'black': '01', 'blue': '10', 'yellow': '11'}
def bits2(order):
    return ''.join(val[grid[r][c]] for r, c in order)

def key_from_bits(b):
    """Return list of (label, hexkey) candidates from a bit string."""
    out = []
    if len(b) >= 256:
        out.append(('first256', int(b[:256], 2).to_bytes(32, 'big').hex()))
        out.append(('last256', int(b[-256:], 2).to_bytes(32, 'big').hex()))
    out.append(('sha256', hashlib.sha256(int(b, 2).to_bytes((len(b)+7)//8, 'big')).hexdigest()))
    return out

cands = []
for name, order in [('spiral', spiral), ('rowmajor', rowmajor)]:
    b2 = bits2(order)
    print(f'{name} 2-bit stream: {len(b2)} bits')
    for label, hx in key_from_bits(b2):
        cands.append((f'{name}-2bit-{label}', hx))
    # colour bit (blue/yellow=1) and ink bit (black/blue=1) streams, concatenated
    colour = ''.join('1' if grid[r][c] in ('blue', 'yellow') else '0' for r, c in order)
    ink = ''.join('1' if grid[r][c] in ('black', 'blue') else '0' for r, c in order)
    for cname, cb in [('ink+colour', ink + colour), ('colour+ink', colour + ink)]:
        for label, hx in key_from_bits(cb):
            cands.append((f'{name}-{cname}-{label}', hx))

print('candidates:', len(cands))
hits = []
for label, hx in cands:
    try:
        comp, uncomp = privkey_to_addrs(hx)
    except Exception as e:
        print(f'  {label}: invalid key ({e})')
        continue
    if comp in TARGETS or uncomp in TARGETS:
        hits.append((label, hx, comp, uncomp))
        print(f'  HIT: {label} {hx} -> {comp} / {uncomp}')
print('hits:', hits)
print('DONE: 0 hits' if not hits else 'DONE WITH HITS')
