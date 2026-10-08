# Pokémon Néris

Hack ROM de Pokémon Rouge/Bleu basé sur la désassemblée **pokered** (pret).

Région **Néris** en français : nouveau départ, 3 starters inédits, 2 légendaires
statiques, une arène de glace inédite, une Académie avec tournoi final et une
fin secrète.

## Contenu Néris (état actuel)

| Élément | Détail |
|---|---|
| **Départ** | Port-Lune (Pallet), Prof. Sylve, starters Flambino / Aquinou / Verdillo |
| **Sentier Embruns** | Route 1 renommée, wilds Néris, rival Kael en combat |
| **Phare de Port-Lune** | Nouvelle carte ; **Lunaris** (Psychic, lvl 70) en encounter statique |
| **Mont Néris** | Mt Moon renommé ; **Solaris** (Psychic, lvl 70) en encounter statique |
| **Val-Boréal** | Nouvelle ville reliée à la Route 23 (bord ouest) |
| **Arène d'Olga** | Championne Glace à Val-Boréal : GIVRALP 52 + GLACIETTE 51 |
| **Académie Néris** | Jadielle (porte de l'ancienne école) : tournoi — 4 champions lvl 57-58 ; **Maître Oran** (PETIROC / AQUAJET / AQUAJET 58) refuse le combat tant que les 4 ne sont pas battus |
| **Fin secrète** | Oran réagit si Lunaris ou Solaris a été rencontré |
| **Pokédex** | 181 espèces (30 nouvelles avec entrées dex, palettes et icônes) |
| **Noms FR** | Gym leaders : Pierre, Onde, Voltaic, Erika, Koga, Ardo, Safira ; Elite 4 : Olga, Bruno, Agatha, Peter |
| **Niveaux** | wilds/dresseurs +30 % |

Les 3 Rockets + boss de la Cave Azure (proto Ordre du Crépuscule) restent
jouables.

## Construire

Voir [**INSTALL.md**](INSTALL.md). Le build produit `pokered.gbc` (titre
« POKEMON NERIS »).

```
make
```

## Sauvegardes

Une sauvegarde d'une version antérieure n'est pas compatible : les objets
des cartes sont enregistrés par index, et ces index ont changé. Commencez
une nouvelle partie.

## Documentation

- [**docs/NERIS_DESIGN.md**](docs/NERIS_DESIGN.md) — feuille de route Néris (FR)
- [**INSTALL.md**](INSTALL.md) — dépendances et installation

## Base

Désassemblée Pokémon Rouge/Bleu de [pret](https://github.com/pret/pokered) —
voir le wiki pret pour les tutoriels de la désassemblée.
