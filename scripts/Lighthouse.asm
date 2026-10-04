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
	CheckEvent EVENT_BEAT_CHAMPION_RIVAL
	jr z, .fightLunaris
	; Chapter 1 (post-tournament): the ground shakes, Lunaris takes flight.
	predef PredefShakeScreenHorizontally
	ld hl, LighthouseQuakeText
	call PrintText
	ld a, TOGGLE_LIGHTHOUSE_LUNARIS
	ld [wToggleableObjectIndex], a
	predef HideObject
	ld a, MEWTWO
	call PlayCry
	call WaitForSoundToFinish
	ld hl, LighthouseLunarisVanishedText
	call PrintText
	jp TextScriptEnd
.fightLunaris
	ld hl, LighthouseLunarisTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

LighthouseQuakeText:
	text_far _LighthouseQuakeText
	text_end

LighthouseLunarisVanishedText:
	text_far _LighthouseLunarisVanishedText
	text_end

LighthouseLunarisBattleText:
	text_far _LighthouseLunarisBattleText
	text_asm
	ld a, MEWTWO
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd
