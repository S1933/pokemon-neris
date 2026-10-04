Route5WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 17, FLORAQUE
	db 17, OISEAULO
	db 20, OISEAULO
	db 13, SERPICOL
	db 16, SERPICOL
	db 20, FLORAQUE
	db 21, FLORAQUE
	db 21, OISEAULO
	db 19, SERPICOL
	db 21, SERPICOL
ENDC
IF DEF(_BLUE)
	db 17, FLORAQUE
	db 17, AILESOR
	db 20, AILESOR
	db 13, SERPICOL
	db 16, SERPICOL
	db 20, FLORAQUE
	db 21, FLORAQUE
	db 21, AILESOR
	db 19, SERPICOL
	db 21, SERPICOL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
