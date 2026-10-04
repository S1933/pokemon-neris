CeruleanCaveB1FWildMons:
	def_grass_wildmons 25 ; encounter rate
	db 72, TERRAKOR
	db 72, TERREUX
	db 72, ELECTROX
	db 84, CHANSEY
	db 84, FLORAQUE
	db 84, FULGURAX
IF DEF(_RED)
	db 75, SERPICOL
ENDC
IF DEF(_BLUE)
	db 75, ROCBOUL
ENDC
	db 62, CRAMORIL
	db 64, OBSCURAX
	db 66, PYROFELIS
	end_grass_wildmons

	def_water_wildmons 0 ; encounter rate
	end_water_wildmons
