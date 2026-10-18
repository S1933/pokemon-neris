_CableClubNPCPleaseComeAgainText::
	text "Revenez bientot!"
	done

_CableClubNPCMakingPreparationsText::
	text "Nous preparons"
	line "la connexion."
	cont "Patientez."
	done

_UsedStrengthText::
	text_ram wNameBuffer
	text " utilise"
	line "FORCE.@"
	text_end

_CanMoveBouldersText::
	text_ram wNameBuffer
	text " peut"
	line "deplacer les"
	cont "rochers."
	prompt

_CurrentTooFastText::
	text "Le courant est"
	line "bien trop fort!"
	prompt

_CyclingIsFunText::
	text "Le velo c'est fun!"
	line "Oublie le SURF!"
	prompt

_FlashLightsAreaText::
	text "Un FLASH aveuglant"
	line "eclaire les lieux!"
	prompt

_WarpToLastPokemonCenterText::
	text "Retour au dernier"
	line "CENTRE #MON."
	done

_CannotUseTeleportNowText::
	text_ram wNameBuffer
	text " ne"
	line "peut pas utiliser"
	cont "TELEPORT ici."
	prompt

_CannotFlyHereText::
	text_ram wNameBuffer
	text " ne"
	line "peut pas VOLER"
	cont "ici."
	prompt

_NotHealthyEnoughText::
	text "Pas assez de PV."
	prompt

_NewBadgeRequiredText::
	text "Non! Un nouveau"
	line "BADGE est requis."
	prompt

_CannotUseItemsHereText::
	text "Impossible"
	line "d'utiliser des"
	cont "objets ici."
	prompt

_CannotGetOffHereText::
	text "Impossible de"
	line "descendre ici."
	prompt

_GotMonText::
	text "<PLAYER> obtient"
	line "@"
	text_ram wNameBuffer
	text "!@"
	text_end

_SentToBoxText::
	text "Plus de place"
	line "pour les #MON!"
	cont "@"
	text_ram wBoxMonNicks
	text " est"
	cont "envoye dans la"
	cont "BOITE @"
	text_ram wStringBuffer
	text " du PC!"
	done

_BoxIsFullText::
	text "Plus de place"
	line "pour les #MON!"
	para "La BOITE #MON"
	line "est pleine!"
	para "Change de BOITE"
	line "dans un CENTRE"
	cont "#MON!"
	done
