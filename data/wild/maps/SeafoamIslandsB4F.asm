SeafoamIslandsB4FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, HORSEA
	db 41, SHELLDER
	db 43, GOLDUCK
	db 43, PSYDUCK
	db 38, SLOWPOKE
	db 41, SEEL
	db 41, STARYU
	db 38, KRABBY
	db 51, OMANYTE
ENDC
IF DEF(_BLUE)
	db 41, KRABBY
	db 41, STARYU
	db 43, SLOWBRO
	db 43, SLOWPOKE
	db 38, PSYDUCK
	db 41, SEEL
	db 41, SHELLDER
	db 38, HORSEA
	db 51, OMANYTE
ENDC
	db 62, GIVRALP
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
