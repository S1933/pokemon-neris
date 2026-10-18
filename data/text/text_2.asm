_AIBattleWithdrawText::
	text_ram wTrainerName
	text " rappelle"
	line "@"
	text_ram wEnemyMonNick
	text "!"
	prompt

_AIBattleUseItemText::
	text_ram wTrainerName
	text_start
	line "utilise @"
	text_ram wNameBuffer
	text_start
	cont "sur @"
	text_ram wEnemyMonNick
	text "!"
	prompt

_TradeWentToText::
	text_ram wStringBuffer
	text " part"
	line "chez @"
	text_ram wLinkEnemyTrainerName
	text "."
	done

_TradeForText::
	text "Contre le #MON"
	line "de <PLAYER>,"
	cont "@"
	text_ram wStringBuffer
	text ","
	done

_TradeSendsText::
	text_ram wLinkEnemyTrainerName
	text " envoie"
	line "@"
	text_ram wNameBuffer
	text "."
	done

_TradeWavesFarewellText::
	text_ram wLinkEnemyTrainerName
	text " fait"
	line "ses adieux et"
	done

_TradeTransferredText::
	text_ram wNameBuffer
	text " est"
	line "transfere."
	done

_TradeTakeCareText::
	text "Prends soin de"
	line "@"
	text_ram wNameBuffer
	text "."
	done

_TradeWillTradeText::
	text_ram wLinkEnemyTrainerName
	text " va"
	line "echanger @"
	text_ram wNameBuffer
	text_start
	done

_TradeforText::
	text "contre le #MON"
	line "de <PLAYER>,"
	cont "@"
	text_ram wStringBuffer
	text "."
	done

_PlaySlotMachineText::
	text "Machine a sous!"
	line "On joue?"
	done

_OutOfCoinsSlotMachineText::
	text "Zut!"
	line "Plus de jetons!"
	done

_BetHowManySlotMachineText::
	text "Combien de jetons"
	line "miser?"
	done

_StartSlotMachineText::
	text "C'est parti!"
	done

_NotEnoughCoinsSlotMachineText::
	text "Pas assez de"
	line "jetons!"
	prompt

_OneMoreGoSlotMachineText::
	text "Encore une"
	line "partie?"
	done

_LinedUpText::
	text " alignes!"
	line "Gain: @"
	text_ram wStringBuffer
	text " jetons!"
	done

_NotThisTimeText::
	text "Pas cette fois!"
	prompt

_YeahText::
	text "Ouais!@"
	text_end

_DexSeenOwnedText::
	text "#DEX   Vus:@"
	text_decimal wDexRatingNumMonsSeen, 1, 3
	text_start
	line "         Pris:@"
	text_decimal wDexRatingNumMonsOwned, 1, 3
	text_end

_DexRatingText::
	text "Note du #DEX<COLON>"
	done

_GymStatueText1::
	text_ram wGymCityName
	text_start
	line "CHAMPION D'ARENE:"
	cont "@"
	text_ram wGymLeaderName
	text_start
	para "VAINQUEURS:"
	line "<RIVAL>"
	done

_GymStatueText2::
	text_ram wGymCityName
	text_start
	line "CHAMPION D'ARENE:"
	cont "@"
	text_ram wGymLeaderName
	text_start
	para "VAINQUEURS:"
	line "<RIVAL>"
	cont "<PLAYER>"
	done

_ViridianCityPokecenterGuyText::
	text "Les CENTRES"
	line "soignent tes"
	cont "#MON fatigues,"
	cont "blesses ou K.O.!"
	done

_PewterCityPokecenterGuyText::
	text "Baaah!"
	para "Quand RONDOUDOU"
	line "chante, les"
	cont "#MON dorment..."
	para "...Moi aussi..."
	line "Rrrr..."
	done

_CeruleanPokecenterGuyText::
	text "BILL a plein de"
	line "#MON!"
	para "Il collectionne"
	line "aussi les rares!"
	done

_LavenderPokecenterGuyText::
	text "Les OSSELAIT"
	line "portent un crane,"
	cont "pas vrai?"
	para "Ca vaut une"
	line "fortune!"
	done

_MtMoonPokecenterBenchGuyText::
	text "Si tu as trop de"
	line "#MON, range-les"
	cont "dans le PC!"
	done

_RockTunnelPokecenterGuyText::
	text "Il parait que des"
	line "SPECTRES hantent"
	cont "LAVANVILLE!"
	done

_UnusedBenchGuyText1::
	text "J'aimerais bien"
	line "attraper des"
	cont "#MON."
	done

_UnusedBenchGuyText2::
	text "Je suis creve,"
	line "on s'est bien"
	cont "amuses..."
	done

