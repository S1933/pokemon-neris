"""Stage helpers for tools/smoke_test.py.

walk_to_town: from the new-game state (player in bed on the SNES tile,
bedroom REDS_HOUSE_2F) mash through the intro, close the SNES text box,
walk down to 1F and out of the house until wCurMap == PALLET_TOWN
(Port-Lune, map 0).

run_stage_battle: from Port-Lune, play the real opening (Prof. Sylve
cutscene at the north exit, starter in the lab, battle against Kael, out
of the lab), walk north into the Route 1 grass (Sentier Embruns) until a
wild battle starts (wIsInBattle == 1), then verify the enemy sprite was
loaded from the right pic:
  - wEnemyMonSpecies must be set;
  - wMonHFrontSprite must equal the *PicFront address declared in the
    species' base_stats file (what tools/check_rom.py expects);
  - the decompressed sprite buffers must not be empty.

The bot is driven by WRAM state (map, step coordinates, text/joypad
locks, party, battle flag), never by a fixed route; it is deterministic
for a given ROM. Walking uses render=False frames for speed.

The battle screenshot is saved to smoke_battle.png (git-ignored) for review.
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


# Step-grid navigation. wXCoord/wYCoord count steps (2 per block), so a
# map is 2*wCurMapWidth x 2*wCurMapHeight steps (20x18 for Port-Lune).
# Collisions are learnt: a free step that does not move the player
# marks its target blocked (forgotten when no path is left, so a
# wandering NPC only blocks a tile for a while). Warp tiles other than
# the goal are avoided.
OAKS_LAB = 40       # 0x28
ROUTE_1 = 12        # 0x0C
PAD_CTRL_PAD = 0xF0
_DIRS = (("up", 0, -1), ("down", 0, 1), ("left", -1, 0), ("right", 1, 0))


def _free(wram):
    """True when the overworld takes d-pad input: no text box or menu
    (wFontLoaded bit 0), no scripted d-pad lock (wJoyIgnore), no battle."""
    return not (wram("wFontLoaded") & 1 or wram("wJoyIgnore") & PAD_CTRL_PAD
                or wram("wIsInBattle"))


def _settle(pb, wram, limit=40):
    """Tick until the current step animation is over."""
    n = 0
    while wram("wWalkCounter") and n < limit:
        pb.tick(1, False)
        n += 1
    pb.tick(1, False)
    return n + 1


def _step(pb, wram, key, limit=24):
    """Hold `key` until the player moves, the map changes or the game
    takes control; returns the frames used."""
    start = (wram("wCurMap"), wram("wXCoord"), wram("wYCoord"))
    pb.button_press(key)
    n = 0
    while n < limit:
        pb.tick(1, False)
        n += 1
        if (wram("wCurMap"), wram("wXCoord"), wram("wYCoord")) != start \
                or not _free(wram):
            break
    pb.button_release(key)
    return n + _settle(pb, wram)


def _warps(pb, syms):
    base = _wram_addr(syms, "wWarpEntries")
    n = pb.memory[_wram_addr(syms, "wNumberOfWarps")]
    return {(pb.memory[base + 4 * i + 1], pb.memory[base + 4 * i])
            for i in range(n)}


def _first_move(start, goal, w, h, avoid):
    """BFS on the step grid; first direction of a shortest path or None."""
    from collections import deque
    first = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            return first[cur]
        for k, dx, dy in _DIRS:
            nxt = (cur[0] + dx, cur[1] + dy)
            if 0 <= nxt[0] < w and 0 <= nxt[1] < h and nxt not in first \
                    and (nxt == goal or nxt not in avoid):
                first[nxt] = first[cur] or k
                q.append(nxt)
    return None


def _goal(wram):
    """(x, y, action) for the current map and progress: walk to (x, y),
    then press each key of `action`. None when the bot has nowhere to go."""
    m, has_mon = wram("wCurMap"), wram("wPartyCount") > 0
    if m == PALLET_TOWN:
        # no starter: step onto the north-exit row (y=1), which starts
        # the vanilla Prof. Sylve cutscene (PalletTownDefaultScript);
        # with a starter: leave north into Route 1
        return (10, 1, ()) if not has_mon else (10, 0, ("up",))
    if m == OAKS_LAB:
        # no starter: face the middle Poke Ball (7,3) from below and
        # take it; then leave through the bottom-edge exit (4,11)
        return (7, 4, ("up", "a")) if not has_mon else (4, 11, ("down",))
    if m == ROUTE_1:
        return (10, 0, ("up",))  # northwards, until grass is found
    return None


def _on_grass(pb, syms):
    """The game's own test (TryDoWildEncounter): the tile at screen
    (9,9) of the step the player stands on is the tileset's grass tile."""
    tile = pb.memory[_wram_addr(syms, "wTileMap") + 20 * 9 + 9]
    return tile == pb.memory[_wram_addr(syms, "wGrassTile")]


