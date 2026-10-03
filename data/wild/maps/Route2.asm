Route2WildMons:
	def_grass_wildmons 25 ; encounter rate
	db  4, RATTATA
	db  4, PIDGEY
	db  6, PIDGEY
	db  6, RATTATA
	db  7, PIDGEY
IF DEF(_RED)
	db  4, WEEDLE
	db  3, RATTATA
	db  7, RATTATA
	db  6, WEEDLE
	db  7, WEEDLE
ENDC
IF DEF(_BLUE)
	db  4, CATERPIE
	db  3, RATTATA
	db  7, RATTATA
	db  6, CATERPIE
	db  7, CATERPIE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
