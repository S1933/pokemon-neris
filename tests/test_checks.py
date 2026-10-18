"""Fixture tests for the static checks (one passing case, one broken case each).

Run with: python3 -m pytest tests/ -q
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script, cwd, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / 'tools' / script), *args],
        cwd=cwd, capture_output=True, text=True,
    )


def text_tree(tmp_path, body):
    (tmp_path / 'constants').mkdir()
    shutil.copy(ROOT / 'constants/charmap.asm', tmp_path / 'constants/charmap.asm')
    (tmp_path / 'text').mkdir()
    (tmp_path / 'text/Test.asm').write_text(body, encoding='utf-8')
    return tmp_path


def test_text_width_accepts_a_line_that_fits(tmp_path):
    tree = text_tree(tmp_path, '\ttext "Les #MON sont"\n')
    r = run('check_text_width.py', tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'fits in 18 tiles' in r.stdout


def test_text_width_rejects_a_line_too_wide(tmp_path):
    # "POKé" is 4 tiles, so "#MON" is 7: this line renders 19 tiles wide.
    tree = text_tree(tmp_path, '\ttext "Mes #MON sont de"\n')
    r = run('check_text_width.py', tree)
    assert r.returncode == 1
    assert '19 tiles' in r.stdout


def map_tree(tmp_path, rom0_free, text_bank_free):
    (tmp_path / 'pokered.map').write_text(
        'SUMMARY:\n'
        f'\tROM0: 16282 bytes used / {rom0_free} free\n'
        '\tWRAM0: 8170 bytes used / 22 free\n'
        '\n'
        'ROMX bank #32:\n'
        '\tSECTION: $4000-$6e51 ($2e52 bytes) ["Text 1"]\n'
        f'\tTOTAL EMPTY: ${text_bank_free:04x} bytes\n',
        encoding='utf-8',
    )
    return tmp_path


def test_check_space_accepts_margins(tmp_path):
    tree = map_tree(tmp_path, 102, 4526)
    r = run('check_space.py', tree, 'pokered.map')
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'within margins' in r.stdout


def test_check_space_parses_lowercase_hex(tmp_path):
    """$11ae must read as 4526 bytes, not 17 (the [0-9A-F] truncation bug)."""
    tree = map_tree(tmp_path, 102, 0x11AE)
    r = run('check_space.py', tree, 'pokered.map')
    assert r.returncode == 0
    assert '1 text banks' in r.stdout


def test_check_space_rejects_a_full_text_bank(tmp_path):
    tree = map_tree(tmp_path, 102, 12)
    r = run('check_space.py', tree, 'pokered.map')
    assert r.returncode == 1
    assert 'need 256' in r.stdout


def test_check_space_rejects_low_rom0(tmp_path):
    tree = map_tree(tmp_path, 8, 4526)
    r = run('check_space.py', tree, 'pokered.map')
    assert r.returncode == 1
    assert 'ROM0' in r.stdout
