Route22WildMons:
	def_grass_wildmons 25 ; encounter rate
	db  4, OISEAULO
IF DEF(_RED)
	db  4, SERPICOL
	db  6, OISEAULO
	db  6, SERPICOL
	db  3, OISEAULO
	db  3, SERPICOL
	db  4, AILESOR
	db  7, AILESOR
	db  4, FLORAQUE
	db  6, FLORAQUE
ENDC
IF DEF(_BLUE)
	db  4, GLACIETTE
	db  6, SERPICOL
	db  6, GLACIETTE
	db  3, SERPICOL
	db  3, GLACIETTE
	db  4, OISEAULO
	db  7, OISEAULO
	db  4, TERREUX
	db  6, TERREUX
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
