Route14WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, ODDISH
	db 34, PIDGEY
	db 30, DITTO
	db 32, VENONAT
	db 29, ODDISH
	db 34, VENONAT
	db 34, ODDISH
	db 39, GLOOM
ENDC
IF DEF(_BLUE)
	db 32, BELLSPROUT
	db 34, PIDGEY
	db 30, DITTO
	db 32, VENONAT
	db 29, BELLSPROUT
	db 34, VENONAT
	db 34, BELLSPROUT
	db 39, WEEPINBELL
ENDC
	db 37, PIDGEOTTO
	db 39, PIDGEOTTO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
