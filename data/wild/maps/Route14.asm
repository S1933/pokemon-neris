Route14WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, FLORAQUE
	db 34, OISEAULO
	db 30, DITTO
	db 32, VENOMBRU
	db 29, FLORAQUE
	db 34, VENOMBRU
	db 34, FLORAQUE
	db 39, FLORAQUE
ENDC
IF DEF(_BLUE)
	db 32, FLORAQUE
	db 34, AILESOR
	db 30, DITTO
	db 32, SPECTRELA
	db 29, FLORAQUE
	db 34, SPECTRELA
	db 34, FLORAQUE
	db 39, FLORAQUE
ENDC
	db 37, OISEAULO
	db 39, OISEAULO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