_UnusedBenchGuyText3::
	text "Le directeur de"
	line "SYLPHE se cache"
	cont "au PARC SAFARI."
	done

_VermilionPokecenterGuyText::
	text "C'est vrai qu'un"
	line "#MON de haut"
	cont "niveau est plus"
	cont "puissant..."
	para "Mais tous les"
	line "#MON ont des"
	cont "faiblesses contre"
	cont "certains types."
	para "Aucun #MON"
	line "n'est donc fort"
	cont "contre tout."
	done

_CeladonCityPokecenterGuyText::
	text "Si j'avais un"
	line "VELO, j'irais sur"
	cont "la PISTE CYCLABLE!"
	done

_FuchsiaCityPokecenterGuyText::
	text "Pour etudier les"
	line "#MON, va au"
	cont "PARC SAFARI."
	para "Il y a plein de"
	line "#MON rares."
	done

_CinnabarPokecenterGuyText::
	text "Un #MON peut"
	line "apprendre des"
	cont "capacites meme si"
	cont "tu annules son"
	cont "evolution."
	para "L'evolution peut"
	line "attendre qu'il ait"
	cont "appris ses"
	cont "capacites."
	done

_SaffronCityPokecenterGuyText1::
	text "Ce serait super"
	line "si le CONSEIL 4"
	cont "venait ecraser"
	cont "la TEAM ROCKET!"
	done

_SaffronCityPokecenterGuyText2::
	text "La TEAM ROCKET est"
	line "partie! On peut"
	cont "ressortir sans"
	cont "danger! Genial!"
	done

_CeladonCityHotelText::
	text "Ma soeur m'emmene"
	line "en vacances ici!"
	done

_BookcaseText::
	text "Plein de livres"
	line "sur les #MON!"
	done

_NewBicycleText::
	text "Une BICYCLETTE"
	line "toute neuve!"
	done

_PushStartText::
	text "Appuie sur START"
	line "pour le MENU!"
	done

_SaveOptionText::
	text "L'option SAUVER"
	line "est dans le MENU."
	done

_StrengthsAndWeaknessesText::
	text "Chaque type de"
	line "#MON a des"
	cont "forces et des"
	cont "faiblesses."
	done

_TimesUpText::
	text "HP: Ding-dong!"
	para "Temps ecoule!"
	prompt

_GameOverText::
	text "HP: Votre partie"
	line "SAFARI est finie!"
	done

_CinnabarGymQuizIntroText::
	text "Quiz #MON!"
	para "Bonne reponse: la"
	line "porte s'ouvre sur"
	cont "la salle suivante!"
	para "Mauvaise reponse:"
	line "un dresseur!"
	para "Pour garder tes"
	line "#MON en forme"
	cont "pour le CHAMPION"
	cont "D'ARENE..."
	para "Reponds juste!"
	line "C'est parti!"
	prompt

_CinnabarQuizQuestionsText1::
	text "CHENIPAN evolue"
	line "en PAPILUSION?"
	done

_CinnabarQuizQuestionsText2::
	text "Il existe 9"
	line "BADGES officiels"
	cont "de la LIGUE?"
	done

_CinnabarQuizQuestionsText3::
	text "PTITARD evolue"
	line "3 fois?"
	done

_CinnabarQuizQuestionsText4::
	text "Les attaques"
	line "electriques sont"
	cont "efficaces contre"
	cont "le type SOL?"
	done

_CinnabarQuizQuestionsText5::
	text "Deux #MON de"
	line "meme espece et"
	cont "meme niveau sont"
	cont "differents?"
	done

_CinnabarQuizQuestionsText6::
	text "La CT28 contient"
	line "PIERRETOMBE?"
	done

_CinnabarGymQuizCorrectText::
	text "Parfaitement"
	line "exact!"
	para "Tu peux passer!@"
	text_end

_CinnabarGymQuizIncorrectText::
	text "Desole! Rate!"
	prompt

_MagazinesText::
	text "Magazines #MON!"
	para "Carnets #MON!"
	para "Courbes #MON!"
	done

_BillsHouseMonitorText::
	text "TELEPORTEUR est"
	line "affiche sur"
	cont "l'ecran du PC."
	done

_BillsHouseInitiatedText::
	text "<PLAYER> lance le"
	line "Separateur de"
	cont "Cellules!@"
	text_end

_BillsHousePokemonListText1::
	text "Les #MON"
	line "preferes de BILL!"
	prompt

_BillsHousePokemonListText2::
	text "Quel #MON"
	line "veux-tu voir?"
	done

