Route2WildMons:
	def_grass_wildmons 25 ; encounter rate
	db  4, OISEAULO
	db  4, AILESOR
	db  6, OISEAULO
	db  6, OISEAULO
	db  7, OISEAULO
IF DEF(_RED)
	db  4, BUGGAIE
	db  3, OISEAULO
	db  7, OISEAULO
	db  6, BUGGAIE
	db  7, BUGGAIE
ENDC
IF DEF(_BLUE)
	db  4, FLORALYS
	db  3, SERPICOL
	db  7, SERPICOL
	db  6, BUGGAIE
	db  7, FLORALYS
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
