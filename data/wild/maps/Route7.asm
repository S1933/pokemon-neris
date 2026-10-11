Route7WildMons:
	def_grass_wildmons 15 ; encounter rate
	db 25, PIDGEY
IF DEF(_RED)
	db 25, ODDISH
	db 23, MANKEY
	db 29, SERPICOL
	db 29, FLORAQUE
	db 24, OISEAULO
	db 24, GROWLITHE
	db 26, VULPIX
	db 25, MEOWTH
	db 26, BELLSPROUT
ENDC
IF DEF(_BLUE)
	db 25, BELLSPROUT
	db 23, MEOWTH
	db 29, SERPICOL
	db 29, FLORAQUE
	db 24, OISEAULO
	db 24, VULPIX
	db 26, GROWLITHE
	db 25, MANKEY
	db 26, ODDISH
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