_OakLabEmailText::
	text "Il y a un e-mail"
	line "ici!"
	para "..."
	para "Appel a tous les"
	line "dresseurs #MON!"
	para "L'elite de la"
	line "LIGUE #MON"
	cont "attend tous les"
	cont "challengers!"
	para "Venez avec vos"
	line "meilleurs #MON"
	cont "et mesurez votre"
	cont "talent!"
	para "QG LIGUE #MON"
	line "PLATEAU INDIGO"
	para "PS: PROF.SYLVE,"
	line "venez nous voir!"
	cont "..."
	done

_GameCornerCoinCaseText::
	text "Il faut une"
	line "BOITE JETON!"
	done

_GameCornerNoCoinsText::
	text "Tu n'as aucun"
	line "jeton!"
	done

_GameCornerOutOfOrderText::
	text "HORS SERVICE"
	line "C'est en panne."
	done

_GameCornerOutToLunchText::
	text "PARTI DEJEUNER"
	line "C'est reserve."
	done

_GameCornerSomeonesKeysText::
	text "Des cles!"
	line "On va revenir."
	done

_JustAMomentText::
	text "Un instant."
	done

TMNotebookText::
	text "C'est une brochure"
	line "sur les CT."
	para "..."
	para "Il existe 50 CT"
	line "en tout."
	para "Il existe aussi 5"
	line "CS reutilisables"
	cont "a volonte."
	para "SYLPHE SARL@"
	text_end

_TurnPageText::
	text "Tourner la page?"
	done

_ViridianSchoolNotebookText5::
	text "FILLE: He! Ne"
	line "lis pas mes notes!@"
	text_end

_ViridianSchoolNotebookText1::
	text "Tu regardes le"
	line "cahier!"
	para "Premiere page..."
	para "Les # BALLS"
	line "servent a"
	cont "capturer des"
	cont "#MON."
	para "On peut porter"
	line "jusqu'a 6 #MON."
	para "Ceux qui elevent"
	line "et font combattre"
	cont "des #MON sont"
	cont "des dresseurs."
	prompt

_ViridianSchoolNotebookText2::
	text "Deuxieme page..."
	para "Un #MON en"
	line "pleine forme est"
	cont "dur a capturer:"
	cont "affaiblis-le!"
	para "Poison, brulure"
	line "et autres degats"
	cont "sont efficaces!"
	prompt

_ViridianSchoolNotebookText3::
	text "Troisieme page..."
	para "Les dresseurs"
	line "cherchent des"
	cont "adversaires pour"
	cont "se battre."
	para "On se bat sans"
	line "cesse dans les"
	cont "ARENES #MON."
	prompt

_ViridianSchoolNotebookText4::
	text "Quatrieme page..."
	para "Le but des"
	line "dresseurs est de"
	cont "battre les 8"
	cont "CHAMPIONS"
	cont "D'ARENE."
	para "Ils gagnent alors"
	line "le droit d'aller"
	cont "defier..."
	para "Le CONSEIL 4 de"
	line "la LIGUE #MON!"
	prompt

_EnemiesOnEverySideText::
	text "Des ennemis de"
	line "tous cotes!"
	done

_WhatGoesAroundComesAroundText::
	text "Qui seme le vent"
	line "recolte la"
	cont "tempete!"
	done

_FightingDojoText::
	text "DOJO DE COMBAT"
	done

_IndigoPlateauHQText::
	text "PLATEAU INDIGO"
	line "QG LIGUE #MON"
	done

_RedBedroomSNESText::
	text "<PLAYER> joue"
	line "a la SNES!"
	cont "...Bon!"
	cont "Il est temps"
	cont "d'y aller!"
	done

_Route15UpstairsBinocularsText::
	text "Tu regardes dans"
	line "les jumelles..."
	para "Un grand oiseau"
	line "brillant vole"
	cont "vers la mer."
	done

_AerodactylFossilText::
	text "Fossile PTERA"
	line "Un #MON rare"
	cont "et primitif."
	done

_KabutopsFossilText::
	text "Fossile KABUTOPS"
	line "Un #MON rare"
	cont "et primitif."
	done

_LinkCableHelpText1::
	text "CONSEILS"
	line "DE DRESSEUR"
	para "Utiliser un"
	line "Cable Link"
	prompt

_LinkCableHelpText2::
	text "Quel sujet"
	line "veux-tu lire?"
	done

_LinkCableInfoText1::
	text "Une fois ta GAME"
	line "BOY reliee a une"
	cont "autre GAME BOY,"
	cont "parle a l'hotesse"
	cont "de droite dans"
	cont "un CENTRE #MON."
	prompt

_LinkCableInfoText2::
	text "Le COLISEE permet"
	line "d'affronter un"
	cont "ami."
	prompt

_LinkCableInfoText3::
	text "Le CENTRE TROC"
	line "sert a echanger"
	cont "des #MON."
	prompt

_ViridianSchoolBlackboardText1::
	text "Le tableau parle"
	line "des changements"
	cont "de STATUT en"
	cont "combat."
	prompt

