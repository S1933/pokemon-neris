_DaycareGentlemanAllRightThenText::
	text "Tres bien,"
	line "@"
	text_end

_DaycareGentlemanComeAgainText::
	text "reviens me"
	line "voir."
	done

_DaycareGentlemanNoRoomForMonText::
	text "Tu n'as pas de"
	line "place pour ce"
	cont "#MON!"
	done

_DaycareGentlemanOnlyHaveOneMonText::
	text "Tu n'as qu'un"
	line "seul #MON sur"
	cont "toi."
	done

_DaycareGentlemanCantAcceptMonWithHMText::
	text "Je ne peux pas"
	line "accepter un"
	cont "#MON qui"
	cont "connait une CS."
	done

_DaycareGentlemanHeresYourMonText::
	text "Merci! Voici"
	line "ton #MON!"
	prompt

_DaycareGentlemanNotEnoughMoneyText::
	text "He, tu n'as pas"
	line "assez de ¥!"
	done
