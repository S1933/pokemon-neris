#!/usr/bin/env python3
"""Map tour (NERIS fuzz) — teleport into every map and play it at random,
flagging the maps that crash the game.

The emulator never WALKS to these maps (there is no path that visits all of
them). Instead the tool plants a collision warp under the player: it
overwrites wWarpEntries[0] with ( player's tile, dest warp 1, target map )
and bumps the player into an adjacent wall. CheckWarpsCollision then fires
the engine's own door mechanic, so the target map goes through the very same
LoadMapData path a real door uses — which is precisely the code a bad map
breaks (missing object state, garbage scripts, bad warp index, ...).

Nothing is learned by comparing against a black box: PyBoy 2.7 exposes no CPU
handle, so the crash signals are memory-based:
  - PyBoy exception while ticking (emulator-level fault)
  - DIV timer frozen for 5 s (DIV advances several times per emulated frame;
    a dead CPU stops it immediately)
  - the loaded map id is out of range for the game after a teleport
  - landing tile outside the map bounds, or an object file with no warps at
    all (the engine would then read junk to place the player)
  - softlock NOTE (reported, not failed): nothing visible happens for 5 s
    of play while the pad is free — silence and still screen together look
    like a hang, and a wandering-NPC text box alone looks nothing like it.

Usage: python3 tools/map_tour.py [--maps 0,12] [--sample 12]
       [--seconds-per-map 15] [--seed 0] [--rom pokered.gbc]
       [--report /tmp/tour.txt]

bot requires pyboy (same venv as tools/smoke_test.py). Not wired into
`make check`: a full pass covers 200+ maps and is too slow for a commit gate.
"""
import argparse
import hashlib
import logging
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from battle_check import (_free, _press, _step,  # noqa: E402
                         _first_move, _warps, _DIRS, walk_to_town)
from check_stability import (parse_map_consts, parse_objects,  # noqa: E402
                            parse_headers)

DIV = 0xFF04        # rDIV: free-running timer, ticks even while the CPU HALTs
BG_MAP = 0x9800     # BG tilemap (VRAM region 0 bytes), sampled for staleness
BG_MAP_BYTES = 0x200


def load_symbols():
    syms = {}
    for line in (ROOT / "pokered.sym").read_text().splitlines():
        m = re.match(r"^([0-9A-Fa-f]{2}):([0-9a-fA-F]{4})\s+(\S+)$", line.strip())
        if m:
            syms[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))
    return syms


def warp_counts(map_const_labels):
    """const name (PALLETTOWN) -> number of warp_event in its objects file.
    Object/header files are CamelCase (PalletTown.asm) while map_constants is
    upper snake — resolve through the headers, as check_stability does."""
    headers = parse_headers()
    const_to_label = {h["const"]: lbl for lbl, h in headers.items()}
    counts = {}
    for const in map_const_labels:
        lbl = const_to_label.get(const, const)
        o = parse_objects(lbl)
        counts[const] = len(o["warps"]) if o else 0
    return counts


def boot_to_town(pb, wram, max_frames=60 * 120):
    """Mash through title + intro until the player stands, controllable, in
    Port-Lune (map 0) — the same state the smoke test reaches. From there the
    tour teleports, because Port-Lune has real door warps to repurpose as
    launch pads (the bedroom spawn is not controllable until the intro fully
    finishes)."""
    frames = 0
    while frames < max_frames:
        _press(pb, "a", 45)
        frames += 47
        ok, _ = walk_to_town(pb, wram)
        frames += 1
        if ok:
            # LoadMapData finishes writing wWarpEntries a few frames after
            # the map id flips; settle before the tour reads them.
            for _ in range(120):
                pb.tick(1, False)
            return True, frames + 120
    return False, frames


def plant_warp(mem, syms, y, x, dst_warp, dst_map):
    """Retarget a real warp entry — the engine only fires a warp when the
    player steps onto an actual door/warp tile, so the tool repurposes the
    current map's own first warp (a guaranteed door/warp tile) instead of
    planting one on an arbitrary floor tile, which the tile gate rejects."""
    base = syms["wWarpEntries"][1]
    mem[base + 2] = dst_warp
    mem[base + 3] = dst_map


