CeruleanCaveB1F_Script:
	call EnableAutoTextBoxDrawing
	ld hl, CeruleanCaveB1FTrainerHeaders
	ld de, CeruleanCaveB1F_ScriptPointers
	ld a, [wCeruleanCaveB1FCurScript]
	call ExecuteCurMapScriptInTable
	ld [wCeruleanCaveB1FCurScript], a
	ret

CeruleanCaveB1F_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_CERULEANCAVEB1F_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_CERULEANCAVEB1F_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_CERULEANCAVEB1F_END_BATTLE

CeruleanCaveB1F_TextPointers:
	def_text_pointers
	dw_const CeruleanCaveB1FMewtwoText, TEXT_CERULEANCAVEB1F_MEWTWO
	dw_const PickUpItemText,            TEXT_CERULEANCAVEB1F_ULTRA_BALL
	dw_const PickUpItemText,            TEXT_CERULEANCAVEB1F_MAX_REVIVE
	dw_const CeruleanCaveB1FOranText,   TEXT_CERULEANCAVEB1F_ORAN
	dw_const CeruleanCaveB1FGrunt1Text, TEXT_CERULEANCAVEB1F_GRUNT1
	dw_const CeruleanCaveB1FGrunt2Text, TEXT_CERULEANCAVEB1F_GRUNT2
	dw_const CeruleanCaveB1FGrunt3Text, TEXT_CERULEANCAVEB1F_GRUNT3

CeruleanCaveB1FTrainerHeaders:
	def_trainers
MewtwoTrainerHeader:
	trainer EVENT_BEAT_MEWTWO, 0, MewtwoBattleText, MewtwoBattleText, MewtwoBattleText
CeruleanCaveB1FOranTrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_0, 0, CeruleanCaveB1FOranBattleText, CeruleanCaveB1FOranEndBattleText, CeruleanCaveB1FOranAfterBattleScript
CeruleanCaveB1FGrunt1TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_1, 2, CeruleanCaveB1FGrunt1BattleText, CeruleanCaveB1FGrunt1EndBattleText, CeruleanCaveB1FGrunt1AfterBattleText
CeruleanCaveB1FGrunt2TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_2, 2, CeruleanCaveB1FGrunt2BattleText, CeruleanCaveB1FGrunt2EndBattleText, CeruleanCaveB1FGrunt2AfterBattleText
CeruleanCaveB1FGrunt3TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_3, 2, CeruleanCaveB1FGrunt3BattleText, CeruleanCaveB1FGrunt3EndBattleText, CeruleanCaveB1FGrunt3AfterBattleText
	db -1 ; end

CeruleanCaveB1FMewtwoText:
	text_asm
	ld hl, MewtwoTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

MewtwoBattleText:
	text_far _MewtwoBattleText
	text_asm
	ld a, MEWTWO
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd

; Maitre Oran only fights once the player is Champion (game clear flag).
CeruleanCaveB1FOranText:
	text_asm
	CheckEvent EVENT_BEAT_CHAMPION_RIVAL
	jr z, .notChampion
	ld hl, CeruleanCaveB1FOranTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd
.notChampion
	ld hl, CeruleanCaveB1FOranLockedText
	call PrintText
	jp TextScriptEnd

CeruleanCaveB1FOranLockedText:
	text_far _CeruleanCaveB1FOranLockedText
	text_end

CeruleanCaveB1FOranBattleText:
	text_far _CeruleanCaveB1FOranBattleText
	text_end

CeruleanCaveB1FOranEndBattleText:
	text_far _CeruleanCaveB1FOranEndBattleText
	text_end

CeruleanCaveB1FOranAfterBattleScript:
	text_asm
	SetEvent EVENT_MARK_OF_NERIS
	ld hl, CeruleanCaveB1FOranMarkText
	call PrintText
	jp TextScriptEnd

CeruleanCaveB1FOranMarkText:
	text_far _CeruleanCaveB1FOranMarkText
	text_end

CeruleanCaveB1FGrunt1Text:
	text_asm
	ld hl, CeruleanCaveB1FGrunt1TrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

CeruleanCaveB1FGrunt1BattleText:
	text_far _CeruleanCaveB1FGrunt1BattleText
	text_end

CeruleanCaveB1FGrunt1EndBattleText:
	text_far _CeruleanCaveB1FGrunt1EndBattleText
	text_end

CeruleanCaveB1FGrunt1AfterBattleText:
	text_far _CeruleanCaveB1FGrunt1AfterBattleText
	text_end

CeruleanCaveB1FGrunt2Text:
	text_asm
	ld hl, CeruleanCaveB1FGrunt2TrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

CeruleanCaveB1FGrunt2BattleText:
	text_far _CeruleanCaveB1FGrunt2BattleText
	text_end

CeruleanCaveB1FGrunt2EndBattleText:
	text_far _CeruleanCaveB1FGrunt2EndBattleText
	text_end

CeruleanCaveB1FGrunt2AfterBattleText:
	text_far _CeruleanCaveB1FGrunt2AfterBattleText
	text_end

CeruleanCaveB1FGrunt3Text:
	text_asm
	ld hl, CeruleanCaveB1FGrunt3TrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

CeruleanCaveB1FGrunt3BattleText:
	text_far _CeruleanCaveB1FGrunt3BattleText
	text_end

CeruleanCaveB1FGrunt3EndBattleText:
	text_far _CeruleanCaveB1FGrunt3EndBattleText
	text_end

CeruleanCaveB1FGrunt3AfterBattleText:
	text_far _CeruleanCaveB1FGrunt3AfterBattleText
	text_end
