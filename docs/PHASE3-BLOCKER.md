# Phase 3 blocker: Port-Lune north exit does not transfer to Route 1

**Status: closed (2026-10-07).** The map and the engine were never broken.
The smoke-test bot was. `tools/smoke_test.py` now passes its `battle` stage.

## Symptom (as reported)
After leaving the player's house in Port-Lune (PalletTown), the smoke-test
bot never walked north into Route 1 (Sentier Embruns). It stalled around
row 1/2 of the town, and the `battle` stage (wild battle on Route 1) failed.

## Mechanism
Two independent faults, both in the bot:

1. **Blocks vs steps.** `wXCoord`/`wYCoord` count steps (two per block).
   Port-Lune is 10x9 blocks, so 20x18 steps. The old BFS in
   `tools/battle_check.py` searched a 10x9 grid (`_TOWN_W, _TOWN_H = 10, 9`),
   which is the block size. The north opening is at step x=10/11 (block 5),
   outside that grid. The "blocked (5,1)" it kept hitting is a tree in block 2.
2. **Vanilla Prof. Oak intercept.** In the right place, it still could not
   have left. `PalletTownDefaultScript` (`scripts/PalletTown.asm`, unchanged
   from vanilla) fires when `wYCoord == 1` and `EVENT_FOLLOWED_OAK_INTO_LAB`
   is not set. It sets `wJoyIgnore = PAD_SELECT | PAD_START | PAD_CTRL_PAD`
   and starts the Prof. Sylve cutscene ("He! Attends!"). From then on no
   arrow key moves the player until the cutscene is advanced with A. The
   bot never pressed A there and never took a starter, so a wild battle on
   Route 1 was unreachable by construction.

Because of fault 2, the map resizes tried and reverted in 7fc7248d could not
have fixed anything.

## Resolution
`tools/battle_check.py` now drives the opening from WRAM state:

- navigation is a BFS on the step grid (`2*wCurMapWidth` x
  `2*wCurMapHeight`). It learns collisions from failed steps, relearns
  when no path is left (wandering NPCs), and avoids warp tiles read from
  `wWarpEntries`;
- whenever a text box, menu, script lock (`wFontLoaded`, `wJoyIgnore`) or
  battle (`wIsInBattle`) holds the d-pad, the bot presses A. That plays the
  Prof. Sylve cutscene, takes the starter, fights Kael in the lab and closes
  every dialog;
- the goals depend on map and progress (`wPartyCount`): north-exit row,
  then a Poke Ball in the lab, then the lab exit, then Route 1. On Route 1
  the bot paces on the first grass step, tested the way the game tests it
  (`wTileMap` (9,9) == `wGrassTile`), until `wIsInBattle == 1`;
- the stage fails if no trainer battle was fought in the lab.

While doing this, the enemy-sprite check was found to read
`wMonHeader + 1` (base HP) instead of `wMonHFrontSprite`. It now reads the
symbol. It had never run before, because the stage was unreachable.

No game data or script was changed.
