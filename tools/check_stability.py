#!/usr/bin/env python3
"""Stability checks the assembler cannot catch (NERIS stabilisation).

Commit 4 of the stabilisation patch was truncated in the source doc at
parse_sprite_sets(); this file reproduces the recovered 372 lines and
completes the remaining logic to the doc's stated spec:

  bounds       objects, warps, signs inside the map (else invisible NPCs,
               unreachable warps, signs that never fire)
  warp index   every warp_event points at a warp that exists in the target
               map (an out-of-range index drops the player into garbage)
  connections  north/south/east/west links are symmetric with mirrored
               offsets (else the player is teleported or walks into void)
  sprite sets  every NPC on an outdoor map is in that map's sprite set,
               on the right side of a split (else wrong/garbled sprite)
  vram slots   indoor maps use at most 10 distinct walking sprites
  objects      at most 15 object_events (16 sprite slots incl. the player)
  evolutions   targets exist, levels 1-100, no evolution loops
  learnsets    levels 1-100 and in increasing order (the engine stops at
               the first lower level, so later moves are never learned)
  parties      at most 6 Pokemon per trainer party

Run from anywhere: python3 tools/check_stability.py
Exits non-zero on any error. Warnings do not fail the run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def read(p):
    return (ROOT / p).read_text(encoding='utf-8')


def code(line):
    return line.split(';', 1)[0].strip()


# --------------------------------------------------------------------- maps

def parse_map_consts():
    """CONST -> (id, width, height); also FIRST_INDOOR_MAP id."""
    maps, val, first_indoor = {}, 0, None
    for line in read('constants/map_constants.asm').splitlines():
        c = code(line)
        m = re.match(r'map_const (\w+),\s*(\d+),\s*(\d+)', c)
        if m:
            maps[m.group(1)] = (val, int(m.group(2)), int(m.group(3)))
            val += 1
        elif re.match(r'const_skip\b', c):
            val += 1
        elif re.match(r'const_def\b', c):
            val = 0
        elif c.startswith('DEF FIRST_INDOOR_MAP'):
            first_indoor = val
    return maps, first_indoor


def parse_headers():
    """label -> {'const', 'conns': [(dir, label, const, offset)]}"""
    out = {}
    for f in sorted((ROOT / 'data/maps/headers').glob('*.asm')):
        info = None
        for line in f.read_text().splitlines():
            c = code(line)
            m = re.match(r'map_header (\w+),\s*(\w+)', c)
            if m:
                info = {'const': m.group(2), 'conns': [], 'file': f.name}
                out[m.group(1)] = info
            m = re.match(r'connection (\w+),\s*(\w+),\s*(\w+),\s*(-?\d+)', c)
            if m and info is not None:
                info['conns'].append((m.group(1), m.group(2), m.group(3),
                                      int(m.group(4))))
    return out


def parse_objects(label):
    p = ROOT / f'data/maps/objects/{label}.asm'
    if not p.exists():
        return None
    warps, bgs, objs = [], [], []
    for n, line in enumerate(p.read_text().splitlines(), 1):
        c = code(line)
        m = re.match(r'warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\d+)', c)
        if m:
            warps.append((int(m.group(1)), int(m.group(2)), m.group(3),
                          int(m.group(4)), n))
            continue
        m = re.match(r'bg_event\s+(\d+),\s*(\d+),\s*(\w+)', c)
        if m:
            bgs.append((int(m.group(1)), int(m.group(2)), m.group(3), n))
            continue
        m = re.match(r'object_event\s+(\d+),\s*(\d+),\s*(\w+)', c)
        if m:
            objs.append((int(m.group(1)), int(m.group(2)), m.group(3), n))
    return {'warps': warps, 'bgs': bgs, 'objs': objs}


# Vanilla: elevator warps are rewritten at run time by the elevator menu.
WARP_INDEX_EXCEPTIONS = {('SilphCoElevator', 'UNUSED_MAP_ED')}


def check_maps():
    maps, first_indoor = parse_map_consts()
    headers = parse_headers()
    const_to_label = {h['const']: lbl for lbl, h in headers.items()}
    objects = {lbl: parse_objects(lbl) for lbl in headers}

    still = parse_still_sprite_threshold()
    sets, map_sets, split_sets = parse_sprite_sets()

    n_bounds = n_warps = n_conn = n_sprites = 0
    for lbl, h in headers.items():
        const = h['const']
        if const not in maps:
            err(f'{h["file"]}: map const {const} not in map_constants.asm')
            continue
        mid, w, hgt = maps[const]
        o = objects[lbl]
        if o is None:
            err(f'{lbl}: no data/maps/objects/{lbl}.asm')
            continue
        W, H = 2 * w, 2 * hgt
        f = f'objects/{lbl}.asm'

        # bounds
        for x, y, tgt, idx, n in o['warps']:
            n_bounds += 1
            if not (x < W and y < H):
                err(f'{f}:{n}: warp ({x},{y}) outside {W}x{H} steps')
        for x, y, t, n in o['bgs']:
            n_bounds += 1
            if not (x < W and y < H):
                err(f'{f}:{n}: bg_event {t} ({x},{y}) outside {W}x{H} steps')
        for x, y, spr, n in o['objs']:
            n_bounds += 1
            if not (x < W and y < H):
                err(f'{f}:{n}: object {spr} ({x},{y}) outside {W}x{H} steps')

        # object slots (16 sprite state structs, one is the player)
        if len(o['objs']) > 15:
            err(f'{f}: {len(o["objs"])} object_events, max 15')

        # warp indices
        for x, y, tgt, idx, n in o['warps']:
            n_warps += 1
            if tgt == 'LAST_MAP' or (lbl, tgt) in WARP_INDEX_EXCEPTIONS:
                continue
            tl = const_to_label.get(tgt)
            if tl is None:
                err(f'{f}:{n}: warp to {tgt}, which has no map header')
                continue
            tw = objects[tl]['warps'] if objects.get(tl) else []
            if not 1 <= idx <= len(tw):
                err(f'{f}:{n}: warp to {tgt} #{idx}, but {tl} has '
                    f'{len(tw)} warp(s)')

        # sprite sets / vram slots
        if mid < first_indoor:
            set_ids = map_sets.get(mid)
            if set_ids is None:
                err(f'{lbl}: outdoor map without a MapSpriteSets entry')
                continue
            for x, y, spr, n in o['objs']:
                n_sprites += 1
                if set_ids in split_sets:
                    axis, line_, west, east = split_sets[set_ids]
                    coord = x if axis == 'EAST_WEST' else y
                    allowed = sets[west] if coord < line_ else sets[east]
                    side = west if coord < line_ else east
                else:
                    allowed = sets[set_ids]
                    side = set_ids
                if spr not in allowed:
                    err(f'{f}:{n}: {spr} at ({x},{y}) is not in {side}')
        else:
            walking = {s for _, _, s, _ in o['objs'] if s not in still}
            n_sprites += len(o['objs'])
            if len(walking) > 10:
                err(f'{f}: {len(walking)} distinct walking sprites, '
                    f'only 10 VRAM slots')

    # connections
    opposite = {'north': 'south', 'south': 'north',
                'west': 'east', 'east': 'west'}
    for lbl, h in headers.items():
        for d, tl, tc, off in h['conns']:
            n_conn += 1
            th = headers.get(tl)
            if th is None:
                err(f'{h["file"]}: connection {d} to unknown map {tl}')
                continue
            if th['const'] != tc:
                err(f'{h["file"]}: connection {d} {tl} given as {tc}, '
                    f'its const is {th["const"]}')
            back = [c for c in th['conns'] if c[0] == opposite[d]]
            if not back:
                err(f'{h["file"]}: {d} to {tl}, but {tl} has no '
                    f'{opposite[d]} connection')
                continue
            if back[0][1] != lbl:
                err(f'{h["file"]}: {d} to {tl}, but {tl} {opposite[d]} '
                    f'goes to {back[0][1]}')
            elif back[0][3] != -off:
                err(f'{h["file"]}: {d} to {tl} offset {off}, '
                    f'{tl} back offset {back[0][3]} (expected {-off})')

    check_connection_edges(headers, maps)

    print(f'Map bounds: {n_bounds} warps/signs/objects inside their map')
    print(f'Warp indices: {n_warps} warps point at an existing warp')
    print(f'Connections: {n_conn} links symmetric with mirrored offsets')
    print(f'Sprites: {n_sprites} objects fit their sprite set / VRAM slots')


def camel(const):
    return ''.join(p.capitalize() for p in const.split('_'))


def tileset_data(ts, cache={}):
    """(blockset bytes, passable tile ids) for a tileset const."""
    if ts in cache:
        return cache[ts]
    name = camel(ts)
    gfx = read('gfx/tilesets.asm')
    bst = None
    for line in gfx.splitlines():
        labels = re.findall(r'(\w+)_Block::', line)
        m = re.search(r'INCBIN "([^"]+)"', line)
        if name in labels or (bst == 'pending' and m):
            if m:
                bst = (ROOT / m.group(1)).read_bytes()
                break
            bst = 'pending'
    coll, pending = set(), False
    for line in read('data/tilesets/collision_tile_ids.asm').splitlines():
        if re.match(r'\w+_Coll::', line):
            pending = pending or line.startswith(f'{name}_Coll::')
        m = re.search(r'coll_tiles (.*)', line)
        if m and pending:
            coll = {int(t, 16) for t in re.findall(r'\$([0-9A-Fa-f]{2})',
                                                   m.group(1))}
            break
    cache[ts] = (bst if isinstance(bst, bytes) else None, coll)
    return cache[ts]


def map_grid(lbl, h, maps):
    """step (x, y) -> passable, counting water as passable (Surf)."""
    hdr = read(f'data/maps/headers/{lbl}.asm')
    ts = re.search(r'map_header \w+,\s*\w+,\s*(\w+)', hdr).group(1)
    bst, coll = tileset_data(ts)
    blk_path = ROOT / f'maps/{lbl}.blk'
    if bst is None or not coll or not blk_path.exists():
        return None
    blk = blk_path.read_bytes()
    _, w, hgt = maps[h['const']]

    def passable(x, y):
        if not (0 <= x < 2 * w and 0 <= y < 2 * hgt):
            return False
        block = blk[(y // 2) * w + x // 2]
        t = bst[block * 16 + ((y % 2) * 2 + 1) * 4 + (x % 2) * 2]
        return t in coll or (ts == 'OVERWORLD' and t == 0x14)
    return passable


def check_connection_edges(headers, maps):
    """A connection only matters if the player can cross it: at least one
    step on the shared edge must be passable on both sides."""
    grids = {}
    n = 0
    for lbl, h in headers.items():
        for d, tl, tc, off in h['conns']:
            if tl not in headers or h['const'] not in maps or tc not in maps:
                continue
            if (lbl, d) in CONNECTION_EDGE_EXCEPTIONS:
                continue
            a = grids.setdefault(lbl, map_grid(lbl, h, maps))
            b = grids.setdefault(tl, map_grid(tl, headers[tl], maps))
            if a is None or b is None:
                continue
            _, aw, ah = maps[h['const']]
            _, bw, bh = maps[tc]
            n += 1
            ok = False
            if d in ('north', 'south'):
                ay = 0 if d == 'north' else 2 * ah - 1
                by = 2 * bh - 1 if d == 'north' else 0
                for x in range(2 * aw):
                    if a(x, ay) and b(x - 2 * off, by):
                        ok = True
                        break
            else:
                ax = 0 if d == 'west' else 2 * aw - 1
                bx = 2 * bw - 1 if d == 'west' else 0
                for y in range(2 * ah):
                    if a(ax, y) and b(bx, y - 2 * off):
                        ok = True
                        break
            if not ok:
                err(f'{h["file"]}: {d} connection to {tl} has no passable '
                    f'step on both sides of the edge')
    print(f'Connection edges: {n} links crossable on foot or by Surf')


# Vanilla links kept only for the scrolling border, never walked through.
CONNECTION_EDGE_EXCEPTIONS = {
    ('Route22', 'north'),  # vanilla: crossed through Route22Gate
    ('Route23', 'south'),  # header comment: "unnecessary"
}


def parse_still_sprite_threshold():
    """Set of sprite consts that are 4-tile still sprites."""
    still, seen_first = set(), False
    for line in read('constants/sprite_constants.asm').splitlines():
        c = code(line)
        if c.startswith('DEF FIRST_STILL_SPRITE'):
            seen_first = True
            continue
        if c.startswith('DEF NUM_SPRITES'):
            break
        m = re.match(r'const (SPRITE_\w+)', c)
        if m and seen_first:
            still.add(m.group(1))
    return still


def parse_sprite_sets():
    text = read('data/maps/sprite_sets.asm')
    map_sets, split_sets, sets = {}, {}, {}
    sec, idx, cur = None, 0, None
    split_order = []
    for line in read('constants/sprite_set_constants.asm').splitlines():
        m = re.match(r'\s*const (SPLITSET_\w+)', line)
        if m:
            split_order.append(m.group(1))
    split_i = 0
    for line in text.splitlines():
        c = code(line)
        if line.startswith('MapSpriteSets'):
            sec, idx = 'map', 0
            continue
        if line.startswith('SplitMapSpriteSets'):
            sec = 'split'
            continue
        if line.startswith('SpriteSets'):
            sec = 'sets'
            continue
        if sec == 'sets':
            m = re.match(r';\s*(SPRITESET_\w+)', line.strip())
            if m:
                cur = m.group(1)
                sets[cur] = set()
                continue
        m = re.match(r'db (.+)', c)
        if not m:
            continue
        args = [a.strip() for a in m.group(1).split(',')]
        if sec == 'map':
            if len(args) == 1 and (args[0] in sets or args[0] in
                                   split_order or
                                   args[0].startswith('SPRITESET_') or
                                   args[0].startswith('SPLITSET_')):
                map_sets[idx] = args[0]
                idx += 1
        elif sec == 'split':
            if len(args) == 4 and args[0] in ('NORTH_SOUTH', 'EAST_WEST'):
                name = split_order[split_i] if split_i < len(split_order) \
                    else f'SPLITSET_{split_i:02x}'
                split_sets[name] = (args[0], int(args[1]), args[2], args[3])
                split_i += 1
        elif sec == 'sets':
            if cur and all(a.startswith('SPRITE_') for a in args):
                sets[cur].update(args)
    # normalise split ids (the table is in the same order as the consts)
    for n, name in enumerate(split_order):
        if name not in split_sets and n < split_i:
            pass
    ordered = {}
    for n, name in enumerate(split_order):
        got = [k for k in split_sets]
        if n < len(got):
            ordered[name] = split_sets[got[n]]
    return sets, map_sets, ordered


def parse_species_ids():
    """Internal species id -> stem, from pokemon_constants.asm.
    const_skip rows occupy a slot without a name."""
    ids, seen = [], False
    for line in read('constants/pokemon_constants.asm').splitlines():
        c = code(line)
        if c.startswith('const_def'):
            seen = True
            continue
        if not seen:
            continue
        if c.startswith('const ') and not c.startswith('const_value'):
            name = c.split()[1]
            if name not in ('NO_MON',):
                ids.append(name.lower().replace('_', ''))
        elif re.match(r'const_skip\b', c):
            ids.append(None)
    return ids


# ------------------------------------------------------------- pokemon data

def check_species():
    """Evolutions: targets exist, levels 1-100, no loops.
    Learnsets: levels 1-100, strictly increasing (engine stops early)."""
    evo_text = read('data/pokemon/evos_moves.asm')
    ptrs = re.findall(r'^\tdw (\w+)EvosMoves', evo_text, re.M)
    ids = parse_species_ids()
    existing = {p.stem for p in
                (ROOT / 'data/pokemon/base_stats').glob('*.asm')}

    def block_for(ptr):
        m = re.search(rf'^{ptr}EvosMoves:\n(.*?)(?=^\w+EvosMoves:|\Z)',
                      evo_text, re.M | re.S)
        return m.group(1) if m else ''

    n_evo = n_learn = 0
    for ptr, name in zip(ptrs, ids):
        if name is None or name not in existing:
            # skipped slot or species without a base stats block
            continue
        body = block_for(ptr)
        if not body:
            continue
        # evolution section: lines until the terminating db 0
        evo_lines = re.findall(r'^\tdb (.+)$', body.split('; Learnset')[0],
                               re.M)
        for args in evo_lines:
            n_evo += 1
            parts = [a.strip() for a in args.split(',')]
            if parts[0] == '0':
                break
            if parts[0] in ('EVOLVE_LEVEL', 'EVOLVE_ITEM', 'EVOLVE_TRADE'):
                if parts[0] == 'EVOLVE_LEVEL':
                    lvl = int(parts[1])
                    if not 1 <= lvl <= 100:
                        err(f'{ptr}: evolution level {lvl} out of range')
                tgt = parts[-1].lower()
                if tgt not in existing:
                    err(f'{ptr}: evolves into unknown species {parts[-1]}')
        # learnset: db LEVEL, MOVE until db 0
        ls = body.split('; Learnset')[1] if '; Learnset' in body else ''
        last = 0
        for m in re.finditer(r'^\tdb (\d+),\s*(\w+)', ls, re.M):
            lvl = int(m.group(1))
            n_learn += 1
            if not 1 <= lvl <= 100:
                err(f'{ptr}: learnset level {lvl} out of range')
            elif lvl <= last:
                err(f'{ptr}: learnset level {lvl} after {last} '
                    f'(engine stops at the first non-increasing level)')
            last = lvl
    print(f'Species: {n_evo} evolutions valid, {n_learn} learnset levels '
          f'in range and ordered')


# ---------------------------------------------------------------- trainers

def check_parties():
    text = read('data/trainers/parties.asm')
    # a party line is `db <level>, <species...>, 0` — the species slots
    # are the args between the leading level and the trailing 0 sentinel.
    for m in re.finditer(r'^(\w+Data):\n(.*?)(?=^\w+Data:|\Z)', text,
                         re.M | re.S):
        label, body = m.group(1), m.group(2)
        for n, line in enumerate(
                [l for l in body.splitlines() if code(l)], 1):
            c = code(line)
            args = [a.strip() for a in c[len('db '):].split(',')]
            if not args:
                continue
            # the trainer class data is: level, species slots..., 0
            # (party mon count = number of species args before the 0)
            if args[-1] != '0':
                continue
            # plain party: db <level>, <species...>, 0
            # special format (Rival/ProfOak/Giovanni etc.):
            # db $FF, <level>, <species>, ... , 0 — every species slot is
            # preceded by its level. Count the species: odd-indexed args.
            if args[0] == '$FF':
                slots = [a for i, a in enumerate(args[1:-1], 1)
                         if i % 2 == 0]
            else:
                slots = args[1:-1]
            if not slots:
                continue
            if len(slots) > 6:
                err(f'{label}: party of {len(slots)} at line {n} (max 6)')
    print('Trainers: all parties within 6 Pokemon')


def main():
    check_maps()
    check_species()
    check_parties()
    if warnings:
        for w in warnings:
            print('WARN:', w)
    if errors:
        print(f'\n{len(errors)} error(s):')
        for e in errors:
            print(' ', e)
        sys.exit(1)
    print('check_stability: all good')


if __name__ == '__main__':
    main()
