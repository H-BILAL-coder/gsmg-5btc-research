from PIL import Image
from collections import Counter

im = Image.open('/home/hatch/workspace/gsmg-repo/puzzle.png').convert('RGB')
px = im.load()

def classify(c):
    # majority vote over a 9x9 neighbourhood around the centre, to be robust to edge artefacts
    return c

def cell_colour(r, c):
    cx, cy = 37 + 75 * c, 37 + 75 * r
    votes = Counter()
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            p = px[cx + dx, cy + dy]
            if p == (255, 255, 255) or p == (254, 254, 254):
                votes['W'] += 1
            elif p == (0, 0, 0):
                votes['K'] += 1
            elif p == (63, 72, 204):
                votes['B'] += 1
            elif p == (255, 242, 0):
                votes['Y'] += 1
            else:
                votes['?'] += 1
    return votes.most_common(1)[0][0]

grid = [[cell_colour(r, c) for c in range(14)] for r in range(14)]
for row in grid:
    print(''.join(row))
flat = [v for row in grid for v in row]
print('counts:', Counter(flat))

# spiral counterclockwise from (0,0): down left col, right along bottom, up right col, left along top, inward
order = []
top, bot, left, right = 0, 13, 0, 13
while top <= bot and left <= right:
    for r in range(top, bot + 1):
        order.append((r, left))
    left += 1
    for c in range(left, right + 1):
        order.append((bot, c))
    bot -= 1
    if left <= right:
        for r in range(bot, top - 1, -1):
            order.append((r, right))
        right -= 1
    if top <= bot:
        for c in range(right, left - 1, -1):
            order.append((top, c))
        top += 1
print('spiral len:', len(order))
bits = ''.join('1' if grid[r][c] in 'KB' else '0' for r, c in order)
txt = ''.join(chr(int(bits[i:i + 8], 2)) for i in range(0, 192, 8))
print('spiral decode (first 24 chars):', repr(txt))

col = [(i, order[i], grid[order[i][0]][order[i][1]])
       for i in range(len(order)) if grid[order[i][0]][order[i][1]] in 'BY']
print('coloured count:', len(col), 'blue:', sum(1 for _, _, v in col if v == 'B'),
      'yellow:', sum(1 for _, _, v in col if v == 'Y'))
print('0-based spiral indices:', [i for i, _, _ in col])
print('0-based residues mod 8:', sorted(set(i % 8 for i, _, _ in col)))
print('1-based residues mod 8:', sorted(set((i + 1) % 8 for i, _, _ in col)))
# row-major index of each coloured cell, mod 8
rm = [(r * 14 + c) % 8 for (r, c), v in [((rr, cc), vv) for _, (rr, cc), vv in col]]
print('row-major residues mod 8:', sorted(set(rm)))
# positions of coloured cells
print('coloured cells (r,c,val):', [(rr, cc, vv) for _, (rr, cc), vv in col])
