#!/usr/bin/env python3
"""Boost wild and trainer Pokemon levels by a percentage (default 30%).

Formats (pokered):
- Wild encounters (data/wild/maps/*.asm):  db LEVEL, SPECIES
- Trainer parties (data/trainers/parties.asm):
    db LEVEL, SPECIES[, SPECIES...], 0        (normal: one level for the team)
    db $FF, LEVEL, SPECIES, LEVEL, SPECIES, 0 (special: level/species pairs)

Usage: python3 tools/boost_levels.py [percent]   (default 30, caps at 100)
Run from the repo root.
"""
import math
import re
import sys
from pathlib import Path

PCT = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0

def boost(level: int) -> int:
    return min(100, math.ceil(level * (1 + PCT / 100)))

WILD_RE = re.compile(r'^(\s*db\s+)(\d+)(,\s*[A-Z_][A-Z_0-9]*\s*)$')
DB_LINE_RE = re.compile(r'^(\s*db\s+)(.*?)(\s*)$')
SPECIES_RE = re.compile(r'^[A-Z_][A-Z_0-9]*$')

def bump_party(tokens: list[str]) -> list[str] | None:
    """Return boosted tokens, or None if the line is not a party entry."""
    if tokens[-1] != '0':
        return None
    if tokens[0] == '$FF':
        # special: LEVEL, SPECIES pairs
        body = tokens[1:-1]
        if len(body) % 2 != 0:
            return None
        for i in range(0, len(body), 2):
            if not body[i].isdigit() or not SPECIES_RE.match(body[i + 1]):
                return None
            body[i] = str(boost(int(body[i])))
        return ['$FF'] + body + ['0']
    # normal: first token is the level of every Pokemon on the team
    if not tokens[0].isdigit():
        return None
    if not all(SPECIES_RE.match(t) for t in tokens[1:-1]) or not tokens[1:-1]:
        return None
    tokens[0] = str(boost(int(tokens[0])))
    return tokens

def process(path: Path) -> int:
    lines, changed = path.read_text().split('\n'), 0
    for i, line in enumerate(lines):
        m = WILD_RE.match(line)
        if m:
            lines[i] = f'{m.group(1)}{boost(int(m.group(2)))}{m.group(3)}'
            changed += 1
            continue
        m = DB_LINE_RE.match(line)
        if not m:
            continue
        tokens = [t.strip() for t in m.group(2).split(',')]
        new = bump_party(tokens)
        if new:
            lines[i] = f'{m.group(1)}{", ".join(new)}{m.group(3)}'
            changed += 1
    path.write_text('\n'.join(lines))
    return changed

total = 0
files = sorted(Path('data/wild/maps').glob('*.asm')) + [Path('data/trainers/parties.asm')]
for f in files:
    n = process(f)
    if n:
        total += n
        print(f'{f}: {n} lines boosted')
print(f'TOTAL: {total} lines (+{PCT:.0f}%)')
