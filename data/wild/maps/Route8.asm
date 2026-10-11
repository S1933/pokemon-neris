Route8WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 24, PIDGEY
IF DEF(_RED)
	db 24, MANKEY
	db 23, EKANS
	db 21, GROWLITHE
	db 26, FLAMELET
	db 26, SERPICOL
	db 25, OISEAULO
	db 23, VULPIX
	db 20, SANDSHREW
	db 24, MEOWTH
ENDC
IF DEF(_BLUE)
	db 24, MEOWTH
	db 23, SANDSHREW
	db 21, VULPIX
	db 26, FLAMELET
	db 26, SERPICOL
	db 25, OISEAULO
	db 23, GROWLITHE
	db 20, EKANS
	db 24, MANKEY
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
