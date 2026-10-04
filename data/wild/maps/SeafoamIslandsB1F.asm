SeafoamIslandsB1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 39, AQUAJET
	db 39, DRAGONET
	db 42, GLACIETTE
	db 42, DRAGONET
	db 37, MARAISOR
	db 39, GLACIETTE
	db 39, MARAISOR
	db 37, GLACIETTE
	db 50, GLACIETTE
	db 49, DRACOZELLE
ENDC
IF DEF(_BLUE)
	db 39, CRABEAU
	db 39, MARAISOR
	db 42, CRABEAU
	db 42, MARAISOR
	db 37, MARAISOR
	db 39, MARAISOR
	db 39, MARAISOR
	db 37, MARAISOR
	db 50, GLACIETTE
	db 49, MARAISOR
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
