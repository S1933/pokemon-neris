Route4WildMons:
	def_grass_wildmons 20 ; encounter rate
	db 13, RATTATA
	db 13, SPEAROW
	db  11, RATTATA
IF DEF(_RED)
	db  8, EKANS
	db  11, SPEAROW
	db 13, EKANS
	db 16, RATTATA
	db 16, SPEAROW
	db  11, EKANS
	db 16, EKANS
ENDC
IF DEF(_BLUE)
	db  8, SANDSHREW
	db  11, SPEAROW
	db 13, SANDSHREW
	db 16, RATTATA
	db 16, SPEAROW
	db  11, SANDSHREW
	db 16, SANDSHREW
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
