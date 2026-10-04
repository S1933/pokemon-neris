Route12WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, AQUAJET
	db 33, CRABEAU
	db 30, OISEAULO
	db 32, VENOMBRU
	db 29, FLORAQUE
	db 34, SERPICOL
	db 34, FLORAQUE
	db 36, OISEAULO
	db 37, FLORALYS
	db 39, FLORAQUE
ENDC
IF DEF(_BLUE)
	db 32, AQUAJET
	db 33, CRABEAU
	db 30, AILESOR
	db 32, SPECTRELA
	db 29, FLORAQUE
	db 34, SERPICOL
	db 34, FLORAQUE
	db 36, AILESOR
	db 37, FLORALYS
	db 39, FLORAQUE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
