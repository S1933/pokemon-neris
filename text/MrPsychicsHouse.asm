_MrPsychicsHouseMrPsychicYouWantedThisText::
	text "...Attends! Ne"
	line "dis rien!"

	para "Tu voulais"
	line "ceci!"
	prompt

_MrPsychicsHouseMrPsychicReceivedTM29Text::
	text "<PLAYER> recoit"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_MrPsychicsHouseMrPsychicTM29ExplanationText::
	text "TM29, c'est"
	line "PSYCHIC!"

	para "Ca peut baisser"
	line "la stat SPECIAL"
	cont "de la cible."
	done

_MrPsychicsHouseMrPsychicTM29NoRoomText::
	text "Ou veux-tu"
	line "mettre ca?"
	done
