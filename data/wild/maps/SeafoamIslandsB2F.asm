SeafoamIslandsB2FWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 39, SEEL
IF DEF(_RED)
	db 39, SLOWPOKE
	db 42, SEEL
	db 42, SLOWPOKE
	db 37, HORSEA
	db 39, STARYU
	db 39, HORSEA
	db 37, SHELLDER
	db 39, GOLBAT
	db 49, SLOWBRO
ENDC
IF DEF(_BLUE)
	db 39, PSYDUCK
	db 42, SEEL
	db 42, PSYDUCK
	db 37, KRABBY
	db 39, SHELLDER
	db 39, KRABBY
	db 37, STARYU
	db 39, GOLBAT
	db 49, GOLDUCK
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
