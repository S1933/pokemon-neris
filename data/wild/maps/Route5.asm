Route5WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 17, ODDISH
	db 17, PIDGEY
	db 20, PIDGEY
	db 13, MANKEY
	db 16, MANKEY
	db 20, ODDISH
	db 21, ODDISH
	db 21, PIDGEY
	db 19, MANKEY
	db 21, MANKEY
ENDC
IF DEF(_BLUE)
	db 17, BELLSPROUT
	db 17, PIDGEY
	db 20, PIDGEY
	db 13, MEOWTH
	db 16, MEOWTH
	db 20, BELLSPROUT
	db 21, BELLSPROUT
	db 21, PIDGEY
	db 19, MEOWTH
	db 21, MEOWTH
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
