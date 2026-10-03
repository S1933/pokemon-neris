_SafariZoneSecretHouseFishingGuruYouHaveWonText::
	text "Ah! Enfin!"

	para "Tu es le premier a"
	line "atteindre la"
	cont "MAISON SECRETE!"

	para "Je craignais que"
	line "personne ne gagne"
	cont "notre prix!"

	para "Felicitations!"
	line "Tu as gagne!"
	prompt

_SafariZoneSecretHouseFishingGuruReceivedHM03Text::
	text "<PLAYER> recoit"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_SafariZoneSecretHouseFishingGuruHM03ExplanationText::
	text "HM03, c'est SURF!"

	para "Les #MON pourront"
	line "te faire traverser"
	cont "l'eau!"

	para "Et cette HM n'est"
	line "pas a usage"
	cont "unique! Tu peux"
	cont "l'utiliser encore"
	cont "et encore!"

	para "Tu as bien de la"
	line "chance d'avoir"
	cont "gagne ce fabuleux"
	cont "prix!"
	done

_SafariZoneSecretHouseFishingGuruHM03NoRoomText::
	text "Tu n'as pas de"
	line "place pour ce"
	cont "fabuleux prix!"
	done
