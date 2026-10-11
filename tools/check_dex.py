#!/usr/bin/env python3
"""Can every Pokemon be owned in ONE save, without trading? (per version)

Sources read from the source tree:
  repeatable  wild grass/water (data/wild/maps), Good/Super Rod tables,
              the Old Rod Magikarp, Game Corner prizes (data/events/prizes)
  one-time    static object_events (legendaries, Snorlax, Voltorb...),
              gifts (GIFTS below, checked against their scripts), and the
              in-game trades of data/events/trades.asm whose "give" species
              can itself be owned
  choices     one of a set only (starter, Mt Moon fossil, Fighting Dojo)

Owning a species registers it, so one specimen covers its whole linear
evolution chain; a branching family (Eevee) needs one specimen per branch.
Trade evolutions need a link cable and do not count.

Usage: python3 tools/check_dex.py [--version red|blue|both] [--strict]
--strict exits non-zero when anything is missing (for make check).
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# one-time gifts: species -> script that gives it (verified in main())
GIFTS = {
    'LAPRAS': 'scripts/SilphCo7F.asm',
    'EEVEE': 'scripts/CeladonMansionRoofHouse.asm',
    'MAGIKARP': 'scripts/MtMoonPokecenter.asm',
    'AERODACTYL': 'engine/events/cinnabar_lab.asm',  # Old Amber
}
# exclusive choices: only one of each group per save
CHOICES = {
    'starter': ['STARTER1', 'STARTER2', 'STARTER3'],
    'Mt Moon fossil': ['KABUTO', 'OMANYTE'],
    'Fighting Dojo': ['HITMONLEE', 'HITMONCHAN'],
}
NOT_IN_DEX = ('MISSINGNO', 'FOSSIL_', 'MON_GHOST')


def read(p):
    return (ROOT / p).read_text(encoding='utf-8')


def versioned_lines(text, version):
    """Lines kept for one version (IF DEF(_RED)/_BLUE ... ELSE/ENDC)."""
    keep, stack = [], []
    for line in text.splitlines():
        c = line.split(';', 1)[0].strip()
        m = re.match(r'IF DEF\(_(RED|BLUE)\)', c)
        if m:
            stack.append(m.group(1) == version.upper())
            continue
        if c.startswith('IF '):
            stack.append(True)
            continue
        if c == 'ELSE' and stack:
            stack[-1] = not stack[-1]
            continue
        if c == 'ENDC' and stack:
            stack.pop()
            continue
        if all(stack):
            keep.append(c)
    return keep


def species_consts():
    out, aliases = [], {}
    for line in read('constants/pokemon_constants.asm').splitlines():
        c = line.split(';', 1)[0].strip()
        m = re.match(r'const (\w+)', c)
        if m and m.group(1) != 'NO_MON':
            out.append(m.group(1))
        elif c.startswith('const_skip'):
            out.append(None)
        m = re.match(r'DEF (STARTER\d) EQU (\w+)', c)
        if m:
            aliases[m.group(1)] = m.group(2)
    return out, aliases


def evolutions(consts):
    text = read('data/pokemon/evos_moves.asm')
    ptrs = re.findall(r'^\tdw (\w+)EvosMoves', text, re.M)
    lab = {p: c for c, p in zip(consts, ptrs) if c}
    edges = {}
    for m in re.finditer(r'^(\w+)EvosMoves:\n(.*?)\n; Learnset', text,
                         re.M | re.S):
        src = lab.get(m.group(1))
        for kind, rest in re.findall(r'db EVOLVE_(\w+), ([^\n]*)',
                                     m.group(2)):
            tgt = rest.split(';')[0].split(',')[-1].strip()
            edges.setdefault(src, []).append((tgt, kind))
    return edges


def repeatable(version, valid):
    found = {}
    for f in sorted((ROOT / 'data/wild/maps').glob('*.asm')):
        for c in versioned_lines(f.read_text(), version):
            for sp in re.findall(r'db +\d+, *(\w+)', c):
                if sp in valid:
                    found.setdefault(sp, f'wild {f.stem}')
    for f in ('data/wild/good_rod.asm', 'data/wild/super_rod.asm'):
        for c in versioned_lines(read(f), version):
            for sp in re.findall(r'\b([A-Z][A-Z_]+)\b', c):
                if sp in valid:
                    found.setdefault(sp, Path(f).stem.replace('_', ' '))
    if 'lb bc, 5, MAGIKARP' in read('engine/items/item_effects.asm'):
        found.setdefault('MAGIKARP', 'old rod')
    for c in versioned_lines(read('data/events/prizes.asm'), version):
        m = re.match(r'db (\w+)$', c)
        if m and m.group(1) in valid:
            found.setdefault(m.group(1), 'game corner')
    return found


def one_time(version, valid):
    found = []
    for f in sorted((ROOT / 'data/maps/objects').glob('*.asm')):
        for c in versioned_lines(f.read_text(), version):
            m = re.match(r'object_event\b.*,\s*(\w+),\s*(\d+)$', c)
            if m and m.group(1) in valid:
                found.append((m.group(1), f'static {f.stem}'))
    # scripted encounters: ld a, SPECIES / ld [wCurOpponent], a (Snorlax)
    for f in sorted((ROOT / 'scripts').glob('*.asm')):
        lines = versioned_lines(f.read_text(), version)
        for a, b in zip(lines, lines[1:]):
            m = re.match(r'ld a, (\w+)$', a)
            if m and m.group(1) in valid and b == 'ld [wCurOpponent], a':
                found.append((m.group(1), f'scripted {f.stem}'))
    for sp, src in GIFTS.items():
        found.append((sp, f'gift ({Path(src).stem})'))
    return found


def trades(version, valid):
    out = []
    for line in read('data/events/trades.asm').splitlines():
        m = re.match(r'\s*npctrade (\w+),\s*(\w+),.*;\s*used in (\w+)', line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3)))
    return out


def analyse(version):
    consts, aliases = species_consts()
    valid = {c for c in consts if c}
    edges = evolutions(consts)
    dex = sorted(c for c in valid if not c.startswith(NOT_IN_DEX))
    # unlimited specimens
    rep = repeatable(version, valid)
    owned = dict(rep)
    todo = list(rep)
    trade_evo = {}
    while todo:
        s = todo.pop()
        for t, kind in edges.get(s, []):
            if kind == 'TRADE':
                trade_evo.setdefault(t, s)
                continue
            if t not in owned:
                owned[t] = f'evolves from {s}'
                todo.append(t)

    def chain(s, why):
        """one specimen: s and its non-trade evolutions (one branch only
        counts if the family branches)."""
        got = {s: why}
        cur = [s]
        while cur:
            x = cur.pop()
            nxt = [t for t, k in edges.get(x, []) if k != 'TRADE']
            branching = len(nxt) > 1
            for t in nxt[:1] if branching else nxt:
                got.setdefault(t, f'evolves from {x}')
                cur.append(t)
            if branching:
                for t in nxt[1:]:
                    got.setdefault(t, None)  # needs another specimen
        return got

    for sp, why in one_time(version, valid):
        for k, v in chain(sp, why).items():
            if v and k not in owned:
                owned[k] = v
    for give, get, where in trades(version, valid):
        if give in owned and get not in owned:
            for k, v in chain(get, f'trade {give} ({where})').items():
                if v and k not in owned:
                    owned[k] = v
    exclusive = {}
    for group, members in CHOICES.items():
        mem = [aliases.get(m, m) for m in members]
        for m in mem:
            fam = chain(m, group)
            for k in fam:
                if k not in owned:
                    exclusive[k] = f'{group}: only one of {", ".join(mem)}'
    missing = [s for s in dex if s not in owned]
    return dex, owned, missing, exclusive, trade_evo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', default='both',
                    choices=['red', 'blue', 'both'])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()
    for sp, src in GIFTS.items():
        if sp not in read(src):
            print(f'warn: gift {sp} no longer in {src}')
    bad = 0
    for v in (['red', 'blue'] if args.version == 'both' else [args.version]):
        dex, owned, missing, exclusive, trade_evo = analyse(v)
        print(f'{v.upper()}: {len(dex) - len(missing)}/{len(dex)} species '
              f'can be owned in one save without trading')
        for s in missing:
            why = exclusive.get(s)
            if not why and s in trade_evo:
                why = f'trade evolution of {trade_evo[s]}'
            print(f'  missing {s}' + (f' ({why})' if why else ''))
        if args.verbose:
            for s in dex:
                if s in owned:
                    print(f'  ok {s}: {owned[s]}')
        bad += len(missing)
    if args.strict and bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
