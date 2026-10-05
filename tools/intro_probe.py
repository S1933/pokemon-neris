#!/usr/bin/env python3
"""Reproduce the post-intro soft-lock (NERIS-061, OPEN).

After a fresh game (title -> START -> Oak intro -> naming), the player
appears in the bedroom but the overworld engine never starts:
  - wCurMap stays 0 (PALLET_TOWN) while the bedroom is on screen
  - wYCoord / wXCoord stay 0 while the sprite stands mid-room
  - D-pad and START do nothing (menu never opens, joypad ignored)
  - A re-opens the SNES hidden-event text in a loop

Reproduced on pokered.gbc at master AND at v0.1.0-rc1, so this is NOT
a regression of the MonsterPicBanks fixes.

Usage: python3 tools/intro_probe.py [--rom pokered.gbc]
Exits 0 if the player reaches the overworld (lock gone), 1 if still locked.
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
    logging_default = __import__("logging")
    logging_default.getLogger("pyboy").setLevel(logging_default.ERROR)
    from pyboy import PyBoy

    syms = {}
    for line in (ROOT / "pokered.sym").read_text().splitlines():
        m = re.match(r"^([0-9A-Fa-f]{2}):([0-9a-fA-F]{4})\s+(\S+)$", line.strip())
        if m:
            syms[m.group(3)] = (int(m.group(1), 16), int(m.group(2), 16))

    pb = PyBoy(str(ROOT / args.rom), sound_emulated=False)

    def mem(n):
        a = syms[n][1]
        if a >= 0xD000:
            return pb.memory[0xE000 - 0x2000 + (a - 0xD000)]
        return pb.memory[a]

    def tap(k, f=12):
        pb.button_press(k)
        for _ in range(f):
            pb.tick(1, False)
        pb.button_release(k)

    pb.tick(500, False)
    tap("start")
    pb.tick(400, True)

    for i in range(900):
        tap("a")
        if i % 3 == 2:
            tap("start")
        pb.tick(1, True)
        if mem("wCurMap") == 0 and mem("wYCoord") != 0:
            print(f"overworld reached at iter {i} "
                  f"(map={mem('wCurMap')} y={mem('wYCoord')} "
                  f"x={mem('wXCoord')})")
            pb.stop()
            return 0

    tap("b", 15)
    pb.tick(15, True)
    pb.button_press("down")
    for _ in range(120):
        pb.tick(1, True)
    pb.button_release("down")
    pb.tick(10, True)
    moved = mem("wYCoord") != 0 or mem("wXCoord") != 0
    pb.screen.image.save(ROOT / "docs" / "intro_probe.png")
    pb.stop()
    print(f"locked: map={mem('wCurMap')} y={mem('wYCoord')} "
          f"x={mem('wXCoord')} moved={moved} "
          f"(screenshot docs/intro_probe.png)")
    return 0 if moved else 1


if __name__ == "__main__":
    sys.exit(main())