_ViridianSchoolBlackboardText2::
	text "Quel sujet"
	line "veux-tu lire?"
	done

_ViridianBlackboardSleepText::
	text "Un #MON"
	line "endormi ne peut"
	cont "pas attaquer!"
	para "Il reste endormi"
	line "meme apres le"
	cont "combat."
	para "Utilise un REVEIL"
	line "pour le reveiller!"
	prompt

_ViridianBlackboardPoisonText::
	text "Empoisonne, un"
	line "#MON perd des"
	cont "PV peu a peu."
	para "Le poison reste"
	line "apres le combat."
	para "Utilise un"
	line "ANTIDOTE pour"
	cont "le soigner!"
	prompt

_ViridianBlackboardPrlzText::
	text "La paralysie peut"
	line "faire rater les"
	cont "attaques!"
	para "Elle reste apres"
	line "le combat."
	para "Utilise un"
	line "ANTI-PARA pour"
	cont "la soigner!"
	prompt

_ViridianBlackboardBurnText::
	text "Une brulure baisse"
	line "la puissance et"
	cont "la vitesse, et"
	cont "fait des degats."
	para "Elle reste apres"
	line "le combat."
	para "Utilise un"
	line "ANTI-BRULE pour"
	cont "la soigner!"
	prompt

_ViridianBlackboardFrozenText::
	text "Gele, un #MON"
	line "ne peut plus"
	cont "bouger du tout!"
	para "Il reste gele"
	line "meme apres le"
	cont "combat."
	para "Utilise un"
	line "ANTIGEL pour le"
	cont "degeler!"
	prompt

_VermilionGymTrashText::
	text "Non, il n'y a que"
	line "des dechets ici."
	done

_VermilionGymTrashSuccessText1::
	text "He! Il y a un"
	line "interrupteur sous"
	cont "les dechets!"
	cont "Allume-le!"
	para "Le 1er verrou"
	line "electrique saute!@"
	text_end

_VermilionGymTrashSuccessText2::
	text "He! Il y a un"
	line "autre interrupteur"
	cont "sous les dechets!"
	cont "Allume-le!"
	prompt

_VermilionGymTrashSuccessText3::
	text "Le 2e verrou"
	line "electrique saute!"
	para "La porte"
	line "motorisee s'ouvre!@"
	text_end

_VermilionGymTrashFailText::
	text "Non! Rien que des"
	line "dechets ici."
	cont "He! Les verrous"
	cont "sont remis a zero!@"
	text_end

_FoundHiddenItemText::
	text "<PLAYER> trouve"
	line "@"
	text_ram wNameBuffer
	text "!@"
	text_end

_HiddenItemBagFullText::
	text "Mais <PLAYER> n'a"
	line "plus de place pour"
	cont "d'autres objets!"
	done

_FoundHiddenCoinsText::
	text "<PLAYER> trouve"
	line "@"
	text_bcd hCoins, 2 | LEADING_ZEROES | LEFT_ALIGN
	text " jetons!@"
	text_end

_FoundHiddenCoins2Text::
	text "<PLAYER> trouve"
	line "@"
	text_bcd hCoins, 2 | LEADING_ZEROES | LEFT_ALIGN
	text " jetons!@"
	text_end

_DroppedHiddenCoinsText::
	text_start
	para "Oups! Des jetons"
	line "sont tombes!"
	done

_IndigoPlateauStatuesText1::
	text "PLATEAU INDIGO"
	prompt

_IndigoPlateauStatuesText2::
	text "Le but ultime"
	line "des dresseurs!"
	cont "QG LIGUE #MON"
	done

_IndigoPlateauStatuesText3::
	text "La plus haute"
	line "autorite #MON"
	cont "QG LIGUE #MON"
	done

_PokemonBooksText::
	text "Plein de livres"
	line "sur les #MON!"
	done

_DiglettSculptureText::
	text "Une sculpture"
	line "de TAUPIQUEUR."
	done

_ElevatorText::
	text "C'est un"
	line "ascenseur."
	done

_TownMapText::
	text "Une CARTE.@"
	text_end

_PokemonStuffText::
	text "Ouah! Des tas de"
	line "trucs #MON!"
	done

_OutOfSafariBallsText::
	text "HP: Ding-dong!"
	para "Vous n'avez plus"
	line "de SAFARI BALLS!"
	prompt

_WildRanText::
	text_ram wEnemyMonNick
	text " sauvage"
	line "s'enfuit!"
	prompt

_EnemyRanText::
	text_ram wEnemyMonNick
	text " ennemi"
	line "s'enfuit!"
	prompt

_HurtByPoisonText::
	text "<USER>"
	line "souffre du poison!"
	prompt

