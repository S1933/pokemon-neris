SeafoamIslands1FWildMons:
	def_grass_wildmons 15 ; encounter rate
	db 39, AQUAJET
IF DEF(_RED)
	db 39, MARAISOR
	db 39, GLACIETTE
	db 39, CRABEAU
	db 37, DRAGONET
	db 28, CHAUVESPI
	db 38, CHAUVESPI
	db 37, PSYMINI
	db 37, GLACIETTE
	db 50, MENTALIS
ENDC
IF DEF(_BLUE)
	db 39, MARAISOR
	db 39, GLACIETTE
	db 39, CRABEAU
	db 37, MARAISOR
	db 28, SPECTRELA
	db 38, CHAUVESPI
	db 37, GLACIETTE
	db 37, CRABEAU
	db 50, GLACIETTE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
