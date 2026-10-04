Route4WildMons:
	def_grass_wildmons 20 ; encounter rate
	db 13, OISEAULO
	db 13, AILESOR
	db  11, OISEAULO
IF DEF(_RED)
	db  8, SERPICOL
	db  11, AILESOR
	db 13, SERPICOL
	db 16, OISEAULO
	db 16, AILESOR
	db  11, SERPICOL
	db 16, SERPICOL
ENDC
IF DEF(_BLUE)
	db  8, ROCBOUL
	db  11, OISEAULO
	db 13, ROCBOUL
	db 16, SERPICOL
	db 16, OISEAULO
	db  11, ROCBOUL
	db 16, ROCBOUL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
