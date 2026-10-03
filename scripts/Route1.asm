Route1_Script:
	call EnableAutoTextBoxDrawing
	ld hl, Route1TrainerHeaders
	ld de, Route1_ScriptPointers
	ld a, [wRoute1CurScript]
	call ExecuteCurMapScriptInTable
	ld [wRoute1CurScript], a
	ret

Route1_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_ROUTE1_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_ROUTE1_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_ROUTE1_END_BATTLE

Route1TrainerHeaders:
	def_trainers 2
Route1TrainerHeader0:
	trainer EVENT_BEAT_ROUTE1_KAEL, 2, Route1KaelBattleText, Route1KaelEndBattleText, Route1KaelAfterBattleText
	db -1 ; end

Route1_TextPointers:
	def_text_pointers
	dw_const Route1Youngster1Text, TEXT_ROUTE1_YOUNGSTER1
	dw_const Route1Youngster2Text, TEXT_ROUTE1_YOUNGSTER2
	dw_const Route1KaelText,       TEXT_ROUTE1_KAEL
	dw_const Route1SignText,       TEXT_ROUTE1_SIGN

Route1KaelText:
	text_asm
	ld hl, Route1TrainerHeader0
	call TalkToTrainer
	jp TextScriptEnd

Route1KaelBattleText:
	text_far _Route1KaelBattleText
	text_end

Route1KaelEndBattleText:
	text_far _Route1KaelEndBattleText
	sound_cry_nidorina
	text_end

Route1KaelAfterBattleText:
	text_far _Route1KaelAfterBattleText
	text_end

Route1Youngster1Text:
	text_asm
	CheckAndSetEvent EVENT_GOT_POTION_SAMPLE
	jr nz, .got_item
	ld hl, .MartSampleText
	call PrintText
	lb bc, POTION, 1
	call GiveItem
	jr nc, .bag_full
	ld hl, .GotPotionText
	jr .done
.bag_full
	ld hl, .NoRoomText
	jr .done
.got_item
	ld hl, .AlsoGotPokeballsText
.done
	call PrintText
	jp TextScriptEnd

.MartSampleText:
	text_far _Route1Youngster1MartSampleText
	text_end

.GotPotionText:
	text_far _Route1Youngster1GotPotionText
	sound_get_item_1
	text_end

.AlsoGotPokeballsText:
	text_far _Route1Youngster1AlsoGotPokeballsText
	text_end

.NoRoomText:
	text_far _Route1Youngster1NoRoomText
	text_end

Route1Youngster2Text:
	text_far _Route1Youngster2Text
	text_end

Route1SignText:
	text_far _Route1SignText
	text_end
