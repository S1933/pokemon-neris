Route24WildMons:
	def_grass_wildmons 25 ; encounter rate
IF DEF(_RED)
	db  10, WEEDLE
	db  11, KAKUNA
	db 16, BUGGAIE
	db 16, ODDISH
	db 17, BELLSPROUT
	db 13, METAPOD
	db 19, CATERPIE
ENDC
IF DEF(_BLUE)
	db  10, CATERPIE
	db  11, METAPOD
	db 16, BUGGAIE
	db 16, BELLSPROUT
	db 17, ODDISH
	db 13, KAKUNA
	db 19, WEEDLE
ENDC
	db 17, PIDGEY
	db  11, ABRA
	db 16, OISEAULO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
