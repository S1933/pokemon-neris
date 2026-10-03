ViridianForestWildMons:
	def_grass_wildmons 8 ; encounter rate
IF DEF(_RED)
	db  6, WEEDLE
	db  7, KAKUNA
	db  4, WEEDLE
	db  7, WEEDLE
	db  6, KAKUNA
	db  8, KAKUNA
	db  6, METAPOD
	db  4, CATERPIE
ENDC
IF DEF(_BLUE)
	db  6, CATERPIE
	db  7, METAPOD
	db  4, CATERPIE
	db  7, CATERPIE
	db  6, METAPOD
	db  8, METAPOD
	db  6, KAKUNA
	db  4, WEEDLE
ENDC
	db  4, PIKACHU
	db  7, PIKACHU
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
