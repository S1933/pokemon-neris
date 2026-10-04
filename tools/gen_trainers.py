#!/usr/bin/env python3
"""Trainer registry generator (NERIS-054/055) — docs/TRAINERS.md.

Walks data/trainers/parties.asm (teams) and data/maps/objects/*.asm
(OPP_CLASS, N placements) to produce, for every trainer that is actually
placed in a map: class, trainer number, location, team with levels.
Trainer classes with no map placement (unused slots) are skipped.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# class constant -> block name in parties.asm (e.g. OPP_YOUNGSTER -> YoungsterData)
CLASS_NAMES = {
    'OPP_YOUNGSTER': 'Youngster', 'OPP_BUGCATCHER': 'BugCatcher',
    'OPP_LASS': 'Lass', 'OPP_SAILOR': 'Sailor', 'OPP_JRTRAINERM': 'JrTrainerM',
    'OPP_JRTRAINERF': 'JrTrainerF', 'OPP_POKEMANIAC': 'Pokemaniac',
    'OPP_SUPERNERD': 'SuperNerd', 'OPP_HIKER': 'Hiker', 'OPP_BIKER': 'Biker',
    'OPP_BURGLAR': 'Burglar', 'OPP_ENGINEER': 'Engineer',
    'OPP_FISHER': 'Fisher', 'OPP_SWIMMER': 'Swimmer', 'OPP_CUEBALL': 'CueBall',
    'OPP_GAMBLER': 'Gambler', 'OPP_BEAUTY': 'Beauty', 'OPP_PSYCHIC': 'Psychic',
    'OPP_ROCKER': 'Rocker', 'OPP_JUGGLER': 'Juggler', 'OPP_TAMER': 'Tamer',
    'OPP_BIRDKEEPER': 'BirdKeeper', 'OPP_BLACKBELT': 'Blackbelt',
    'OPP_RIVAL1': 'Rival1', 'OPP_RIVAL2': 'Rival2', 'OPP_RIVAL3': 'Rival3',
    'OPP_PROF_OAK': 'ProfOak', 'OPP_CHIEF': 'Chief',
    'OPP_SCIENTIST': 'Scientist', 'OPP_GIOVANNI': 'Giovanni',
    'OPP_ROCKET': 'Rocket', 'OPP_COOLTRAINERM': 'CooltrainerM',
    'OPP_COOLTRAINERF': 'CooltrainerF', 'OPP_BRUNO': 'Bruno',
    'OPP_BROCK': 'Brock', 'OPP_MISTY': 'Misty', 'OPP_LT_SURGE': 'LtSurge',
    'OPP_ERIKA': 'Erika', 'OPP_KOGA': 'Koga', 'OPP_BLAINE': 'Blaine',
    'OPP_SABRINA': 'Sabrina', 'OPP_GENTLEMAN': 'Gentleman',
    'OPP_LORELEI': 'Lorelei', 'OPP_CHANNELER': 'Channeler',
    'OPP_AGATHA': 'Agatha', 'OPP_LANCE': 'Lance',
}

NOTES = {
    ('Lorelei', '2'): 'Olga — Val-Boreal Gym (Ice)',
    ('Lorelei', '1'): 'Elite Four',
    ('Bruno', '2'): 'Maître Oran — Académie (finale du tournoi)',
    ('Bruno', '1'): 'Elite Four',
    ('Giovanni', '1'): 'Rocket Hideout B4F',
    ('Giovanni', '2'): 'Silph Co. 11F',
    ('Giovanni', '3'): 'Viridian Gym',
    ('Giovanni', '4'): 'Ordre du Crépuscule — Maître Oran (Cerulean Cave B1F, postgame)',
    ('Rival1', '*'): 'Kael (jeunesse)',
    ('Rival2', '*'): 'Kael',
    ('Rival3', '*'): 'Kael (champion)',
}


def parse_parties():
    """block name -> {trainer_no: [(level, species), ...]}"""
    text = strip_comments((ROOT / 'data/trainers/parties.asm').read_text())
    parties = {}
    for block in re.findall(r'^(\w+Data):\n((?:.|\n)*?)(?=^\w+Data:|\Z)',
                            text, re.M):
        name, body = block
        if name == 'TrainerDataPointers':
            continue
        idx = 0
        entries = {}
        for line in (l for l in body.splitlines() if l.strip()):
            idx += 1
            m = re.match(r'^\tdb\s+(.+?),\s*0\s*$', line)
            if not m:
                continue
            toks = [t.strip() for t in m.group(1).split(',')]
            if toks[0] == '$FF':
                pairs = [(int(toks[k]), toks[k + 1])
                         for k in range(1, len(toks) - 1, 2)]
            else:
                pairs = [(int(toks[0]), sp) for sp in toks[1:]]
            entries[idx] = pairs
        parties[name.replace('Data', '')] = entries
    return parties


def parse_placements():
    """map name -> [(class_block, trainer_no, x, y)]"""
    placements = {}
    for f in sorted((ROOT / 'data/maps/objects').glob('*.asm')):
        hits = re.findall(
            r'object_event\s+(\d+),\s*(\d+),.*OPP_([A-Z_0-9]+),\s*(\d+)',
            f.read_text())
        if not hits:
            continue
        rows = []
        for y, x, cls, num in hits:
            block = CLASS_NAMES.get(f'OPP_{cls}')
            if block:
                rows.append((block, num, int(x), int(y)))
        if rows:
            placements[f.stem] = rows
    return placements


def strip_comments(text):
    return '\n'.join(l.split(';')[0] for l in text.splitlines())


def main():
    parties = parse_parties()
    placements = parse_placements()
    lines = ['# Registre des dresseurs (NERIS-054/055)', '',
             '_Généré par `python3 tools/gen_trainers.py` depuis',
             '`data/trainers/parties.asm` + `data/maps/objects/`.',
             'Seuls les dresseurs placés dans une map apparaissent._', '',
             '| Map | Dresseur | Équipe (niveaux) |',
             '|---|---|---|']
    total = 0
    for map_name, rows in sorted(placements.items()):
        for block, num, x, y in rows:
            team = parties.get(block, {}).get(int(num))
            if team is None:
                continue
            label = NOTES.get((block, num)) or NOTES.get((block, '*')) or block
            team_str = ', '.join(f'{sp.lower()} {lv}' for lv, sp in team)
            lines.append(f'| {map_name} | {label} (#{num}) | {team_str} |')
            total += 1
    out = ROOT / 'docs' / 'TRAINERS.md'
    out.write_text('\n'.join(lines) + '\n')
    print(f'wrote {out.relative_to(ROOT)}: {total} placed trainers')
    return 0


if __name__ == '__main__':
    sys.exit(main())