_BluesHouseDaisyRivalAtLabText::
	text "Salut <PLAYER>!"
	line "<RIVAL> est au"
	cont "labo de Papy."
	done

_BluesHouseDaisyOfferMapText::
	text "Papy t'a demande"
	line "de faire une"
	cont "course? Tiens,"
	cont "ca t'aidera!"
	prompt

_GotMapText::
	text "<PLAYER> obtient"
	line "une @"
	text_ram wStringBuffer
	text "!@"
	text_end

_BluesHouseDaisyBagFullText::
	text "Tu as trop de"
	line "trucs sur toi."
	done

_BluesHouseDaisyUseMapText::
	text "Utilise la"
	line "TOWN MAP pour"
	cont "savoir ou tu es."
	done

_BluesHouseDaisyWalkingText::
	text "Les #MON sont"
	line "des etres"
	cont "vivants! S'ils"
	cont "sont fatigues,"
	cont "laisse-les se"
	cont "reposer!"
	done

_BluesHouseTownMapText::
	text "C'est une grande"
	line "carte! C'est"
	cont "bien utile!"
	done
