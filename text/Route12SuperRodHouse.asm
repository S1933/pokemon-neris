_Route12SuperRodHouseFishingGuruDoYouLikeToFishText::
	text "Je suis le frere"
	line "du GURU PECHE!"

	para "J'adore vraiment"
	line "la peche!"

	para "Tu aimes"
	line "pecher?"
	done

_Route12SuperRodHouseFishingGuruReceivedSuperRodText::
	text "Super! J'aime"
	line "ton style!"

	para "Prends ceci et"
	line "va pecher, petit!"

	para "<PLAYER> recoit"
	line "un @"
	text_ram wStringBuffer
	text "!@"
	text_end

_Route12SuperRodHouseFishingGuruFishingWayOfLifeText::
	text_start

	para "La peche, c'est"
	line "un art de vivre!"

	para "Des mers aux"
	line "rivieres, va"
	cont "attraper le gros"
	cont "poisson!"
	done

_Route12SuperRodHouseFishingGuruThatsDisappointingText::
	text "Oh... C'est si"
	line "decevant..."
	done

_Route12SuperRodHouseFishingGuruTryFishingText::
	text "Salut par ici,"
	line "<PLAYER>!"

	para "Utilise la SUPER"
	line "ROD dans l'eau!"
	cont "Tu peux attraper"
	cont "plein de #MON"
	cont "differents."

	para "Essaie de"
	line "pecher partout!"
	done

_Route12SuperRodHouseFishingGuruNoRoomText::
	text "Oh non!"

	para "J'avais un"
	line "cadeau pour toi,"
	cont "mais tu n'as pas"
	cont "de place!"
	done
