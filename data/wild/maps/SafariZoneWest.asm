SafariZoneWestWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 33, SERPICOL
	db 34, OISEAULO
	db 30, SERPICOL
	db 32, FLORALYS
	db 43, SERPICOL
	db 34, FLORALYS
	db 33, FLORAQUE
ENDC
IF DEF(_BLUE)
	db 33, GLACIETTE
	db 34, AILESOR
	db 30, SERPICOL
	db 32, FLORAQUE
	db 43, GLACIETTE
	db 34, FLORAQUE
	db 33, TERREUX
ENDC
	db 41, VENOMBRU
	db 34, MARAISOR
	db 37, KANGASKHAN
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
