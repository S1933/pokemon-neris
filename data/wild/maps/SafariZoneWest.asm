SafariZoneWestWildMons:
	def_grass_wildmons 30 ; encounter rate
IF DEF(_RED)
	db 33, NIDORAN_M
	db 34, DODUO
	db 30, SERPICOL
	db 32, EXEGGCUTE
	db 43, NIDORINO
	db 34, EXEGGCUTE
	db 33, NIDORAN_F
ENDC
IF DEF(_BLUE)
	db 33, NIDORAN_F
	db 34, DODUO
	db 30, SERPICOL
	db 32, EXEGGCUTE
	db 43, NIDORINA
	db 34, EXEGGCUTE
	db 33, NIDORAN_M
ENDC
	db 41, VENOMOTH
	db 34, MARAISOR
	db 37, KANGASKHAN
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
