Route13WildMons:
	def_grass_wildmons 20 ; encounter rate
IF DEF(_RED)
	db 32, ODDISH
	db 33, PIDGEY
	db 36, VENOMBRU
	db 32, VENONAT
	db 29, OISEAULO
	db 34, FLORAQUE
	db 34, WEEPINBELL
	db 33, DITTO
	db 37, GLOOM
	db 39, BELLSPROUT
ENDC
IF DEF(_BLUE)
	db 32, BELLSPROUT
	db 33, PIDGEY
	db 36, VENOMBRU
	db 32, VENONAT
	db 29, OISEAULO
	db 34, FLORAQUE
	db 34, GLOOM
	db 33, DITTO
	db 37, WEEPINBELL
	db 39, ODDISH
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
