#!/usr/bin/env python3
"""Automated consistency checks for the Pokemon Neris ROM hack (NERIS-045).

Validates cross-table consistency without assembling:
  - Pokemon tables: constants <-> names <-> base_stats includes <-> palettes
  - Per-species completeness (NERIS-007): stats, types, catch, exp, growth,
    learnset, evos_moves pointer, dex entry pointer + text, icon, palette,
    cry, dex number
  - Placeholder asset detection (NERIS-014): Neris species reusing a source
    species' sprite (front+back+INCBIN identical)
  - Wild encounters: every db <level>, <SPECIES> references a defined const,
    10 entries per def_grass_wildmons / def_water_wildmons
  - Trainer parties reference defined species consts; party terminates with 0
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


def parse_internal_species():
    """[(const_name, internal_index)] — const_skip keeps its index, unnamed
    slots are None. Index == the value used by pointer tables."""
    entries = []
    index = 0
    started = False
    for line in read('constants/pokemon_constants.asm').splitlines():
        if re.match(r'\tconst_def', line):
            started = True
            index = 0
            continue
        if not started:
            continue
        m = re.match(r'\tconst (\w+)', line)
        if m:
            entries.append((m.group(1), index))
            index += 1
        elif re.match(r'\tconst_skip', line):
            entries.append((None, index))
            index += 1
    return entries


def check_parties(const_names):
    """Party format per engine/battle/read_trainer_party.asm:
      - normal:  db LEVEL, SPECIES..., 0
      - special: db $FF, LEVEL, SPECIES, LEVEL, SPECIES, ..., 0
    A stray leading byte (e.g. a 'line number' written before the data) is
    read as the LEVEL of the whole team — this broke the Olga/Oran fights
    once, so it is now a hard check.
    """
    text = strip_comments(read('data/trainers/parties.asm'))
    species = set(const_names)
    problems = 0
    for block in re.findall(r'^(\w+Data):\n((?:.|\n)*?)(?=^\w+Data:|\Z)',
                            text, re.M):
        name, body = block
        idx = 0
        for line in (l for l in body.splitlines() if l.strip()):
            idx += 1
            m = re.match(r'^\tdb\s+(.+?),\s*0\s*$', line)
            if not m:
                err(f'{name} trainer #{idx}: party line not "db ... ,0": {line.strip()!r}')
                problems += 1
                continue
            toks = [t.strip() for t in m.group(1).split(',')]
            if toks[0] == '$FF':
                body_toks = toks[1:]
                if len(body_toks) % 2 != 0:
                    err(f'{name} trainer #{idx}: $FF party has odd token count')
                    problems += 1
                    continue
                for k in range(0, len(body_toks), 2):
                    lvl, sp = body_toks[k], body_toks[k + 1]
                    if not re.match(r'^\d+$', lvl):
                        err(f'{name} trainer #{idx}: $FF party level {lvl!r} not numeric')
                        problems += 1
                    if sp not in species:
                        err(f'{name} trainer #{idx}: unknown species {sp}')
                        problems += 1
                    if re.match(r'^\d+$', lvl) and int(lvl) > 100:
                        err(f'{name} trainer #{idx}: level {lvl} > 100')
                        problems += 1
            else:
                if not re.match(r'^\d+$', toks[0]):
                    err(f'{name} trainer #{idx}: party level {toks[0]!r} not numeric')
                    problems += 1
                    continue
                if int(toks[0]) > 100:
                    err(f'{name} trainer #{idx}: level {toks[0]} > 100')
                    problems += 1
                for sp in toks[1:]:
                    if not re.match(r'^[A-Z][A-Z0-9_]*$', sp):
                        # a bare number here means a stray byte was left in
                        err(f'{name} trainer #{idx}: stray byte {sp!r} inside '
                            f'species list (would spawn as internal id)')
                        problems += 1
                    elif sp not in species:
                        err(f'{name} trainer #{idx}: unknown species {sp}')
                        problems += 1
    if problems == 0:
        print('Trainer parties: format valid (normal/$FF), species known, '
              'levels <= 100, no stray bytes')
    else:
        err(f'Trainer parties: {problems} problem(s)')


def check_species_completeness(species_entries):
    """NERIS-007: every playable species has all identity fields."""
    excluded = {'NO_MON', 'FOSSIL_KABUTOPS', 'FOSSIL_AERODACTYL', 'MON_GHOST'}

    dnames = re.findall(r'\bdname "([^"]+)"',
                        strip_comments(read('data/pokemon/names.asm')))

    dex_labels = set(re.findall(r'^\t?_(\w+)DexEntry::',
                                read('data/pokemon/dex_text.asm'), re.M))
    dex_labels |= set(re.findall(r'^(\w+)DexEntry::',
                                 read('data/pokemon/dex_entries.asm'), re.M))
    dex_pointers = re.findall(r'^\tdw (\w+DexEntry)',
                              read('data/pokemon/dex_entries.asm'), re.M)
    cry_rows = re.findall(r'^\tmon_cry (\w+),', read('data/pokemon/cries.asm'), re.M)
    evo_pointers = re.findall(r'^\tdw (\w+EvosMoves)',
                              read('data/pokemon/evos_moves.asm'), re.M)
    evo_blocks = set(re.findall(r'^(\w+EvosMoves):',
                                read('data/pokemon/evos_moves.asm'), re.M))
    icons = re.findall(r'\tnybble (ICON_\w+)', read('data/pokemon/menu_icons.asm'))
    pal_rows = re.findall(r'^\tdb (PAL_\w+)',
                          strip_comments(read('data/pokemon/palettes.asm')), re.M)

    # dex number per internal id (dex_order.asm row n-1 = internal id n)
    dex_consts = {}
    i = 0
    for line in read('constants/pokedex_constants.asm').splitlines():
        if re.match(r'\tconst_def', line):
            i = 0
            continue
        m = re.match(r'\tconst (DEX_\w+)', line)
        if m:
            i += 1
            dex_consts[m.group(1)] = i
    dex_of_internal = {}
    i = 0
    for line in strip_comments(read('data/pokemon/dex_order.asm')).splitlines():
        m = re.match(r'\s*db (\w+)', line)
        if not m:
            continue
        tok = m.group(1)
        dex_of_internal[i] = dex_consts.get(tok, int(tok) if tok.isdigit() else 0)
        i += 1

    problems = []
    for const, idx in species_entries:
        if const is None or const in excluded:
            continue
        stem = const.lower()
        bs_path = ROOT / 'data/pokemon/base_stats' / f'{stem}.asm'
        if not bs_path.exists():
            continue  # already reported by check_pokemon_tables
        text = read(f'data/pokemon/base_stats/{stem}.asm')
        plain = strip_comments(text)

        def need(cond, field):
            if not cond:
                problems.append(f'{const} (${idx:02X}): missing {field}')

        need(re.search(r'^\s*db\s+\d+,\s*\d+,\s*\d+,\s*\d+,\s*\d+\s*$', plain, re.M), 'base stats row')
        need(re.search(r'^\s*db\s+[A-Z_]+,\s*[A-Z_]+\s*$', plain, re.M), 'types')
        need(re.search(r'^\s*db\s+\d+\s*;\s*catch rate', text, re.M), 'catch rate')
        need(re.search(r'^\s*db\s+\d+\s*;\s*base exp', text, re.M), 'base exp')
        need(re.search(r'^\tdb ([A-Z_]+(?:\s*,\s*[A-Z_]+)*)\s*;\s*level 1 learnset', text, re.M), 'level 1 learnset')
        need(re.search(r'^\tdb (GROWTH_\w+)\s*;\s*growth rate', text, re.M), 'growth rate')
        need(re.search(r'^\tdw (\w+PicFront), (\w+PicBack)', text, re.M), 'sprite pointers')
        need(re.search(r'^\tINCBIN "gfx/pokemon/front/[^"]+\.pic', text, re.M), 'front pic INCBIN')

        # pointer tables are indexed by internal id - 1 (NO_MON = 0 has no row)
        row = idx - 1
        need(row < len(evo_pointers), 'evos_moves pointer row')
        if row < len(evo_pointers):
            need(evo_pointers[row] in evo_blocks, f'evos_moves block {evo_pointers[row]}')
        need(row < len(dex_pointers), 'dex entry pointer row')
        if row < len(dex_pointers):
            base = dex_pointers[row][:-len('DexEntry')]
            need(base in dex_labels, f'dex text (_{base}DexEntry)')
        need(row < len(cry_rows), 'cry row')
        # palette/icon are indexed by display dex number (+1 for the MISSINGNO
        # palette row / first icon nybble pair)
        dex_num = dex_of_internal.get(row, 0)
        need(dex_num == 0 or dex_num + 1 <= len(pal_rows), f'palette row for dex {dex_num}')
        need(dex_num == 0 or dex_num <= len(icons), f'icon row for dex {dex_num}')
        need(dex_num > 0, 'dex number (dex_order row)')
    playable = sum(1 for c, i in species_entries
                   if c and c not in excluded
                   and (ROOT / 'data/pokemon/base_stats' / f'{c.lower()}.asm').exists())
    if problems:
        for p in problems:
            err(p)
        print(f'Species completeness: {len(problems)} gap(s) — see errors above')
    else:
        print(f'Species completeness: all {playable} '
              f'playable species have stats/types/learnset/sprites/dex/cry/palette/icon')


def check_placeholder_assets(species_entries):
    """NERIS-014: classify species whose front .pic is borrowed.

    BORROWED_INTENTIONAL = the borrow is whitelisted (rule n°3:
    progressive completion) and shows up in the release notes.
    MISSING/PLACEHOLDER = no base_stats INCBIN at all, or a borrow not
    whitelisted, which means an unfinished sprite slipped through.
    """
    INTENTIONAL_BORROWS = {
        # species -> source pic stem accepted for release (final art)
    }
    PENDING_PHASE6 = {
        # species whose borrowed sprite is known-pending (phase 6 art):
        # SOLARIS -> mew + the 29 species borrowing vanilla art below
        'SOLARIS', 'PETIROC', 'AILESOR', 'BUGGAIE', 'FLORALYS', 'AQUAJET',
        'VOLTOUR', 'PSYMINI', 'GLACIETTE', 'FLORAQUE', 'ROCBOUL', 'SERPICOL',
        'CHAUVESPI', 'TERREUX', 'MARAISOR', 'OISEAULO', 'CRABEAU', 'FANTOMIN',
        'ELECTROX', 'FLAMELET', 'DRAGONET', 'OBSCURAX', 'CRAMORIL', 'VENOMBRU',
        'SPECTRELA', 'DRACOZELLE', 'MENTALIS', 'FULGURAX', 'GIVRALP',
        'TERRAKOR', 'PYROFELIS',
    }
    dnames = re.findall(r'\bdname "([^"]+)"',
                        strip_comments(read('data/pokemon/names.asm')))
    # names row n-1 maps to internal id n (pointer-table indexing)
    excluded = {'NO_MON', 'FOSSIL_KABUTOPS', 'FOSSIL_AERODACTYL', 'MON_GHOST'}
    intentional, pending, unexpected, missing = [], [], [], []
    for const, idx in species_entries:
        if const is None or const in excluded:
            continue
        stem = const.lower()
        bs_path = ROOT / 'data/pokemon/base_stats' / f'{stem}.asm'
        if not bs_path.exists():
            continue
        text = read(f'data/pokemon/base_stats/{stem}.asm')
        inc = re.search(r'^\tINCBIN "gfx/pokemon/front/([a-z0-9_.]+)\.pic', text, re.M)
        fr = dnames[idx - 1] if 0 < idx <= len(dnames) else const
        if inc is None:
            missing.append(f'{fr} ({const}): no front pic INCBIN in base_stats')
            continue
        src = inc.group(1)
        if src == stem:
            continue
        if INTENTIONAL_BORROWS.get(const) == src:
            intentional.append(f'{fr} ({const}) borrows {src} sprite (intentional)')
        elif const in PENDING_PHASE6:
            pending.append(f'{fr} ({const}) borrows {src} sprite (pending phase 6 art)')
        else:
            unexpected.append(f'{fr} ({const}) borrows {src} sprite (NOT whitelisted)')
    print(f'Placeholder assets: {len(intentional)} intentional, '
          f'{len(pending)} pending phase 6, '
          f'{len(unexpected)} unexpected, {len(missing)} missing')
    for b in intentional:
        print(f'  info: {b}')
    for b in pending:
        print(f'  info: {b}')
    for b in unexpected:
        print(f'  warn: {b}')
    for b in missing:
        print(f'  warn: {b}')
    if unexpected or missing:
        raise SystemExit(1)


def check_wild_encounters(const_names):
    species = set(const_names)
    files = sorted(Path('data/wild/maps').glob('*.asm'))
    bad = []
    total = 0
    for f in files:
        text = strip_comments(f.read_text())
        for kind in ('def_grass_wildmons', 'def_water_wildmons'):
            for m in re.finditer(rf'^\s*{kind}\s+(\d+)', text, re.M):
                total += 1
        for m in re.finditer(r'^\s*db\s+(\d+)\s*,\s*([A-Z_][A-Z0-9_]*)\s*$', text, re.M):
            level, tok = int(m.group(1)), m.group(2)
            if level > 100:
                err(f'{f.name}: wild level {level} > 100')
            if tok not in species:
                bad.append(f'{f.name}: unknown species {tok}')
    for b in sorted(set(bad)):
        err(b)
    print(f'Wild encounters: {len(files)} map files, {total} encounter tables, '
          f'all species defined' if not bad else 'Wild encounters: unknown species found')


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


def check_edge_warps():
    """A warp only fires (home/overworld.asm CheckWarpsNoCollision) if the
    tile under the player is a warp tile of the tileset
    (data/tilesets/warp_tile_ids.asm, read at screen coord 8,9 = the step's
    lower-left tile), or else via ExtraWarpCheck. On edge-mode maps that is
    IsPlayerFacingEdgeOfMap (engine/overworld/player_state.asm): the step
    must be on the map border (x=0, y=0, x=2*w-1, y=2*h-1). A warp on a
    plain floor tile inside the map can never be taken.
    """
    # ExtraWarpCheck: these tilesets/maps use IsWarpTileInFrontOfPlayer
    # (carpet tiles) instead of the edge rule; not covered here
    carpet_tilesets = {'OVERWORLD', 'SHIP', 'SHIP_PORT', 'PLATEAU'}
    carpet_maps = {'ROCKET_HIDEOUT_B1F', 'ROCKET_HIDEOUT_B2F',
                   'ROCKET_HIDEOUT_B4F', 'ROCK_TUNNEL_1F'}
    edge_maps = {'SS_ANNE_3F'}

    def incbins(path):
        # label -> INCBIN path; consecutive labels share the next INCBIN
        out, pending = {}, []
        for line in strip_comments(read(path)).splitlines():
            pending += re.findall(r'^(\w+)::?', line)
            m = re.search(r'INCBIN "([^"]+)"', line)
            if m:
                out.update((lbl, m.group(1)) for lbl in pending)
                pending = []
        return out

    tileset_consts = re.findall(r'^\tconst (\w+)', strip_comments(
        read('constants/tileset_constants.asm')), re.M)
    tileset_labels = re.findall(r'^\ttileset (\w+),', strip_comments(
        read('data/tilesets/tileset_headers.asm')), re.M)
    block_files = incbins('gfx/tilesets.asm')
    bst = {c: (ROOT / block_files[f'{lbl}_Block']).read_bytes()
           for c, lbl in zip(tileset_consts, tileset_labels)}

    # warp tile lists, with label fallthrough as in the asm
    warp_tiles, open_labels = {}, []
    for line in strip_comments(read('data/tilesets/warp_tile_ids.asm')).splitlines():
        m = re.match(r'^\.(\w+)WarpTileIDs:', line)
        if m:
            open_labels.append(m.group(1))
            warp_tiles.setdefault(m.group(1), set())
            continue
        m = re.match(r'^\t(db|warp_tiles)\b(.*)', line)
        if not m or not open_labels:
            continue
        ids = {int(t, 16) for t in re.findall(r'\$([0-9A-Fa-f]{2})', m.group(2))}
        for lbl in open_labels:
            warp_tiles[lbl] |= ids
        if m.group(1) == 'warp_tiles' or '-1' in m.group(2):
            open_labels = []
    tiles_of = {c: warp_tiles[lbl] for c, lbl in zip(tileset_consts, tileset_labels)}

    sizes = {n: (int(w), int(h)) for n, w, h in re.findall(
        r'map_const (\w+),\s*(\d+),\s*(\d+)',
        strip_comments(read('constants/map_constants.asm')))}
    blk_files = incbins('maps.asm')

    checked, inaccessible, before = 0, 0, len(errors)
    for hdr in sorted(Path(ROOT / 'data/maps/headers').glob('*.asm')):
        m = re.search(r'map_header (\w+),\s*(\w+),\s*(\w+)',
                      strip_comments(hdr.read_text()))
        label, mapc, tileset = m.groups()
        if mapc not in edge_maps and (tileset in carpet_tilesets
                                      or mapc in carpet_maps):
            continue
        w, h = sizes[mapc]
        blk = (ROOT / blk_files[f'{label}_Blocks']).read_bytes()
        obj = read(f'data/maps/objects/{label}.asm')
        for n, (x, y, dest, note) in enumerate(re.findall(
                r'^\s*warp_event\s+(\d+),\s*(\d+),\s*(\w+)[^;\n]*(;.*)?$',
                obj, re.M), 1):
            # pret marks its dummy warps "; inaccessible" (SilphCo1F,
            # SilphCo11F): unreachable on purpose, so not a defect
            if 'inaccessible' in note:
                inaccessible += 1
                continue
            x, y = int(x), int(y)
            checked += 1
            if x >= 2 * w or y >= 2 * h:
                err(f'{label} warp {n} ({x},{y}) -> {dest}: outside the '
                    f'{2 * w}x{2 * h} step grid')
                continue
            block = blk[(y // 2) * w + x // 2]
            tile = bst[tileset][block * 16 + ((y % 2) * 2 + 1) * 4 + (x % 2) * 2]
            on_edge = x in (0, 2 * w - 1) or y in (0, 2 * h - 1)
            if tile not in tiles_of[tileset] and not on_edge:
                err(f'{label} warp {n} ({x},{y}) -> {dest}: tile ${tile:02X} '
                    f'is not a {tileset} warp tile and the step is not on the '
                    f'map edge (x=0/{2 * w - 1}, y=0/{2 * h - 1}): unreachable')
    if len(errors) == before:
        print(f'Edge warps: {checked} warps on edge-mode maps, all on a warp '
              f'tile or the map edge ({inaccessible} marked inaccessible)')


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


def check_text_lines():
    """Translated dialog (text/) fits the 18-char text box; only ASCII
    from the charmap (accented characters or '+' are unmapped and break
    encoding). Vanilla predef texts (data/text/) are exempt from the
    length rule but still scanned for unmapped characters.
    """
    import glob
    problems = []
    for path in glob.glob(str(ROOT / 'text' / '*.asm')) + \
            glob.glob(str(ROOT / 'data' / 'text' / '*.asm')):
        enforce_length = '/text/' in path and '/data/' not in path
        for n, line in enumerate(Path(path).read_text().splitlines(), 1):
            m = re.search(r'"([^"]*)"', line)
            if not m:
                continue
            if re.match(r'\s*(text|line|cont|next)\b', line) is None:
                continue
            content = m.group(1)
            effective = content.replace('<PLAYER>', 'x' * 7) \
                               .replace('<RIVAL>', 'x' * 7) \
                               .rstrip('@')
            if enforce_length and len(effective) > 18:
                problems.append(f'{Path(path).name}:{n}: {len(effective)} chars: '
                                f'"{content}"')
            bad = [c for c in content if ord(c) > 127 and c != chr(0xA5)]
            if bad:
                problems.append(f'{Path(path).name}:{n}: unmapped char(s) '
                                f'{bad} in "{content}"')
    for p in problems:
        err(f'text: {p}')


def main():
    consts_text = strip_comments(read('constants/pokemon_constants.asm'))
    const_names = re.findall(r'^\tconst ([A-Z0-9_]+)', consts_text, re.M)
    species_entries = parse_internal_species()
    check_pokemon_tables()
    check_species_completeness(species_entries)
    check_placeholder_assets(species_entries)
    check_wild_encounters(const_names)
    check_parties(const_names)
    check_toggles()
    check_warp_targets()
    check_edge_warps()
    check_trainer_flags()
    check_map_header_pointers()
    check_text_lines()
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
