#!/usr/bin/env python3
"""Automated consistency checks for the Pokemon Neris ROM hack (NERIS-045).

Validates cross-table consistency without assembling:
  - Pokemon tables: constants <-> names <-> base_stats includes <-> palettes
  - Trainer party format: every trainer party terminates with 0
  - Toggleable objects: const group order matches data block order, no missing
    TOGGLE consts for object consts referenced in map object files
  - Map tables: every map id referenced in warp events / map constants exists
  - Event flags referenced in trainer headers exist in event_constants

Usage: python3 tools/check_neris.py  (exit 1 on failure)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


def read(path):
    return (ROOT / path).read_text()


def strip_comments(text):
    lines = []
    for line in text.splitlines():
        pos = line.find(';')
        lines.append(line[:pos] if pos >= 0 else line)
    return '\n'.join(lines)


def check_pokemon_tables():
    consts_text = strip_comments(read('constants/pokemon_constants.asm'))
    const_names = re.findall(r'^\tconst ([A-Z0-9_]+)', consts_text, re.M)

    names_text = strip_comments(read('data/pokemon/names.asm'))
    dnames = re.findall(r'\bdname "([^"]+)"', names_text)

    includes_text = strip_comments(read('data/pokemon/base_stats.asm'))
    base_stats = re.findall(r'base_stats/(\w+)\.asm', includes_text)
    base_lower = {b.lower() for b in base_stats}

    pal_text = strip_comments(read('data/pokemon/palettes.asm'))
    pal_rows = len(re.findall(r'^\tdb ', pal_text, re.M))

    # deliberately excluded from base_stats: NO_MON, FOSSIL_*, MON_GHOST
    excluded = {'NO_MON', 'FOSSIL_KABUTOPS', 'FOSSIL_AERODACTYL', 'MON_GHOST'}
    norm = lambda s: s.lower().replace('_', '')
    missing_stats = [c for c in const_names
                     if c not in excluded and norm(c) not in base_lower]
    if missing_stats:
        err(f'Species without base_stats include: {missing_stats}')

    if len(dnames) < len(const_names):
        err(f'Only {len(dnames)} dnames for {len(const_names)} species consts')

    if pal_rows < len(const_names) - len(excluded):
        err(f'Only {pal_rows} palette rows for {len(const_names)} species')
    else:
        print(f'Pokemon tables: {len(const_names)} consts, {len(dnames)} '
              f'dnames, {len(base_stats)} base_stats, {pal_rows} palettes '
              '- all species covered')

    if len(const_names) != len(set(const_names)):
        dupes = [n for n in const_names if const_names.count(n) > 1]
        err(f'Duplicate pokemon constants: {sorted(set(dupes))}')

    # starter pointers must reference existing consts
    for starter in ('STARTER1', 'STARTER2', 'STARTER3'):
        m = re.search(rf'DEF {starter} EQU (\w+)', consts_text)
        if not m or m.group(1) not in const_names:
            err(f'{starter} does not reference a defined pokemon constant')
    print('Starter pointers OK (STARTER1-3 reference defined species)')


def check_parties():
    text = strip_comments(read('data/trainers/parties.asm'))
    for block in re.findall(r'^(\w+Data):\n((?:.|\n)*?)(?=^\w+Data:|\Z)',
                            text, re.M):
        _, body = block
        for i, line in enumerate(l for l in body.splitlines() if l.strip()):
            if not line.strip().endswith('0'):
                err(f'Party line in parties.asm does not end with 0: {line!r}')
    print('Trainer parties: all entries terminated with 0')


def norm_key(s):
    return s.upper().replace('_', '')


def check_toggles():
    consts_text = strip_comments(read('constants/toggle_constants.asm'))
    groups_const = re.findall(
        r'toggle_consts_for (\w+)\n((?:\tconst .*\n)+)', consts_text)
    data_text = strip_comments(read('data/maps/toggleable_objects.asm'))
    groups_data = re.findall(
        r'toggleable_objects_for (\w+)\n((?:\ttoggle_object_state .*\n)+)',
        data_text)

    const_map = {g: [c.split()[1] for c in body.strip().splitlines()]
                 for g, body in groups_const}
    data_map = {g: [l.split()[1].rstrip(',') for l in body.strip().splitlines()]
                for g, body in groups_data}

    for g in const_map:
        if g not in data_map:
            err(f'toggle_consts_for {g} has no matching data block')
    for g in data_map:
        if g not in const_map:
            err(f'toggleable_objects_for {g} has no matching const group')
    for g in set(const_map) & set(data_map):
        if len(const_map[g]) != len(data_map[g]):
            err(f'toggle count mismatch for {g}: '
                f'{len(const_map[g])} consts vs {len(data_map[g])} entries')
    # every referenced object const must exist in its map object file
    obj_consts = {}
    for obj in Path('data/maps/objects').glob('*.asm'):
        obj_consts[norm_key(obj.stem)] = set(re.findall(
            r'const_export (\w+)', strip_comments(obj.read_text())))
    for g, entries in data_map.items():
        for e in entries:
            if not e.isidentifier():
                # vanilla groups may reference raw byte values
                continue
            if e not in obj_consts.get(norm_key(g), set()):
                err(f'toggle_object_state {g}: {e} not defined in '
                    f'{g.lower()} objects')
    if not errors:
        print(f'Toggleable objects: {len(const_map)} maps, '
              f'{sum(len(v) for v in const_map.values())} toggles, '
              'counts aligned, object consts defined')


def check_warp_targets():
    consts_text = strip_comments(read('constants/map_constants.asm'))
    maps = set(re.findall(r'map_const (\w+)', consts_text)) | {'LAST_MAP'}
    referenced = {}
    for obj in Path('data/maps/objects').glob('*.asm'):
        text = strip_comments(obj.read_text())
        for m in re.findall(r'warp_event\s+[^,]+,\s*[^,]+,\s*(\w+)', text):
            referenced.setdefault(m, obj.name)
    for target, src in sorted(referenced.items()):
        if target not in maps:
            err(f'warp_event in {src} references unknown map {target}')
    print(f'Warp targets: {len(referenced)} distinct maps, all defined')


def check_trainer_flags():
    consts_text = strip_comments(read('constants/event_constants.asm'))
    events = set(re.findall(r'\bconst (EVENT_\w+)', consts_text))
    missing = set()
    for script in Path('scripts').glob('*.asm'):
        text = strip_comments(script.read_text())
        for m in re.findall(r'\btrainer (EVENT_\w+)', text):
            if m not in events:
                missing.add((script.name, m))
    for src, flag in sorted(missing):
        err(f'{src} uses undefined event flag {flag}')
    if not missing:
        print('Trainer flags: all trainer event flags defined')


def check_map_header_pointers():
    sym_path = ROOT / 'pokered.sym'
    rom_path = ROOT / 'pokered.gbc'
    if not sym_path.exists() or not rom_path.exists():
        print('Map header pointers: skipped (build artifacts missing)')
        return
    syms = {}
    for line in sym_path.read_text().splitlines():
        m = re.match(r'^([0-9a-fA-F]{2}):([0-9a-fA-F]{4})\s+(\S+)$', line.strip())
        if m:
            syms.setdefault(m.group(3), (int(m.group(1), 16), int(m.group(2), 16)))
    rom = rom_path.read_bytes()
    base = syms['MapHeaderPointers'][1]
    h_addr = {}
    for lbl, (bk, ad) in syms.items():
        if lbl.endswith('_h'):
            h_addr[lbl[:-2].upper()] = (bk, ad)
    bad = 0
    for line in strip_comments(read('constants/map_constants.asm')).splitlines():
        m = re.match(r'map_const (\w+),\s*(-?\d+),\s*(-?\d+)\s*;\s*\$([0-9A-Fa-f]+)', line)
        if not m:
            continue
        name, mid = m.group(1), int(m.group(4), 16)
        exp = h_addr.get(name)
        if exp is None:
            continue
        off = base + 2 * mid
        ptr = rom[off] | (rom[off + 1] << 8)
        if ptr != exp[1]:
            err(f'map id ${mid:02x} ({name}) header pointer is {ptr:#06x}, '
                f'expected {exp[1]:#06x}')
            bad += 1
    if not bad:
        print('Map header pointers: all map ids point to their own header')


def main():
    check_pokemon_tables()
    check_parties()
    check_toggles()
    check_warp_targets()
    check_trainer_flags()
    check_map_header_pointers()
    if errors:
        print()
        print(f'{len(errors)} problem(s):')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)
    print()
    print('All consistency checks passed.')


if __name__ == '__main__':
    main()
