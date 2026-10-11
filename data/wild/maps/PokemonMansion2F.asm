PokemonMansion2FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 42, GROWLITHE
	db 45, KOFFING
	db 45, PYROFELIS
	db 39, PONYTA
	db 39, VENOMBRU
	db 42, FLAMELET
	db 39, GRIMER
	db 37, VULPIX
	db 51, WEEZING
	db 49, MUK
ENDC
IF DEF(_BLUE)
	db 42, VULPIX
	db 45, GRIMER
	db 45, PYROFELIS
	db 39, PONYTA
	db 39, VENOMBRU
	db 42, FLAMELET
	db 39, KOFFING
	db 37, GROWLITHE
	db 51, MUK
	db 49, WEEZING
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
