Route13WildMons:
	def_grass_wildmons 20 ; encounter rate
IF DEF(_RED)
	db 32, FLORAQUE
	db 33, OISEAULO
	db 36, OISEAULO
	db 32, VENOMBRU
	db 29, FLORAQUE
	db 34, VENOMBRU
	db 34, FLORAQUE
	db 33, DITTO
	db 37, FLORAQUE
	db 39, FLORAQUE
ENDC
IF DEF(_BLUE)
	db 32, FLORAQUE
	db 33, AILESOR
	db 36, AILESOR
	db 32, SPECTRELA
	db 29, FLORAQUE
	db 34, SPECTRELA
	db 34, FLORAQUE
	db 33, DITTO
	db 37, FLORAQUE
	db 39, FLORAQUE
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
