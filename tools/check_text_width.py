#!/usr/bin/env python3
"""Fail if a dialogue line is wider than the 18-tile text box.

Counts the rendered width: '#' expands to "POKé" (4 tiles), name
placeholders are counted at their maximum length, and multi-character
charmap keys ("<COLON>", "'s", ...) count as a single tile.
"""
import glob
import re
import sys

MAX = 18
EXPAND = {  # placeholder -> rendered width (worst case)
    '<PLAYER>': 7, '<RIVAL>': 7, '<TARGET>': 13, '<USER>': 13,
    '<PKMN>': 7, '<TM>': 2, '<PC>': 2, '<ROCKET>': 6, '<TRAINER>': 7,
}
CMD = re.compile(r'^\s*(text|line|cont|para|next)\s+"((?:[^"\\]|\\.)*)"')
ALLOW = {  # (file, line) intentionally wider, with a reason
}


def load_charmap(path='constants/charmap.asm'):
    """Multi-character charmap keys ("<COLON>", "'s", ...) are one tile."""
    keys = set()
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'\s*charmap\s+"((?:[^"\\]|\\.)+)"', line)
            if m and len(m.group(1)) > 1:
                keys.add(m.group(1))
    return sorted(keys, key=len, reverse=True)


MULTI = load_charmap()


def width(s):
    s = s.rstrip('@')
    w = i = 0
    while i < len(s):
        for k in EXPAND:
            if s.startswith(k, i):
                w += EXPAND[k]
                i += len(k)
                break
        else:
            if s[i] == '#':
                w, i = w + 4, i + 1
                continue
            for k in MULTI:
                if s.startswith(k, i):
                    w, i = w + 1, i + len(k)
                    break
            else:
                w, i = w + 1, i + 1
    return w


def main():
    bad = []
    for path in sorted(glob.glob('text/*.asm') + glob.glob('data/text/*.asm')):
        with open(path, encoding='utf-8') as f:
            for n, line in enumerate(f, 1):
                m = CMD.match(line)
                if not m or (path, n) in ALLOW:
                    continue
                w = width(m.group(2))
                if w > MAX:
                    bad.append(f'{path}:{n}: {w} tiles: "{m.group(2)}"')
    for b in bad:
        print('  error:', b)
    if bad:
        sys.exit(f'Text width: {len(bad)} line(s) wider than {MAX} tiles')
    print(f'Text width: every dialogue line fits in {MAX} tiles')


if __name__ == '__main__':
    main()
