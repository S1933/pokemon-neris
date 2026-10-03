Route8WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 24, PIDGEY
IF DEF(_RED)
	db 24, MANKEY
	db 23, EKANS
	db 21, GROWLITHE
	db 26, PIDGEY
	db 26, MANKEY
	db 25, EKANS
	db 23, GROWLITHE
	db 20, GROWLITHE
	db 24, GROWLITHE
ENDC
IF DEF(_BLUE)
	db 24, MEOWTH
	db 23, SANDSHREW
	db 21, VULPIX
	db 26, PIDGEY
	db 26, MEOWTH
	db 25, SANDSHREW
	db 23, VULPIX
	db 20, VULPIX
	db 24, VULPIX
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
