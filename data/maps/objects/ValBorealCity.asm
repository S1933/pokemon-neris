object_const_def
const_export VALBOREALCITY_HIKER
const_export VALBOREALCITY_GIRL

ValBorealCity_Object:
	db $e ; border block

	def_warp_events
	warp_event 23, 25, VIRIDIAN_POKECENTER, 1
	warp_event 29, 19, VIRIDIAN_MART, 1
	warp_event 32,  7, VALBOREAL_GYM, 1

	def_bg_events

	def_object_events
	object_event  7, 14, SPRITE_HIKER, STAY, DOWN, TEXT_VALBOREALCITY_HIKER
	object_event 14, 21, SPRITE_LITTLE_GIRL, WALK, UP_DOWN, TEXT_VALBOREALCITY_GIRL

	def_warps_to VALBOREAL_CITY
