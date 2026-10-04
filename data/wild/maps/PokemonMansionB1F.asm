PokemonMansionB1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 43, VENOMBRU
	db 41, VENOMBRU
	db 46, FLAMELET
	db 42, FLAMELET
	db 41, VENOMBRU
	db 52, VENOMBRU
	db 45, FLAMELET
	db 46, VENOMBRU
	db 55, VENOMBRU
	db 55, VENOMBRU
ENDC
IF DEF(_BLUE)
	db 43, VENOMBRU
	db 41, VENOMBRU
	db 46, PYROFELIS
	db 42, PYROFELIS
	db 41, VENOMBRU
	db 52, VENOMBRU
	db 45, PYROFELIS
	db 46, CHAUVESPI
	db 50, PYROFELIS
	db 55, CHAUVESPI
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
