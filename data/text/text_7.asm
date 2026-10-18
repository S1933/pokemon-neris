_ItemUseText001::
	text "<PLAYER> utilise@"
	text_end

_ItemUseText002::
	text_ram wStringBuffer
	text "!"
	done

_GotOnBicycleText1::
	text "<PLAYER> monte sur@"
	text_end

_GotOnBicycleText2::
	text_ram wStringBuffer
	text "!"
	prompt

_GotOffBicycleText1::
	text "<PLAYER> descend@"
	text_end

_GotOffBicycleText2::
	text "de la @"
	text_ram wStringBuffer
	text "."
	prompt

_ThrewAwayItemText::
	text "Tu jettes"
	line "@"
	text_ram wNameBuffer
	text "."
	prompt

_IsItOKToTossItemText::
	text "Jeter vraiment"
	line "@"
	text_ram wStringBuffer
	text "?"
	prompt

_TooImportantToTossText::
	text "C'est trop"
	line "important!"
	prompt

_AlreadyKnowsText::
	text_ram wNameBuffer
	text " connait"
	line "deja @"
	text_ram wStringBuffer
	text "!"
	prompt

_ConnectCableText::
	text "Bien, branche le"
	line "cable comme ca!"
	prompt

_TradedForText::
	text "<PLAYER> echange"
	line "@"
	text_ram wInGameTradeGiveMonName
	text " contre"
	cont "@"
	text_ram wInGameTradeReceiveMonName
	text "!@"
	text_end

_WannaTrade1Text::
	text "Je cherche un"
	line "@"
	text_ram wInGameTradeGiveMonName
	text "! Tu"
	para "l'echanges contre"
	line "@"
	text_ram wInGameTradeReceiveMonName
	text "? "
	done

_NoTrade1Text::
	text "Ooooh!"
	line "Tant pis..."
	done

_WrongMon1Text::
	text "Quoi? Ce n'est pas"
	line "@"
	text_ram wInGameTradeGiveMonName
	text "!"
	para "Si tu en trouves"
	line "un, reviens ici!"
	done

_Thanks1Text::
	text "Merci!"
	done

_AfterTrade1Text::
	text "Il est super, mon"
	line "@"
	text_ram wInGameTradeReceiveMonName
	text ", hein?"
	done

_WannaTrade2Text::
	text "Salut! Veux-tu"
	line "echanger ton"
	para "@"
	text_ram wInGameTradeGiveMonName
	text_start
	line "contre @"
	text_ram wInGameTradeReceiveMonName
	text "?"
	done

_NoTrade2Text::
	text "Bon, si tu ne"
	line "veux pas..."
	done

_WrongMon2Text::
	text "Hmm? Ce n'est pas"
	line "@"
	text_ram wInGameTradeGiveMonName
	text "."
	para "Pense a moi si"
	line "tu en trouves un."
	done

_Thanks2Text::
	text "Merci!"
	done

_AfterTrade2Text::
	text "Le @"
	text_ram wInGameTradeGiveMonName
	text " que"
	line "tu m'as donne"
	para "a evolue!"
	done

_WannaTrade3Text::
	text "Salut! As-tu un"
	line "@"
	text_ram wInGameTradeGiveMonName
	text "?"
	para "On l'echange"
	line "contre @"
	text_ram wInGameTradeReceiveMonName
	text "?"
	done

_NoTrade3Text::
	text "Dommage."
	done

_WrongMon3Text::
	text "...Ce n'est pas"
	line "@"
	text_ram wInGameTradeGiveMonName
	text "."
	para "Si tu en trouves"
	line "un, echange-le!"
	done

_Thanks3Text::
	text "Merci l'ami!"
	done

_AfterTrade3Text::
	text "Comment va mon"
	line "@"
	text_ram wInGameTradeReceiveMonName
	text "?"
	para "Mon @"
	text_ram wInGameTradeGiveMonName
	text " va"
	line "tres bien!"
	done

_NothingToCutText::
	text "Il n'y a rien"
	line "a COUPER!"
	prompt

_UsedCutText::
	text_ram wNameBuffer
	text " utilise"
	line "COUPE!"
	prompt
