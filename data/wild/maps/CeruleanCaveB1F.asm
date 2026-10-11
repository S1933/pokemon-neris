CeruleanCaveB1FWildMons:
	def_grass_wildmons 25 ; encounter rate
	db 72, RHYDON
	db 72, MAROWAK
	db 72, ELECTRODE
	db 84, CHANSEY
	db 84, PARASECT
	db 84, RAICHU
IF DEF(_RED)
	db 75, SANDSLASH
ENDC
IF DEF(_BLUE)
	db 75, SANDSLASH
ENDC
	db 62, DITTO
	db 64, TERRAKOR
	db 66, CRAMORIL
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