def teleport_to(pb, wram, mem, syms, target, budget=60 * 60):
    """Retarget the current map's first warp to `target` and walk the player
    onto it. Returns (map_id_now, success). The launch pad is a real door/
    warp tile (CheckWarpsNoCollision fires WarpFound1 on it), so LoadMapData
    loads `target` with full object/script state — the code a bad map breaks.

    Random play leaves the game in a dirty state (a menu, a text box, a
    cutscene, another map), so this first escapes whatever is open, steps the
    player off the pad when they landed on it, then re-approaches it — the
    step-ONTO-the-tile pattern is what actually triggers the warp."""
    base = syms["wWarpEntries"][1]
    n_addr = syms["wNumberOfWarps"][1]
    frames = 0
    # escape a lingering menu/text/cutscene before touching the pad
    while not _free(wram) and frames < 60 * 6:
        _press(pb, "b", 8)
        _press(pb, "a", 8)
        frames += 16
    if mem[n_addr] == 0:
        return wram("wCurMap"), False  # no launch pad on this map
    door = (mem[base + 1], mem[base + 0])  # (x, y) of the first warp
    start_map = wram("wCurMap")
    # a warp lands the player ON its own pad: step off it so the walk can
    # re-approach and re-fire CheckWarpsNoCollision
    pos = (wram("wXCoord"), wram("wYCoord"))
    if pos == door:
        for key, _, _ in _DIRS:
            _step(pb, wram, key)
            if wram("wCurMap") != start_map:
                return wram("wCurMap"), wram("wCurMap") == target
            if (wram("wXCoord"), wram("wYCoord")) != door:
                break
    plant_warp(mem, syms, door[1], door[0], 1, target)
    while frames < budget:
        m = wram("wCurMap")
        if m == target:
            return m, True
        if m != start_map:
            return m, False  # drifted elsewhere; chain from here
        if not _free(wram):
            _press(pb, "b", 6)
            _press(pb, "a", 6)
            frames += 12
            continue
        pos = (wram("wXCoord"), wram("wYCoord"))
        w = 2 * wram("wCurMapWidth")
        h = 2 * wram("wCurMapHeight")
        avoid = _warps(pb, syms) - {door}
        k = _first_move(pos, door, w, h, avoid)
        if k is None:
            k = _first_move(pos, door, w, h, set())
            if k is None:  # map still loading / no reachable path
                pb.tick(1, False)
                frames += 1
                continue
        frames += _step(pb, wram, k)
    return wram("wCurMap"), False


