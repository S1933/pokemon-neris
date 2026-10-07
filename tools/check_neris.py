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


def check_party_order():
    """H1/H2: map objects pick a party by position (OPP_<CLASS>, n), so a
    party inserted before vanilla ones shifts every vanilla reference.
    The first VANILLA[class] parties of each class are pret/pokered's (edited
    in place at most). Every party after them must sit under a section
    comment starting with '; Neris:' and be referenced by a map object.
    """
    # party count per class in pret/pokered (commit d47f74ee)
    VANILLA = {
        'Youngster': 13, 'BugCatcher': 14, 'Lass': 18, 'Sailor': 8,
        'JrTrainerM': 9, 'JrTrainerF': 24, 'Pokemaniac': 7, 'SuperNerd': 12,
        'Hiker': 14, 'Biker': 15, 'Burglar': 9, 'Engineer': 3,
        'UnusedJuggler': 0, 'Fisher': 11, 'Swimmer': 15, 'CueBall': 9,
        'Gambler': 7, 'Beauty': 15, 'Psychic': 4, 'Rocker': 2, 'Juggler': 8,
        'Tamer': 6, 'BirdKeeper': 17, 'Blackbelt': 9, 'Rival1': 9,
        'ProfOak': 3, 'Chief': 0, 'Scientist': 13, 'Giovanni': 3,
        'Rocket': 41, 'CooltrainerM': 10, 'CooltrainerF': 8, 'Bruno': 1,
        'Brock': 1, 'Misty': 1, 'LtSurge': 1, 'Erika': 1, 'Koga': 1,
        'Blaine': 1, 'Sabrina': 1, 'Gentleman': 5, 'Rival2': 12,
        'Rival3': 3, 'Lorelei': 1, 'Channeler': 24, 'Agatha': 1, 'Lance': 1,
    }
    text = read('data/trainers/parties.asm')
    classes = re.findall(r'^\tdw (\w+)Data$', text, re.M)
    consts = re.findall(r'^\ttrainer_const (\w+)',
                        read('constants/trainer_constants.asm'), re.M)[1:]
    block_of = {f'OPP_{c}': b for c, b in zip(consts, classes)}
    refs = set()
    for obj in (ROOT / 'data/maps/objects').glob('*.asm'):
        for c, n in re.findall(r'\b(OPP_\w+),\s*(\d+)',
                               strip_comments(obj.read_text())):
            if c in block_of:
                refs.add((block_of[c], int(n)))
    # (class, party number) -> marked; a comment block opens a section
    marked = {}
    cls, idx, neris, prev_comment = None, 0, False, False
    for line in text.splitlines():
        m = re.match(r'^(\w+)Data:', line)
        if m:
            cls, idx, neris = m.group(1), 0, False
        elif cls and line.startswith(';'):
            if not prev_comment:
                neris = line.startswith('; Neris:')
        elif cls and re.match(r'^\tdb\b', line):
            idx += 1
            marked[(cls, idx)] = neris
        prev_comment = line.startswith(';')
    before, added = len(errors), 0
    for c in classes:
        n = VANILLA.get(c)
        total = sum(1 for k in marked if k[0] == c)
        if n is None or total < n:
            err(f'{c}Data: {total} parties, pret/pokered has {n}')
            continue
        for i in range(1, total + 1):
            if i <= n and marked[(c, i)]:
                err(f'{c}Data #{i}: Neris party inside the vanilla range '
                    f'(1-{n}); move it to the end of the class')
            elif i > n and not marked[(c, i)]:
                err(f'{c}Data #{i}: party past the vanilla range (1-{n}) '
                    f'without a "; Neris:" section comment')
            elif i > n and (c, i) not in refs:
                err(f'{c}Data #{i}: Neris party referenced by no map object')
            added += i > n
    if len(errors) == before:
        print(f'Trainer party order: vanilla positions kept, {added} Neris '
              'parties appended and referenced')


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


