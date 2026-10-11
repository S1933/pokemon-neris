PowerPlantWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 28, VOLTORB
	db 28, MAGNEMITE
	db 26, PIKACHU
	db 32, PIKACHU
	db 30, MAGNEMITE
	db 30, ELECTROX
	db 42, MAGNETON
	db 46, VOLTOUR
IF DEF(_RED)
	db 43, ELECTABUZZ
	db 47, RAICHU
ENDC
IF DEF(_BLUE)
	db 43, RAICHU
	db 47, ELECTABUZZ
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
