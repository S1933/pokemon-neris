#!/usr/bin/env python3
"""Generate docs/POKEMON.md — the full species registry (NERIS-005/006).

Reads the ROM data tables (no hardcoded species list) and cross-references
them into one markdown document:

  - constants/pokemon_constants.asm  internal id order (const / const_skip)
  - constants/pokedex_constants.asm  DEX_* display numbers
  - data/pokemon/names.asm           dname per internal id
  - data/pokemon/dex_order.asm       display dex number per internal id
  - data/pokemon/base_stats/         stats, types, catch, exp, growth,
                                     learnset, TM/HM, sprite pointers
  - data/pokemon/palettes.asm        palette per display dex number
  - data/pokemon/menu_icons.asm      icon per display dex number
  - data/pokemon/evos_moves.asm      evolutions + learnset
  - data/pokemon/cries.asm           cry base/pitch/length per internal id
  - data/pokemon/dex_entries.asm     Pokedex entry pointer per internal id
  - data/pokemon/dex_text.asm        entry text labels
  - gfx/pics.asm                     front/back pic labels (provenance)

Status vocabulary (NERIS-005):
  COMPLETE    every field present (sprite provenance is reported, not judged)
  VANILLA     FR name == EN source species (slot kept vanilla identity)
  NERIS       FR name differs from the EN source species
  LEGENDARY   Lunaris / Solaris
  PLACEHOLDER dex number is 0 or a required field is missing

Usage: python3 tools/gen_registry.py   (writes docs/POKEMON.md, exit 1 on
unrecoverable parsing errors)
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "POKEMON.md"

LEGENDARY_NAMES = {"LUNARIS", "SOLARIS"}
EXCLUDED_CONSTS = {"NO_MON", "FOSSIL_KABUTOPS", "FOSSIL_AERODACTYL", "MON_GHOST"}

# The Néris identity names (master plan phases 3-6 + design doc). Everything
# else is a Gen 1 slot kept vanilla with its French localisation (rule n°2).
NERIS_NAMES = {
    # starters
    "FLAMBINO", "AQUINOU", "VERDILLO",
    # legendaries
    "LUNARIS", "SOLARIS",
    # the 30 species (plan batches A-F)
    "CRAMORIL", "OBSCURAX", "PYROFELIS", "GIVRALP", "FULGURAX",
    "TERRAKOR", "VENOMBRU", "SPECTRELA", "DRACOZELLE", "MENTALIS",
    "PETIROC", "AILESOR", "BUGGAIE", "FLORALYS", "AQUAJET",
    "VOLTOUR", "PSYMINI", "GLACIETTE", "FLORAQUE", "ROCBOUL",
    "SERPICOL", "CHAUVESPI", "TERREUX", "MARAISOR", "OISEAULO",
    "CRABEAU", "FANTOMIN", "ELECTROX", "FLAMELET", "DRAGONET",
}


def err(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def read(path):
    return (ROOT / path).read_text()


def strip_comments(text):
    return "\n".join(line.split(";", 1)[0] for line in text.splitlines())


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def parse_internal_consts():
    """[(const_name, internal_index)] in table order; skipped slots are None."""
    text = read("constants/pokemon_constants.asm")
    consts = []
    index = 0
    in_table = False
    for line in text.splitlines():
        m = re.match(r"\tconst (?:_skip|(\w+))", line)
        if re.match(r"\tconst_def", line):
            in_table = True
            index = 0
            continue
        if not in_table:
            continue
        m = re.match(r"\tconst (\w+)", line)
        if m:
            consts.append((m.group(1), index))
        elif re.match(r"\tconst_skip", line):
            consts.append((None, index))
        else:
            continue
        index += 1
    return consts


def parse_dex_consts():
    """DEX_<NAME> -> number."""
    text = read("constants/pokedex_constants.asm")
    dex = {}
    index = 0
    for line in text.splitlines():
        if re.match(r"\tconst_def", line):
            index = 0
            continue
        m = re.match(r"\tconst (DEX_\w+)", line)
        if m:
            index += 1
            dex[m.group(1)] = index
    return dex


def parse_dnames():
    """Internal index -> FR name."""
    text = read("data/pokemon/names.asm")
    names = {}
    index = 0
    for line in text.splitlines():
        m = re.search(r'\bdname "([^"]+)"', line)
        if m:
            index += 1
            names[index] = m.group(1)
    return names


def parse_dex_order(dex_const_to_number):
    """Internal index -> display dex number (0 = none)."""
    text = strip_comments(read("data/pokemon/dex_order.asm"))
    order = {}
    index = 0
    for line in text.splitlines():
        m = re.match(r"\s*db (\w+)", line)
        if not m:
            continue
        token = m.group(1)
        index += 1
        if token.startswith("DEX_"):
            order[index] = dex_const_to_number.get(token, 0)
        elif token.isdigit():
            order[index] = int(token)
        else:
            err(f"dex_order.asm row {index}: unrecognized token {token!r}")
    return order


def parse_base_stats():
    """stem -> dict(fields)."""
    stats = {}
    for f in sorted((ROOT / "data/pokemon/base_stats").glob("*.asm")):
        text = read(f"data/pokemon/base_stats/{f.name}")
        plain = strip_comments(text)
        row = {"stem": f.stem}
        m = re.search(r"^\s*db\s+(.+)$", plain, re.M)
        first = m.group(1).strip() if m else ""
        row["dex_ref"] = None if first.startswith("0") else first
        m = re.search(r"^\s*db\s+(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*$",
                      plain, re.M)
        if m:
            row["hp"], row["atk"], row["def"], row["spd"], row["spc"] = map(int, m.groups())
        m = re.search(r"^\s*db\s+([A-Z_]+),\s*([A-Z_]+|BLANK)\s*$", plain, re.M)
        if m:
            row["types"] = [t for t in m.groups() if t != "BLANK"]
        m = re.search(r"^\s*db\s+(\d+)\s*;\s*catch rate", text, re.M)
        row["catch_rate"] = int(m.group(1)) if m else None
        m = re.search(r"^\s*db\s+(\d+)\s*;\s*base exp", text, re.M)
        row["base_exp"] = int(m.group(1)) if m else None
        m = re.search(r"^\tdw (\w+PicFront), (\w+PicBack)", text, re.M)
        row["pic_front"], row["pic_back"] = (m.group(1), m.group(2)) if m else (None, None)
        m = re.search(r"^\tdb ([A-Z_]+(?:\s*,\s*[A-Z_]+)*)\s*;\s*level 1 learnset", text, re.M)
        row["start_moves"] = [s.strip() for s in m.group(1).split(",")] if m else []
        row["start_moves"] = [s for s in row["start_moves"] if s != "NO_MOVE"]
        m = re.search(r"^\tdb (\w+)\s*; growth rate", text, re.M)
        row["growth"] = m.group(1) if m else None
        m = re.search(r"\ttmhm ([^;]+?)(?:\s*;.*)?$", text, re.M)
        moves = []
        if m:
            moves = [s.strip().rstrip(",") for s in m.group(1).replace("\\\n", " ").split(",")]
        row["tmhm"] = [s for s in moves if s and s != "TM_HM_COMPAT"]
        stats[f.stem] = row
    return stats


def parse_pics():
    return set(re.findall(r"^(\w+PicFront)::", read("gfx/pics.asm"), re.M))


def parse_palettes():
    """Display dex number (row order, row 1 = dex 0 MISSINGNO) -> PAL_*."""
    text = strip_comments(read("data/pokemon/palettes.asm"))
    pals = []
    for line in text.splitlines():
        m = re.match(r"\s*db (PAL_\w+)", line)
        if m:
            pals.append(m.group(1))
    return pals  # pals[i] is palette for dex number i (0-based)


def parse_icons():
    text = read("data/pokemon/menu_icons.asm")
    icons = re.findall(r"\tnybble (ICON_\w+)", text)
    return icons  # indexed by (dex number - 1); dex 0 uses the first nybble


def parse_cries():
    """Internal index -> cry base name."""
    text = read("data/pokemon/cries.asm")
    cries = []
    for line in text.splitlines():
        m = re.match(r"\tmon_cry (\w+),", line)
        if m:
            cries.append(m.group(1))
    return cries  # row n-1 = internal id n (first row Rhydon = 1)


def parse_evos_moves():
    """Internal index -> (pointer label, evolutions, learnset levels)."""
    text = read("data/pokemon/evos_moves.asm")
    pointers = re.findall(r"^\tdw (\w+EvosMoves)", text, re.M)
    blocks = {}
    for m in re.finditer(r"^(\w+EvosMoves):\n((?:\s*;[^\n]*\n|\tdb [^\n]*\n)*)",
                         text, re.M):
        label, body = m.group(1), m.group(2)
        evo_lines, learn_levels = [], []
        in_learn = False
        for line in body.splitlines():
            dm = re.match(r"\s*db\s+(.+?)\s*(?:;.*)?$", line)
            if not dm:
                continue
            parts = [p.strip() for p in dm.group(1).split(",")]
            if parts[0] == "0" and len(parts) == 1:
                if in_learn:
                    in_learn = False
                continue
            if parts[0] in ("EV_LEVEL", "EV_ITEM", "EV_TRADE", "EV_HAPPINESS",
                            "EV_STAT", "EV_FRIENDSHIP"):
                evo_lines.append(parts)
                in_learn = True
            elif re.match(r"^\d+$", parts[0]):
                learn_levels.append(int(parts[0]))
        blocks[label] = {"evos": evo_lines, "levels": learn_levels}
    return pointers, blocks


def parse_dex_entries():
    text = read("data/pokemon/dex_entries.asm")
    pointers = re.findall(r"^\tdw (\w+DexEntry)", text, re.M)
    text_labels = set(re.findall(r"^\t?_(\w+)DexEntry::", read("data/pokemon/dex_text.asm"), re.M))
    # labels also exist as blocks inside dex_entries.asm itself
    text_labels |= set(re.findall(r"^(\w+)DexEntry::", text, re.M))
    return pointers, text_labels


dex_const_to_number = parse_dex_consts()
internal_consts = parse_internal_consts()
dnames = parse_dnames()
dex_order = parse_dex_order(dex_const_to_number)
base_stats = parse_base_stats()
own_pics = parse_pics()
palettes = parse_palettes()
icons = parse_icons()
cries = parse_cries()
evo_pointers, evo_blocks = parse_evos_moves()
dex_pointers, dex_text_labels = parse_dex_entries()

# Map internal const -> base_stats file. pokered file stems are the EN
# species identity of the slot; const names are uppercased file stems for
# vanilla slots, and Néris renames map through the dname.
stats_by_stem = {k: v for k, v in base_stats.items()}
stats_by_norm = {norm(k): v for k, v in base_stats.items()}

rows = []
for const, internal in internal_consts:
    if const is None or const in EXCLUDED_CONSTS:
        continue
    fr_name = dnames.get(internal)
    dex_num = dex_order.get(internal, 0)
    stem = const.lower()
    row = stats_by_stem.get(stem) or stats_by_norm.get(norm(const))
    if row is None:
        err(f"no base_stats file for {const} (internal {internal})")
    cry = cries[internal - 1] if internal - 1 < len(cries) else None
    evo_ptr = evo_pointers[internal - 1] if internal - 1 < len(evo_pointers) else None
    evo = evo_blocks.get(evo_ptr, {}) if evo_ptr else {}
    dex_ptr = dex_pointers[internal - 1] if internal - 1 < len(dex_pointers) else None
    entry_name = dex_ptr[:-len("DexEntry")] if dex_ptr else ""
    has_text = entry_name in dex_text_labels if entry_name else False
    dex_n = dex_const_to_number.get(row["dex_ref"], 0) if row.get("dex_ref") else 0
    pal = palettes[dex_num] if 0 <= dex_num < len(palettes) else None
    icon = icons[dex_num - 1] if 1 <= dex_num <= len(icons) else None
    own_pic = bool(row["pic_front"] and row["pic_front"] in own_pics)
    pic_src = row["pic_front"].replace("PicFront", "") if row["pic_front"] else "?"

    upper_name = (fr_name or "").upper()
    if upper_name in LEGENDARY_NAMES:
        status = "LEGENDARY"
    elif dex_num == 0:
        status = "PLACEHOLDER"
    elif upper_name in NERIS_NAMES:
        status = "NERIS"
    else:
        status = "VANILLA"

    missing = []
    if not row.get("hp"):
        missing.append("stats")
    if not row.get("types"):
        missing.append("types")
    if row.get("catch_rate") is None:
        missing.append("catch")
    if row.get("base_exp") is None:
        missing.append("exp")
    if not row.get("growth"):
        missing.append("growth")
    if not (row["start_moves"] or evo.get("levels")):
        missing.append("learnset")
    if not evo_ptr:
        missing.append("evos_moves_ptr")
    if not dex_ptr:
        missing.append("dex_entry_ptr")
    if not has_text:
        missing.append("dex_text")
    if not pal:
        missing.append("palette")
    if not icon:
        missing.append("icon")
    if not cry:
        missing.append("cry")
    if dex_num == 0:
        missing.append("dex_number")
    rows.append({
        "const": const, "internal": internal, "fr": fr_name, "en": stem,
        "dex": dex_num, "dexn": dex_n, "stats": row, "cry": cry,
        "evo": evo, "has_dex": has_text, "pal": pal, "icon": icon,
        "own_pic": own_pic, "pic_src": pic_src, "status": status,
        "missing": missing,
    })

# ---- Document ----
out = []
out.append("# Registry Pokémon Néris (001–181+)")
out.append("")
out.append(f"_Généré par `tools/gen_registry.py` — ne pas éditer à la main. "
           f"{len(rows)} espèces actives (slots internes exclus : "
           f"{', '.join(sorted(EXCLUDED_CONSTS))})._")
out.append("")
out.append("Statuts : **VANILLA** = slot conservé à l'identique (nom FR = espèce "
           "source) · **NERIS** = espèce renommée/réinventée · **LEGENDARY** = "
           "Lunaris/Solaris · **PLACEHOLDER** = pas de numéro de dex (inutilisé).")
out.append("")
out.append("## Table principale")
out.append("")
out.append("| Int. | Dex | Nom FR | Source EN | Status | Type(s) | PV | Atk | Def | Vit | Spe | Catch | Exp | Spr. |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    st = r["stats"]
    types = "/".join(t.replace("_", " ").title() for t in st.get("types", [])) or "?"
    dex = r["dex"] if r["dex"] else "—"
    mark = "" if not r["missing"] else " ⚠"
    spr = r["pic_src"].lower()
    out.append(
        f"| {r['internal']} | {dex} | {r['fr']}{mark} | {r['en']} | {r['status']} "
        f"| {types} | {st.get('hp','?')} | {st.get('atk','?')} | {st.get('def','?')} "
        f"| {st.get('spd','?')} | {st.get('spc','?')} | {st.get('catch_rate','?')} "
        f"| {st.get('base_exp','?')} | {spr} |")

incomplete = [r for r in rows if r["missing"]]
out.append("")
out.append(f"{len(rows) - len(incomplete)}/{len(rows)} espèces complètes. "
           + ("⚠ = champ manquant (voir Audit ci-dessous)." if incomplete else ""))

# Names the master plan expects but the ROM does not have yet.
present_upper = {(r["fr"] or "").upper() for r in rows}
absent = sorted(NERIS_NAMES - present_upper)
out.append("")
out.append("## Couverture du plan")
out.append("")
present_plan = [r for r in rows if (r["fr"] or "").upper() in NERIS_NAMES]
out.append(f"{len(present_plan)}/{len(NERIS_NAMES)} "
           f"noms Néris du plan présents dans la ROM.")
if absent:
    out.append("")
    out.append("Manquants : " + ", ".join(sorted(absent)))

# ---- Provenance (NERIS-006 + NERIS-014) ----
neris_rows = [r for r in rows if r["status"] in ("NERIS", "LEGENDARY")]
reused = [r for r in neris_rows if not r["own_pic"]]
own = [r for r in neris_rows if r["own_pic"]]
out.append("")
out.append("## Audit des slots internes (NERIS-006)")
out.append("")
out.append("Chaque Pokémon Néris occupe un slot interne Gen 1 (règle projet n°2). "
           "Correspondance Néris → slot → fichier :")
out.append("")
out.append("| Néris | Slot interne | base_stats | Sprite (front) | Cry (base) |")
out.append("|---|---|---|---|---|")
for r in neris_rows:
    out.append(f"| {r['fr']} | ${r['internal']:02X} | `{r['stats']['stem']}.asm` "
               f"| {r['pic_src'].lower()} | {r['cry']} |")

out.append("")
out.append("## Sprites réutilisés (NERIS-014)")
out.append("")
out.append(f"{len(reused)} espèce(s) Néris pointent encore vers un sprite "
           f"vanilla (report, non bloquant — règle n°3 : complétion progressive) :")
out.append("")
if reused:
    out.append("| Néris | Emprunte le sprite de |")
    out.append("|---|---|")
    for r in reused:
        out.append(f"| {r['fr']} | {r['pic_src'].lower()} |")
else:
    out.append("_Aucun — toutes les espèces Néris ont leur propre pic._")
out.append("")
out.append(f"{len(own)} espèce(s) Néris ont leur propre front/back pic dans `gfx/pics.asm`.")

# ---- Placeholders ----
placeholders = [r for r in rows if r["status"] == "PLACEHOLDER"]
out.append("")
out.append("## Slots sans numéro de dex")
out.append("")
if placeholders:
    out.append(", ".join(f"{r['fr'] or r['const']} (${r['internal']:02X})" for r in placeholders))
else:
    out.append("_Aucun._")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(out) + "\n")
print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} species, "
      f"{len(neris_rows)} Néris, {len(reused)} with reused sprites, "
      f"{len(incomplete)} incomplete, {len(placeholders)} without dex number")
if incomplete:
    print("incomplete:", "; ".join(
        f"{r['fr'] or r['const']}[{','.join(r['missing'])}]" for r in incomplete[:20]))
