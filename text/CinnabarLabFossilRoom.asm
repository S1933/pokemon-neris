_CinnabarLabFossilRoomScientist1Text::
	text "Coucou!"

	para "Je suis un"
	line "important"
	cont "docteur!"

	para "J'etudie ici de"
	line "rares fossiles"
	cont "de #MON!"

	para "Toi! Tu as un"
	line "fossile pour"
	cont "moi?"
	prompt

_CinnabarLabFossilRoomScientist1NoFossilsText::
	text "Non! Quel"
	line "dommage!"
	done

_CinnabarLabFossilRoomScientist1GoForAWalkText::
	text "Ca prend un"
	line "moment!"

	para "Va faire un"
	line "petit tour!"
	done

_CinnabarLabFossilRoomScientist1FossilIsBackToLifeText::
	text "Ou etais-tu?"

	para "Ton fossile a"
	line "repris vie!"

	para "C'etait @"
	text_ram wStringBuffer
	text_start
	line "comme prevu!"
	prompt

_CinnabarLabFossilRoomScientist1SeesFossilText::
	text "Oh! C'est"
	line "@"
	text_ram wNameBuffer
	text "!"

	para "C'est le"
	line "fossile de"
	line "@"
	text_ram wStringBuffer
	text ", un"
	cont "#MON deja"
	cont "disparu!"

	para "Ma machine de"
	line "resurrection le"
	cont "fera revivre!"
	done

_CinnabarLabFossilRoomScientist1TakesFossilText::
	text "Alors! Donne-le"
	line "moi vite!"

	para "<PLAYER> tend"
	line "le @"
	text_ram wNameBuffer
	text "!"
	prompt

_CinnabarLabFossilRoomScientist1GoForAWalkText2::
	text "Ca prend un"
	line "moment!"

	para "Va faire un"
	line "petit tour!"
	done

_CinnabarLabFossilRoomScientist1ComeAgainText::
	text "Bah! Tu es"
	line "revenu!"
	done
