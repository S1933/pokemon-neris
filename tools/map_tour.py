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

from battle_check import _free, _press, _close_box, REDS_HOUSE_2F  # noqa: E402
from check_stability import parse_map_consts, parse_objects  # noqa: E402

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


def warp_counts(map_labels):
    """label -> number of warp_event in its objects file (0 = landing junk)."""
    counts = {}
    for label in map_labels:
        o = parse_objects(label)
        counts[label] = len(o["warps"]) if o else 0
    return counts


def boot_to_bedroom(pb, wram, max_frames=60 * 120):
    """Mash through title + intro until the player stands in the bedroom
    (REDS_HOUSE_2F). The intro hands control at any point, so this loop is
    input-driven: A advances text, B sweeps the SNES hidden-event box."""
    frames = 0
    while frames < max_frames:
        if wram("wCurMap") == REDS_HOUSE_2F and wram("wYCoord"):
            # make sure control really is ours before planting warps
            for _ in range(30):
                _press(pb, "a", 6)
            return True, frames
        _press(pb, "a", 14)
        frames += 16
        if frames % (16 * 10) < 16:
            _close_box(pb)
            frames += 44
    return False, frames


def plant_warp(mem, syms, y, x, dst_warp, dst_map):
    """Plant a single collision warp at step (y, x) leading to dest map."""
    base = syms["wWarpEntries"][1]
    mem[syms["wNumberOfWarps"][1]] = 1
    mem[base + 0] = y
    mem[base + 1] = x
    mem[base + 2] = dst_warp
    mem[base + 3] = dst_map


def teleport_to(pb, wram, mem, syms, target, rounds=8):
    """Bump into walls until LoadMapData lands the player on `target`.
    Returns (map_id_now, success). A NEIGHBOUR map load (a pathier step
    walked through a map connection) just moves the player; the caller's
    next teleport continues chaining from wherever the player ended up."""
    for _ in range(rounds):
        if not _free(wram):
            _press(pb, "a", 6)
            continue
        y, x = wram("wYCoord"), wram("wXCoord")
        plant_warp(mem, syms, y, x, 1, target)
        for key in ("down", "left", "down", "right", "up", "left"):
            _press(pb, key, 12)
            for _ in range(60):  # let the fade-out + LoadMapData finish
                if wram("wCurMap") == target:
                    return target, True
                pb.tick(1, False)
        # the planted warp was a non-starter: reload the map's live entries
        # for the next round's plant to stay stable
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
            "a", "a", "a", "b", "b", "start"]
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
        ok, fr = boot_to_bedroom(pb, wram)
        if not ok:
            print(f"FAIL intro: bedroom never reached after {fr} frames")
            pb.stop()
            return 1
        print(f"intro: bedroom reached after {fr} frames")
        rng = random.Random(args.seed)
        for mid in maps:
            lbl, w, h = by_id[mid]
            line = f"  {mid:3d} {lbl}: "
            before = wram("wCurMap")
            landed, ok = teleport_to(pb, wram, mem, syms, mid)
            if not ok:
                notes.append(f"{mid} {lbl}: teleport failed "
                             f"(still on {before}; chain continues from "
                             f"{landed})")
                # any map change the stumble caused still counts as played
                m_now = wram("wCurMap")
                if m_now == mid:
                    ok = True
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
