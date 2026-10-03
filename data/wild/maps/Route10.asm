Route10WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 21, VOLTORB
	db 21, SPEAROW
	db 19, VOLTORB
IF DEF(_RED)
	db 15, EKANS
	db 17, SPEAROW
	db 20, EKANS
	db 23, VOLTORB
	db 23, SPEAROW
	db 17, EKANS
	db 23, EKANS
ENDC
IF DEF(_BLUE)
	db 15, SANDSHREW
	db 17, SPEAROW
	db 20, SANDSHREW
	db 23, VOLTORB
	db 23, SPEAROW
	db 17, SANDSHREW
	db 23, SANDSHREW
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
