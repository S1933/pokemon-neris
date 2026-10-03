PowerPlantWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 28, VOLTORB
	db 28, VOLTOUR
	db 26, ELECTROX
	db 32, PIKACHU
	db 30, MAGNEMITE
	db 30, VOLTORB
	db 42, MAGNETON
	db 46, MAGNETON
IF DEF(_RED)
	db 43, ELECTABUZZ
	db 47, ELECTABUZZ
ENDC
IF DEF(_BLUE)
	db 43, RAICHU
	db 47, RAICHU
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
