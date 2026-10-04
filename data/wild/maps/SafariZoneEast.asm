SafariZoneEastWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 32, PSYMINI
	db 34, CRABEAU
	db 29, FLORAQUE
	db 33, FLORALYS
	db 43, DRAGONET
	db 30, FLORALYS
	db 32, FLORAQUE
	db 33, FLORAQUE
	db 33, KANGASKHAN
	db 37, BUGGAIE
ENDC
IF DEF(_BLUE)
	db 32, PSYMINI
	db 34, CRABEAU
	db 29, SERPICOL
	db 33, FLORAQUE
	db 43, DRAGONET
	db 30, FLORAQUE
	db 32, TERREUX
	db 33, SERPICOL
	db 33, KANGASKHAN
	db 37, BUGGAIE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
