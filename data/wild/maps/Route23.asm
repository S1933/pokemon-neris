Route23WildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 34, SERPICOL
ENDC
IF DEF(_BLUE)
	db 34, ROCBOUL
ENDC
	db 43, PSYMINI
	db 34, TERREUX
	db 50, AILESOR
	db 50, DITTO
	db 50, AILESOR
IF DEF(_RED)
	db 54, SERPICOL
ENDC
IF DEF(_BLUE)
	db 54, ROCBOUL
ENDC
	db 56, DITTO
	db 54, AILESOR
	db 56, AILESOR
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
