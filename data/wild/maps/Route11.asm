Route11WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 19, SERPICOL
	db 20, AILESOR
	db 16, SERPICOL
	db  12, PSYMINI
	db 17, AILESOR
	db 17, PSYMINI
	db 20, SERPICOL
ENDC
IF DEF(_BLUE)
	db 19, ROCBOUL
	db 20, OISEAULO
	db 16, ROCBOUL
	db  12, MENTALIS
	db 17, OISEAULO
	db 17, MENTALIS
	db 20, ROCBOUL
ENDC
	db 23, AILESOR
	db 15, PSYMINI
	db 20, PSYMINI
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
