_ItemUseBallText00::
	text "Il a evite la"
	line "BALL!"
	para "Ce #MON ne peut"
	line "pas etre capture!"
	prompt

_ItemUseBallText01::
	text "Tu as rate le"
	line "#MON!"
	prompt

_ItemUseBallText02::
	text "Zut! Le #MON"
	line "s'est libere!"
	prompt

_ItemUseBallText03::
	text "Raah! On y etait"
	line "presque!"
	prompt

_ItemUseBallText04::
	text "Mince! C'etait"
	line "si proche!"
	prompt

_ItemUseBallText05::
	text "Et hop!"
	line "@"
	text_ram wEnemyMonNick
	text " est"
	cont "capture!@"
	text_end

_ItemUseBallText07::
	text_ram wBoxMonNicks
	text " est"
	line "envoye sur le"
	cont "PC de BILL!"
	prompt

_ItemUseBallText08::
	text_ram wBoxMonNicks
	text " est"
	line "envoye sur le"
	cont "PC de quelqu'un!"
	prompt

_ItemUseBallText06::
	text "Les donnees de"
	line "@"
	text_ram wEnemyMonNick
	text " sont"
	cont "dans le #DEX!@"
	text_end

_SurfingGotOnText::
	text "<PLAYER> monte sur"
	line "@"
	text_ram wNameBuffer
	text "!"
	prompt

_SurfingNoPlaceToGetOffText::
	text "Pas d'endroit"
	line "pour descendre!"
	prompt

_VitaminStatRoseText::
	text_ram wNameBuffer
	text ":"
	line "@"
	text_ram wStringBuffer
	text " monte."
	prompt

_VitaminNoEffectText::
	text "Ca n'aura aucun"
	line "effet."
	prompt

_ThrewBaitText::
	text "<PLAYER> lance"
	line "un APPAT."
	done

_ThrewRockText::
	text "<PLAYER> lance"
	line "un CAILLOU."
	done

_PlayedFluteNoEffectText::
	text "Tu joues de la"
	line "#FLUTE."
	para "Quel air"
	line "entrainant!"
	prompt

_FluteWokeUpText::
	text "Tous les #MON"
	line "endormis se"
	cont "reveillent."
	prompt

_PlayedFluteHadEffectText::
	text "<PLAYER> joue de"
	line "la #FLUTE.@"
	text_end

_CoinCaseNumCoinsText::
	text "Jetons"
	line "@"
	text_bcd wPlayerCoins, 2 | LEADING_ZEROES | LEFT_ALIGN
	text " "
	prompt

_ItemfinderFoundItemText::
	text "Oui! Le CHERCH'"
	line "OBJET indique un"
	cont "objet tout pres."
	prompt

_ItemfinderFoundNothingText::
	text "Non! Le CHERCH'"
	line "OBJET ne reagit"
	cont "pas."
	prompt

_RaisePPWhichTechniqueText::
	text "Augmenter les PP"
	line "de quelle attaque?"
	done

_RestorePPWhichTechniqueText::
	text "Restaurer les PP"
	line "de quelle attaque?"
	done

_PPMaxedOutText::
	text "Les PP de"
	line "@"
	text_ram wStringBuffer
	text_start
	cont "sont au maximum."
	prompt

_PPIncreasedText::
	text "Les PP de"
	line "@"
	text_ram wStringBuffer
	text_start
	cont "augmentent."
	prompt

_PPRestoredText::
	text "PP restaures."
	prompt

_BootedUpTMText::
	text "Lecture d'une CT!"
	prompt

_BootedUpHMText::
	text "Lecture d'une CS!"
	prompt

_TeachMachineMoveText::
	text "Elle contient"
	line "@"
	text_ram wStringBuffer
	text "!"
	para "Apprendre @"
	text_ram wStringBuffer
	text_start
	line "a un #MON?"
	done

_MonCannotLearnMachineMoveText::
	text_ram wNameBuffer
	text " n'est"
	line "pas compatible"
	cont "avec @"
	text_ram wStringBuffer
	text "."
	para "Il ne peut pas"
	line "apprendre"
	cont "@"
	text_ram wStringBuffer
	text "."
	prompt

_ItemUseNotTimeText::
	text "PROF.SYLVE:"
	line "<PLAYER>!"
	line "Ce n'est pas le"
	cont "moment!"
	prompt

_ItemUseNotYoursToUseText::
	text "Ce n'est pas a"
	line "toi!"
	prompt

_ItemUseNoEffectText::
	text "Ca n'aura aucun"
	line "effet."
	prompt

_ThrowBallAtTrainerMonText1::
	text "Le dresseur"
	line "devie la BALL!"
	prompt

_ThrowBallAtTrainerMonText2::
	text "Pas de vol!"
	prompt

_NoCyclingAllowedHereText::
	text "Velo interdit"
	next "ici."
	prompt

_NoSurfingHereText::
	text "Pas de SURF sur"
	line "@"
	text_ram wNameBuffer
	text " ici!"
	prompt

_BoxFullCannotThrowBallText::
	text "La BOITE #MON"
	line "est pleine! Objet"
	cont "inutilisable!"
	prompt
