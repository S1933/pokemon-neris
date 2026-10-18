_PokemartGreetingText::
	text "Bonjour!"
	next "Je peux t'aider?"
	done

_PokemonFaintedText::
	text_ram wNameBuffer
	text_start
	line "est K.O.!"
	done

_PlayerBlackedOutText::
	text "<PLAYER> n'a plus"
	line "de #MON valide!"
	para "<PLAYER> est"
	line "hors jeu!"
	prompt

_RepelWoreOffText::
	text "Le REPOUSSE ne"
	line "fait plus effet."
	done

_PokemartBuyingGreetingText::
	text "Prends ton temps."
	done

_PokemartTellBuyPriceText::
	text_ram wStringBuffer
	text "?"
	line "Ca fera"
	cont "¥@"
	text_bcd hMoney, 3 | LEADING_ZEROES | LEFT_ALIGN
	text ". OK?"
	done

_PokemartBoughtItemText::
	text "Voici!"
	line "Merci!"
	prompt

_PokemartNotEnoughMoneyText::
	text "Tu n'as pas assez"
	line "d'argent."
	prompt

_PokemartItemBagFullText::
	text "Tu ne peux plus"
	line "rien porter."
	prompt

_PokemonSellingGreetingText::
	text "Que veux-tu"
	line "vendre?"
	done

_PokemartTellSellPriceText::
	text "Je t'en donne"
	line "¥@"
	text_bcd hMoney, 3 | LEADING_ZEROES | LEFT_ALIGN
	text "."
	done

_PokemartItemBagEmptyText::
	text "Tu n'as rien"
	line "a vendre."
	prompt

_PokemartUnsellableItemText::
	text "Je ne peux pas"
	line "acheter ca."
	prompt

_PokemartThankYouText::
	text "Merci!"
	done

_PokemartAnythingElseText::
	text "Autre chose pour"
	line "ton service?"
	done

_LearnedMove1Text::
	text_ram wLearnMoveMonName
	text " apprend"
	line "@"
	text_ram wStringBuffer
	text "!@"
	text_end

_WhichMoveToForgetText::
	text "Quelle capacite"
	next "oublier?"
	done

_AbandonLearningText::
	text "Renoncer a"
	line "@"
	text_ram wStringBuffer
	text "?"
	done

_DidNotLearnText::
	text_ram wLearnMoveMonName
	text_start
	line "n'apprend pas"
	cont "@"
	text_ram wStringBuffer
	text "!"
	prompt

_TryingToLearnText::
	text_ram wLearnMoveMonName
	text " veut"
	line "apprendre"
	cont "@"
	text_ram wStringBuffer
	text "!"
	para "Mais @"
	text_ram wLearnMoveMonName
	text_start
	line "ne peut avoir que"
	cont "4 capacites!"
	para "Oublier une"
	line "capacite pour"
	cont "@"
	text_ram wStringBuffer
	text "?"
	done

_OneTwoAndText::
	text "1, 2 et...@"
	text_end

_PoofText::
	text " Tada!@"
	text_end

_ForgotAndText::
	text_start
	para "@"
	text_ram wLearnMoveMonName
	text " oublie"
	line "@"
	text_ram wNameBuffer
	text "!"
	para "Et..."
	prompt

_HMCantDeleteText::
	text "Impossible"
	line "d'oublier une CS!"
	prompt

_PokemonCenterWelcomeText::
	text "Bienvenue au"
	line "CENTRE #MON!"
	para "Nous soignons"
	line "vos #MON"
	cont "parfaitement!"
	prompt

_ShallWeHealYourPokemonText::
	text "Voulez-vous"
	line "soigner vos"
	cont "#MON?"
	done

_NeedYourPokemonText::
	text "Bien. Confiez-moi"
	line "vos #MON."
	done

_PokemonFightingFitText::
	text "Merci!"
	line "Vos #MON sont"
	cont "en pleine forme!"
	prompt

_PokemonCenterFarewellText::
	text "A bientot!"
	done

_CableClubNPCAreaReservedFor2FriendsLinkedByCableText::
	text "Cette zone est"
	line "reservee a 2"
	cont "amis relies par"
	cont "un cable."
	done

_CableClubNPCWelcomeText::
	text "Bienvenue au"
	line "Club Cable!"
	done

_CableClubNPCPleaseApplyHereHaveToSaveText::
	text "Inscrivez-vous."
	para "Avant la connexion"
	line "il faut sauver"
	cont "la partie."
	done

_CableClubNPCPleaseWaitText::
	text "Patientez.@"
	text_end

_CableClubNPCLinkClosedBecauseOfInactivityText::
	vc_patch Change_link_closed_inactivity_message
IF DEF(_RED_VC) || DEF(_BLUE_VC)
	text "Revenez bientot!"
	done
	text_start
	db   "osed because of"
	cont "inactivity."
ELSE
	text "La connexion a"
	line "ete coupee pour"
	cont "inactivite."
ENDC
	vc_patch_end

	para "Contactez votre"
	line "ami et revenez!"
	done