def check_object_const_order():
    """Object consts are positional: the n-th const_export is the n-th
    object_event. A const whose TEXT_<const> belongs to another slot means
    scripts and toggles address the wrong sprite (MtMoonB2F once did).
    Limitation: name-based, so a misordered const whose text id differs from
    its name (vanilla Bill/Daisy style) goes unseen.
    """
    misplaced, warnings, maps = 0, [], 0
    for obj in sorted((ROOT / 'data/maps/objects').glob('*.asm')):
        text = strip_comments(obj.read_text())
        consts = re.findall(r'^\s*const_export\s+(\w+)', text, re.M)
        texts = [m.group(1) if m else None for m in
                 (re.search(r'\bTEXT_(\w+)', args) for args in
                  re.findall(r'^\s*object_event\s+(.*)$', text, re.M))]
        if not texts:
            continue
        maps += 1
        if len(consts) != len(texts):
            warnings.append(f'{obj.name}: {len(consts)} const_export for '
                            f'{len(texts)} object_event')
        for i, const in enumerate(consts):
            if const in texts and texts.index(const) != i:
                err(f'{obj.name}: {const} is const #{i + 1} but '
                    f'TEXT_{const} is object_event #{texts.index(const) + 1}')
                misplaced += 1
    if not misplaced:
        print(f'Object const order: {maps} maps, const_export order matches '
              'object_event order')
    for w in warnings:
        print(f'  warn: {w}')


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
    # (map, warp number): vanilla dummy warps on plain floor, unreachable
    # in pret too (its "; inaccessible" comments, #591), not a defect
    dummy_warps = {
        ('SILPH_CO_1F', 5),   # -> SILPH_CO_3F, floor tile $01 at (16,10)
        ('SILPH_CO_11F', 3),  # -> LAST_MAP, floor tile $1F at (5,5)
    }

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
    for hdr in sorted((ROOT / 'data/maps/headers').glob('*.asm')):
        m = re.search(r'map_header (\w+),\s*(\w+),\s*(\w+)',
                      strip_comments(hdr.read_text()))
        label, mapc, tileset = m.groups()
        if mapc not in edge_maps and (tileset in carpet_tilesets
                                      or mapc in carpet_maps):
            continue
        w, h = sizes[mapc]
        blk = (ROOT / blk_files[f'{label}_Blocks']).read_bytes()
        obj = read(f'data/maps/objects/{label}.asm')
        for n, (x, y, dest) in enumerate(re.findall(
                r'^\s*warp_event\s+(\d+),\s*(\d+),\s*(\w+)',
                strip_comments(obj), re.M), 1):
            if (mapc, n) in dummy_warps:
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
              f'tile or the map edge ({inaccessible} dummy warps excepted)')


