SeafoamIslandsB3FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, SLOWPOKE
	db 41, SEEL
	db 43, SLOWPOKE
	db 43, SEEL
	db 38, HORSEA
	db 41, SHELLDER
	db 41, HORSEA
	db 38, SHELLDER
	db 51, SEADRA
ENDC
IF DEF(_BLUE)
	db 41, PSYDUCK
	db 41, SEEL
	db 43, PSYDUCK
	db 43, SEEL
	db 38, KRABBY
	db 41, STARYU
	db 41, KRABBY
	db 38, STARYU
	db 51, KINGLER
ENDC
	db 49, GLACIETTE
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
