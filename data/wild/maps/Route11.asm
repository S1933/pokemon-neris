Route11WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 19, EKANS
	db 20, SPEAROW
	db 16, EKANS
	db  12, DROWZEE
	db 17, SPEAROW
	db 17, DROWZEE
	db 20, EKANS
ENDC
IF DEF(_BLUE)
	db 19, SANDSHREW
	db 20, SPEAROW
	db 16, SANDSHREW
	db  12, DROWZEE
	db 17, SPEAROW
	db 17, DROWZEE
	db 20, SANDSHREW
ENDC
	db 23, SPEAROW
	db 15, DROWZEE
	db 20, DROWZEE
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