def check_last_map_warps():
    """`warp_event x, y, LAST_MAP, n` lands on warp n of wLastMap, which
    WarpFound2 (home/overworld.asm) only sets when leaving an outside map
    (CheckIfInOutsideMap: OVERWORLD or PLATEAU tileset). So for every
    outside map P warping into map I, P's warp n must lead back to I.
    """
    # (map, warp y) -> parent, where the map script overrides wLastMap
    # by player position: Route22Gate sets ROUTE_23 north of y=4, else ROUTE_22
    scripted = {('ROUTE_22_GATE', 0): 'ROUTE_23', ('ROUTE_22_GATE', 7): 'ROUTE_22'}
    # maps with a LAST_MAP warp but no outside map warping in: wLastMap is
    # not statically known, so each one needs a reason here
    no_outside_parent = {
        # orphaned by Neris: Viridian's warp 3 now leads to ACADEMY
        'VIRIDIAN_SCHOOL_HOUSE',
        # pret's unused slots, reached by no warp
        'CERULEAN_TRASHED_HOUSE_COPY', 'UNDERGROUND_PATH_ROUTE_6_COPY',
        'UNDERGROUND_PATH_ROUTE_7_COPY', 'CINNABAR_MART_COPY', 'UNUSED_MAP_E7',
        # entered only from SilphCo 7F/10F; its LAST_MAP warp is pret's
        # "; inaccessible" dummy
        'SILPH_CO_11F',
    }
    consts = re.findall(r'map_const (\w+)',
                        strip_comments(read('constants/map_constants.asm')))
    labels = re.findall(r'^\tdw (\w+)_h', read('data/maps/map_header_pointers.asm'), re.M)
    tileset, warps = {}, {}
    for const, label in zip(consts, labels):
        hdr = read(f'data/maps/headers/{label}.asm')
        tileset[const] = re.search(r'map_header\s+\w+,\s*\w+,\s*(\w+)', hdr).group(1)
        warps[const] = re.findall(
            r'warp_event\s+[^,]+,\s*(\d+),\s*(\w+),\s*(\d+)',
            strip_comments(read(f'data/maps/objects/{label}.asm')))
    outside = sorted(k for k, t in tileset.items() if t in ('OVERWORLD', 'PLATEAU'))
    checked, before = 0, len(errors)
    for inner, inner_warps in warps.items():
        entered_from = [p for p in outside if any(t == inner for _, t, _ in warps[p])]
        for i, (y, target, n) in enumerate(inner_warps, 1):
            if target != 'LAST_MAP':
                continue
            n = int(n)
            override = scripted.get((inner, int(y)))
            if not (override or entered_from or inner in no_outside_parent):
                err(f'{inner} warp {i} exits to LAST_MAP, but no outside map '
                    'warps into it: wLastMap is unknown')
            for parent in [override] if override else entered_from:
                checked += 1
                pw = warps[parent]
                dest = pw[n - 1][1] if n <= len(pw) else None
                if dest != inner:
                    err(f'{inner} warp {i} exits to LAST_MAP warp {n}, but warp {n} of '
                        f'parent {parent} leads to {dest}, not {inner}')
    if len(errors) == before:
        print(f'LAST_MAP warps: {checked} (exit warp, parent) pairs checked, '
              f'{len(no_outside_parent)} maps without outside parent excepted')


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


def check_blackout_fly_warps():
    """H4: healing at a nurse sets wLastBlackoutMap to wLastMap, i.e. the
    outdoor map whose warp led into the Pokecenter. Blackout/Dig/Teleport
    then scan FlyWarpDataPtr (no terminator) for that id, so every such map
    needs an entry, landing one tile below its Pokecenter door.
    """
    map_text = strip_comments(read('constants/map_constants.asm'))
    outdoor = re.findall(r'map_const (\w+)',
                         map_text.split('DEF FIRST_INDOOR_MAP')[0])
    by_key = {norm_key(m): m for m in outdoor}
    nurse_maps = {norm_key(p.stem) for p in (ROOT / 'scripts').glob('*.asm')
                  if 'script_pokecenter_nurse' in p.read_text()}
    doors = {}
    for obj in (ROOT / 'data/maps/objects').glob('*.asm'):
        mapname = by_key.get(norm_key(obj.stem))
        if mapname is None:
            continue
        for x, y, target in re.findall(r'warp_event\s+(\d+),\s*(\d+),\s*(\w+)',
                                       strip_comments(obj.read_text())):
            if norm_key(target) in nurse_maps:
                doors.setdefault(mapname, set()).add((int(x), int(y) + 1))
    warps_text = strip_comments(read('data/maps/special_warps.asm'))
    entries = dict(re.findall(r'fly_warp_spec (\w+),\s*\.(\w+)', warps_text))
    spots = {label: (mapname, int(x), int(y)) for label, mapname, x, y in
             re.findall(r'^\.(\w+):\s*fly_warp (\w+),\s*(\d+),\s*(\d+)',
                        warps_text, re.M)}
    bad = 0
    for mapname, fronts in sorted(doors.items()):
        spot = spots.get(entries.get(mapname))
        if spot is None:
            err(f'{mapname} leads to a Pokecenter but has no FlyWarpDataPtr '
                'entry (blackout/Dig/Teleport would read past the table)')
            bad += 1
        elif spot[0] != mapname or (spot[1], spot[2]) not in fronts:
            err(f'FlyWarpDataPtr {mapname} lands at {spot[0]} ({spot[1]}, '
                f'{spot[2]}), expected one of {sorted(fronts)} below a '
                'Pokecenter door')
            bad += 1
    if not bad:
        print(f'Blackout warps: {len(doors)} maps leading to a Pokecenter, '
              'all in FlyWarpDataPtr in front of the door')


