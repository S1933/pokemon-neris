PowerPlantWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 28, VOLTOUR
	db 28, VOLTOUR
	db 26, ELECTROX
	db 32, ELECTROX
	db 30, VOLTOUR
	db 30, VOLTOUR
	db 42, ELECTROX
	db 46, ELECTROX
IF DEF(_RED)
	db 43, ELECTROX
	db 47, ELECTROX
ENDC
IF DEF(_BLUE)
	db 43, ELECTROX
	db 47, ELECTROX
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
