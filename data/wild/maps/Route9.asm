Route9WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 21, OISEAULO
	db 21, AILESOR
	db 19, SERPICOL
IF DEF(_RED)
	db 15, SERPICOL
	db 17, AILESOR
	db 20, SERPICOL
	db 23, TERREUX
	db 23, AILESOR
	db 17, SERPICOL
	db 23, SERPICOL
ENDC
IF DEF(_BLUE)
	db 15, ROCBOUL
	db 17, OISEAULO
	db 20, ROCBOUL
	db 23, TERREUX
	db 23, OISEAULO
	db 17, ROCBOUL
	db 23, ROCBOUL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
