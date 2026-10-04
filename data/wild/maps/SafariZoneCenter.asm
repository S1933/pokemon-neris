SafariZoneCenterWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 29, SERPICOL
	db 33, ROCBOUL
	db 29, PSYMINI
	db 32, FLORALYS
	db 41, DRAGONET
	db 33, FLORALYS
	db 41, FLORAQUE
	db 39, FLORAQUE
	db 30, BUGGAIE
ENDC
IF DEF(_BLUE)
	db 29, GLACIETTE
	db 33, TERREUX
	db 29, PSYMINI
	db 32, FLORAQUE
	db 41, DRAGONET
	db 33, FLORAQUE
	db 41, TERREUX
	db 39, SERPICOL
	db 30, BUGGAIE
ENDC
	db 30, CHANSEY
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
