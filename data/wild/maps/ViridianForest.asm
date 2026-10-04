ViridianForestWildMons:
	def_grass_wildmons 8 ; encounter rate
IF DEF(_RED)
	db  6, BUGGAIE
	db  7, BUGGAIE
	db  4, BUGGAIE
	db  7, BUGGAIE
	db  6, FLORAQUE
	db  8, FLORALYS
	db  6, BUGGAIE
	db  4, BUGGAIE
ENDC
IF DEF(_BLUE)
	db  6, FLORALYS
	db  7, FLORALYS
	db  4, FLORALYS
	db  7, FLORALYS
	db  6, FLORAQUE
	db  8, FLORALYS
	db  6, SERPICOL
	db  4, SERPICOL
ENDC
	db  4, ELECTROX
	db  7, ELECTROX
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
