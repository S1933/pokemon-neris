Route8WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 24, OISEAULO
IF DEF(_RED)
	db 24, SERPICOL
	db 23, SERPICOL
	db 21, FLAMELET
	db 26, OISEAULO
	db 26, SERPICOL
	db 25, SERPICOL
	db 23, FLAMELET
	db 20, FLAMELET
	db 24, FLAMELET
ENDC
IF DEF(_BLUE)
	db 24, SERPICOL
	db 23, ROCBOUL
	db 21, PYROFELIS
	db 26, AILESOR
	db 26, SERPICOL
	db 25, SERPICOL
	db 23, PYROFELIS
	db 20, PYROFELIS
	db 24, FLAMELET
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
