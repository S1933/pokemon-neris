Route5WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 17, ODDISH
	db 17, PIDGEY
	db 20, PIDGEY
	db 13, MANKEY
	db 16, AILESOR
	db 20, SERPICOL
	db 21, OISEAULO
	db 21, FLORAQUE
	db 19, MEOWTH
	db 21, BELLSPROUT
ENDC
IF DEF(_BLUE)
	db 17, BELLSPROUT
	db 17, PIDGEY
	db 20, PIDGEY
	db 13, MEOWTH
	db 16, AILESOR
	db 20, SERPICOL
	db 21, OISEAULO
	db 21, FLORAQUE
	db 19, MANKEY
	db 21, ODDISH
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
