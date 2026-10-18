#!/usr/bin/env python3
"""Fail when a memory region drops below its safety margin.

Reads pokered.map (RGBDS map file) and enforces:
  - ROM0 and WRAM0 keep enough headroom for the next fix;
  - every "Text N" bank keeps room for translation edits (French is ~15% longer).

The thresholds are deliberately conservative: the point is to fail BEFORE the
translator hits a wall, not after.
"""
import re
import sys

MAPFILE = sys.argv[1] if len(sys.argv) > 1 else 'pokered.map'
SUMMARY_MIN = {'ROM0': 64, 'WRAM0': 16}  # bytes that must stay free
TEXT_BANK_MIN = 256  # each "Text N" bank keeps room for translation edits


def main():
    t = open(MAPFILE, encoding='utf-8').read()
    errors = []
    for region, need in SUMMARY_MIN.items():
        m = re.search(rf'^\s*{region}: \d+ bytes used / (\d+) free', t, re.M)
        if not m:
            errors.append(f'{region}: not found in {MAPFILE}')
        elif int(m.group(1)) < need:
            errors.append(f'{region}: {m.group(1)} B free, need {need}')
    text_banks = 0
    # RGBDS prints the amount lowercase; [0-9A-F] alone silently truncates "$11ae"
    # to "$11" (17 bytes) and reports a full bank as nearly empty.
    for m in re.finditer(r'ROMX bank #(\d+):\n((?:.*\n)*?)\s+TOTAL EMPTY: \$([0-9A-Fa-f]+)', t):
        bank, body, empty = m.group(1), m.group(2), int(m.group(3), 16)
        if re.search(r'\["Text \d+"\]', body):
            text_banks += 1
            if empty < TEXT_BANK_MIN:
                errors.append(f'ROMX bank {bank} (text): {empty} B free, need {TEXT_BANK_MIN}')
    for e in errors:
        print('  error:', e)
    if errors:
        sys.exit(f'check_space: {len(errors)} region(s) below margin')
    print(f'check_space: ROM0, WRAM0 and {text_banks} text banks within margins')


if __name__ == '__main__':
    main()
