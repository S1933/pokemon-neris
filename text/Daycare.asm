_DaycareGentlemanIntroText::
	text "Je tiens une"
	line "PENSION."
	cont "Veux-tu que"
	cont "j'eleve un de"
	cont "tes #MON?"
	done

_DaycareGentlemanWhichMonText::
	text "Quel #MON"
	line "dois-je elever?"
	prompt

_DaycareGentlemanWillLookAfterMonText::
	text "D'accord, je"
	line "m'occupe de @"
	text_ram wNameBuffer
	text_start
	cont "un moment."
	prompt

_DaycareGentlemanComeSeeMeInAWhileText::
	text "Reviens me voir"
	line "bientot."
	done

_DaycareGentlemanMonHasGrownText::
	text "Ton @"
	text_ram wNameBuffer
	text_start
	line "a beaucoup"
	cont "grandi!"

	para "En niveau, il a"
	line "gagne @"
	text_decimal wDayCareNumLevelsGrown, 1, 3
	text "!"

	para "Pas mal, non?"
	prompt

_DaycareGentlemanOweMoneyText::
	text "Tu me dois ¥@"
	text_bcd wDayCareTotalCost, 2 | LEADING_ZEROES | LEFT_ALIGN
	text_start
	line "pour recuperer"
	cont "ce #MON."
	done

_DaycareGentlemanGotMonBackText::
	text "<PLAYER> recoit"
	line "@"
	text_ram wDayCareMonName
	text " de retour!"
	done

_DaycareGentlemanMonNeedsMoreTimeText::
	text "Deja de retour?"
	line "Ton @"
	text_ram wNameBuffer
	text_start
	cont "a besoin de"
	cont "plus de temps"
	cont "avec moi."
	prompt
