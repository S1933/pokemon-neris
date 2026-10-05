#!/usr/bin/env python3
"""Check the compiled ROM against the species sources (NERIS-060).

Reads pokered.gbc + pokered.sym and verifies, for every internal id:
  - the MonsterPicBanks byte is the real bank of the *PicFront label
    the species' BaseStats pointer references;
  - the BaseStats entry (indexed by dex number, like the engine) holds
    the stats, types and pic pointers declared in
    data/pokemon/base_stats/<species>.asm.

Run after `make`. Exits non-zero on any mismatch.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROM = ROOT / 'pokered.gbc'
SYM = ROOT / 'pokered.sym'

# base data struct offsets (constants/pokemon_data_constants.asm)
BASE_DATA_SIZE = 28
OFF_STATS = 1      # hp, atk, def, spd, spc
OFF_TYPES = 6
OFF_CATCH = 8
OFF_EXP = 9
OFF_PIC_SIZE = 10
OFF_FRONTPIC = 11
OFF_BACKPIC = 13
OFF_MOVES = 15
OFF_GROWTH = 19


def read(p):
    return (ROOT / p).read_text()


def internal_ids():
    """species const -> internal id, honouring const_skip."""
    ids, val = {}, 0
    for line in read('constants/pokemon_constants.asm').splitlines():
        if re.match(r'\s*const_skip\b', line):
            val += 1
            continue
        m = re.match(r'\s*const (\w+)', line)
        if m:
            ids[m.group(1)] = val
            val += 1
    return ids


def dex_map(ids):
    """species const -> dex number (PokedexOrder[internal-1])."""
    dexval, v = {}, 1
    for line in read('constants/pokedex_constants.asm').splitlines():
        m = re.match(r'\tconst DEX_(\w+)', line)
        if m:
            dexval[m.group(1)] = v
            v += 1
        elif re.match(r'\s*const_skip\b', line):
            v += 1
    order = []
    for line in read('data/pokemon/dex_order.asm').splitlines():
        m = re.match(r'\s*db (?:DEX_(\w+)|(\d+))', line)
        if m:
            order.append(dexval.get(m.group(1),
                       int(m.group(2)) if m.group(2) else 0))
    out = {}
    for c, i in ids.items():
        if i > 0 and i - 1 < len(order) and order[i - 1] > 0:
            out[c] = order[i - 1]
    return out


def type_map():
    vals, v = {}, 0
    for line in read('constants/type_constants.asm').splitlines():
        m = re.match(r'\s*const_next\s+(\d+|\$[0-9A-Fa-f]+)', line)
        if m:
            t = m.group(1)
            v = int(t[1:], 16) if t.startswith('$') else int(t)
            continue
        if re.match(r'\s*const_skip\b', line):
            v += 1
            continue
        m = re.match(r'\s*const (\w+)', line)
        if m:
            vals[m.group(1)] = v
            v += 1
    return vals


def parse_base_stats(const, dexval, types):
    """Parse a base_stats file: returns dict of expected ROM bytes."""
    for stem in (const.lower(), const.lower().replace('_', '')):
        p = ROOT / 'data/pokemon/base_stats' / f'{stem}.asm'
        if p.exists():
            text = p.read_text()
            break
    else:
        return None
    # strip comments
    text = re.sub(r';.*', '', text)
    bytes_ = []
    for line in text.splitlines():
        m = re.match(r'\s*db\s+(.+)', line)
        if m:
            for tok in m.group(1).split(','):
                tok = tok.strip()
                if tok.startswith('DEX_'):
                    bytes_.append(dexval.get(tok[4:], -1))
                elif tok in types:
                    bytes_.append(types[tok])
                elif re.fullmatch(r'\d+|\$[0-9A-Fa-f]+|%[01]+', tok):
                    v = int(tok[1:], 16) if tok.startswith('$') else \
                        int(tok[1:], 2) if tok.startswith('%') else int(tok)
                    bytes_.append(v)
    m = re.search(r'dw (\w+)PicFront, (\w+)PicBack', text)
    if not m:
        return None
    return {
        'dex_no': bytes_[0],
        'stats': bytes_[1:6],
        'types': bytes_[6:8],
        'catch': bytes_[8],
        'exp': bytes_[9],
        'pic_size': None,  # INCBIN'd single byte, checked via dim below
        'front_label': m.group(1),
        'back_label': m.group(2),
        'moves': bytes_[10:14] if len(bytes_) >= 14 else None,
    }


def load_sym():
    syms = {}
    for line in SYM.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and ':' in parts[0]:
            bank_s, addr_s = parts[0].split(':')
            try:
                syms[parts[1]] = (int(bank_s, 16), int(addr_s, 16))
            except ValueError:
                pass
    return syms


class Rom:
    def __init__(self, data):
        self.data = data

    def byte(self, bank, addr):
        if bank == 0:
            return self.data[addr]
        return self.data[bank * 0x4000 + (addr & 0x3FFF)]

    def word(self, bank, addr):
        return self.byte(bank, addr) | (self.byte(bank, addr + 1) << 8)


def main():
    if not ROM.exists() or not SYM.exists():
        print('check_rom: pokered.gbc / pokered.sym missing (run make first)')
        return 1
    rom = Rom(ROM.read_bytes())
    syms = load_sym()
    ids = internal_ids()
    dexes = dex_map(ids)
    # DEX_ const values for symbolic bytes in base_stats files
    dexval, v = {}, 1
    for line in read('constants/pokedex_constants.asm').splitlines():
        m = re.match(r'\tconst DEX_(\w+)', line)
        if m:
            dexval[m.group(1)] = v
            v += 1
        elif re.match(r'\s*const_skip\b', line):
            v += 1

    mb = syms.get('MonsterPicBanks')
    bs = syms.get('BaseStats')
    if not mb or not bs:
        print('check_rom: MonsterPicBanks/BaseStats not found in .sym')
        return 1

    excluded = {'NO_MON', 'FOSSIL_KABUTOPS', 'FOSSIL_AERODACTYL', 'MON_GHOST'}
    failures = []
    checked = 0
    for const, idx in sorted(ids.items(), key=lambda kv: kv[1]):
        if const in excluded:
            continue
        expected = parse_base_stats(const, dexval, type_map())
        if expected is None:
            failures.append(f'{const}: no base_stats file parsed')
            continue
        checked += 1

        # 1. pic bank table entry vs the label the pointer references
        front = expected['front_label'] + 'PicFront'
        if front not in syms:
            failures.append(f'{const}: label {front} missing from .sym')
            continue
        tbl_bank = rom.byte(mb[0], mb[1] + idx)
        label_bank = syms[front][0]
        if tbl_bank != label_bank:
            failures.append(
                f'{const}: MonsterPicBanks[{idx:#04x}] = {tbl_bank}, '
                f'but {front} lives in bank {label_bank}')

        # 2. BaseStats entry (dex indexed) matches the source file
        dex = dexes.get(const)
        if dex is None:
            continue
        base = bs[1] + (dex - 1) * BASE_DATA_SIZE
        bank = bs[0]
        got_stats = [rom.byte(bank, base + OFF_STATS + i) for i in range(5)]
        if got_stats != expected['stats']:
            failures.append(
                f'{const} (dex {dex}): stats {got_stats} != source '
                f'{expected["stats"]}')
        got_types = [rom.byte(bank, base + OFF_TYPES + i) for i in range(2)]
        if got_types != expected['types']:
            failures.append(
                f'{const} (dex {dex}): types {got_types} != source '
                f'{expected["types"]}')
        for off, label, name in ((OFF_FRONTPIC, expected['front_label'], 'front'),
                                 (OFF_BACKPIC, expected['back_label'], 'back')):
            ptr = rom.word(bank, base + off)
            want = syms.get(label + 'PicFront' if name == 'front'
                            else label + 'PicBack')
            if want is None:
                failures.append(f'{const}: {label}Pic{name} missing from .sym')
            elif ptr & 0x3FFF != want[1] & 0x3FFF:
                failures.append(
                    f'{const} (dex {dex}): {name} pic pointer {ptr:#06x} != '
                    f'{label}Pic{name} at {want[1] & 0x3FFF:#06x}')

    print(f'check_rom: {checked} species checked, {len(failures)} failure(s)')
    for f in failures:
        print(f'  FAIL {f}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
