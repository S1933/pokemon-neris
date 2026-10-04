#!/usr/bin/env python3
"""Encounter matrix generator (NERIS-051/052/053).

Rewrites data/wild/maps/*.asm so every progression window has a coherent
Néris presence while keeping:
  - the exact level curve (unchanged numbers — NERIS-052 is separate work)
  - the vanilla RED/BLUE branch structure (symmetric rows get the same
    replacement species in both branches, asymmetric rows get branch-specific
    counterparts of the same role)
  - row counts identical (10-entry grass tables stay 10 entries)

Mapping is version-agnostic: each vanilla species maps to a species ROLE
(common bird / rodent / bug / rock / …) and each role maps to a Néris pool.
Branch-specific version exclusives map to Néris species that keep a
RED/BLUE difference (e.g. Route5 MANKEY(R)/MEOWTH(B) → SERPICOL(R)/FANTOMIN(B)).

Usage: python3 tools/encounter_matrix.py [--dry-run]
The mapping table at the top of the file is the source of truth; adjust
there, run, build, `make check`.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WILD = ROOT / "data" / "wild" / "maps"

# ---------------------------------------------------------------------------
# Species pools (Néris identity, plan batches A–F + starters/legendaries)
# COMMON = appears in many zones; RARE = 1-2 late zones only.
# ---------------------------------------------------------------------------

POOL = {
    # vanilla species -> (replacement species, must_match_branch) — the tuple
    # value is the RED counterpart for branch-exclusive rows.
    # Common early species
    "PIDGEY":    "OISEAULO",
    "PIDGEOTTO": "OISEAULO",
    "PIDGEOT":   "AILESOR",
    "SPEAROW":   "AILESOR",
    "FEAROW":    "AILESOR",
    "RATTATA":   "OISEAULO",   # keep a 1st-step common: oiseaulo doubles down
    "RATICATE":  "OISEAULO",
    "CATERPIE":  "BUGGAIE",
    "METAPOD":   "BUGGAIE",
    "BUTTERFREE": "BUGGAIE",
    "WEEDLE":    "BUGGAIE",
    "KAKUNA":    "BUGGAIE",
    "BEEDRILL":  "BUGGAIE",
    "GEODUDE":   "ROCBOUL",
    "GRAVELER":  "ROCBOUL",
    "GOLEM":     "PETIROC",
    "ONIX":      "PETIROC",
    "ODDISH":    "FLORAQUE",
    "GLOOM":     "FLORAQUE",
    "VILEPLUME": "FLORALYS",
    "BELLSPROUT": "FLORALYS",
    "WEEPINBELL": "FLORALYS",
    "VICTREEBEL": "FLORAQUE",
    "EKANS":     "SERPICOL",
    "ARBOK":     "SERPICOL",
    "SANDSHREW": "TERREUX",
    "SANDSLASH": "TERREUX",
    "DIGLETT":   "TERREUX",
    "DUGTRIO":   "TERREUX",
    "ZUBAT":     "CHAUVESPI",
    "GOLBAT":    "CHAUVESPI",
    "MANKEY":    "SERPICOL",   # branch-exclusive rows get pool counterparts below
    "PRIMEAPE":  "SERPICOL",
    "MEOWTH":    "FANTOMIN",
    "PERSIAN":   "FANTOMIN",
    "GROWLITHE": "FLAMELET",
    "ARCANINE":  "PYROFELIS",
    "VULPIX":    "FLAMELET",
    "NINETALES": "PYROFELIS",
    "ABRA":      "PSYMINI",
    "KADABRA":   "PSYMINI",
    "ALAKAZAM":  "MENTALIS",
    "MACHOP":    "AQUAJET",
    "MACHOKE":   "AQUAJET",
    "MACHAMP":   "AQUAJET",
    "GASTLY":    "FANTOMIN",
    "HAUNTER":   "FANTOMIN",
    "GENGAR":    "SPECTRELA",
    "MAGNEMITE": "VOLTOUR",
    "MAGNETON":  "ELECTROX",
    "VOLTORB":   "VOLTOUR",
    "ELECTRODE": "ELECTROX",
    "PONYTA":    "FLAMELET",
    "RAPIDASH":  "PYROFELIS",
    "SLOWPOKE":  "MARAISSOR",
    "SLOWBRO":   "MARAISSOR",
    "PSYDUCK":   "PSYMINI",
    "GOLDUCK":   "MENTALIS",
    "DROWZEE":   "PSYMINI",
    "HYPNO":     "OBSCURAX",
    "KRABBY":    "CRABEAU",
    "KINGLER":   "CRABEAU",
    "STARYU":    "AQUAJET",
    "STARMIE":   "GLACIETTE",
    "TENTACOOL": "MARAISSOR",
    "TENTACRUEL": "VENOMBRU",
    "HORSEA":    "DRAGONET",
    "SEADRA":    "DRACOZELLE",
    "SHELLDER":  "GLACIETTE",
    "CLOYSTER":  "GLACIETTE",
    "POLIWAG":   "AQUAJET",
    "POLIWHIRL": "AQUAJET",
    "POLIWRATH": "AQUAJET",
    "TANGELA":   "FLORALYS",
    "DODUO":     "OISEAULO",
    "DODRIO":    "AILESOR",
    "SEEL":      "GLACIETTE",
    "DEWGONG":   "GIVRALP",
    "JYNX":      "GLACIETTE",
    "ELECTABUZZ": "ELECTROX",
    "MAGMAR":    "FLAMELET",
    "PARAS":     "FLORAQUE",
    "PARASECT":  "FLORAQUE",
    "VENONAT":   "VENOMBRU",
    "VENOMOTH":  "VENOMBRU",
    "CUBONE":    "TERREUX",
    "MAROWAK":   "TERREUX",
    "RHYHORN":   "ROCBOUL",
    "RHYDON":    "TERRAKOR",
    "LAPRAS":    "GIVRALP",
    "AERODACTYL": "DRACOZELLE",
    "DRATINI":   "DRAGONET",
    "DRAGONAIR": "DRACOZELLE",
    "DRAGONITE": "DRACOZELLE",
    "GOLDEEN":   "CRABEAU",
    "SEAKING":   "CRABEAU",
    "GRIMER":    "VENOMBRU",
    "MUK":       "VENOMBRU",
    "KOFFING":   "VENOMBRU",
    "WEEZING":   "VENOMBRU",
    "NIDORAN_M": "SERPICOL",
    "NIDORINO":  "SERPICOL",
    "NIDOKING":  "TERRAKOR",
    "NIDORAN_F": "FLORAQUE",
    "NIDORINA":  "FLORAQUE",
    "NIDOQUEEN": "TERRAKOR",
    "WIGGLYTUFF": "OISEAULO",
    "JIGGLYPUFF": "OISEAULO",
    "CHANSEY":   None,        # keep
    "SNORLAX":   None,        # keep (story block)
    "PIKACHU":   "ELECTROX",
    "RAICHU":    "FULGURAX",
    "FARFETCHD": "OISEAULO",
    "DITTO":     None,        # keep
    "TAUROS":    None,        # keep (safari iconic)
    "KANGASKHAN": None,
    "LICKITUNG": "OISEAULO",
    "EXEGGCUTE": "FLORALYS",
    "EXEGGUTOR": "FLORALYS",
    "MR_MIME":   "MENTALIS",
    "SCYTHER":   "BUGGAIE",
    "PINSIR":    "BUGGAIE",
    "HITMONLEE": "AQUAJET",
    "HITMONCHAN": "AQUAJET",
    "KABUTO":    "PETIROC",
    "KABUTOPS":  "TERRAKOR",
    "OMANYTE":   "PETIROC",
    "OMASTAR":   "TERRAKOR",
    "ARTICUNO":  "GIVRALP",
    "ZAPDOS":    "FULGURAX",
    "MOLTRES":   "PYROFELIS",
    "MISSINGNO.": None,
}

# Branch-exclusive vanilla species keep a RED/BLUE difference: each maps to a
# PAIR (red_species, blue_species) of distinct Néris species.
BRANCH_PAIRS = {
    "MANKEY":  ("SERPICOL", "FANTOMIN"),
    "PRIMEAPE": ("SERPICOL", "FANTOMIN"),
    "MEOWTH":  ("FANTOMIN", "SERPICOL"),
    "PERSIAN": ("FANTOMIN", "SERPICOL"),
    "ODDISH":  ("FLORAQUE", "FLORALYS"),
    "GLOOM":   ("FLORAQUE", "FLORALYS"),
    "VILEPLUME": ("FLORALYS", "FLORAQUE"),
    "BELLSPROUT": ("FLORALYS", "FLORAQUE"),
    "WEEPINBELL": ("FLORALYS", "FLORAQUE"),
    "VICTREEBEL": ("FLORAQUE", "FLORALYS"),
    "EKANS":   ("SERPICOL", "CHAUVESPI"),
    "ARBOK":   ("SERPICOL", "CHAUVESPI"),
    "SANDSHREW": ("TERREUX", "ROCBOUL"),
    "SANDSLASH": ("TERREUX", "ROCBOUL"),
    "GROWLITHE": ("FLAMELET", "VULPIX_PLACEHOLDER"),
    "VULPIX":  ("FLAMELET", "PYROFELIS"),
    "NINETALES": ("PYROFELIS", "FLAMELET"),
    "ELECTABUZZ": ("ELECTROX", "VOLTOUR"),
    "MAGMAR":  ("FLAMELET", "PYROFELIS"),
    "KOFFING": ("VENOMBRU", "CHAUVESPI"),
    "WEEZING": ("VENOMBRU", "CHAUVESPI"),
    "SCYTHER": ("BUGGAIE", "AILESOR"),
    "PINSIR":  ("BUGGAIE", "BUGGAIE"),
    "SEEL":    ("GLACIETTE", "MARAISSOR"),
    "DEWGONG": ("GIVRALP", "GLACIETTE"),
    "STARYU":  ("AQUAJET", "CRABEAU"),
    "STARMIE": ("GLACIETTE", "AQUAJET"),
    "HORSEA":  ("DRAGONET", "CRABEAU"),
    "SEADRA":  ("DRACOZELLE", "CRABEAU"),
    "JYNX":    ("GLACIETTE", "PSYMINI"),
    "MR_MIME": ("MENTALIS", "PSYMINI"),
    "TANGELA": ("FLORALYS", "FLORAQUE"),
    "PARAS":   ("FLORAQUE", "SERPICOL"),
    "PARASECT": ("FLORAQUE", "SERPICOL"),
    "PORYGON": ("PSYMINI", "VOLTOUR"),
    "OMANYTE": ("PETIROC", "ROCBOUL"),
    "OMASTAR": ("TERRAKOR", "PETIROC"),
    "KABUTO":  ("ROCBOUL", "PETIROC"),
    "KABUTOPS": ("TERRAKOR", "ROCBOUL"),
    "DITTO": (None, None),
    "CHANSEY": (None, None),
    "TAUROS": (None, None),
    "SNORLAX": (None, None),
    "LAPRAS": (None, None),
    "PIKACHU": ("ELECTROX", "VOLTOUR"),
    "RAICHU": ("FULGURAX", "ELECTROX"),
    "MAGNEMITE": ("VOLTOUR", "ELECTROX"),
    "MAGNETON": ("ELECTROX", "VOLTOUR"),
    "GASTLY": ("FANTOMIN", "SPECTRELA"),
    "HAUNTER": ("FANTOMIN", "SPECTRELA"),
    "GENGAR": ("SPECTRELA", "FANTOMIN"),
    "ABRA": ("PSYMINI", "MENTALIS"),
    "KADABRA": ("PSYMINI", "MENTALIS"),
    "ALAKAZAM": ("MENTALIS", "PSYMINI"),
    "MACHOP": ("AQUAJET", "SERPICOL"),
    "MACHOKE": ("AQUAJET", "SERPICOL"),
    "MACHAMP": ("AQUAJET", "SERPICOL"),
    "GOLDEEN": ("CRABEAU", "MARAISSOR"),
    "SEAKING": ("CRABEAU", "MARAISSOR"),
    "KRABBY": ("CRABEAU", "MARAISSOR"),
    "KINGLER": ("CRABEAU", "MARAISSOR"),
    "PSYDUCK": ("PSYMINI", "MARAISSOR"),
    "GOLDUCK": ("MENTALIS", "PSYMINI"),
    "DROWZEE": ("PSYMINI", "MENTALIS"),
    "HYPNO": ("OBSCURAX", "MENTALIS"),
    "SLOWPOKE": ("MARAISSOR", "GLACIETTE"),
    "SLOWBRO": ("MARAISSOR", "GLACIETTE"),
    "FARFETCHD": ("OISEAULO", "AILESOR"),
    "DODUO": ("OISEAULO", "AILESOR"),
    "DODRIO": ("AILESOR", "OISEAULO"),
    "LICKITUNG": ("OISEAULO", "CRABEAU"),
    "EXEGGCUTE": ("FLORALYS", "FLORAQUE"),
    "EXEGGUTOR": ("FLORALYS", "FLORAQUE"),
    "RHYHORN": ("ROCBOUL", "TERREUX"),
    "RHYDON": ("TERRAKOR", "PETIROC"),
    "CUBONE": ("TERREUX", "ROCBOUL"),
    "MAROWAK": ("TERREUX", "ROCBOUL"),
    "VENONAT": ("VENOMBRU", "SPECTRELA"),
    "VENOMOTH": ("VENOMBRU", "SPECTRELA"),
    "TENTACOOL": ("MARAISSOR", "VENOMBRU"),
    "TENTACRUEL": ("VENOMBRU", "MARAISSOR"),
    "POLIWAG": ("AQUAJET", "MARAISSOR"),
    "POLIWHIRL": ("AQUAJET", "MARAISSOR"),
    "POLIWRATH": ("AQUAJET", "CRABEAU"),
    "ZUBAT": ("CHAUVESPI", "SPECTRELA"),
    "GOLBAT": ("CHAUVESPI", "SPECTRELA"),
    "GEODUDE": ("ROCBOUL", "PETIROC"),
    "GRAVELER": ("ROCBOUL", "PETIROC"),
    "GOLEM": ("TERRAKOR", "PETIROC"),
    "ONIX": ("PETIROC", "ROCBOUL"),
    "PIDGEY": ("OISEAULO", "AILESOR"),
    "PIDGEOTTO": ("OISEAULO", "AILESOR"),
    "PIDGEOT": ("AILESOR", "OISEAULO"),
    "SPEAROW": ("AILESOR", "OISEAULO"),
    "FEAROW": ("AILESOR", "OISEAULO"),
    "RATTATA": ("OISEAULO", "SERPICOL"),
    "RATICATE": ("OISEAULO", "SERPICOL"),
    "CATERPIE": ("BUGGAIE", "FLORALYS"),
    "METAPOD": ("BUGGAIE", "FLORALYS"),
    "BUTTERFREE": ("BUGGAIE", "FLORALYS"),
    "WEEDLE": ("BUGGAIE", "SERPICOL"),
    "KAKUNA": ("BUGGAIE", "SERPICOL"),
    "BEEDRILL": ("BUGGAIE", "SERPICOL"),
    "JIGGLYPUFF": ("OISEAULO", "FANTOMIN"),
    "WIGGLYTUFF": ("OISEAULO", "FANTOMIN"),
    "NIDORAN_M": ("SERPICOL", "TERREUX"),
    "NIDORINO": ("SERPICOL", "TERREUX"),
    "NIDOKING": ("TERRAKOR", "SERPICOL"),
    "NIDORAN_F": ("FLORAQUE", "GLACIETTE"),
    "NIDORINA": ("FLORAQUE", "GLACIETTE"),
    "NIDOQUEEN": ("TERRAKOR", "GLACIETTE"),
    "VULPIX_PLACEHOLDER": None,  # guard against typos
    "PONYTA": ("FLAMELET", "PYROFELIS"),
    "RAPIDASH": ("PYROFELIS", "FLAMELET"),
    "SHELLDER": ("GLACIETTE", "CRABEAU"),
    "CLOYSTER": ("GLACIETTE", "GIVRALP"),
    "HITMONLEE": ("AQUAJET", "SERPICOL"),
    "HITMONCHAN": ("AQUAJET", "SERPICOL"),
    "ELECTRODE": ("ELECTROX", "VOLTOUR"),
    "VOLTORB": ("VOLTOUR", "ELECTROX"),
    "DRATINI": ("DRAGONET", "DRACOZELLE"),
    "DRAGONAIR": ("DRACOZELLE", "DRAGONET"),
    "DRAGONITE": ("DRACOZELLE", "DRAGONET"),
    "AERODACTYL": ("DRACOZELLE", "PETIROC"),
    "ARTICUNO": ("GIVRALP", "GLACIETTE"),
    "ZAPDOS": ("FULGURAX", "ELECTROX"),
    "MOLTRES": ("PYROFELIS", "FLAMELET"),
}

# fix the typo'd pool entries
POOL.pop("MARAISSOR", None)
POOL["MARAISSOR"] = None
MARAISSOR_FIX = "MARAISOR"

ROW_RE = re.compile(r"^(\s*db\s+)(\d+)(,\s*)([A-Z_][A-Z0-9_]*)(\s*)$")


def fix(species):
    if species == "MARAISSOR":
        return "MARAISOR"
    return species


def rewrite_file(path, dry_run):
    text = path.read_text()
    lines = text.splitlines()
    out = []
    branch = None  # None / "RED" / "BLUE"
    changes = 0
    for line in lines:
        if "IF DEF(_RED)" in line:
            branch = "RED"
            out.append(line)
            continue
        if "IF DEF(_BLUE)" in line:
            branch = "BLUE"
            out.append(line)
            continue
        if "ENDC" in line:
            branch = None
            out.append(line)
            continue
        m = ROW_RE.match(line)
        if not m:
            out.append(line)
            continue
        indent, level, sep, species, tail = m.groups()
        new_species = None
        if branch:
            pair = BRANCH_PAIRS.get(species)
            if pair:
                new_species = pair[0] if branch == "RED" else pair[1]
                new_species = fix(new_species) if new_species else None
        if new_species is None:
            new_species = fix(POOL.get(species, species) or species)
        if new_species and new_species != species:
            out.append(f"{indent}{level}{sep}{new_species}{tail}")
            changes += 1
        else:
            out.append(line)
    if changes and not dry_run:
        path.write_text("\n".join(out) + "\n")
    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_files = 0
    total_changes = 0
    for f in sorted(WILD.glob("*.asm")):
        n = rewrite_file(f, args.dry_run)
        if n:
            total_files += 1
            total_changes += n
            print(f"{f.stem}: {n} rows rewritten")
    print(f"\n{total_changes} rows in {total_files} files"
          + (" (dry run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
