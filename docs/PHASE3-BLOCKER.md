# Phase 3 blocker: Port-Lune north exit does not transfer to Route 1

## Symptom
After exiting the player's house in Port-Lune (PalletTown), the smoke
test bot can never walk north into Route 1 (Sentier Embruns). The
player reaches (5,2) (or (3,2)/(8,2) depending on build) but the tile
directly above (row 1 of the connection strip) is always blocked, so
the north map transfer never fires. Walking east along row 2 lets the
player stand on tiles that route 1 marks blocked (0x31) and vice versa.

## What was ruled out
- Engine: home/overworld.asm and engine/overworld/* are identical to
  vanilla pret except the "hold B to run" feature (DoPlayerSpeedup).
  The warp check (CheckWarpsNoCollision / door tile logic) is vanilla.
- Tilesets: gfx/tilesets/overworld.* and warp_tile_ids.asm identical.
- Warp data: wNumberOfWarps/wWarpEntries load correctly in WRAM with
  the right coordinates and destination maps.
- Door warps work when the map has EXACT vanilla geometry: with the
  fork's original 10x9 PalletTown, stepping up from (5,6) onto the
  door tile (5,5) warps into REDS_HOUSE_1F, exactly like vanilla.

## What was tried and failed
- Enlarging Port-Lune to 16x14 (offset 0), then 16x14 with connection
  offsets +/-3, then 20x18 with offsets +/-5: in ALL variants the door
  warps stop firing and the north connection strip collision does not
  line up. Vanilla-geometry builds always work.
- Navigating the north strip empirically: on 10x9 offset 0, (5,2) is
  walkable but (5,1) is blocked although Route1's row 16 x5 is 0x0b
  (walkable). Reads like the collision of the connection strip rows
  does not match the drawn strip - or the bot's understanding of the
  strip rows is off by something.

## Still unknown / next steps
1. Build a RELIABLE vanilla intro bot (walk_to_town flakes on vanilla:
   sometimes times out in the intro/naming screens). Then run the exact
   same north-exit sequence on the vanilla ROM: if vanilla blocks at
   (5,1) too, the bot's reading is wrong, not the fork.
2. If vanilla transfers, dump the collision code path (GetTileAndTileColl
   / wTileMap lookups) for the connection strip rows in both ROMs and
   compare the buffer bytes under the player.
3. Note: the fork's ORIGINAL PalletTown warps (13,5), (12,11) and the
   fork-added LIGHTHOUSE (15,13) are the vanilla-style coordinates;
   they were never proven broken. The "house exit lands on the beach"
   observation matches vanilla behaviour of the LAST_MAP exit spawn.
4. The gen1 connection strip geometry (rows 0-2 of a north-connected
   map) is the remaining suspect: verify against pret documentation
   (docs/pret map_connection format) before touching the maps again.

The 16x14 enlargement was reverted in 7fc7248d; do NOT re-apply a map
resize until the vanilla control test explains the strip behaviour.
