Route24WildMons:
	def_grass_wildmons 25 ; encounter rate
IF DEF(_RED)
	db  10, WEEDLE
	db  11, KAKUNA
	db 16, PIDGEY
	db 16, ODDISH
	db 17, ODDISH
	db 13, ABRA
	db 19, ODDISH
ENDC
IF DEF(_BLUE)
	db  10, CATERPIE
	db  11, METAPOD
	db 16, PIDGEY
	db 16, BELLSPROUT
	db 17, BELLSPROUT
	db 13, ABRA
	db 19, BELLSPROUT
ENDC
	db 17, PIDGEY
	db  11, ABRA
	db 16, ABRA
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
