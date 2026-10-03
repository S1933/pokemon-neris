_Route1Youngster1MartSampleText::
	text "Salut! Je"
	line "travaille"
	cont "au #MON MART."

	para "C'est une"
	line "boutique"
	cont "pratique,"
	cont "passe nous"
	cont "voir a"
	cont "VIRIDIAN CITY."

	para "Tiens, je"
	line "vais te"
	cont "donner un"
	cont "echantillon!"
	cont "Voila!"
	prompt

_Route1Youngster1GotPotionText::
	text "<PLAYER> obtient"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_Route1Youngster1AlsoGotPokeballsText::
	text "On vend aussi"
	line "des # BALLs"
	cont "pour capturer"
	cont "des #MON!"
	done

_Route1Youngster1NoRoomText::
	text "Tu as trop"
	line "de trucs"
	cont "sur toi!"
	done

_Route1Youngster2Text::
	text "Tu vois ces"
	line "corniches le"
	cont "long de la"
	cont "route?"

	para "Ca fait un"
	line "peu peur,"
	cont "mais tu peux"
	cont "sauter."

	para "Tu peux"
	line "revenir a"
	cont "PALLET TOWN"
	cont "plus vite."
	done

_Route1SignText::
	text "ROUTE 1"
	line "PALLET TOWN -"
	cont "VIRIDIAN CITY"
	done
