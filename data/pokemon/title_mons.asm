TitleMons:
; mons on the title screen are randomly chosen from here.
; Neris: the list holds the game's own line-up only — the nine species that
; exist nowhere else, the three starter lines and the two legendaries — so the
; vanilla Kanto list it used to be (Weedle, Scyther, Abra, Ditto, ...) never
; scrolls by. Exactly 16 entries: TitleScreenPickNewMon indexes it with a
; random byte AND $f.
IF DEF(_RED)
	db DRACOZELLE  ; DRACOZELLE
	db SPECTRELA   ; SPECTRELA
	db VENOMBRU    ; VENOMBRU
	db TERRAKOR    ; TERRAKOR
	db FULGURAX    ; FULGURAX
	db GIVRALP     ; GIVRALP
	db PYROFELIS   ; PYROFELIS
	db OBSCURAX    ; OBSCURAX
	db CRAMORIL    ; CRAMORIL
	db CHARIZARD   ; FLAMBRAISE
	db BLASTOISE   ; AQUATITAN
	db VENUSAUR    ; VERDINKING
	db MEWTWO      ; LUNARIS
	db MEW         ; SOLARIS
	db STARMIE     ; STAROSS
	db AERODACTYL  ; PTERA
ENDC
IF DEF(_BLUE)
	db STARTER2
	db STARTER1
	db STARTER3
	db MANKEY
	db HITMONLEE
	db VULPIX
	db CHANSEY
	db AERODACTYL
	db JOLTEON
	db SNORLAX
	db GLOOM
	db POLIWAG
	db DODUO
	db PORYGON
	db GENGAR
	db RAICHU
ENDC
