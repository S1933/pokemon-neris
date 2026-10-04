Route15WildMons:
	def_grass_wildmons 15 ; encounter rate
IF DEF(_RED)
	db 32, FLORAQUE
	db 34, CRABEAU
	db 30, OISEAULO
	db 34, VENOMBRU
	db 29, FLORAQUE
	db 37, VENOMBRU
	db 34, FLORAQUE
	db 39, FLORALYS
ENDC
IF DEF(_BLUE)
	db 32, FLORAQUE
	db 34, CRABEAU
	db 30, AILESOR
	db 34, SPECTRELA
	db 29, FLORAQUE
	db 37, SPECTRELA
	db 34, FLORAQUE
	db 39, FLORALYS
ENDC
	db 37, OISEAULO
	db 39, OISEAULO
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
