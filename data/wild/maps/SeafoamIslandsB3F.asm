SeafoamIslandsB3FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, SLOWPOKE
	db 41, SEEL
	db 43, KINGLER
	db 43, STARYU
	db 38, HORSEA
	db 41, SHELLDER
	db 41, KRABBY
	db 38, PSYDUCK
	db 51, SEADRA
ENDC
IF DEF(_BLUE)
	db 41, PSYDUCK
	db 41, SEEL
	db 43, SEADRA
	db 43, SHELLDER
	db 38, KRABBY
	db 41, STARYU
	db 41, HORSEA
	db 38, SLOWPOKE
	db 51, KINGLER
ENDC
	db 49, KABUTO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
