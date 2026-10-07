object_const_def
const_export ACADEMY_ORAN
const_export ACADEMY_CHAMP_1
const_export ACADEMY_CHAMP_2
const_export ACADEMY_CHAMP_3
const_export ACADEMY_CHAMP_4

Academy_Object:
	db $3 ; border block

	def_warp_events
	warp_event  4, 11, LAST_MAP, 3
	warp_event  5, 11, LAST_MAP, 3
	warp_event  8, 13, ACADEMY_EAST, 1
	warp_event  9, 13, ACADEMY_EAST, 1

	def_bg_events

	def_object_events
	object_event  4,  1, SPRITE_BRUNO, STAY, DOWN, TEXT_ACADEMY_ORAN, OPP_BRUNO, 2
	object_event  2,  4, SPRITE_COOLTRAINER_M, STAY, RIGHT, TEXT_ACADEMY_CHAMP_1, OPP_COOLTRAINER_M, 11
	object_event  6,  4, SPRITE_COOLTRAINER_F, STAY, LEFT, TEXT_ACADEMY_CHAMP_2, OPP_COOLTRAINER_F, 9
	object_event  2,  8, SPRITE_COOLTRAINER_F, STAY, RIGHT, TEXT_ACADEMY_CHAMP_3, OPP_COOLTRAINER_F, 10
	object_event  6,  8, SPRITE_COOLTRAINER_M, STAY, LEFT, TEXT_ACADEMY_CHAMP_4, OPP_COOLTRAINER_M, 12

	def_warps_to ACADEMY
