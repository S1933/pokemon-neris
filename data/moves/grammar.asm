; Used by GetMoveGrammar (see engine/battle/core.asm)
; Each move is given an identifier for what usedmovetext to use (0-4).
; Made redundant in English localization, where all are just "[mon]<LINE>used [move]!"

MoveGrammar:
; Neris (French): "<USER>" / "lance [move]!" is 19 tiles for a 12-letter
; move name, so those moves use set 0, whose end text drops the "!".
; Every other move falls through to set 1 ("!").
	db KARATE_CHOP
	db COMET_PUNCH
	db FIRE_PUNCH
	db THUNDERPUNCH
	db VICEGRIP
	db VINE_WHIP
	db ROLLING_KICK
	db SAND_ATTACK
	db HEADBUTT
	db FLAMETHROWER
	db WATER_GUN
	db AURORA_BEAM
	db SEISMIC_TOSS
	db MEGA_DRAIN
	db RAZOR_LEAF
	db SOLARBEAM
	db POISONPOWDER
	db THUNDER
	db QUICK_ATTACK
	db FIRE_BLAST
	db CONSTRICT
	db HI_JUMP_KICK
	db GLARE
	db FURY_SWIPES
	db HYPER_FANG
	db TRI_ATTACK
	db 0 ; end set
	db -1 ; end
