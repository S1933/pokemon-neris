SafariZoneNorthWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 29, NIDORAN_M
	db 34, RHYHORN
	db 30, PARAS
	db 33, EXEGGCUTE
	db 39, NIDORINO
	db 36, EXEGGCUTE
	db 39, NIDORINA
ENDC
IF DEF(_BLUE)
	db 29, NIDORAN_F
	db 34, RHYHORN
	db 30, PARAS
	db 33, EXEGGCUTE
	db 39, NIDORINA
	db 36, EXEGGCUTE
	db 39, NIDORINO
ENDC
	db 42, VENOMOTH
	db 34, CHANSEY
	db 37, TAUROS
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
