ValBorealGym_Script:
	call EnableAutoTextBoxDrawing
	ld hl, ValBorealGymTrainerHeaders
	ld de, ValBorealGym_ScriptPointers
	ld a, [wValBorealGymCurScript]
	call ExecuteCurMapScriptInTable
	ld [wValBorealGymCurScript], a
	ret

ValBorealGym_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_VALBOREALGYM_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_VALBOREALGYM_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_VALBOREALGYM_END_BATTLE

ValBorealGymTrainerHeaders:
	def_trainers 2
ValBorealGymOlgaTrainerHeader:
	trainer EVENT_BEAT_VALBOREAL_GYM_TRAINER_0, 0, ValBorealGymOlgaBattleText, ValBorealGymOlgaEndBattleText, ValBorealGymOlgaAfterBattleText
	db -1 ; end

ValBorealGym_TextPointers:
	def_text_pointers
	dw_const ValBorealGymOlgaText, TEXT_VALBOREALGYM_OLGA

ValBorealGymOlgaText:
	text_asm
	ld hl, ValBorealGymOlgaTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

ValBorealGymOlgaBattleText:
	text_far _ValBorealGymOlgaBattleText
	text_end

ValBorealGymOlgaEndBattleText:
	text_far _ValBorealGymOlgaEndBattleText
	text_end

ValBorealGymOlgaAfterBattleText:
	text_far _ValBorealGymOlgaAfterBattleText
	text_end
