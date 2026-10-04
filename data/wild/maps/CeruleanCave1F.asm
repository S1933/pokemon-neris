CeruleanCave1FWildMons:
	def_grass_wildmons 10 ; encounter rate
	db 60, CHAUVESPI
	db 60, OBSCURAX
	db 60, ELECTROX
	db 64, AILESOR
	db 64, VENOMBRU
IF DEF(_RED)
	db 68, SERPICOL
ENDC
IF DEF(_BLUE)
	db 68, ROCBOUL
ENDC
	db 64, PSYMINI
	db 68, FLORAQUE
	db 69, FULGURAX
	db 69, DITTO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
