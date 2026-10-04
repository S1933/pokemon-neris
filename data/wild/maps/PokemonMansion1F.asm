PokemonMansion1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 42, VENOMBRU
	db 39, VENOMBRU
	db 45, FLAMELET
	db 39, FLAMELET
	db 45, FLAMELET
	db 42, FLAMELET
	db 39, VENOMBRU
	db 37, FLAMELET
	db 49, VENOMBRU
	db 51, VENOMBRU
ENDC
IF DEF(_BLUE)
	db 42, VENOMBRU
	db 39, VENOMBRU
	db 45, PYROFELIS
	db 39, PYROFELIS
	db 45, FLAMELET
	db 42, PYROFELIS
	db 39, CHAUVESPI
	db 37, PYROFELIS
	db 49, VENOMBRU
	db 51, CHAUVESPI
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
