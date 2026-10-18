_FileDataDestroyedText::
	text "Les donnees de"
	line "sauvegarde sont"
	cont "detruites!"
	prompt

_WouldYouLikeToSaveText::
	text "Voulez-vous"
	line "SAUVER la partie?"
	done

_GameSavedText::
	text "<PLAYER> a"
	line "sauve la partie!"
	done

_OlderFileWillBeErasedText::
	text "L'ancienne partie"
	line "sera effacee."
	cont "D'accord?"
	done

_WhenYouChangeBoxText::
	text "Changer de BOITE"
	line "#MON sauvegarde"
	cont "la partie."
	para "D'accord?"
	done

_ChooseABoxText::
	text "Choisis une"
	line "BOITE <PKMN>.@"
	text_end

_EvolvedText::
	text_ram wStringBuffer
	text " evolue"
	done

_IntoText::
	text_start
	line "en @"
	text_ram wNameBuffer
	text "!"
	done

_StoppedEvolvingText::
	text "Hein? @"
	text_ram wStringBuffer
	text_start
	line "n'evolue plus!"
	prompt

_IsEvolvingText::
	text "Quoi? @"
	text_ram wStringBuffer
	text_start
	line "evolue!"
	done

_FellAsleepText::
	text "<TARGET>"
	line "s'endort!"
	prompt

_AlreadyAsleepText::
	text "<TARGET>"
	line "dort deja!"
	prompt

_PoisonedText::
	text "<TARGET>"
	line "est empoisonne!"
	prompt

_BadlyPoisonedText::
	text "<TARGET>"
	line "est gravement"
	cont "empoisonne!"
	prompt

_BurnedText::
	text "<TARGET>"
	line "est brule!"
	prompt

_FrozenText::
	text "<TARGET>"
	line "est gele!"
	prompt

_FireDefrostedText::
	text "Le feu degele"
	line "<TARGET>!"
	prompt

_MonsStatsRoseText::
	text "<USER>"
	line "@"
	text_ram wStringBuffer
	text "@"
	text_end

_GreatlyRoseText::
	text " monte"
	cont "beaucoup!"
	prompt

_RoseText::
	text " monte!"
	prompt

_MonsStatsFellText::
	text "<TARGET>"
	line "@"
	text_ram wStringBuffer
	text "@"
	text_end

_GreatlyFellText::
	text " baisse"
	cont "beaucoup!"
	prompt

_FellText::
	text " baisse!"
	prompt

_RanFromBattleText::
	text "<USER>"
	line "fuit le combat!"
	prompt

_RanAwayScaredText::
	text "<TARGET>"
	line "s'enfuit, apeure!"
	prompt

_WasBlownAwayText::
	text "<TARGET>"
	line "est expulse!"
	prompt

_ChargeMoveEffectText::
	text "<USER>@"
	text_end

_MadeWhirlwindText::
	text_start
	line "cree un cyclone!"
	prompt

_TookInSunlightText::
	text_start
	line "absorbe le soleil!"
	prompt

_LoweredItsHeadText::
	text_start
	line "baisse la tete!"
	prompt

_SkyAttackGlowingText::
	text_start
	line "brille!"
	prompt

_FlewUpHighText::
	text_start
	line "s'envole haut!"
	prompt

_DugAHoleText::
	text_start
	line "creuse un trou!"
	prompt

_BecameConfusedText::
	text "<TARGET>"
	line "devient confus!"
	prompt

_MimicLearnedMoveText::
	text "<USER>"
	line "apprend"
	cont "@"
	text_ram wNameBuffer
	text "!"
	prompt

_MoveWasDisabledText::
	text "<TARGET>:"
	line "@"
	text_ram wNameBuffer
	text_start
	cont "est bloquee!"
	prompt

_NothingHappenedText::
	text "Il ne se passe"
	line "rien!"
	prompt

_NoEffectText::
	text "Sans effet!"
	prompt

_ButItFailedText::
	text "Mais cela echoue!"
	prompt

_DidntAffectText::
	text "Ca n'affecte pas"
	line "<TARGET>!"
	prompt

_IsUnaffectedText::
	text "<TARGET>"
	line "n'est pas affecte!"
	prompt

_ParalyzedMayNotAttackText::
	text "<TARGET>"
	line "est paralyse! Il"
	cont "peut rater son"
	cont "attaque!"
	prompt

_SubstituteText::
	text "Un CLONAGE est"
	line "cree!"
	prompt

_HasSubstituteText::
	text "<USER>"
	line "a deja un CLONAGE!"
	prompt

_TooWeakSubstituteText::
	text "Trop faible pour"
	line "un CLONAGE!"
	prompt

_CoinsScatteredText::
	text "Des pieces"
	line "s'eparpillent!"
	prompt

_GettingPumpedText::
	text "<USER>"
	line "se concentre!"
	prompt

_WasSeededText::
	text "<TARGET>"
	line "est infecte!"
	prompt

_EvadedAttackText::
	text "<TARGET>"
	line "esquive l'attaque!"
	prompt

_HitWithRecoilText::
	text "<USER>"
	line "subit le recul!"
	prompt

_ConvertedTypeText::
	text "Type copie sur"
	line "<TARGET>!"
	prompt

_StatusChangesEliminatedText::
	text "Les changements"
	line "de STATUT sont"
	cont "annules!"
	prompt

_StartedSleepingEffect::
	text "<USER>"
	line "s'endort!"
	done

_FellAsleepBecameHealthyText::
	text "<USER>"
	line "s'endort et"
	cont "regagne ses PV!"
	done

_RegainedHealthText::
	text "<USER>"
	line "regagne des PV!"
	prompt

_TransformedText::
	text "<USER>"
	line "se transforme en"
	cont "@"
	text_ram wNameBuffer
	text "!"
	prompt

_LightScreenProtectedText::
	text "<USER>"
	line "se protege contre"
	cont "les attaques"
	cont "speciales!"
	prompt

_ReflectGainedArmorText::
	text "<USER>"
	line "gagne une armure!"
	prompt

_ShroudedInMistText::
	text "<USER>"
	line "est dans la brume!"
	prompt

_SuckedHealthText::
	text "L'energie de"
	line "<TARGET>"
	cont "est drainee!"
	prompt

_DreamWasEatenText::
	text "Le reve de"
	line "<TARGET>"
	cont "est devore!"
	prompt

_TradeCenterOpponentText::
	text "!"
	done

_ColosseumOpponentText::
	text "!"
	done
