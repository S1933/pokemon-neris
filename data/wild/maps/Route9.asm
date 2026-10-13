Route9WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 21, RATTATA
	db 21, SPEAROW
	db 19, RATTATA
IF DEF(_RED)
	db 15, EKANS
	db 17, ROCBOUL
	db 20, TERREUX
	db 23, SERPICOL
	db 23, AILESOR
	db 17, OISEAULO
	db 23, SANDSHREW
ENDC
IF DEF(_BLUE)
	db 15, SANDSHREW
	db 17, ROCBOUL
	db 20, TERREUX
	db 23, SERPICOL
	db 23, AILESOR
	db 17, OISEAULO
	db 23, EKANS
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
