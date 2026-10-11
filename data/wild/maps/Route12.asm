Route12WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, ODDISH
	db 33, PIDGEY
	db 30, VENOMBRU
	db 32, VENONAT
	db 29, OISEAULO
	db 34, CRABEAU
	db 34, AQUAJET
	db 36, WEEPINBELL
	db 37, GLOOM
	db 39, SPECTRELA
ENDC
IF DEF(_BLUE)
	db 32, BELLSPROUT
	db 33, PIDGEY
	db 30, VENOMBRU
	db 32, VENONAT
	db 29, OISEAULO
	db 34, CRABEAU
	db 34, AQUAJET
	db 36, GLOOM
	db 37, WEEPINBELL
	db 39, SPECTRELA
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
