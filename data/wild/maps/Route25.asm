Route25WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db  11, WEEDLE
	db  12, KAKUNA
	db 17, PIDGEY
	db 16, ODDISH
	db 17, ODDISH
	db 16, ABRA
	db 19, ODDISH
	db 13, ABRA
	db  10, METAPOD
	db  11, CATERPIE
ENDC
IF DEF(_BLUE)
	db  11, CATERPIE
	db  12, METAPOD
	db 17, PIDGEY
	db 16, BELLSPROUT
	db 17, BELLSPROUT
	db 16, ABRA
	db 19, BELLSPROUT
	db 13, ABRA
	db  10, KAKUNA
	db  11, WEEDLE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
