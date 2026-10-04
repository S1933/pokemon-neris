SafariZoneNorthWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 29, SERPICOL
	db 34, ROCBOUL
	db 30, FLORAQUE
	db 33, FLORALYS
	db 39, DRAGONET
	db 36, FLORALYS
	db 39, FLORAQUE
ENDC
IF DEF(_BLUE)
	db 29, GLACIETTE
	db 34, TERREUX
	db 30, SERPICOL
	db 33, FLORAQUE
	db 39, DRAGONET
	db 36, FLORAQUE
	db 39, TERREUX
ENDC
	db 42, VENOMBRU
	db 34, CHANSEY
	db 37, MARAISOR
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