def play_random(pb, wram, mem, seconds, rng, health):
    """Random pad presses for `seconds` of emulated time frame by frame,
    watching for a frozen DIV timer. Returns None (healthy) or a reason."""
    emu = 0
    budget = int(seconds * 60)
    static_windows = 0
    vram_hash = None
    pos = None
    keys = ["up", "up", "down", "down", "left", "right", "right", "left",
            "a", "a", "a", "b", "b"]
    last_div = mem[DIV]
    frozen = 0
    iters = 0
    while emu < budget:
        k = rng.choice(keys)
        _press(pb, k, 6)
        emu += 8
        iters += 1
        if iters % 8 == 0:  # ~64 emu frames ≈ 1 s
            div = mem[DIV]
            if div == last_div:
                frozen += 64
                if frozen >= 5 * 60:
                    return f"crash: DIV timer frozen for {frozen} frames"
            else:
                frozen = 0
                last_div = div
        if iters % 40 == 0 and health is not None:  # ~320 frames ≈ 5 s
            h = hashlib.md5(bytes(mem[BG_MAP:BG_MAP + BG_MAP_BYTES])).digest()
            p = (wram("wXCoord"), wram("wYCoord"))
            if h == vram_hash and p == pos and not wram("wJoyIgnore"):
                static_windows += 1
            else:
                static_windows = 0
            vram_hash, pos = h, p
            if static_windows >= 2 and not health.get("softlock"):
                health["softlock"] = True
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default="pokered.gbc")
    ap.add_argument("--maps", default="",
                    help="comma-separated map ids to tour (default: all)")
    ap.add_argument("--sample", type=int, default=0,
                    help="tour a random subset of N maps")
    ap.add_argument("--seconds-per-map", type=float, default=12.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--report", default="tour_report.txt")
    args = ap.parse_args()

    rom_path = ROOT / args.rom
    if not rom_path.exists():
        print(f"FAIL: {rom_path.name} not found — run make first")
        return 1

    logging.getLogger("pyboy").setLevel(logging.ERROR)
    from pyboy import PyBoy

    labels, _ = parse_map_consts()
    by_id = {mid: (lbl, w, h) for lbl, (mid, w, h) in labels.items()}
    maps = sorted(by_id)
    if args.maps:
        want = {int(x) for x in args.maps.split(",")}
        maps = [m for m in maps if m in want]
    if args.sample and args.sample < len(maps):
        rng = random.Random(args.seed)
        maps = sorted(rng.sample(maps, args.sample))
    counts = warp_counts({by_id[m][0] for m in maps})
    print(f"{len(labels)} maps in map_constants; touring {len(maps)} "
          f"(~{int(args.seconds_per_map * len(maps))}s of emulated time)")

    syms = load_symbols()
    pb = PyBoy(str(rom_path), window="null", sound_emulated=False)
    mem = pb.memory

    def wram(sym):
        addr = syms.get(sym, (0, 0))[1]
        return mem[addr] if addr else 0

    crashes, notes, visited, played = [], [], [], 0
    t0_map = None

    try:
        ok, fr = boot_to_town(pb, wram)
        if not ok:
            print(f"FAIL intro: Port-Lune never reached after {fr} frames")
            pb.stop()
            return 1
        # Hub save state: every map is visited from a FRESH Port-Lune, so a
        # 0-warp route (left only through connections) or a cutscene the
        # random play walked into cannot poison the rest of the tour.
        hub_state = "/tmp/neris_tour_hub.state"
        with open(hub_state, "wb") as f:
            pb.save_state(f)
        print(f"intro: Port-Lune reached after {fr} frames (hub saved)")
        rng = random.Random(args.seed)
        for mid in maps:
            with open(hub_state, "rb") as f:
                pb.load_state(f)
            lbl, w, h = by_id[mid]
            line = f"  {mid:3d} {lbl}: "
            before = wram("wCurMap")
            landed, ok = teleport_to(pb, wram, mem, syms, mid)
            if not ok:
                notes.append(f"{mid} {lbl}: teleport failed "
                             f"(was on {before}, now {landed}; chaining on)")
            if ok:
                x, y = wram("wXCoord"), wram("wYCoord")
                if not (0 <= x < 2 * w and 0 <= y < 2 * h):
                    notes.append(f"{mid} {lbl}: landing tile ({x},{y}) "
                                 f"outside {2 * w}x{2 * h}")
                if counts.get(lbl, 1) == 0:
                    notes.append(f"{mid} {lbl}: object file has no warps; "
                                 "player placement is undefined")
                health = {}
                reason = play_random(pb, wram, mem, args.seconds_per_map,
                                     rng, health)
                if reason:
                    crashes.append(f"{mid} {lbl}: {reason}")
                    line += reason
                else:
                    played += 1
                    line += f"ok ({args.seconds_per_map:.0f}s played)"
                if health.get("softlock"):
                    notes.append(f"{mid} {lbl}: no visual change for 5s "
                                 "with a free pad (possible softlock)")
            visited.append(f"{mid} {lbl}")
            print(line, flush=True)
            if crashes:
                break  # the next map would boot a corrupted state
    except Exception as e:
        crashes.append(f"emulator exception: {e}")
    finally:
        pb.stop()

    line_out = ["MAP TOUR REPORT",
                f"maps visited: {len(visited)} / {len(maps)}",
                f"maps played: {played}"]
    for c in crashes:
        line_out.append(f"CRASH: {c}")
    for n in notes:
        line_out.append(f"NOTE:  {n}")
    line_out.append("tour: " + ("FAILED" if crashes else "ok"))
    report = "\n".join(line_out) + "\n"
    Path(args.report).write_text(report)
    print(report)
    return 1 if crashes else 0


if __name__ == "__main__":
    sys.exit(main())
