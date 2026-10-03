ValBorealCity_Script:
	call EnableAutoTextBoxDrawing
	ret

ValBorealCity_TextPointers:
	def_text_pointers
	dw_const ValBorealCityHikerText, TEXT_VALBOREALCITY_HIKER
	dw_const ValBorealCityGirlText,  TEXT_VALBOREALCITY_GIRL

ValBorealCityHikerText:
	text_far _ValBorealCityHikerText
	text_end

ValBorealCityGirlText:
	text_far _ValBorealCityGirlText
	text_end
