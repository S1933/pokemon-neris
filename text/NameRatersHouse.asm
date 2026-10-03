_NameRatersHouseNameRaterWantMeToRateText::
	text "Bonjour,"
	line "bonjour! Je"
	cont "suis le juge"
	cont "des noms!"

	para "Veux-tu que"
	line "je note les"
	cont "surnoms de"
	cont "tes #MON?"
	done

_NameRatersHouseNameRaterWhichPokemonText::
	text "Quel #MON"
	line "dois-je"
	cont "voir?"
	prompt

_NameRatersHouseNameRaterGiveItANiceNameText::
	text_ram wNameBuffer
	text ", c'est ca?"
	line "Quel joli"
	cont "surnom!"

	para "Mais veux-tu"
	line "que je lui"
	cont "donne un nom"
	cont "plus beau?"

	para "Alors?"
	done

_NameRatersHouseNameRaterWhatShouldWeNameItText::
	text "Bon! Quel nom"
	line "lui donne-t-on?"
	prompt

_NameRatersHouseNameRaterPokemonHasBeenRenamedText::
	text "OK! Ce #MON"
	line "s'appelle"
	cont "desormais"
	cont "@"
	text_ram wBuffer
	text "!"

	para "C'est mieux"
	line "qu'avant!"
	done

_NameRatersHouseNameRaterComeAnyTimeYouLikeText::
	text "Bon! Reviens"
	line "quand tu veux!"
	done

_NameRatersHouseNameRaterATrulyImpeccableNameText::
	text_ram wNameBuffer
	text ", c'est ca?"
	line "Quel nom"
	cont "vraiment"
	cont "impeccable!"

	para "Prends bien"
	line "soin de @"
	text_ram wNameBuffer
	text "!"
	done