_HurtByBurnText::
	text "<USER>"
	line "souffre de sa"
	cont "brulure!"
	prompt

_HurtByLeechSeedText::
	text "VAMPIGRAINE draine"
	line "<USER>!"
	prompt

_EnemyMonFaintedText::
	text_ram wEnemyMonNick
	text " ennemi"
	line "est K.O.!"
	prompt

_MoneyForWinningText::
	text "<PLAYER> gagne"
	line "¥@"
	text_bcd wAmountMoneyWon, 3 | LEADING_ZEROES | LEFT_ALIGN
	text "!"
	prompt

_TrainerDefeatedText::
	text "<PLAYER> a battu"
	line "@"
	text_ram wTrainerName
	text "!"
	prompt

_PlayerMonFaintedText::
	text_ram wBattleMonNick
	text_start
	line "est K.O.!"
	prompt

_UseNextMonText::
	text "Envoyer un autre"
	line "#MON?"
	done

_Rival1WinText::
	text "<RIVAL>: Ouais!"
	line "Je suis trop fort!"
	prompt

_PlayerBlackedOutText2::
	text "<PLAYER> n'a plus"
	line "de #MON valide!"
	para "<PLAYER> est"
	line "hors jeu!"
	prompt

_LinkBattleLostText::
	text "<PLAYER> a perdu"
	line "contre @"
	text_ram wTrainerName
	text "!"
	prompt

_TrainerAboutToUseText::
	text_ram wTrainerName
	text " va"
	line "envoyer @"
	text_ram wEnemyMonNick
	text "!"
	para "<PLAYER> change"
	line "de #MON?"
	done

_TrainerSentOutText::
	text_ram wTrainerName
	text " envoie"
	line "@"
	text_ram wEnemyMonNick
	text "!"
	done

_NoWillText::
	text "Il n'a plus la"
	line "force de lutter!"
	prompt

_CantEscapeText::
	text "Fuite impossible!"
	prompt

_NoRunningText::
	text "Non! Pas de fuite"
	line "dans un combat"
	cont "de dresseurs!"
	prompt

_GotAwayText::
	text "Vous prenez la"
	line "fuite!"
	prompt

_ItemsCantBeUsedHereText::
	text "Pas d'objets"
	line "ici."
	prompt

_AlreadyOutText::
	text_ram wBattleMonNick
	text " est"
	line "deja au combat!"
	prompt

_MoveNoPPText::
	text "Plus de PP pour"
	line "cette capacite!"
	prompt

_MoveDisabledText::
	text "Cette capacite"
	line "est bloquee!"
	prompt

_NoMovesLeftText::
	text_ram wBattleMonNick
	text " n'a"
	line "plus de capacite!"
	done

_MultiHitText::
	text "Touche @"
	text_decimal wPlayerNumHits, 1, 1
	text " fois!"
	prompt

_ScaredText::
	text_ram wBattleMonNick
	text " a trop"
	line "peur pour bouger!"
	prompt

_GetOutText::
	text "SPECTRE: Va-t'en.."
	line "Va-t'en..."
	prompt

_FastAsleepText::
	text "<USER>"
	line "dort profondement!"
	prompt

_WokeUpText::
	text "<USER>"
	line "se reveille!"
	prompt

_IsFrozenText::
	text "<USER>"
	line "est gele!"
	prompt

_FullyParalyzedText::
	text "<USER>"
	line "est paralyse!"
	prompt

_FlinchedText::
	text "<USER>"
	line "a la trouille!"
	prompt

_MustRechargeText::
	text "<USER>"
	line "doit recharger!"
	prompt

_DisabledNoMoreText::
	text "<USER>"
	line "n'est plus bloque!"
	prompt

_IsConfusedText::
	text "<USER>"
	line "est confus!"
	prompt

_HurtItselfText::
	text "Il se blesse dans"
	line "sa confusion!"
	prompt

_ConfusedNoMoreText::
	text "<USER>"
	line "n'est plus confus!"
	prompt

_SavingEnergyText::
	text "<USER>"
	line "concentre son"
	cont "energie!"
	prompt

_UnleashedEnergyText::
	text "<USER>"
	line "libere l'energie!"
	prompt

_ThrashingAboutText::
	text "<USER>"
	line "se dechaine!"
	done

_AttackContinuesText::
	text "<USER>"
	line "poursuit!"
	done

_CantMoveText::
	text "<USER>"
	line "ne peut bouger!"
	prompt

_MoveIsDisabledText::
	text "<USER>:"
	line "@"
	text_ram wNameBuffer
	text_start
	cont "est bloquee!"
	prompt

_ActorNameText::
	text "<USER>@"
	text_end

_UsedMove1Text::
	text_start
	line "lance @"
	text_end

