	object_const_def
	const_export ACADEMYEAST_CURATOR
	const_export ACADEMYEAST_STATUE_1
	const_export ACADEMYEAST_STATUE_2

AcademyEast_Object:
	db $3 ; border block

	def_warp_events
	warp_event  4, 13, ACADEMY, 3
	warp_event  5, 13, ACADEMY, 4

	def_bg_events

	def_object_events
	object_event  2,  2, SPRITE_GENTLEMAN, STAY, DOWN, TEXT_ACADEMYEAST_CURATOR
	object_event  2,  4, SPRITE_MONSTER, STAY, DOWN, TEXT_ACADEMYEAST_STATUE_1
	object_event  6,  4, SPRITE_MONSTER, STAY, DOWN, TEXT_ACADEMYEAST_STATUE_2

	def_warps_to ACADEMY_EAST
