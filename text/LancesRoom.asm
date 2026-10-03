_LancesRoomLanceBeforeBattleText::
	text "Ah! J'ai"
	line "entendu"
	cont "parler de toi"
	cont "<PLAYER>!"

	para "Je dirige le"
	line "CONSEIL 4!"
	cont "Appelle-moi"
	cont "LANCE, le"
	cont "dresseur de"
	cont "dragons!"

	para "Tu sais que"
	line "les dragons"
	cont "sont des"
	cont "#MON"
	cont "mythiques!"

	para "Ils sont"
	line "durs a"
	cont "attraper et"
	cont "a elever,"
	cont "mais leurs"
	cont "pouvoirs"
	cont "sont"
	cont "superieurs!"

	para "Ils sont"
	line "presque"
	cont "invincibles!"

	para "Bon, t'es"
	line "pret a"
	cont "perdre?"

	para "Ton defi de"
	line "la LIGUE"
	cont "se termine"
	cont "avec moi,"
	cont "<PLAYER>!"
	done

_LancesRoomLanceEndBattleText::
	text "C'est ca!"

	para "Je deteste"
	line "l'admettre,"
	cont "mais tu es un"
	cont "maitre #MON!"
	prompt

_LancesRoomLanceAfterBattleText::
	text "J'arrive pas"
	line "a croire que"
	cont "mes dragons"
	cont "ont perdu"
	cont "contre toi,"
	cont "<PLAYER>!"

	para "Tu es"
	line "maintenant"
	cont "champion de"
	cont "la LIGUE"
	cont "#MON!"

	para "...Ou tu"
	line "l'aurais ete,"
	cont "mais il te"
	cont "reste un"
	cont "defi a"
	cont "relever."

	para "Tu dois"
	line "affronter"
	cont "un autre"
	cont "dresseur!"
	cont "Son nom"
	cont "est..."

	para "<RIVAL>!"
	line "Il a battu"
	cont "le CONSEIL 4"
	cont "avant toi!"

	para "C'est lui"
	line "le vrai"
	cont "champion de"
	cont "la LIGUE"
	cont "#MON!@"
	text_end
