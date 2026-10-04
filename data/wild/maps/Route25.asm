Route25WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db  11, BUGGAIE
	db  12, BUGGAIE
	db 17, OISEAULO
	db 16, FLORAQUE
	db 17, FLORAQUE
	db 16, PSYMINI
	db 19, FLORAQUE
	db 13, PSYMINI
	db  10, BUGGAIE
	db  11, BUGGAIE
ENDC
IF DEF(_BLUE)
	db  11, FLORALYS
	db  12, FLORALYS
	db 17, AILESOR
	db 16, FLORAQUE
	db 17, FLORAQUE
	db 16, MENTALIS
	db 19, FLORAQUE
	db 13, MENTALIS
	db  10, SERPICOL
	db  11, SERPICOL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
