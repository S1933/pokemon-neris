# Pokémon Néris — Design Draft (pokered base)

English repo doc; in-game French names kept as proper nouns.

## 1. New cities (Kanto extension, east of Route 22)
| City | Concept | Key location |
|---|---|---|
| Port-Lune | Harbour town, departure point | Lighthouse, harbor |
| Sentier des Embruns | Coastal route city 1 | Pokémon Center |
| Val-Boréal | Mountain city, cold north | Gym — Ice leader |
| Lumiville | Small farming village | Nursery / daycare |
| Académie Néris | Endgame city | Final tournament arena |

## 2. New characters
- **Prof. Sylve**: regional professor, gives the starter.
- **Rival Kael**: aggressive rival, ghost-type specialist, blocks key gates.
- **Elite 4 Néris**: 4 new champions + final tournament organizer **Maître Oran**.

## 3. New Pokémon (3 starters + 2 legendaries to start)
| Name | Type | Role |
|---|---|---|
| Flambino | Fire | Fire starter (lvl 5) |
| Aquinou | Water | Water starter (lvl 5) |
| Verdillo | Grass | Grass starter (lvl 5) |
| Lunaris | Psychic | Lighthouse legendary |
| Solaris | Fire/Flying | Mountain legendary |

## 4. Post-tournament story (after the final tournament)
- New badge unlock: **La Marque de Néris** → gates open east of Académie Néris.
- Chapter 1: strange seismic events — Lunaris disappears from the lighthouse.
- Chapter 2: Team-like antagonist group **L'Ordre du Crépuscule** hunts Solaris.
- Chapter 3: final showdown at Mont Néris, dual legendary battle, new ending + credits variant.

## 5. Mechanics
- All wild/trainer levels already boosted +30% (commit c89170a).
- Level cap stays 100; starter given at level 5 (scale up if the boost makes Pallet trainers too hard).

## Build order (each step = one buildable commit)
1. Rename title/intro to "POKEMON NERIS".
2. Starter swap: Flambino/Aquinou/Verdillo replace Bulbasaur/Charmander/Squirtle in the intro choice.
3. Port-Lune: clone Pallet Town map + rename, wire as start town.
4. Lighthouse event + Lunaris static encounter.
5. Post-tournament map gating + Ordre du Crépuscule grunts.
6. Mont Néris finale + ending.