_UsedMove2Text::
	text_start
	line "lance @"
	text_end

_UsedInsteadText::
	text "plutot"
	cont "@"
	text_end

_MoveNameText::
	text_ram wStringBuffer
	text "@"

_EndUsedMove1Text:: ; 12-letter move names: no room for "!"
	text "@"
	done

_EndUsedMove2Text::
	text "!"
	done

_EndUsedMove3Text::
	text "!"
	done

_EndUsedMove4Text::
	text "!"
	done

_EndUsedMove5Text::
	text "!"
	done

_AttackMissedText::
	text "<USER>"
	line "rate son attaque!"
	prompt

_KeptGoingAndCrashedText::
	text "<USER>"
	line "s'ecrase au sol!"
	prompt

_UnaffectedText::
	text "<TARGET>"
	line "n'est pas affecte!"
	prompt

_DoesntAffectMonText::
	text "Ca n'affecte pas"
	line "<TARGET>!"
	prompt

_CriticalHitText::
	text "Coup critique!"
	prompt

_OHKOText::
	text "K.O. en un coup!"
	prompt

_LoafingAroundText::
	text_ram wBattleMonNick
	text " paresse."
	prompt

_BeganToNapText::
	text_ram wBattleMonNick
	text " fait"
	line "la sieste!"
	prompt

_WontObeyText::
	text_ram wBattleMonNick
	text_start
	line "n'obeit pas!"
	prompt

_TurnedAwayText::
	text_ram wBattleMonNick
	text_start
	line "se detourne!"
	prompt

_IgnoredOrdersText::
	text_ram wBattleMonNick
	text_start
	line "ignore les ordres!"
	prompt

_SubstituteTookDamageText::
	text "Le CLONAGE subit"
	line "les degats pour"
	cont "<TARGET>!"
	prompt

_SubstituteBrokeText::
	text "Le CLONAGE de"
	line "<TARGET>"
	cont "est detruit!"
	prompt

_BuildingRageText::
	text "La FRENESIE de"
	line "<USER>"
	cont "augmente!"
	prompt

_MirrorMoveFailedText::
	text "MIMIQUE"
	next "echoue!"
	prompt

_HitXTimesText::
	text "Touche @"
	text_decimal wEnemyNumHits, 1, 1
	text " fois!"
	prompt

_GainedText::
	text_ram wNameBuffer
	text " gagne"
	line "@"
	text_end

_WithExpAllText::
	text "avec MULTI EXP,"
	cont "@"
	text_end

_BoostedText::
	text "en bonus"
	cont "@"
	text_end

_ExpPointsText::
	text_decimal wExpAmountGained, 2, 4
	text " points EXP.!"
	prompt

_GrewLevelText::
	text_ram wNameBuffer
	text " monte"
	line "au niveau @"
	text_decimal wCurEnemyLevel, 1, 3
	text "!@"
	text_end

_WildMonAppearedText::
	text "Un @"
	text_ram wEnemyMonNick
	text " sauvage"
	line "apparait!"
	prompt

_HookedMonAttackedText::
	text_ram wEnemyMonNick
	text_start
	line "a mordu et"
	cont "attaque!"
	prompt

_EnemyAppearedText::
	text_ram wEnemyMonNick
	text_start
	line "apparait!"
	prompt

_TrainerWantsToFightText::
	text_ram wTrainerName
	text " veut"
	line "se battre!"
	prompt

_UnveiledGhostText::
	text "Le SCOPE SYLPHE"
	line "revele l'identite"
	cont "du SPECTRE!"
	prompt

_GhostCantBeIDdText::
	text "Zut! Impossible"
	line "d'identifier le"
	cont "SPECTRE!"
	prompt

_GoText::
	text "Vas-y! @"
	text_end

_DoItText::
	text "A toi! @"
	text_end

_GetmText::
	text "Fonce! @"
	text_end

_EnemysWeakText::
	text "L'ennemi faiblit!"
	line "Fonce! @"
	text_end

_PlayerMon1Text::
	text_ram wBattleMonNick
	text "!"
	done

_PlayerMon2Text::
	text_ram wBattleMonNick
	text " @"
	text_end

_EnoughText::
	text "ca suffit!@"
	text_end

_OKExclamationText::
	text "OK!@"
	text_end

_GoodText::
	text "bravo!@"
	text_end

_ComeBackText::
	text_start
	line "Reviens!"
	done

_SuperEffectiveText::
	text "C'est super"
	line "efficace!"
	prompt

_NotVeryEffectiveText::
	text "Ce n'est pas tres"
	line "efficace..."
	prompt

_SafariZoneEatingText::
	text_ram wEnemyMonNick
	text " sauvage"
	line "mange!"
	prompt

