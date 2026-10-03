Route7WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 25, PIDGEY
IF DEF(_RED)
	db 25, ODDISH
	db 23, MANKEY
	db 29, ODDISH
	db 29, PIDGEY
	db 24, MANKEY
	db 24, GROWLITHE
	db 26, FLAMELET
	db 25, MANKEY
	db 26, MANKEY
ENDC
IF DEF(_BLUE)
	db 25, BELLSPROUT
	db 23, MEOWTH
	db 29, BELLSPROUT
	db 29, PIDGEY
	db 24, MEOWTH
	db 24, VULPIX
	db 26, FLAMELET
	db 25, MEOWTH
	db 26, MEOWTH
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
