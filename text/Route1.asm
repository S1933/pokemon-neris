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
	cont "PORT-LUNE"
	cont "plus vite."
	done

_Route1SignText::
	text "SENTIER EMBRUNS"
	line "PORT-LUNE -"
	cont "VIRIDIAN CITY"
	done

_Route1KaelBattleText::
	text "KAEL: Tiens te"
	line "voila! Tu as"
	cont "ton #MON?"

	para "Alors montrez"
	line "moi sa force!"
	done

_Route1KaelEndBattleText::
	text "Trop fort"
	line "pour moi!"

	para "On fera mieux"
	line "la prochaine"
	cont "fois!"
	prompt

_Route1KaelAfterBattleText::
	text "KAEL: Je vais"
	line "m'entrainer et"
	cont "revenir te"
	cont "battre!"
	done
