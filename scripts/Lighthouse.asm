Lighthouse_Script:
	call EnableAutoTextBoxDrawing
	ld hl, LighthouseTrainerHeaders
	ld de, Lighthouse_ScriptPointers
	ld a, [wLighthouseCurScript]
	call ExecuteCurMapScriptInTable
	ld [wLighthouseCurScript], a
	ret

Lighthouse_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_LIGHTHOUSE_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_LIGHTHOUSE_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_LIGHTHOUSE_END_BATTLE

LighthouseTrainerHeaders:
	def_trainers 3
LighthouseLunarisTrainerHeader:
	trainer EVENT_BEAT_LIGHTHOUSE_LUNARIS, 0, LighthouseLunarisBattleText, LighthouseLunarisBattleText, LighthouseLunarisBattleText
	db -1 ; end

Lighthouse_TextPointers:
	def_text_pointers
	dw_const LighthouseLunarisText, TEXT_LIGHTHOUSE_LUNARIS

LighthouseLunarisText:
	text_asm
	ld hl, LighthouseLunarisTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

LighthouseLunarisBattleText:
	text_far _LighthouseLunarisBattleText
	text_asm
	ld a, MEWTWO
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd
