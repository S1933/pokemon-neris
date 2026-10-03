PokemonMansion3FWildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 41, KOFFING
	db 43, GROWLITHE
	db 46, KOFFING
	db 42, PONYTA
	db 45, PONYTA
	db 52, WEEZING
	db 45, GRIMER
	db 50, WEEZING
	db 47, PONYTA
	db 55, MUK
ENDC
IF DEF(_BLUE)
	db 41, GRIMER
	db 43, VULPIX
	db 46, GRIMER
	db 42, PONYTA
	db 45, MAGMAR
	db 52, MUK
	db 45, KOFFING
	db 50, MUK
	db 47, PONYTA
	db 55, WEEZING
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
