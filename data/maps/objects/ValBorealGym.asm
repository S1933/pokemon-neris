object_const_def
const_export VALBOREALGYM_OLGA

ValBorealGym_Object:
	db $3 ; border block

	def_warp_events
	warp_event  4, 13, LAST_MAP, 3
	warp_event  5, 13, LAST_MAP, 3

	def_bg_events

	def_object_events
	object_event  4,  1, SPRITE_LORELEI, STAY, DOWN, TEXT_VALBOREALGYM_OLGA, OPP_LORELEI, 2

	def_warps_to VALBOREAL_GYM