_SafariZoneAngryText::
	text_ram wEnemyMonNick
	text " sauvage"
	line "est en colere!"
	prompt
_PickUpPayDayMoneyText::
	text "<PLAYER> ramasse"
	line "¥@"
	text_bcd wTotalPayDayMoney, 3 | LEADING_ZEROES | LEFT_ALIGN
	text "!"
	prompt

_ClearSaveDataText::
	text "Effacer toutes"
	line "les donnees?"
	done

_WhichFloorText::
	text "Quel etage"
	line "voulez-vous?"
	done

_PartyMenuNormalText:: ; short: the battle SWITCH menu covers cols 10+
	text "Quel"
	line "#MON?"
	done

_PartyMenuItemUseText::
	text "Utiliser sur"
	line "quel #MON?"
	done

_PartyMenuBattleText::
	text "Envoyer quel"
	line "#MON?"
	done

_PartyMenuUseTMText::
	text "Utiliser la CT"
	line "sur quel #MON?"
	done

_PartyMenuSwapMonText::
	text "Deplacer le"
	line "#MON ou?"
	done

_PotionText::
	text_ram wNameBuffer
	text_start
	line "recupere @"
	text_decimal wHPBarHPDifference, 2, 3
	text " PV!"
	done

_AntidoteText::
	text_ram wNameBuffer
	text " est"
	line "gueri du poison!"
	done

_ParlyzHealText::
	text_ram wNameBuffer
	text " n'est"
	line "plus paralyse!"
	done

_BurnHealText::
	text_ram wNameBuffer
	text " n'est"
	line "plus brule!"
	done

_IceHealText::
	text_ram wNameBuffer
	text " est"
	line "degele!"
	done

_AwakeningText::
	text_ram wNameBuffer
	text_start
	line "se reveille!"
	done

_FullHealText::
	text_ram wNameBuffer
	text " est"
	line "en pleine forme!"
	done

_ReviveText::
	text_ram wNameBuffer
	text_start
	line "est ranime!"
	done

_RareCandyText::
	text_ram wNameBuffer
	text " monte"
	line "au niveau @"
	text_decimal wCurEnemyLevel, 1, 3
	text "!@"
	text_end

_TurnedOnPC1Text::
	text "<PLAYER> allume"
	line "le PC."
	prompt

_AccessedBillsPCText::
	text "Acces au PC de"
	line "BILL."
	para "Acces au Systeme"
	line "de Stockage"
	cont "#MON."
	prompt

_AccessedSomeonesPCText::
	text "Acces au PC de"
	line "quelqu'un."
	para "Acces au Systeme"
	line "de Stockage"
	cont "#MON."
	prompt

_AccessedMyPCText::
	text "Acces a mon PC."
	para "Acces au Systeme"
	line "de Stockage"
	cont "d'Objets."
	prompt

_TurnedOnPC2Text::
	text "<PLAYER> allume"
	line "le PC."
	prompt

_WhatDoYouWantText::
	text "Que veux-tu"
	line "faire?"
	done

_WhatToDepositText::
	text "Que veux-tu"
	line "deposer?"
	done

_DepositHowManyText::
	text "Combien?"
	done

_ItemWasStoredText::
	text_ram wNameBuffer
	text_start
	line "est stocke(e)."
	prompt

_NothingToDepositText::
	text "Tu n'as rien a"
	line "deposer."
	prompt

_NoRoomToStoreText::
	text "Plus de place"
	line "pour stocker."
	prompt

_WhatToWithdrawText::
	text "Que veux-tu"
	line "retirer?"
	done

_WithdrawHowManyText::
	text "Combien?"
	done

_WithdrewItemText::
	text "Tu retires"
	line "@"
	text_ram wNameBuffer
	text "."
	prompt

_NothingStoredText::
	text "Il n'y a rien"
	line "en stock."
	prompt

_CantCarryMoreText::
	text "Tu ne peux plus"
	line "rien porter."
	prompt

_WhatToTossText::
	text "Que veux-tu"
	line "jeter?"
	done

_TossHowManyText::
	text "Combien?"
	done

_AccessedHoFPCText::
	text "Acces au site de"
	line "la LIGUE #MON."
	para "Acces a la liste"
	line "du PANTHEON."
	prompt

_SwitchOnText::
	text "Allume!"
	prompt

_WhatText::
	text "Quoi?"
	done

_DepositWhichMonText::
	text "Deposer quel"
	line "#MON?"
	done

_MonWasStoredText::
	text_ram wStringBuffer
	text " est"
	line "dans la Boite @"
	text_ram wBoxNumString
	text "."
	prompt

_CantDepositLastMonText::
	text "Impossible de"
	line "deposer le"
	cont "dernier #MON!"
	prompt

