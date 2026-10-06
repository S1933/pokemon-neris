object_const_def
const_export LIGHTHOUSE_LUNARIS

Lighthouse_Object:
	db $3 ; border block

	def_warp_events
	warp_event  4, 11, LAST_MAP, 3
	warp_event  5, 11, LAST_MAP, 3

	def_bg_events

	def_object_events
	object_event  7,  2, SPRITE_MONSTER, STAY, DOWN, TEXT_LIGHTHOUSE_LUNARIS, MEWTWO, 70

	def_warps_to LIGHTHOUSE
