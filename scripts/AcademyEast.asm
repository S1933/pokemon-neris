AcademyEast_Script:
	jp EnableAutoTextBoxDrawing

AcademyEast_TextPointers:
	def_text_pointers
	dw_const AcademyEastCuratorText,   TEXT_ACADEMYEAST_CURATOR
	dw_const AcademyEastStatue1Text,   TEXT_ACADEMYEAST_STATUE_1
	dw_const AcademyEastStatue2Text,   TEXT_ACADEMYEAST_STATUE_2

AcademyEastCuratorText:
	text_asm
	CheckEvent EVENT_MARK_OF_NERIS
	jr nz, .marked
	ld hl, AcademyEastCuratorDefaultText
	call PrintText
	jp TextScriptEnd
.marked
	ld hl, AcademyEastCuratorMarkedText
	call PrintText
	jp TextScriptEnd

AcademyEastCuratorDefaultText:
	text_far _AcademyEastCuratorDefaultText
	text_end

AcademyEastCuratorMarkedText:
	text_far _AcademyEastCuratorMarkedText
	text_end

AcademyEastStatue1Text:
	text_asm
	ld hl, AcademyEastStatue1DexText
	call PrintText
	jp TextScriptEnd

AcademyEastStatue1DexText:
	text_far _AcademyEastStatue1Text
	text_end

AcademyEastStatue2Text:
	text_asm
	ld hl, AcademyEastStatue2DexText
	call PrintText
	jp TextScriptEnd

AcademyEastStatue2DexText:
	text_far _AcademyEastStatue2Text
	text_end