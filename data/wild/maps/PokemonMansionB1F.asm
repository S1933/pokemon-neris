PokemonMansionB1FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 43, KOFFING
	db 41, KOFFING
	db 46, GROWLITHE
	db 42, PONYTA
	db 41, KOFFING
	db 52, WEEZING
	db 45, PONYTA
	db 46, GRIMER
	db 55, WEEZING
	db 55, MUK
ENDC
IF DEF(_BLUE)
	db 43, GRIMER
	db 41, GRIMER
	db 46, VULPIX
	db 42, PONYTA
	db 41, GRIMER
	db 52, MUK
	db 45, PONYTA
	db 46, KOFFING
	db 50, MAGMAR
	db 55, WEEZING
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
