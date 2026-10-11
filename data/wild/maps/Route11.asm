Route11WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 19, EKANS
	db 20, OISEAULO
	db 16, ROCBOUL
	db  12, PSYMINI
	db 17, AILESOR
	db 17, SERPICOL
	db 20, SANDSHREW
ENDC
IF DEF(_BLUE)
	db 19, SANDSHREW
	db 20, OISEAULO
	db 16, ROCBOUL
	db  12, PSYMINI
	db 17, AILESOR
	db 17, SERPICOL
	db 20, EKANS
ENDC
	db 23, SPEAROW
	db 15, DROWZEE
	db 20, MENTALIS
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
