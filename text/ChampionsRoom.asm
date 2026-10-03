_ChampionsRoomRivalIntroText::
	text "<RIVAL>: He!"

	para "Je voulais te"
	line "voir, <PLAYER>!"

	para "Mon rival doit"
	line "etre fort pour"
	cont "me garder vif!"

	para "En faisant le"
	line "#DEX, j'ai"
	cont "cherche partout"
	cont "des #MON"
	cont "puissants!"

	para "Et pas que ca,"
	line "j'ai compose"
	cont "des equipes"
	cont "battant tout"
	cont "type de #MON!"

	para "Et maintenant!"

	para "Je suis le"
	line "champion de la"
	cont "LIGUE #MON!"

	para "<PLAYER>! Sais-tu"
	line "ce que ca"
	cont "veut dire?"

	para "Je vais te le"
	line "dire!"

	para "Je suis le"
	line "dresseur le plus"
	cont "puissant du"
	cont "monde!"
	done

_RivalDefeatedText::
	text "NON!"
	line "C'est pas vrai!"
	cont "Tu m'as battu!"

	para "Apres tout ce"
	line "travail pour"
	cont "etre champion"
	cont "de la LIGUE?"

	para "Mon regne est"
	line "deja fini?"
	cont "C'est pas juste!"
	prompt

_RivalVictoryText::
	text "Hahaha!"
	line "J'ai gagne!"
	cont "J'ai gagne!"

	para "Je suis trop"
	line "fort pour toi,"
	cont "<PLAYER>!"

	para "Tu as bien fait"
	line "d'arriver"
	cont "jusqu'a moi,"
	cont "<RIVAL>, le"
	cont "genie #MON!"

	para "Bien essaye,"
	line "loser! Hahaha!"
	prompt

_ChampionsRoomRivalAfterBattleText::
	text "Pourquoi?"
	line "Pourquoi j'ai"
	cont "perdu?"

	para "Je n'ai fait"
	line "aucune erreur"
	cont "en elevant"
	cont "mes #MON..."

	para "Zut! Tu es le"
	line "nouveau champion"
	cont "de la LIGUE"
	cont "#MON!"

	para "Meme si j'ai"
	line "du mal a"
	cont "l'admettre."
	done

_ChampionsRoomOakText::
	text "PROF.SYLVE:"
	line "<PLAYER>!"
	done

_ChampionsRoomOakCongratulatesPlayerText::
	text "PROF.SYLVE: Tu as"
	line "gagne! Bravo!"
	cont "Tu es le nouveau"
	cont "champion de la"
	cont "LIGUE #MON!"

	para "Tu as tellement"
	line "grandi depuis"
	cont "ton depart avec"
	cont "@"
	text_ram wNameBuffer
	text "!"

	para "<PLAYER>, tu es"
	line "devenu adulte!"
	done

_ChampionsRoomOakDisappointedWithRivalText::
	text "PROF.SYLVE:"
	line "<RIVAL>! Je"
	cont "suis decu!"

	para "Je suis venu en"
	line "apprenant que"
	cont "tu avais battu"
	cont "le CONSEIL 4!"

	para "Mais en arrivant,"
	line "tu avais deja"
	cont "perdu!"

	para "<RIVAL>! Sais-tu"
	line "pourquoi tu as"
	cont "perdu?"

	para "Tu as oublie de"
	line "traiter tes"
	cont "#MON avec"
	cont "confiance et"
	cont "amour!"

	para "Sans eux, tu ne"
	line "seras plus jamais"
	cont "champion!"
	done

_ChampionsRoomOakComeWithMeText::
	text "PROF.SYLVE:"
	line "<PLAYER>!"

	para "Tu comprends"
	line "que ta victoire"
	cont "n'est pas que"
	cont "ton oeuvre!"

	para "Le lien que tu"
	line "partages avec"
	cont "tes #MON est"
	cont "merveilleux!"

	para "<PLAYER>!"
	line "Suis-moi!"
	done
