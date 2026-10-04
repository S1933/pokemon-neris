SeafoamIslandsB2FWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 39, GLACIETTE
IF DEF(_RED)
	db 39, MARAISOR
	db 42, GLACIETTE
	db 42, MARAISOR
	db 37, DRAGONET
	db 39, AQUAJET
	db 39, DRAGONET
	db 37, GLACIETTE
	db 39, CHAUVESPI
	db 49, MARAISOR
ENDC
IF DEF(_BLUE)
	db 39, MARAISOR
	db 42, MARAISOR
	db 42, MARAISOR
	db 37, MARAISOR
	db 39, CRABEAU
	db 39, MARAISOR
	db 37, CRABEAU
	db 39, SPECTRELA
	db 49, MARAISOR
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
