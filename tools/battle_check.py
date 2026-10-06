"""Stage helpers for tools/smoke_test.py.

walk_to_town: from the new-game state (player in bed on the SNES tile,
bedroom REDS_HOUSE_2F) mash through the intro, close the SNES text box,
walk down to 1F and out of the house until wCurMap == PALLET_TOWN
(Port-Lune, map 0).

run_stage_battle: from Port-Lune, walk north into the Route 1 grass
(Sentier Embruns) until a wild battle starts, then verify the enemy
sprite was loaded from the right pic:
  - wEnemyMonSpecies must be set (wIsInBattle is unreliable in this
    fork: it reads 34 during battles);
  - wMonHFrontSprite must equal the *PicFront address declared in the
    species' base_stats file (what tools/check_rom.py expects);
  - the decompressed sprite buffers must not be empty.

Walking uses render=False frames for speed; only occasional frames are
rendered so screenshots stay available.

The battle screenshot is saved to docs/smoke_battle.png for review.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_rom as cr  # noqa: E402

REDS_HOUSE_2F = 38  # 0x26, bedroom (new-game spawn)
REDS_HOUSE_1F = 37  # 0x25
PALLET_TOWN = 0     # Port-Lune


def _tables():
    dexval, v = {}, 1
    for line in (ROOT / "constants/pokedex_constants.asm").read_text().splitlines():
        m = re.match(r"\tconst DEX_(\w+)", line)
        if m:
            dexval[m.group(1)] = v
            v += 1
        elif re.match(r"\s*const_skip\b", line):
            v += 1
    types = cr.type_map()
    id2const = {i: c for c, i in cr.internal_ids().items()}
    return dexval, types, id2const


def _wram_addr(syms, name):
    _, addr = syms[name]
    # PyBoy memory[] does not implement the echo mirror; D000-DFFF is
    # real WRAM, read directly.
    return addr


def _press(pb, key, frames):
    pb.button_press(key)
    for _ in range(frames):
        pb.tick(1, False)
    pb.button_release(key)
    pb.tick(2, False)


def _close_box(pb):
    """Advance past any open text (B skips pages and closes at the end)."""
    for _ in range(4):
        _press(pb, "b", 10)


# Port-Lune town navigation: walk to (5,0) (the north exit opening)
# with BFS over the 10x9 grid, learning blocked tiles as moves fail.
# Needed because the fork's warp wiring is broken (LIGHTHOUSE warp at
# (15,13) is out of bounds for the 10x9 map, shifting LAST_MAP warp
# indices): the house-exit spawn lands on the beach instead of the
# door, so a fixed route is fragile.
_TOWN_W, _TOWN_H = 10, 9


def _navigate(pb, wram, tx, ty, frames, step_frames=25, budget=3000,
              state=None):
    if state is None:
        state = {"blocked": set()}
    blocked = state["blocked"]
    doors = {(5, 5)}  # warp tiles: reaching them warps away, avoid
    while frames < budget and wram("wCurMap") == PALLET_TOWN:
        sx, sy = wram("wXCoord"), wram("wYCoord")
        if (sx, sy) == (tx, ty):
            # standing on the exit opening: step north into Route 1
            _press(pb, "up", 40)
            frames += 42
            return wram("wCurMap") != PALLET_TOWN, frames
        # BFS from (sx,sy) to (tx,ty) on the walkable-so-far grid
        from collections import deque
        prev, seen = {}, {(sx, sy)}
        q = deque([(sx, sy)])
        goal = None
        while q:
            cx, cy = q.popleft()
            if (cx, cy) == (tx, ty):
                goal = (cx, cy)
                break
            for dx, dy, k in ((0, -1, "up"), (0, 1, "down"),
                              (-1, 0, "left"), (1, 0, "right")):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < _TOWN_W and 0 <= ny < _TOWN_H and \
                        (nx, ny) not in blocked and (nx, ny) not in doors \
                        and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    prev[(nx, ny)] = (cx, cy, k)
                    q.append((nx, ny))
        if goal is None:
            return False, frames
        path = []
        cur = goal
        while cur != (sx, sy):
            px, py, k = prev[cur]
            path.append((k, cur))
            cur = (px, py)
        for k, target in path:
            _press(pb, k, step_frames)
            frames += step_frames + 2
            nx, ny = wram("wXCoord"), wram("wYCoord")
            if (nx, ny) == target:
                continue
            # move failed or warped elsewhere
            if wram("wCurMap") != PALLET_TOWN:
                return (nx, ny) == (tx, ty), frames
            blocked.add(target)
            break
    return wram("wCurMap") != PALLET_TOWN, frames


def walk_to_town(pb, wram, max_frames=60 * 300):
    """Intro -> bedroom -> 1F -> Port-Lune. Returns (ok, message).

    State-driven: the caller may invoke this repeatedly and the intro
    may hand control to us at any point (bedroom 38, 1F 37, town 0).
    """
    frames = 0
    while frames < max_frames:
        m = wram("wCurMap")
        if m == PALLET_TOWN:
            if wram("wYCoord") != 0:
                return True, f"Port-Lune reached after {frames} frames"
            # town position not initialised yet: keep going
            _press(pb, "a", 14)
            frames += 14
        elif m == REDS_HOUSE_2F:
            # advance the intro dialogs, close the SNES box (spawn is on
            # its tile), then sweep: out of bed (3,6), to the stairs
            # warp at (7,1)
            for _ in range(30):
                _press(pb, "a", 14)
                frames += 14
            _close_box(pb)
            frames += 44
            for key, f in (("down", 70), ("right", 90), ("up", 100),
                           ("left", 40)):
                if wram("wCurMap") != REDS_HOUSE_2F:
                    break
                _press(pb, key, f)
                frames += f + 2
        elif m == REDS_HOUSE_1F:
            # close any text, then from the stairs (7,1) go down to the
            # bottom row and right/left toward the door at (2..3,7)
            _close_box(pb)
            frames += 44
            for key, f in (("down", 100), ("right", 100), ("left", 60)):
                _press(pb, key, f)
                frames += f + 2
                if wram("wCurMap") == PALLET_TOWN:
                    break
        else:
            # intro / naming screens: mash A
            _press(pb, "a", 14)
            frames += 14
    return False, (f"timed out after {frames} frames "
                   f"(map={wram('wCurMap')}, y={wram('wYCoord')}, "
                   f"x={wram('wXCoord')})")


def _step_to(pb, wram, key, done, max_tries=14, step_frames=22):
    """Walk in `key` until done() or stuck; returns frames used."""
    frames = 0
    for _ in range(max_tries):
        if done():
            break
        last = (wram("wXCoord"), wram("wYCoord"))
        _press(pb, key, step_frames)
        frames += step_frames + 2
        if (wram("wXCoord"), wram("wYCoord")) == last:
            break  # blocked
    return frames


def _walk_town_exit(pb, wram, frames):
    """Walk to the north exit (5,0) then step into Route 1. Closes any
    NPC dialog after every press: the wandering girl NPC frequently
    intercepts the player and a pending dialog swallows all inputs,
    which reads as a blocked tile. The 10x9 Port-Lune layout: spawn
    (4..5,6..8), column x=1 walkable rows 8..3 (rows 2-1 blocked at
    row 2 x1=0x08 but row 1 x1=0x01 walkable), row 3 fully walkable,
    exit opening (5,0) with (5,1)=0x01 grass and (5,2)=0x08 tree.

    Route: up to row 3, west to x=1, north to row 1, east to x=5,
    north through the opening.
    """
    def step(k, f=10):
        nonlocal frames
        _press(pb, k, f)
        frames += f + 2
        _close_box(pb)

    def xy():
        return wram("wXCoord"), wram("wYCoord")

    # The house door is directly above the spawn (5,5): step west
    # FIRST (along row 6/7 to x=1), then north up the clear left
    # column to row 1, east to the exit column, then out.
    for _ in range(5):
        if xy()[0] <= 1 or wram("wCurMap") != PALLET_TOWN:
            break
        step("left")
    for _ in range(7):
        if xy()[1] <= 1 or wram("wCurMap") != PALLET_TOWN:
            break
        step("up")
    for _ in range(6):
        if xy()[0] >= 5 or wram("wCurMap") != PALLET_TOWN:
            break
        step("right")
    for _ in range(3):
        if xy()[1] == 0 or wram("wCurMap") != PALLET_TOWN:
            break
        step("up")
    if wram("wCurMap") == PALLET_TOWN and xy()[1] == 0:
        step("up", 18)
    return frames


def run_stage_battle(pb, wram, hold, syms, max_frames=60 * 180):
    """Returns (ok, message). Called after the world stage (Port-Lune)."""
    dexval, types, id2const = _tables()

    # leave any open menu/text
    _close_box(pb)

    # walk north into the Route 1 grass until a wild battle starts
    # (wIsInBattle is unreliable in this fork; use wEnemyMonSpecies).
    # The house door sits at the exit spawn: clear it rightwards first.
    frames = 0
    nav_state = {"blocked": set()}
    while frames < max_frames:
        m = wram("wCurMap")
        if m == REDS_HOUSE_1F:
            # walked back into the house: escape again (door at 2..3,7)
            _close_box(pb)
            frames += 44
            for key, f in (("down", 100), ("right", 100), ("left", 60)):
                _press(pb, key, f)
                frames += f + 2
                if wram("wCurMap") == PALLET_TOWN:
                    break
            continue
        if m == PALLET_TOWN:
            f0 = frames
            frames = _walk_town_exit(pb, wram, frames)
            if frames == f0 and wram("wCurMap") == PALLET_TOWN:
                # no progress at all: nudge so the loop advances
                _press(pb, "up", 60)
                frames += 62
        else:
            # Route 1: keep pushing north into the grass
            for key, f in (("up", 110), ("right", 40), ("up", 110),
                           ("left", 40)):
                _press(pb, key, f)
                frames += f + 2
        if wram("wEnemyMonSpecies"):
            break
    else:
        return False, (f"no wild battle after {frames} frames of walking "
                       f"(map={wram('wCurMap')}, y={wram('wYCoord')})")

    # let the battle intro play out a bit
    pb.tick(60 * 3, True)

    species = wram("wEnemyMonSpecies")
    const = id2const.get(species)
    if const is None:
        return False, f"unknown enemy species id {species:#04x}"
    exp = cr.parse_base_stats(const, dexval, types)
    front_label = exp["front_label"] + "PicFront"

    hdr = _wram_addr(syms, "wMonHeader") + 1  # wMonHFrontSprite
    front_ptr = pb.memory[hdr] | (pb.memory[hdr + 1] << 8)

    want = cr.load_sym().get(front_label)
    shot = ROOT / "docs" / "smoke_battle.png"
    pb.screen.image.save(shot)

    if want is None:
        return False, f"{front_label} not found in .sym"
    got = front_ptr & 0x3FFF
    if got != want[1] & 0x3FFF:
        return False, (f"enemy front sprite points to {got:#06x}, "
                       f"expected {front_label} at {want[1] & 0x3FFF:#06x}")

    # decompressed sprite buffers live in SRAM (sSpriteBuffer0..2):
    # neither empty nor uniform
    distinct = set()
    for symname in ("sSpriteBuffer0", "sSpriteBuffer1"):
        _, a = syms[symname]
        base = 0xA000 + (a & 0x1FFF)
        distinct.update(bytes(pb.memory[base:base + 0x2A0]))
    if len(distinct) < 8:
        return False, (f"sprite buffers look empty ({len(distinct)} distinct "
                       f"byte values)")
    return True, (f"wild battle ok: {const} (id {species:#04x}), front ptr "
                  f"{got:#06x} == {front_label}, buffers fine "
                  f"({len(distinct)} distinct bytes), "
                  f"screenshot {shot.relative_to(ROOT)}")
