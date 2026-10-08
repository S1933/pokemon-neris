Academy_Script:
	call EnableAutoTextBoxDrawing
	ld hl, AcademyTrainerHeaders
	ld de, Academy_ScriptPointers
	ld a, [wAcademyCurScript]
	call ExecuteCurMapScriptInTable
	ld [wAcademyCurScript], a
	ret

Academy_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_ACADEMY_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_ACADEMY_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_ACADEMY_END_BATTLE

AcademyTrainerHeaders:
	def_trainers 2
AcademyTrainerHeader0:
	trainer EVENT_BEAT_ACADEMY_TRAINER_0, 0, AcademyOranBattleText, AcademyOranEndBattleText, AcademyOranAfterBattleText
AcademyTrainerHeader1:
	trainer EVENT_BEAT_ACADEMY_TRAINER_1, 0, AcademyChamp1BattleText, AcademyChamp1EndBattleText, AcademyChamp1AfterBattleText
AcademyTrainerHeader2:
	trainer EVENT_BEAT_ACADEMY_TRAINER_2, 0, AcademyChamp2BattleText, AcademyChamp2EndBattleText, AcademyChamp2AfterBattleText
AcademyTrainerHeader3:
	trainer EVENT_BEAT_ACADEMY_TRAINER_3, 0, AcademyChamp3BattleText, AcademyChamp3EndBattleText, AcademyChamp3AfterBattleText
AcademyTrainerHeader4:
	trainer EVENT_BEAT_ACADEMY_TRAINER_4, 0, AcademyChamp4BattleText, AcademyChamp4EndBattleText, AcademyChamp4AfterBattleText
	db -1 ; end

Academy_TextPointers:
	def_text_pointers
	dw_const AcademyOranText,    TEXT_ACADEMY_ORAN
	dw_const AcademyChamp1Text,  TEXT_ACADEMY_CHAMP_1
	dw_const AcademyChamp2Text,  TEXT_ACADEMY_CHAMP_2
	dw_const AcademyChamp3Text,  TEXT_ACADEMY_CHAMP_3
	dw_const AcademyChamp4Text,  TEXT_ACADEMY_CHAMP_4

AcademyOranText:
	text_asm
	CheckEvent EVENT_BEAT_ACADEMY_TRAINER_0
	jr nz, .talk
	CheckBothEventsSet EVENT_BEAT_ACADEMY_TRAINER_1, EVENT_BEAT_ACADEMY_TRAINER_2
	jr nz, .locked
	CheckBothEventsSet EVENT_BEAT_ACADEMY_TRAINER_3, EVENT_BEAT_ACADEMY_TRAINER_4
	jr nz, .locked
.talk
	ld hl, AcademyTrainerHeader0
	call TalkToTrainer
	jp TextScriptEnd
.locked
	ld hl, AcademyOranLockedText
	call PrintText
	jp TextScriptEnd
AcademyChamp1Text:
	text_asm
	ld hl, AcademyTrainerHeader1
	call TalkToTrainer
	jp TextScriptEnd
AcademyChamp2Text:
	text_asm
	ld hl, AcademyTrainerHeader2
	call TalkToTrainer
	jp TextScriptEnd
AcademyChamp3Text:
	text_asm
	ld hl, AcademyTrainerHeader3
	call TalkToTrainer
	jp TextScriptEnd
AcademyChamp4Text:
	text_asm
	ld hl, AcademyTrainerHeader4
	call TalkToTrainer
	jp TextScriptEnd

AcademyOranLockedText:
	text_far _AcademyOranLockedText
	text_end

AcademyOranBattleText:
	text_far _AcademyOranBattleText
	text_end
AcademyOranEndBattleText:
	text_far _AcademyOranEndBattleText
	text_end
AcademyOranAfterBattleText:
	text_asm
	CheckEvent EVENT_MARK_OF_NERIS
	jr nz, .true_ending
	CheckEitherEventSet EVENT_BEAT_LIGHTHOUSE_LUNARIS, EVENT_BEAT_MT_MOON_3_TRAINER_4
	jr nz, .secret_ending
	ld hl, .NormalEndingText
	jr .print
.true_ending
	ld hl, .TrueEndingText
	jr .print
.secret_ending
	ld hl, .SecretEndingText
.print
	call PrintText
	jp TextScriptEnd

.NormalEndingText:
	text_far _AcademyOranAfterBattleText
	text_end

.TrueEndingText:
	text_far _AcademyTrueEndingText
	text_end

.SecretEndingText:
	text_far _AcademySecretEndingText
	text_end

AcademyChamp1BattleText:
	text_far _AcademyChamp1BattleText
	text_end
AcademyChamp1EndBattleText:
	text_far _AcademyChamp1EndBattleText
	text_end
AcademyChamp1AfterBattleText:
	text_far _AcademyChamp1AfterBattleText
	text_end
AcademyChamp2BattleText:
	text_far _AcademyChamp2BattleText
	text_end
AcademyChamp2EndBattleText:
	text_far _AcademyChamp2EndBattleText
	text_end
AcademyChamp2AfterBattleText:
	text_far _AcademyChamp2AfterBattleText
	text_end
AcademyChamp3BattleText:
	text_far _AcademyChamp3BattleText
	text_end
AcademyChamp3EndBattleText:
	text_far _AcademyChamp3EndBattleText
	text_end
AcademyChamp3AfterBattleText:
	text_far _AcademyChamp3AfterBattleText
	text_end
AcademyChamp4BattleText:
	text_far _AcademyChamp4BattleText
	text_end
AcademyChamp4EndBattleText:
	text_far _AcademyChamp4EndBattleText
	text_end
AcademyChamp4AfterBattleText:
	text_far _AcademyChamp4AfterBattleText
	text_end
