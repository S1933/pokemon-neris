Route23WildMons:
	def_grass_wildmons 10 ; encounter rate
IF DEF(_RED)
	db 34, EKANS
ENDC
IF DEF(_BLUE)
	db 34, SANDSHREW
ENDC
	db 43, DITTO
	db 34, SPEAROW
	db 50, FEAROW
	db 50, DITTO
	db 50, FEAROW
IF DEF(_RED)
	db 54, ARBOK
ENDC
IF DEF(_BLUE)
	db 54, SANDSLASH
ENDC
	db 56, DITTO
	db 54, FEAROW
	db 56, FEAROW
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
