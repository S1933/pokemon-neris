# Pokémon Néris — Feuille de route (base pokered)

## 1. Villes (implémentation en cours)
| Ville | Concept | Lieu clé | État |
|---|---|---|---|
| Port-Lune | Ville portuaire, point de départ | Phare | ✅ (clone Pallet) |
| Sentier des Embruns | Route côtière | Centre #MON | ✅ (Route 1) |
| Val-Boréal | Ville de montagne, nord froid | Arène Glace | ✅ (reliée à la Route 23) |
| Lumiville | Petit village agricole | Pension | ❌ |
| Académie Néris | Ville d'endgame | Arène du tournoi | ✅ (à Jadielle) |

## 2. Personnages
- **Prof. Sylve** : professeur régional, donne le starter. ✅
- **Kael** : rival agressif, spécialiste spectre, verrouille des passages. ✅ (Sentier Embruns)
- **Champions d'arène FR** : Pierre, Onde, Voltaic, Erika, Koga, Ardo, Safira. ✅
- **Elite 4 Néris** : Olga, Bruno, Agatha, Peter. ✅
- **Maître Oran** : organisateur du tournoi final. ✅ (Académie + proto Cave Azure)

## 3. Nouveaux Pokémon
| Nom | Type | Rôle | État |
|---|---|---|---|
| Flambino | Feu | Starter feu (lvl 5) | ✅ |
| Aquinou | Eau | Starter eau (lvl 5) | ✅ |
| Verdillo | Plante | Starter plante (lvl 5) | ✅ |
| Lunaris | Psy | Légendaire du Phare (lvl 70, statique) | ✅ |
| Solaris | Feu/Vol | Légendaire du Mont Néris (lvl 70, statique) | ✅ |
| + 25 autres | — | dex 152-181 : entrées, palettes, icônes | ✅ |

## 4. Histoire post-tournoi
- Badge débloqué : **La Marque de Néris** → attribuée après le boss de l'Ordre (Cave Azure) ; la fin alternative complète se joue à l'Académie. ✅
- Chapitre 1 : séismes étranges — Lunaris disparaît du phare. ❌
- Chapitre 2 : **L'Ordre du Crépuscule** traque Solaris (proto jouable dans la
  Cave Azure : 3 Rockets + boss). ⏳
- Chapitre 3 : affrontement final au Mont Néris (Mt Moon B2F + Cave Azure), fin alternative complète à l'Académie (fin vraie avec la Marque). ✅
- **Fin secrète (data)** : Oran réagit à l'Académie si Lunaris ou Solaris a
  été rencontré. ✅

## 5. Mécanique
- Niveaux wilds/dresseurs +30 % (commit c89170a).
- Cap de niveau inchangé (100) ; starter donné lvl 5.

## Ordre de construction (1 commit = 1 build)
1. Renommer titre/intro « POKEMON NERIS ». ✅
2. Swap starters Flambino/Aquinou/Verdillo. ✅
3. Port-Lune : clone Pallet renommé, ville de départ. ✅
4. Phare + Lunaris statique. ✅
5. Val-Boréal + arène d'Olga (Route 23). ✅
6. Académie + tournoi (4 champions + Oran). ✅
7. Gating post-tournoi + Ordre du Crépuscule complet. ✅
8. Finale Mont Néris + fin alternative complète. ✅
