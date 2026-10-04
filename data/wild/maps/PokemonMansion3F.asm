PokemonMansion3FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, VENOMBRU
	db 43, FLAMELET
	db 46, VENOMBRU
	db 42, FLAMELET
	db 45, FLAMELET
	db 52, VENOMBRU
	db 45, VENOMBRU
	db 50, VENOMBRU
	db 47, FLAMELET
	db 55, VENOMBRU
ENDC
IF DEF(_BLUE)
	db 41, VENOMBRU
	db 43, PYROFELIS
	db 46, VENOMBRU
	db 42, PYROFELIS
	db 45, PYROFELIS
	db 52, VENOMBRU
	db 45, CHAUVESPI
	db 50, VENOMBRU
	db 47, PYROFELIS
	db 55, CHAUVESPI
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
