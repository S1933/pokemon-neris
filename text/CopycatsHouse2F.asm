_CopycatsHouse2FCopycatDoYouLikePokemonText::
	text "<PLAYER>: Salut!"
	line "T'aimes les"
	cont "#MON?"

	para "<PLAYER>: Bah"
	line "non, je te"
	cont "demandais."

	para "<PLAYER>: Hein?"
	line "T'es bizarre!"

	para "COPYCAT: Hein?"
	line "Tu m'imites?"

	para "Mais c'est mon"
	line "hobby prefere!"
	prompt

_CopycatsHouse2FCopycatTM31PreReceiveText::
	text "Oh wow!"
	line "Une # DOLL!"

	para "Pour moi?"
	line "Merci!"

	para "Alors tu peux"
	line "prendre ca!"
	prompt

_CopycatsHouse2FCopycatReceivedTM31Text::
	text "<PLAYER> recoit"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_CopycatsHouse2FCopycatTM31Explanation1Text::
	text_start

	para "La TM31"
	line "contient"
	cont "MIMIC,"
	cont "mon prefere!"

	para "Utilise-la"
	line "sur un bon"
	cont "#MON!@"
	text_end

_CopycatsHouse2FCopycatTM31Explanation2Text::
	text "<PLAYER>: Salut!"
	line "Merci pour"
	cont "la TM31!"

	para "<PLAYER>: Pardon?"

	para "<PLAYER>: C'est"
	line "si drole de"
	cont "copier tous"
	cont "mes gestes?"

	para "COPYCAT: Et"
	line "comment!"
	cont "C'est"
	cont "tordant!"
	done

_CopycatsHouse2FCopycatTM31NoRoomText::
	text "Tu n'en veux"
	line "pas?@"
	text_end

_CopycatsHouse2FDoduoText::
	text "DODUO: Giiih!"

	para "MIROIR,"
	line "MIROIR, QUI"
	cont "EST LA PLUS"
	cont "BELLE DE"
	cont "TOUTES?"
	done

_CopycatsHouse2FRareDollText::
	text "C'est un #MON"
	line "rare! Hein?"
	cont "C'est qu'une"
	cont "poupee!"
	done

_CopycatsHouse2FSNESText::
	text "Un jeu avec"
	line "MARIO qui"
	cont "porte un"
	cont "seau sur"
	cont "la tete!"
	done

_CopycatsHouse2FPCMySecretsText::
	text "..."

	para "Mes secrets!"

	para "Talent:"
	line "l'imitation!"

	para "Hobby:"
	line "collectionner"
	cont "des poupees!"

	para "#MON prefere:"
	line "CLEFAIRY!"
	done

_CopycatsHouse2FPCCantSeeText::
	text "Hein? Je"
	line "vois rien!"
	done
