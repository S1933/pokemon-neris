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
	dw_const CeruleanCaveB1FOranEndBattleScript,    SCRIPT_CERULEANCAVEB1F_ORAN_END_BATTLE

CeruleanCaveB1FOranEndBattleScript:
	call EndTrainerBattle
	ld a, [wIsInBattle]
	cp LOST_BATTLE
	ret z
	SetEvent EVENT_MARK_OF_NERIS
	ld a, TEXT_CERULEANCAVEB1F_ORAN_MARK
	ldh [hTextID], a
	jp DisplayTextID

CeruleanCaveB1F_TextPointers:
	def_text_pointers
	dw_const PickUpItemText,            TEXT_CERULEANCAVEB1F_ULTRA_BALL
	dw_const PickUpItemText,            TEXT_CERULEANCAVEB1F_MAX_REVIVE
	dw_const CeruleanCaveB1FOranText,   TEXT_CERULEANCAVEB1F_ORAN
	dw_const CeruleanCaveB1FGrunt1Text, TEXT_CERULEANCAVEB1F_GRUNT1
	dw_const CeruleanCaveB1FGrunt2Text, TEXT_CERULEANCAVEB1F_GRUNT2
	dw_const CeruleanCaveB1FGrunt3Text, TEXT_CERULEANCAVEB1F_GRUNT3
	dw_const CeruleanCaveB1FOranMarkText, TEXT_CERULEANCAVEB1F_ORAN_MARK

CeruleanCaveB1FTrainerHeaders:
	def_trainers 2
CeruleanCaveB1FOranTrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_0, 0, CeruleanCaveB1FOranBattleText, CeruleanCaveB1FOranEndBattleText, CeruleanCaveB1FOranAfterBattleText
CeruleanCaveB1FGrunt1TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_1, 2, CeruleanCaveB1FGrunt1BattleText, CeruleanCaveB1FGrunt1EndBattleText, CeruleanCaveB1FGrunt1AfterBattleText
CeruleanCaveB1FGrunt2TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_2, 2, CeruleanCaveB1FGrunt2BattleText, CeruleanCaveB1FGrunt2EndBattleText, CeruleanCaveB1FGrunt2AfterBattleText
CeruleanCaveB1FGrunt3TrainerHeader:
	trainer EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_3, 2, CeruleanCaveB1FGrunt3BattleText, CeruleanCaveB1FGrunt3EndBattleText, CeruleanCaveB1FGrunt3AfterBattleText
	db -1 ; end

; Maitre Oran only fights once the player is Champion (game clear flag).
CeruleanCaveB1FOranText:
	text_asm
	CheckEvent EVENT_BEAT_CHAMPION_RIVAL
	jr z, .notChampion
	ld hl, CeruleanCaveB1FOranTrainerHeader
	call TalkToTrainer
	CheckEvent EVENT_BEAT_CERULEAN_CAVE_B1F_TRAINER_0
	jp nz, TextScriptEnd
	; a battle starts: the Mark is given right after the win
	ld a, SCRIPT_CERULEANCAVEB1F_ORAN_END_BATTLE
	ld [wCeruleanCaveB1FCurScript], a
	ld [wCurMapScript], a
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

CeruleanCaveB1FOranAfterBattleText:
	text_far _CeruleanCaveB1FOranAfterBattleText
	text_end

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
