SafariZoneCenterWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 29, NIDORAN_M
	db 33, RHYHORN
	db 29, VENONAT
	db 32, EXEGGCUTE
	db 41, NIDORINO
	db 33, NIDORAN_F
	db 41, NIDORINA
	db 39, PINSIR
	db 30, GLACIETTE
ENDC
IF DEF(_BLUE)
	db 29, NIDORAN_F
	db 33, RHYHORN
	db 29, VENONAT
	db 32, EXEGGCUTE
	db 41, NIDORINA
	db 33, NIDORAN_M
	db 41, NIDORINO
	db 39, SCYTHER
	db 30, GLACIETTE
ENDC
	db 30, DRAGONET
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
