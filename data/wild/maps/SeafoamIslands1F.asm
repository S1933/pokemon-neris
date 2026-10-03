SeafoamIslands1FWildMons:
	def_grass_wildmons 15 ; encounter rate
	db 39, SEEL
IF DEF(_RED)
	db 39, SLOWPOKE
	db 39, SHELLDER
	db 39, HORSEA
	db 37, HORSEA
	db 28, ZUBAT
	db 38, GOLBAT
	db 37, PSYDUCK
	db 37, SHELLDER
	db 50, GOLDUCK
ENDC
IF DEF(_BLUE)
	db 39, PSYDUCK
	db 39, STARYU
	db 39, KRABBY
	db 37, KRABBY
	db 28, ZUBAT
	db 38, GOLBAT
	db 37, SLOWPOKE
	db 37, STARYU
	db 50, SLOWBRO
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
