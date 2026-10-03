_Route23YouDontHaveTheBadgeYetText::
	text "Tu peux"
	line "passer ici"
	cont "seulement si"
	cont "tu as le @"
	text_ram wNameBuffer
	text "!"

	para "Tu n'as pas"
	line "encore le @"
	text_ram wNameBuffer
	text "!"

	para "Il te le faut"
	line "pour aller a"
	cont "la LIGUE"
	cont "#MON!@"
	text_end

_Route23OhThatIsTheBadgeText::
	text "Tu peux"
	line "passer ici"
	cont "seulement si"
	cont "tu as le @"
	text_ram wNameBuffer
	text "!"

	para "Oh! C'est le @"
	text_ram wNameBuffer
	text "!@"
	text_end

_Route23GoRightAheadText::
	text_start

	para "OK alors!"
	line "Vas-y,"
	cont "je t'en prie!"
	done

_Route23VictoryRoadGateSignText::
	text "PORTE DE LA"
	line "ROUTE VICTOIRE"
	cont "- LIGUE #MON"
	done
