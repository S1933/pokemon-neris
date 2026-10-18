_CardKeySuccessText1::
	text "Bingo!@"
	text_end

_CardKeySuccessText2::
	text_start
	line "La CARTE MAGN."
	cont "a ouvert la porte!"
	done

_CardKeyFailText::
	text "Zut! Il faut une"
	line "CARTE MAGN.!"
	done

_TrainerNameText::
	text_ram wNameBuffer
	text ": @"
	text_end

_NoNibbleText::
	text "Pas une touche!"
	prompt

_NothingHereText::
	text "On dirait qu'il"
	line "n'y a rien ici."
	prompt

_ItsABiteText::
	text "Oh!"
	line "Ca mord!"
	prompt

_ExclamationText::
	text "!"
	done

_GroundRoseText::
	text "Le sol s'est"
	line "souleve!"
	done

_BoulderText::
	text "Il faut FORCE"
	line "pour le bouger!"
	done

_MartSignText::
	text "Tout pour vos"
	line "besoins en objets!"
	cont "BOUTIQUE #MON"
	done

_PokeCenterSignText::
	text "Soins gratuits!"
	line "CENTRE #MON"
	done

_FoundItemText::
	text "<PLAYER> trouve"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_NoMoreRoomForItemText::
	text "Plus de place pour"
	line "les objets!"
	done

_OaksAideHiText::
	text "Salut! Tu te"
	line "souviens de moi?"
	cont "L'ASSISTANT du"
	cont "PROF.SYLVE!"
	para "Si tu as capture"
	line "@"
	text_decimal hOaksAideRequirement, 1, 3
	text " especes de"
	cont "#MON, je dois"
	cont "te donner"
	cont "@"
	text_ram wOaksAideRewardItemName
	text "!"
	para "Alors, <PLAYER>!"
	line "As-tu capture au"
	cont "moins @"
	text_decimal hOaksAideRequirement, 1, 3
	text " especes"
	cont "de #MON?"
	done

_OaksAideUhOhText::
	text "Voyons voir..."
	line "Oh oh! Tu n'as"
	cont "que @"
	text_decimal hOaksAideNumMonsOwned, 1, 3
	text " especes"
	cont "de #MON!"
	para "Il en faut @"
	text_decimal hOaksAideRequirement, 1, 3
	text_start
	line "pour obtenir"
	cont "@"
	text_ram wOaksAideRewardItemName
	text "."
	done

_OaksAideComeBackText::
	text "Oh. Je vois."
	para "Quand tu auras @"
	text_decimal hOaksAideRequirement, 1, 3
	text_start
	line "especes, reviens"
	cont "pour @"
	text_ram wOaksAideRewardItemName
	text "."
	done

_OaksAideHereYouGoText::
	text "Super! Tu as"
	line "capture @"
	text_decimal hOaksAideNumMonsOwned, 1, 3
	text " especes"
	cont "de #MON!"
	cont "Felicitations!"
	para "Voici pour toi!"
	prompt

_OaksAideGotItemText::
	text "<PLAYER> obtient"
	line "@"
	text_ram wOaksAideRewardItemName
	text "!@"
	text_end

_OaksAideNoRoomText::
	text "Oh! Tu n'as plus"
	line "de place pour"
	cont "@"
	text_ram wOaksAideRewardItemName
	text "."
	done
