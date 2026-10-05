"""Stage 4 helper: wild battle sanity check for tools/smoke_test.py.

Walks into tall grass (Sentier Embruns / Route 1) until a wild battle
starts, then verifies the enemy sprite was loaded from the right pic:
  - wMonHFrontSprite must equal the *PicFront address declared in the
    species' base_stats file (what tools/check_rom.py expects);
  - the decompressed sprite buffers must not be empty.

The battle screenshot is saved to docs/smoke_battle.png for review.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_rom as cr  # noqa: E402


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
    return 0xE000 - 0x2000 + (addr - 0xD000)


def run_stage_battle(pb, wram, hold, syms, max_frames=60 * 180):
    """Returns (ok, message). Called after the world stage."""
    dexval, types, id2const = _tables()

    # leave the Start menu if open
    hold(["b"], 15)

    # walk north from Port-Lune into Route 1 grass until a wild battle
    frames = 0
    while frames < max_frames:
        hold(["up"], 60)
        frames += 60
        if wram("wIsInBattle"):
            break
    else:
        return False, f"no wild battle after {frames} frames of walking"

    # let the battle intro play out a bit
    pb.tick(60 * 3, False)

    species = wram("wEnemyMonSpecies")
    if not species:
        return False, "battle started but wEnemyMonSpecies is empty"

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
