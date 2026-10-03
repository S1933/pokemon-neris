PokemonMansion1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 42, KOFFING
	db 39, KOFFING
	db 45, PONYTA
	db 39, PONYTA
	db 45, FLAMELET
	db 42, PONYTA
	db 39, GRIMER
	db 37, PONYTA
	db 49, WEEZING
	db 51, MUK
ENDC
IF DEF(_BLUE)
	db 42, GRIMER
	db 39, GRIMER
	db 45, PONYTA
	db 39, PONYTA
	db 45, FLAMELET
	db 42, PONYTA
	db 39, KOFFING
	db 37, PONYTA
	db 49, MUK
	db 51, WEEZING
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
