SeafoamIslandsB4FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, DRAGONET
	db 41, GLACIETTE
	db 43, DRAGONET
	db 43, GLACIETTE
	db 38, MARAISOR
	db 41, GLACIETTE
	db 41, MARAISOR
	db 38, GLACIETTE
	db 51, MARAISOR
ENDC
IF DEF(_BLUE)
	db 41, MARAISOR
	db 41, CRABEAU
	db 43, MARAISOR
	db 43, CRABEAU
	db 38, MARAISOR
	db 41, MARAISOR
	db 41, MARAISOR
	db 38, MARAISOR
	db 51, PSYMINI
ENDC
	db 62, GIVRALP
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
