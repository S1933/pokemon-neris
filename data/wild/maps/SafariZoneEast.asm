SafariZoneEastWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 32, NIDORAN_M
	db 34, DODUO
	db 29, PARAS
	db 33, EXEGGCUTE
	db 43, NIDORINO
	db 30, EXEGGCUTE
	db 32, NIDORAN_F
	db 33, PARASECT
	db 33, KANGASKHAN
	db 37, SCYTHER
ENDC
IF DEF(_BLUE)
	db 32, NIDORAN_F
	db 34, DODUO
	db 29, PARAS
	db 33, EXEGGCUTE
	db 43, NIDORINA
	db 30, EXEGGCUTE
	db 32, NIDORAN_M
	db 33, PARASECT
	db 33, KANGASKHAN
	db 37, PINSIR
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