def _play_to_wild_battle(pb, wram, syms, max_frames, trainer_battles):
    """Play from Port-Lune until a wild battle starts on Route 1.
    A advances every text, cutscene, menu and battle that holds the
    d-pad (YES to the starter, FIGHT and the first move against Kael).
    Maps where a trainer battle was fought go into `trainer_battles`.
    Returns (ok, frames)."""
    frames, blocked, grass = 0, {}, None
    while frames < max_frames:
        m = wram("wCurMap")
        if m == ROUTE_1 and wram("wIsInBattle") == 1:
            return True, frames
        if wram("wIsInBattle") == 2:
            trainer_battles.add(m)
        if not _free(wram):
            _press(pb, "a", 4)
            frames += 6
            continue
        pos = (wram("wXCoord"), wram("wYCoord"))
        if m == ROUTE_1 and grass is None and _on_grass(pb, syms):
            grass = pos
        # on Route 1, pace off and back onto the first grass step: each
        # step onto it rolls a wild encounter
        goal = (*grass, ("pace",)) if m == ROUTE_1 and grass else _goal(wram)
        if goal is None:
            return False, frames
        gx, gy, action = goal
        if pos == (gx, gy):
            pb.tick(1, False)  # a goal with no action waits for a script
            frames += 1
            for k in action:
                if k == "a":
                    _press(pb, "a", 4)
                    frames += 6
                elif k == "pace":
                    for d, _, _ in _DIRS:
                        frames += _step(pb, wram, d)
                        if (wram("wXCoord"), wram("wYCoord")) != pos:
                            break
                else:
                    frames += _step(pb, wram, k)
            continue
        w, h = 2 * wram("wCurMapWidth"), 2 * wram("wCurMapHeight")
        seen = blocked.setdefault(m, set())
        avoid = seen | (_warps(pb, syms) - {(gx, gy)})
        k = _first_move(pos, (gx, gy), w, h, avoid)
        if k is None:
            seen.clear()  # an NPC may have moved: relearn
            k = _first_move(pos, (gx, gy), w, h, _warps(pb, syms))
            if k is None:  # mid-warp: the map header is still loading
                pb.tick(1, False)
                frames += 1
                continue
        frames += _step(pb, wram, k)
        if _free(wram) and wram("wCurMap") == m and \
                (wram("wXCoord"), wram("wYCoord")) == pos:
            dx, dy = {d: (x, y) for d, x, y in _DIRS}[k]
            seen.add((pos[0] + dx, pos[1] + dy))
    return False, frames


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


def run_stage_battle(pb, wram, hold, syms, max_frames=60 * 600):
    """Returns (ok, message). Called after the world stage (Port-Lune)."""
    dexval, types, id2const = _tables()

    # leave any open menu/text
    _close_box(pb)

    fought = set()
    ok, frames = _play_to_wild_battle(pb, wram, syms, max_frames, fought)
    if not ok:
        return False, (f"no wild battle after {frames} frames of play "
                       f"(map={wram('wCurMap')}, x={wram('wXCoord')}, "
                       f"y={wram('wYCoord')}, party={wram('wPartyCount')})")
    if OAKS_LAB not in fought:
        return False, "wild battle reached without the Kael battle in the lab"

    # let the battle intro play out a bit (the sprite buffers are checked
    # while the enemy pic is still decompressed in them)
    pb.tick(60 * 3, False)

    species = wram("wEnemyMonSpecies")
    const = id2const.get(species)
    if const is None:
        return False, f"unknown enemy species id {species:#04x}"
    exp = cr.parse_base_stats(const, dexval, types)
    front_label = exp["front_label"] + "PicFront"

    hdr = _wram_addr(syms, "wMonHFrontSprite")
    front_ptr = pb.memory[hdr] | (pb.memory[hdr + 1] << 8)

    want = cr.load_sym().get(front_label)

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
    # the screen is still dark at 3s: capture "Wild ... appeared!", where
    # the game waits for A
    pb.tick(60 * 7, False)
    pb.tick(1, True)
    shot = ROOT / "smoke_battle.png"
    pb.screen.image.save(shot)
    return True, (f"wild battle ok: {const} (id {species:#04x}), front ptr "
                  f"{got:#06x} == {front_label}, buffers fine "
                  f"({len(distinct)} distinct bytes), "
                  f"screenshot {shot.relative_to(ROOT)}; reached after "
                  f"{frames} frames of play (starter taken, Kael fought "
                  f"in the lab)")
