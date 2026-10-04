Route7WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 25, OISEAULO
IF DEF(_RED)
	db 25, FLORAQUE
	db 23, SERPICOL
	db 29, FLORAQUE
	db 29, OISEAULO
	db 24, SERPICOL
	db 24, FLAMELET
	db 26, FLAMELET
	db 25, SERPICOL
	db 26, SERPICOL
ENDC
IF DEF(_BLUE)
	db 25, FLORAQUE
	db 23, SERPICOL
	db 29, FLORAQUE
	db 29, AILESOR
	db 24, SERPICOL
	db 24, PYROFELIS
	db 26, FLAMELET
	db 25, SERPICOL
	db 26, SERPICOL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
