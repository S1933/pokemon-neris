CeruleanCave1FWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 60, GOLBAT
	db 60, HYPNO
	db 60, MAGNETON
	db 64, DODRIO
	db 64, VENOMOTH
IF DEF(_RED)
	db 68, ARBOK
ENDC
IF DEF(_BLUE)
	db 68, SANDSLASH
ENDC
	db 64, KADABRA
	db 68, PARASECT
	db 69, RAICHU
	db 69, DITTO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