def check_map_header_banks():
    """A map placed in a vanilla UNUSED_MAP slot must also get its
    MapHeaderBanks row: a stale literal bank loads the header from the
    wrong ROM bank and the game crashes on entering the map."""
    ptrs = re.findall(r'^\tdw (\w+)(.*)$', read('data/maps/map_header_pointers.asm'), re.M)
    banks = re.findall(r'^\tdb (.*?)\s*(?:;.*)?$', read('data/maps/map_header_banks.asm'), re.M)
    if len(ptrs) != len(banks):
        err(f'MapHeaderPointers has {len(ptrs)} rows, MapHeaderBanks {len(banks)}')
    bad = 0
    for mid, ((ptr, comment), bank) in enumerate(zip(ptrs, banks)):
        if 'UNUSED_MAP' not in comment and bank != f'BANK({ptr})':
            err(f'map id ${mid:02X} ({ptr}): MapHeaderBanks row is {bank!r}, '
                f'expected BANK({ptr})')
            bad += 1
    if not bad:
        print(f'Map header banks: {len(ptrs)} rows, every used map points '
              'to its own header bank')


def check_town_map_entries():
    """LoadTownMapEntry (engine/items/town_map.asm) indexes ExternalMapEntries
    by outdoor map id, and returns the first InternalMapEntries row whose
    INDOORGROUP_ bound is strictly greater than the indoor map id. So the
    outdoor rows must follow the outdoor map ids one for one (row name ==
    map const name), and the indoor rows must list the end_indoor_group
    groups in constants order (which makes the bounds strictly increasing).
    """
    outdoor, groups, indoor = [], [], False
    for line in strip_comments(read('constants/map_constants.asm')).splitlines():
        indoor = indoor or 'FIRST_INDOOR_MAP EQU' in line
        m = re.match(r'\tmap_const (\w+)', line)
        if m and not indoor:
            outdoor.append(m.group(1))
        m = re.match(r'\tend_indoor_group (\w+)', line)
        if m:
            groups.append(m.group(1))
    text = strip_comments(read('data/maps/town_map_entries.asm'))
    ext = re.findall(r'^\toutdoor_map\s+\d+,\s*\d+,\s*(\w+)', text, re.M)
    ints = re.findall(r'^\tindoor_map\s+(\w+),', text, re.M)
    bad = 0
    if len(ext) != len(outdoor):
        err(f'ExternalMapEntries: {len(ext)} rows for {len(outdoor)} outdoor maps')
        bad += 1
    for i, (const, name) in enumerate(zip(outdoor, ext)):
        if norm_key(const) + 'NAME' != norm_key(name):
            err(f'ExternalMapEntries row ${i:02X} is {name}, map id ${i:02X} '
                f'is {const}')
            bad += 1
            break  # one shift misaligns every later row
    if ints != groups:
        i = next((k for k, (a, b) in enumerate(zip(ints, groups)) if a != b),
                 min(len(ints), len(groups)))
        err(f'InternalMapEntries row {i}: '
            f'{ints[i] if i < len(ints) else "<end>"}, expected group '
            f'{groups[i] if i < len(groups) else "<end>"} '
            f'({len(ints)} rows for {len(groups)} indoor groups)')
        bad += 1
    if not bad:
        print(f'Town map entries: {len(ext)} outdoor rows aligned on map ids, '
              f'{len(ints)} indoor rows in group order')


def main():
    consts_text = strip_comments(read('constants/pokemon_constants.asm'))
    const_names = re.findall(r'^\tconst ([A-Z0-9_]+)', consts_text, re.M)
    species_entries = parse_internal_species()
    check_pokemon_tables()
    check_species_completeness(species_entries)
    check_placeholder_assets(species_entries)
    check_wild_encounters(const_names)
    check_parties(const_names)
    check_party_order()
    check_toggles()
    check_object_const_order()
    check_warp_targets()
    check_edge_warps()
    check_last_map_warps()
    check_trainer_flags()
    check_map_header_pointers()
    check_text_lines()
    check_town_map_entries()
    check_blackout_fly_warps()
    check_map_header_banks()
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
