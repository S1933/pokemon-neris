#!/usr/bin/env python3
"""Intro + overworld sanity probe (post-mortem of the "soft-lock").

Reads WRAM DIRECTLY: PyBoy's memory[] does NOT emulate the C000-DFFF
echo mirror, so reads through 0xC000+<offset> return zeros. (Earlier
probes used echo reads and made the game look soft-locked; it is not.)

Flow: title -> START -> mash A through the intro (naming screens
included) -> periodically finish/close the SNES hidden-event text box
(the new-game spawn stands on that tile) and try to walk, so control is
taken as soon as the intro hands it over -> walk until wCurMap ==
PALLET_TOWN (Port-Lune).

Exits 0 when Port-Lune is reached with control, 1 otherwise.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default="pokered.gbc")
    args = ap.parse_args()
    logging = __import__("logging")
    logging.getLogger("pyboy").setLevel(logging.ERROR)
    from pyboy import PyBoy

    syms = {}
    for line in (ROOT / "pokered.sym").read_text().splitlines():
        m = re.match(r"^([0-9A-Fa-f]{2}):([0-9a-fA-F]{4})\s+(\S+)$", line.strip())
        if m:
            syms[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))

    pb = PyBoy(str(ROOT / args.rom), sound_emulated=False)

    def mem(n):
        return pb.memory[syms[n][1]]  # direct read; D000-DFFF is real WRAM

    def tap(k, f=12):
        pb.button_press(k)
        for _ in range(f):
            pb.tick(1, False)
        pb.button_release(k)

    pb.tick(500, False)
    tap("start")
    pb.tick(400, True)

    for i in range(5000):
        tap("a")
        pb.tick(1, True)
        if i % 20 == 19:
            # advance/close the SNES text (B skips pages, closes at the
            # end), then sweep the room: the 2F->1F stairs warp sits at
            # (7, 1) (top-right), the bedroom spawn at (3, 6) in bed.
            tap("b")
            pb.tick(6, True)
            tap("b")
            pb.tick(6, True)
            for key, frames in (("down", 60), ("right", 90),
                                ("up", 90), ("left", 60)):
                pb.button_press(key)
                for _ in range(frames):
                    pb.tick(1, True)
                pb.button_release(key)
                pb.tick(6, True)
        if mem("wCurMap") == 0 and mem("wYCoord") != 0:
            print(f"Port-Lune reached at iter {i} "
                  f"(map=0 y={mem('wYCoord')} x={mem('wXCoord')})")
            pb.stop()
            return 0

    pb.screen.image.save(ROOT / "docs" / "intro_probe.png")
    pb.stop()
    print(f"not in Port-Lune: map={mem('wCurMap')} y={mem('wYCoord')} "
          f"x={mem('wXCoord')} (screenshot docs/intro_probe.png)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
