Route12WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, ODDISH
	db 33, PIDGEY
	db 30, PIDGEY
	db 32, VENONAT
	db 29, ODDISH
	db 34, VENONAT
	db 34, ODDISH
	db 36, PIDGEY
	db 37, GLOOM
	db 39, GLOOM
ENDC
IF DEF(_BLUE)
	db 32, BELLSPROUT
	db 33, PIDGEY
	db 30, PIDGEY
	db 32, VENONAT
	db 29, BELLSPROUT
	db 34, VENONAT
	db 34, BELLSPROUT
	db 36, PIDGEY
	db 37, WEEPINBELL
	db 39, WEEPINBELL
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
