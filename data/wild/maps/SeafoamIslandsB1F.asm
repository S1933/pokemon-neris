SeafoamIslandsB1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 39, STARYU
	db 39, HORSEA
	db 42, SHELLDER
	db 42, HORSEA
	db 37, SLOWPOKE
	db 39, SEEL
	db 39, SLOWPOKE
	db 37, SEEL
	db 50, DEWGONG
	db 49, SEADRA
ENDC
IF DEF(_BLUE)
	db 39, SHELLDER
	db 39, KRABBY
	db 42, STARYU
	db 42, KRABBY
	db 37, PSYDUCK
	db 39, SEEL
	db 39, PSYDUCK
	db 37, SEEL
	db 50, DEWGONG
	db 49, KINGLER
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
