SeafoamIslandsB3FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, MARAISOR
	db 41, GLACIETTE
	db 43, MARAISOR
	db 43, GLACIETTE
	db 38, DRAGONET
	db 41, GLACIETTE
	db 41, DRAGONET
	db 38, GLACIETTE
	db 51, DRACOZELLE
ENDC
IF DEF(_BLUE)
	db 41, MARAISOR
	db 41, MARAISOR
	db 43, MARAISOR
	db 43, MARAISOR
	db 38, MARAISOR
	db 41, CRABEAU
	db 41, MARAISOR
	db 38, CRABEAU
	db 51, MARAISOR
ENDC
	db 49, GLACIETTE
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
