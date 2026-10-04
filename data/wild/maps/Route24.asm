Route24WildMons:
	def_grass_wildmons 25 ; encounter rate
IF DEF(_RED)
	db  10, BUGGAIE
	db  11, BUGGAIE
	db 16, OISEAULO
	db 16, FLORAQUE
	db 17, FLORAQUE
	db 13, PSYMINI
	db 19, FLORAQUE
ENDC
IF DEF(_BLUE)
	db  10, FLORALYS
	db  11, FLORALYS
	db 16, AILESOR
	db 16, FLORAQUE
	db 17, FLORAQUE
	db 13, MENTALIS
	db 19, FLORAQUE
ENDC
	db 17, OISEAULO
	db  11, PSYMINI
	db 16, PSYMINI
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