_BoxFullText::
	text "Oups! Cette Boite"
	line "est pleine."
	prompt

_MonIsTakenOutText::
	text_ram wStringBuffer
	text " est"
	line "retire."
	cont "Tu recuperes"
	cont "@"
	text_ram wStringBuffer
	text "."
	prompt

_NoMonText::
	text "Quoi? Il n'y a"
	line "aucun #MON ici!"
	prompt

_CantTakeMonText::
	text "Tu ne peux plus"
	line "prendre de"
	cont "#MON."
	para "Depose d'abord"
	line "un #MON."
	prompt

_ReleaseWhichMonText::
	text "Relacher quel"
	line "#MON?"
	done

_OnceReleasedText::
	text "Une fois relache,"
	line "@"
	text_ram wStringBuffer
	text " sera"
	cont "parti. D'accord?"
	done

_MonWasReleasedText::
	text_ram wStringBuffer
	text " a"
	line "ete relache."
	cont "Adieu @"
	text_ram wStringBuffer
	text "!"
	prompt

_RequireCoinCaseText::
	text "Il faut une"
	line "BOITE JETON!@"
	text_end

_ExchangeCoinsForPrizesText::
	text "Nous echangeons"
	line "vos jetons contre"
	cont "des lots."
	prompt

_WhichPrizeText::
	text "Quel lot"
	line "voulez-vous?"
	done

_HereYouGoText::
	text "Et voila!@"
	text_end

_SoYouWantPrizeText::
	text "Vous voulez donc"
	line "@"
	text_ram wNameBuffer
	text "?"
	done

_SorryNeedMoreCoinsText::
	text "Desole, il vous"
	line "manque des jetons.@"
	text_end

_OopsYouDontHaveEnoughRoomText::
	text "Oups! Vous manquez"
	line "de place.@"
	text_end

_OhFineThenText::
	text "Bon, tant pis.@"
	text_end

_GetDexRatedText::
	text "Veux-tu faire"
	line "noter ton #DEX?"
	done

_ClosedOaksPCText::
	text "Fin de connexion"
	line "au PC du PROF.@"
	text_end

_AccessedOaksPCText::
	text "Acces au PC du"
	line "PROF.SYLVE."
	para "Acces au Systeme"
	line "de Notation du"
	cont "#DEX."
	prompt

_WhereWouldYouLikeText::
	text "Ou voulez-vous"
	line "aller?"
	done

_PleaseWaitText::
	text "Bien, un instant"
	line "s'il vous plait."
	done

_LinkCanceledText::
	text "La connexion a"
	line "ete annulee."
	done

_OakSpeechText1::
	text "Bonjour!"
	line "Bienvenue dans le"
	cont "monde des #MON!"
	para "Je m'appelle"
	line "PROF.SYLVE!"
	cont "On m'appelle le"
	cont "PROF. des #MON!"
	prompt

_OakSpeechText2A::
	text "Ce monde est"
	line "peuple de"
	cont "creatures appelees"
	cont "#MON!@"
	text_end

_OakSpeechText2B::
	text_start
	para "Pour certains, les"
	line "#MON sont des"
	cont "animaux. D'autres"
	cont "les font lutter."
	para "Quant a moi..."
	para "J'etudie les"
	line "#MON, c'est mon"
	cont "metier."
	prompt

_IntroducePlayerText::
	text "D'abord, quel est"
	line "ton nom?"
	prompt

_IntroduceRivalText::
	text "Voici ton voisin."
	line "Il est ton rival"
	cont "depuis que vous"
	cont "etes tout petits."
	para "...Euh, comment"
	line "s'appelle-t-il"
	cont "deja?"
	prompt

_OakSpeechText3::
	text "<PLAYER>!"
	para "Ta propre legende"
	line "#MON est sur le"
	cont "point de s'ecrire!"
	para "Un monde de reves"
	line "et d'aventures"
	cont "avec les #MON"
	cont "t'attend! Allez!"
	done

_DoYouWantToNicknameText::
	text "Veux-tu donner"
	line "un surnom a"
	cont "@"
	text_ram wNameBuffer
	text "?"
	done

_YourNameIsText::
	text "Bien! Ton nom est"
	line "donc <PLAYER>!"
	prompt

_HisNameIsText::
	text "C'est ca! Ca me"
	line "revient! Il"
	cont "s'appelle <RIVAL>!"
	prompt

_WillBeTradedText::
	text_ram wNameOfPlayerMonToBeTraded
	text " et"
	line "@"
	text_ram wNameBuffer
	text " vont"
	cont "etre echanges."
	done

_TextIDErrorText::
	text_decimal hTextID, 1, 2
	text " ERROR."
	done

_ContCharText::
	text "<_CONT>@"
	text_end
