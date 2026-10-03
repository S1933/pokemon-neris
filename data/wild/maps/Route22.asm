Route22WildMons:
	def_grass_wildmons 25 ; encounter rate
	db  4, RATTATA
IF DEF(_RED)
	db  4, NIDORAN_M
	db  6, RATTATA
	db  6, NIDORAN_M
	db  3, RATTATA
	db  3, NIDORAN_M
	db  4, SPEAROW
	db  7, SPEAROW
	db  4, NIDORAN_F
	db  6, NIDORAN_F
ENDC
IF DEF(_BLUE)
	db  4, NIDORAN_F
	db  6, RATTATA
	db  6, NIDORAN_F
	db  3, RATTATA
	db  3, NIDORAN_F
	db  4, SPEAROW
	db  7, SPEAROW
	db  4, NIDORAN_M
	db  6, NIDORAN_M
ENDC
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
