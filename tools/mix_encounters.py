#!/usr/bin/env python3
"""Mix vanilla and Neris species in every wild table (catch-them-all).

encounter_matrix.py replaced every vanilla species with a Neris one, which
left about half the Pokedex unobtainable. This tool rebuilds each grass and
water table from the vanilla table (git VANILLA_REF) and the current one:

  1. every slot gets its vanilla species back (levels are kept: they carry
     the +30 % boost), so no vanilla species is lost;
  2. version exclusives are copied into the other version's table (Ekans in
     Blue, Sandshrew in Red, ...), so one cartridge can complete the dex;
  3. each Neris species of the current table takes a slot whose vanilla
     species also sits in another slot of the same table (rarest first), so
     adding it removes nothing.

A Neris species that finds no duplicate slot is reported; check_dex.py
says whether it is still obtainable elsewhere.

Usage: python3 tools/mix_encounters.py [--dry-run]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VANILLA_REF = 'd2704a63'  # last pret commit before the Neris fork
NERIS_REF = '41acbc16'    # Neris tables (levels, species) before this mix:
                          # reading them, not the files, keeps reruns stable
ROW = re.compile(r'^(\s*db\s+)(\d+)(,\s*)(\w+)(.*)$')


def at(ref, path):
    rel = path.relative_to(ROOT).as_posix()
    r = subprocess.run(['git', 'show', f'{ref}:{rel}'], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else None


def vanilla(path):
    return at(VANILLA_REF, path)


def tables(lines):
    """[(kind, {'RED': [idx...], 'BLUE': [idx...]})] for grass/water."""
    out, cur, stack = [], None, []
    for i, line in enumerate(lines):
        c = line.split(';', 1)[0].strip()
        if c.startswith(('def_grass_wildmons', 'def_water_wildmons')):
            cur = {'RED': [], 'BLUE': []}
            continue
        if c.startswith(('end_grass_wildmons', 'end_water_wildmons')):
            if cur and cur['RED']:
                out.append(cur)
            cur = None
            continue
        m = re.match(r'IF DEF\(_(RED|BLUE)\)', c)
        if m:
            stack.append(m.group(1))
            continue
        if c == 'ENDC' and stack:
            stack.pop()
            continue
        if cur is not None and ROW.match(line):
            for v in ('RED', 'BLUE'):
                if not stack or stack[-1] == v:
                    cur[v].append(i)
    return out


def mix_file(path, dry_run, state):
    cur = at(NERIS_REF, path) or path.read_text().splitlines()
    van = vanilla(path)
    if van is None or len(van) != len(cur):
        return None, ['layout differs from vanilla: skipped']
    sp = {}
    for i, line in enumerate(van):
        m = ROW.match(line)
        if m:
            sp[i] = m.group(4)
    notes = []
    for t in tables(cur):
        idx_all = set(t['RED']) | set(t['BLUE'])
        van_set = {sp[i] for i in idx_all}
        shared = set(t['RED']) & set(t['BLUE'])

        def redundant(i):
            for v in ('RED', 'BLUE'):
                if i in t[v]:
                    names = [sp[j] for j in t[v]]
                    if names.count(sp[i]) < 2:
                        return False
            return True

        def place(species, versions):
            for v in versions:
                if species in [sp[j] for j in t[v]]:
                    continue
                own = [j for j in reversed(t[v]) if j not in shared]
                cands = own + [j for j in reversed(t[v]) if j in shared]
                for j in cands:
                    if redundant(j):
                        sp[j] = species
                        break
                else:
                    return False
            return True

        # 2. version exclusives into the other version
        for v, o in (('RED', 'BLUE'), ('BLUE', 'RED')):
            mine = [sp[j] for j in t[v]]
            for s in dict.fromkeys(mine):
                if s not in [sp[j] for j in t[o]]:
                    if not place(s, [o]):
                        notes.append(f'{s} stays {v.lower()}-only')
        # 3. Neris species of the current table
        neris = []
        for j in sorted(idx_all):
            s = ROW.match(cur[j]).group(4)
            if s not in van_set and s not in neris:
                neris.append(s)
        for s in neris:
            if not place(s, ['RED', 'BLUE']):
                notes.append(f'no duplicate slot left for {s}')
                state['homeless'].setdefault(s, []).append((path.stem, t))
        for s in ('SCYTHER', 'PINSIR'):
            if s in van_set:
                state['homeless'].setdefault(s, []).append((path.stem, t))
        state['tables'].append((path.stem, t))
    state['files'][path] = (cur, sp)
    return sum(1 for i, l in enumerate(cur)
               if ROW.match(l) and i in sp and sp[i] != ROW.match(l).group(4)), notes


# Pass 2: species still absent from a version (or never wild) get a slot
# whose species also lives in another table of that version, so nothing is
# lost globally. EXTRA lists sources added for catch-them-all: the starters,
# fossils and Fighting Dojo Pokemon are one-of-N choices, Eevee's branches
# need several Eevees.
EXTRA = [
    ('BULBASAUR', ['SafariZoneEast', 'SafariZoneCenter']),
    ('CHARMANDER', ['SafariZoneNorth', 'SafariZoneCenter']),
    ('SQUIRTLE', ['SafariZoneWest', 'SafariZoneCenter']),
    ('KABUTO', ['SeafoamIslandsB3F', 'SeafoamIslandsB4F']),
    ('OMANYTE', ['SeafoamIslandsB4F', 'SeafoamIslandsB3F']),
    ('HITMONLEE', ['VictoryRoad2F', 'VictoryRoad3F']),
    ('HITMONCHAN', ['VictoryRoad3F', 'VictoryRoad2F']),
    ('EEVEE', ['Route16', 'Route17', 'Route18']),
]


def second_pass(state):
    def where(version):
        count = {}
        for stem, t in state['tables']:
            sp = state['files'][state['paths'][stem]][1]
            for s in {sp[j] for j in t[version]}:
                count[s] = count.get(s, 0) + 1
        return count

    todo = [(s, [x[0] for x in locs]) for s, locs in state['homeless'].items()]
    todo += EXTRA
    report = []
    for species, stems in todo:
        for v in ('RED', 'BLUE'):
            count = where(v)
            if count.get(species):
                continue
            done = False
            for stem in stems:
                for st, t in state['tables']:
                    if st != stem or done:
                        continue
                    sp = state['files'][state['paths'][st]][1]
                    for j in reversed(t[v]):
                        other = 'BLUE' if v == 'RED' else 'RED'
                        if j in t[other] and count_other(state, other, sp[j]) < 2:
                            continue
                        if count.get(sp[j], 0) >= 2 or \
                                [sp[k] for k in t[v]].count(sp[j]) >= 2:
                            sp[j] = species
                            done = True
                            break
            report.append(f'{species} ({v.lower()}): '
                          + ('placed' if done else 'NOT PLACED'))
    return report


def count_other(state, version, species):
    n = 0
    for stem, t in state['tables']:
        sp = state['files'][state['paths'][stem]][1]
        if species in {sp[j] for j in t[version]}:
            n += 1
    return n


def write_all(state, dry_run):
    total = 0
    for path, (cur, sp) in state['files'].items():
        out, changed = [], 0
        for i, line in enumerate(cur):
            m = ROW.match(line)
            if m and i in sp and sp[i] != m.group(4):
                line = f'{m.group(1)}{m.group(2)}{m.group(3)}{sp[i]}{m.group(5)}'
                changed += 1
            out.append(line)
        now = path.read_text().splitlines()
        changed = sum(1 for a, b in zip(now, out) if a != b)
        total += changed
        if changed and not dry_run:
            path.write_text('\n'.join(out) + '\n')
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()
    state = {'files': {}, 'tables': [], 'homeless': {}, 'paths': {}}
    for f in sorted((ROOT / 'data/wild/maps').glob('*.asm')):
        state['paths'][f.stem] = f
        changed, notes = mix_file(f, args.dry_run, state)
        if args.verbose and notes:
            print(f'{f.stem}:' + ''.join(f'\n  note: {n}' for n in notes))
    for line in second_pass(state):
        print(line)
    total = write_all(state, args.dry_run)
    print(f'{total} slot(s) {"would change" if args.dry_run else "changed"}')


if __name__ == '__main__':
    sys.exit(main())
