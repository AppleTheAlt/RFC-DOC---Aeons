# coding: utf-8

from Civics import *
from RFCUtils import *
from Areas import *
from Locations import *
from Core import *

from Events import handler
from Core import name as short
from Core import adjective as civAdjective

import CityNames as cn


### Constants ###

encoding = "utf-8"

### Dictionaries with text keys

dDefaultInsertNames = {
	iKhmer : "TXT_KEY_CIV_KHMER_CAMBODIAN",
	iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARTICLE",
	iDravidia : "TXT_KEY_CIV_DRAVIDIA_TAMIL_NADU",
	iMaya : "TXT_KEY_CIV_MAYA_YUCATAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAM",
	#iMoors : "TXT_KEY_CIV_MOORS_MOROCCO",
	iHarappa : "TXT_KEY_CIV_HARAPPA_INDUS",
}

dDefaultInsertAdjectives = {
	iKhmer : "TXT_KEY_CIV_KHMER_CAMBODIAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAMESE",
	#iMoors : "TXT_KEY_CIV_MOORS_MOROCCAN",
}

dSpecificVassalTitles = deepdict({

	iRome: {
		iCelts : "TXT_KEY_CIV_ROMAN_CELTS",	
	},
	iEgypt : {
		iPhoenicia : "TXT_KEY_CIV_EGYPTIAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_EGYPTIAN_ETHIOPIA",
		iMinoa : "TXT_KEY_CIV_EGYPTIAN_MINOA",
	},
	iBabylonia : {
		iPhoenicia : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iChina : {
		iKorea : "TXT_KEY_CIV_CHINESE_KOREA",
		iGokturks : "TXT_KEY_CIV_CHINESE_TURKS",
		iVietnam : "TXT_KEY_CIV_CHINESE_VIETNAM",
		iMongols : "TXT_KEY_CIV_CHINESE_MONGOLIA",
	},
	iGreece : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iParthia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
		iKushans : "TXT_KEY_CIV_GREEK_KUSHANS",
		iHittites: "TXT_KEY_CIV_GREEK_NAME_HITTITES",
	},
	iMacedon : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iParthia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
		iKushans : "TXT_KEY_CIV_GREEK_KUSHANS",
		iHittites: "TXT_KEY_CIV_GREEK_NAME_HITTITES",
	},
	iSparta : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iParthia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
		iKushans : "TXT_KEY_CIV_GREEK_KUSHANS",
		iHittites: "TXT_KEY_CIV_GREEK_NAME_HITTITES",
	},
	iMycenae : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iParthia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
		iKushans : "TXT_KEY_CIV_GREEK_KUSHANS",
		iHittites: "TXT_KEY_CIV_GREEK_NAME_HITTITES",
	},
	iMinoa : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
		iKushans : "TXT_KEY_CIV_GREEK_KUSHANS",
	},

	iIndia : {
		iAztecs: "TXT_KEY_CIV_INDIAN_AZTECS",
	},
	iPersia : {
		iEgypt : "TXT_KEY_CIV_PERSIAN_EGYPT",
		iIndia : "TXT_KEY_CIV_PERSIAN_INDIA",
		iBabylonia : "TXT_KEY_CIV_PERSIAN_BABYLONIA",
		iGreece : "TXT_KEY_CIV_PERSIAN_GREECE",
		iEthiopia : "TXT_KEY_CIV_PERSIAN_ETHIOPIA",
		iArabia : "TXT_KEY_CIV_PERSIAN_ARABIA",
		iMongols : "TXT_KEY_CIV_PERSIAN_MONGOLIA",
	},
	iParthia : {
		iEgypt : "TXT_KEY_CIV_PERSIAN_EGYPT",
		iIndia : "TXT_KEY_CIV_PERSIAN_INDIA",
		iBabylonia : "TXT_KEY_CIV_PERSIAN_BABYLONIA",
		iGreece : "TXT_KEY_CIV_PERSIAN_GREECE",
		iEthiopia : "TXT_KEY_CIV_PERSIAN_ETHIOPIA",
		iArabia : "TXT_KEY_CIV_PERSIAN_ARABIA",
		iMongols : "TXT_KEY_CIV_PERSIAN_MONGOLIA",
	},

	iJapan : {
		iChina : "TXT_KEY_CIV_JAPANESE_CHINA",
		iIndia : "TXT_KEY_CIV_JAPANESE_INDIA",
		iKorea : "TXT_KEY_CIV_JAPANESE_KOREA",
		iVietnam : "TXT_KEY_CIV_JAPANESE_VIETNAM",
		iMongols : "TXT_KEY_CIV_JAPANESE_MONGOLIA",
	},
	iByzantium : {
		iEgypt : "TXT_KEY_CIV_BYZANTINE_EGYPT",
		iMisr : "TXT_KEY_CIV_BYZANTINE_EGYPT",
		iBabylonia : "TXT_KEY_CIV_BYZANTINE_BABYLONIA",
		iGreece : "TXT_KEY_CIV_BYZANTINE_GREECE",
		iPhoenicia : "TXT_KEY_CIV_BYZANTINE_CARTHAGE",
		iPersia : "TXT_KEY_CIV_BYZANTINE_PERSIA",
		iRome : "TXT_KEY_CIV_BYZANTINE_ROME",
		iSpain : "TXT_KEY_CIV_BYZANTINE_SPAIN",
	},
	iNorse : {
		iEngland : "TXT_KEY_CIV_NORSE_ENGLAND",
		iCelts : "TXT_KEY_CIV_NORSE_CELTS",
		iByzantium : "TXT_KEY_CIV_NORSE_BYZANTIUM",
		iMali : "TXT_KEY_CIV_NORSE_MALI",
		iTurks : "TXT_KEY_CIV_NORSE_TURKS",
		iArabia : "TXT_KEY_CIV_NORSE_ARABIA",
		iMoors : "TXT_KEY_CIV_NORSE_MOORS",
		iSweden : "TXT_KEY_CIV_NORSE_SWEDEN",
	},
	iArabia : {
		iParthia : "TXT_KEY_CIV_ARABIAN_PARTHIA",
		iOttomans : "TXT_KEY_CIV_ARABIAN_OTTOMANS",
		iGhorids : "TXT_KEY_CIV_ARABIAN_MUGHALS",
	},
	iMoors : {
		iArabia : "TXT_KEY_CIV_MOORISH_ARABIA",
		iMali : "TXT_KEY_CIV_MOORISH_MALI",
	},
	iSpain : {
		iPhoenicia : "TXT_KEY_CIV_SPANISH_CARTHAGE",
		iEthiopia : "TXT_KEY_CIV_SPANISH_ETHIOPIA",
		iMaya : "TXT_KEY_CIV_SPANISH_MAYA",
		iByzantium : "TXT_KEY_CIV_SPANISH_BYZANTIUM",
		iMoors : "TXT_KEY_CIV_SPANISH_MOORS",
		iFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
		iMali : "TXT_KEY_CIV_SPANISH_MALI",
		iPortugal : "TXT_KEY_CIV_SPANISH_PORTUGAL",
		iAshanti : "TXT_KEY_CIV_GOLD_COAST",
		iAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
		iArgentina : "TXT_KEY_CIV_SPANISH_ARGENTINA",
		iColombia : "TXT_KEY_CIV_SPANISH_COLOMBIA",
	},
	iFrance : {
		iGermania : "TXT_KEY_CIV_FRENCH_GERMANIA",
		iTunis : "TXT_KEY_CIV_FRENCH_TUNISIA",
		iEgypt : "TXT_KEY_MANDATE_OF",
		iMisr : "TXT_KEY_MANDATE_OF",
		iBabylonia : "TXT_KEY_CIV_FRENCH_BABYLONIA",
		iGreece : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_FRENCH_PHOENICIA",
		iItaly : "TXT_KEY_CIV_FRENCH_ITALY",
		iEthiopia : "TXT_KEY_CIV_FRENCH_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_FRENCH_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iArabia : "TXT_KEY_MANDATE_OF",
		iEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iSpain : "TXT_KEY_CIV_FRENCH_SPAIN",
		iHolyRome : "TXT_KEY_CIV_FRENCH_HOLY_ROME",
		iVietnam : "TXT_KEY_CIV_FRENCH_VIETNAM",
		iPoland : "TXT_KEY_CIV_FRENCH_POLAND",
		iNetherlands : "TXT_KEY_CIV_FRENCH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_FRENCH_MALI",
		iPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iInca : "TXT_KEY_CIV_FRENCH_INCA",
		iAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iTimurids : "TXT_KEY_MANDATE_OF",
		iCongo : "TXT_KEY_ADJECTIVE_TITLE",
		iRussia : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAshanti : "TXT_KEY_CIV_GOLD_COAST",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iEngland : {
		iEgypt : "TXT_KEY_MANDATE_OF",
		iMisr : "TXT_KEY_MANDATE_OF",
		iIndia : "TXT_KEY_CIV_ENGLISH_INDIA",
		iBabylonia : "TXT_KEY_CIV_ENGLISH_BABYLONIA",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_ENGLISH_PHOENICIA",
		iMaya : "TXT_KEY_CIV_ENGLISH_MAYA",
		iByzantium : "TXT_KEY_CIV_ENGLISH_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_ENGLISH_NORSE",
		iArabia : "TXT_KEY_MANDATE_OF",
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iHolyRome : "TXT_KEY_CIV_ENGLISH_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ENGLISH_GERMANY",
		iSwahili: "TXT_KEY_CIV_ENGLISH_SWAHILI",
		iNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ENGLISH_MALI",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAshanti : "TXT_KEY_CIV_GOLD_COAST",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
		iZulu : "TXT_KEY_CIV_ENGLISH_ZULU",
		iBoers : "TXT_KEY_CIV_ENGLISH_BOERS",
		iSouthAfrica : "TXT_KEY_CIV_ENGLISH_SOUTH_AFRICA"
	},
	iSouthAfrica: {
		iZulu : "TXT_KEY_CIV_ENGLISH_ZULU",
		iBoers : "TXT_KEY_CIV_ENGLISH_BOERS",
	},
	iBoers: {
		iZulu : "TXT_KEY_CIV_ENGLISH_ZULU",
	},
	iHolyRome : {
		iMisr : "TXT_KEY_MANDATE_OF",
		iItaly : "TXT_KEY_CIV_HOLY_ROMAN_ITALY",
		iFrance : "TXT_KEY_CIV_HOLY_ROMAN_FRANCE",
		iNetherlands : "TXT_KEY_CIV_HOLY_ROMAN_NETHERLANDS",
		iByzantium : "TXT_KEY_CIV_HOLY_ROMAN_BYZANTIUM",
		iPoland : "TXT_KEY_CIV_HOLY_ROMAN_POLAND",
	},
	iPortugal : {
		iIndia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iMali : "TXT_KEY_CIV_PORTUGUESE_MALI",
		iMoors : "TXT_KEY_CIV_PORTUGUESE_MOORS",
		iMorocco : "TXT_KEY_CIV_PORTUGUESE_MOORS",
		iSwahili : "TXT_KEY_CIV_PORTUGUESE_SWAHILI",
		iCongo : "TXT_KEY_CIV_PORTUGUESE_CONGO",
		iAshanti : "TXT_KEY_CIV_GOLD_COAST",
		iBrazil : "TXT_KEY_CIV_PORTUGUESE_BRAZIL",
	},
	iPoland : {
		iRus : "TXT_KEY_CIV_POLISH_RUS",
	},
	iMongols : {
		iSamanids : "TXT_KEY_CIV_MONGOLIA_CHAGATAI",
		iParthia : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iBuyids : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iTurks : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iChina : "TXT_KEY_CIV_MONGOL_CHINA",
		iBabylonia : "TXT_KEY_CIV_MONGOL_BABYLONIA",
		iPersia : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iPhoenicia : "TXT_KEY_CIV_MONGOL_PHOENICIA",
		iByzantium : "TXT_KEY_CIV_MONGOL_BYZANTIUM",
		iRus : "TXT_KEY_CIV_MONGOL_RUS",
		iOttomans : "TXT_KEY_CIV_MONGOL_OTTOMANS",
		iTimurids : "TXT_KEY_CIV_MONGOL_MUGHALS",
	},
	iTimurids : {
		iIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iGhorids : {
		iIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iRussia : {
		iRus : "TXT_KEY_CIV_RUSSIAN_RUS",
		iTurks : "TXT_KEY_ADJECTIVE_TITLE",
		iPoland : "TXT_KEY_CIV_RUSSIAN_POLAND",
		iTatars : "TXT_KEY_CIV_RUSSIAN_TATARS",
		iAmerica : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iOttomans : {
		iTunis : "TXT_KEY_CIV_OTTOMAN_TUNIS",
		iMisr : "TXT_KEY_CIV_OTTOMAN_MISR",
		iBabylonia : "TXT_KEY_CIV_OTTOMAN_BABYLONIA",
		iPersia : "TXT_KEY_CIV_OTTOMAN_PERSIA",
		iGreece : "TXT_KEY_CIV_OTTOMAN_GREECE",
		iPhoenicia : "TXT_KEY_CIV_OTTOMAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_OTTOMAN_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_OTTOMAN_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_OTTOMAN_ARABIA",
		iRus : "TXT_KEY_CIV_OTTOMAN_RUS",
	},
	iNetherlands : {
		iMali : "TXT_KEY_CIV_DUTCH_MALI",
		iEthiopia : "TXT_KEY_CIV_DUTCH_ETHIOPIA",
		iCongo : "TXT_KEY_CIV_DUTCH_CONGO",
		iAmerica : "TXT_KEY_CIV_DUTCH_AMERICA",
		iBrazil : "TXT_KEY_CIV_DUTCH_BRAZIL",
	},
	iGermany : {
		iHolyRome : "TXT_KEY_CIV_GERMAN_HOLY_ROME",
		iMali : "TXT_KEY_CIV_GERMAN_MALI",
		iSwahili : "TXT_KEY_CIV_GERMAN_SWAHILI",
		iPoland : "TXT_KEY_CIV_GERMAN_POLAND",
	},
	iAmerica : {
		iEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
		iJapan : "TXT_KEY_CIV_AMERICAN_JAPAN",
		iGermany : "TXT_KEY_CIV_AMERICAN_GERMANY",
		iAztecs : "TXT_KEY_CIV_AMERICAN_MEXICO",
		iMaya : "TXT_KEY_CIV_AMERICAN_MAYA",
		iKorea : "TXT_KEY_CIV_AMERICAN_KOREA",
	},
	iBrazil : {
		iArgentina : "TXT_KEY_CIV_BRAZILIAN_ARGENTINA",
	},
})

dMasterTitles = {
	iEgypt : "TXT_KEY_CIV_EGYPTIAN_VASSAL",
	iChina : "TXT_KEY_CIV_CHINESE_VASSAL",
	iIndia : "TXT_KEY_CIV_INDIAN_VASSAL",
	iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iParthia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iRome : "TXT_KEY_CIV_ROMAN_VASSAL",
	iKushans : "TXT_KEY_CIV_KUSHAN_VASSAL",
	iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL",
	iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL",
	iTurks : "TXT_KEY_CIV_TURKIC_VASSAL",
	iNorse : "TXT_KEY_CIV_NORSE_VASSAL",
	iGokturks : "TXT_KEY_CIV_TURKIC_VASSAL",
	iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iTibet : "TXT_KEY_CIV_TIBETAN_VASSAL",
	iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iJava : "TXT_KEY_CIV_JAVAN_VASSAL",
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iRus : "TXT_KEY_CIV_RUS_VASSAL",
	iPoland : "TXT_KEY_CIV_POLISH_VASSAL",
	iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iPortugal : "TXT_KEY_ADJECTIVE_TITLE",
	iMongols : "TXT_KEY_CIV_MONGOL_VASSAL",
	iTimurids : "TXT_KEY_CIV_MUGHAL_VASSAL",
	iTatars : "TXT_KEY_CIV_TATAR_VASSAL",
	iRussia : "TXT_KEY_CIV_RUSSIAN_VASSAL",
	iOttomans : "TXT_KEY_CIV_OTTOMAN_VASSAL",
	iThailand : "TXT_KEY_CIV_THAI_VASSAL",
}

dCommunistVassalTitlesGeneric = {
	iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET",
}

dCommunistVassalTitles = deepdict({
	iRussia : {
		iChina : "TXT_KEY_CIV_RUSSIA_SOVIET_REPUBLIC_ADJECTIVE",
		iTurks : "TXT_KEY_CIV_RUSSIA_SOVIET_TURKS",
		iJapan : "TXT_KEY_CIV_RUSSIA_SOVIET_JAPAN",
		iOttomans : "TXT_KEY_CIV_RUSSIA_SOVIET_OTTOMANS",
		iGermany : "TXT_KEY_CIV_RUSSIA_SOVIET_GERMANY",
	},
})

dFascistVassalTitlesGeneric = {
	iGermany : "TXT_KEY_ADJECTIVE_TITLE"
}

dFascistVassalTitles = deepdict({
	iGermany : {
		iEgypt : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iChina : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iGreece : "TXT_KEY_CIV_GERMANY_NAZI_GREECE",
		iPhoenicia : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iRome : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iEthiopia : "TXT_KEY_CIV_GERMANY_NAZI_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_GERMANY_NAZI_BYZANTIUM",
		iSpain : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iFrance : "TXT_KEY_CIV_GERMANY_NAZI_FRANCE",
		iEngland : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iHolyRome : "TXT_KEY_CIV_GERMANY_NAZI_HOLY_ROME",
		iRus : "TXT_KEY_CIV_GERMANY_NAZI_RUS",
		iNetherlands : "TXT_KEY_CIV_GERMANY_NAZI_NETHERLANDS",
		iMali : "TXT_KEY_CIV_GERMANY_NAZI_MALI",
		iPoland : "TXT_KEY_CIV_GERMANY_NAZI_POLAND",
		iPortugal : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iTimurids : "TXT_KEY_CIV_GERMANY_NAZI_MUGHALS",
		iRussia : "TXT_KEY_CIV_GERMANY_NAZI_RUSSIA",
		iOttomans : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCanada : "TXT_KEY_CIV_GERMANY_NAZI_CANADA",
	},
})

dForeignAdjectives = deepdict({
	iChina : {
		iEgypt : "TXT_KEY_CIV_CHINESE_ADJECTIVE_EGYPT",
		iIndia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDIA",
		iBabylonia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BABYLONIA",
		iPersia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_PERSIA",
		iRome : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ROME",
		iKushans : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KUSHANS",
		iJapan : "TXT_KEY_CIV_CHINESE_ADJECTIVE_JAPAN",
		iKorea : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KOREA",
		iByzantium : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ARABIA",
		iKhmer : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KHMER",
		iJava : "TXT_KEY_CIV_CHINESE_ADJECTIVE_JAVA",
		iMongols : "TXT_KEY_CIV_CHINESE_ADJECTIVE_MONGOLIA",
		iOttomans : "TXT_KEY_CIV_CHINESE_ADJECTIVE_OTTOMANS",
		iTibet : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TIBET",
	},
})

dForeignNames = deepdict({
	iEgypt : {
		iNubia : "TXT_KEY_CIV_EGYPTIAN_NAME_NUBIA",
	},
	iGreece : {
		iAssyria : "TXT_KEY_CIV_GREEK_NAME_ASSYRIA",
		iTurks : "TXT_KEY_CIV_GREEK_NAME_TURKS",
	},
	iIndia : {
		iKushans : "TXT_KEY_CIV_INDIAN_NAME_KUSHANS",
		iJava: "TXT_KEY_CIV_INDIAN_NAME_JAVA",
	},
	iPersia : {
		iAssyria : "TXT_KEY_CIV_PERSIAN_NAME_ASSYRIA",
		iByzantium : "TXT_KEY_CIV_PERSIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_PERSIAN_NAME_TURKS",
	},
	iRome : {
		iEgypt : "TXT_KEY_CIV_ROMAN_NAME_EGYPT",
		iChina : "TXT_KEY_CIV_ROMAN_NAME_CHINA",
		iBabylonia : "TXT_KEY_CIV_ROMAN_NAME_BABYLONIA",
		iGreece : "TXT_KEY_CIV_ROMAN_NAME_GREECE",
		iPersia : "TXT_KEY_CIV_ROMAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ROMAN_NAME_PHOENICIA",
		iCelts : "TXT_KEY_CIV_ROMAN_NAME_CELTS",
		iEthiopia : "TXT_KEY_CIV_ROMAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ROMAN_NAME_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_ROMAN_NAME_NORSE",
		iTurks : "TXT_KEY_CIV_ROMAN_NAME_TURKS",
		iKhmer : "TXT_KEY_CIV_ROMAN_NAME_KHMER",
		iSpain : "TXT_KEY_CIV_ROMAN_NAME_SPAIN",
		iFrance : "TXT_KEY_CIV_ROMAN_NAME_FRANCE",
		iEngland : "TXT_KEY_CIV_ROMAN_NAME_ENGLAND",
		iHolyRome : "TXT_KEY_CIV_ROMAN_NAME_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ROMAN_NAME_GERMANY",
		iNetherlands : "TXT_KEY_CIV_ROMAN_NAME_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ROMAN_NAME_MALI",
		iPortugal : "TXT_KEY_CIV_ROMAN_NAME_PORTUGAL",
		iMongols : "TXT_KEY_CIV_ROMAN_NAME_MONGOLIA",
		iRussia : "TXT_KEY_CIV_ROMAN_NAME_RUSSIA",
		iOttomans : "TXT_KEY_CIV_ROMAN_NAME_OTTOMANS",
		iThailand : "TXT_KEY_CIV_ROMAN_NAME_THAILAND",
	},
	iKhmer : {
		iJava : "TXT_KEY_CIV_KHMER_NAME_JAVA",
	},
	iTurks : {
		iByzantium : "TXT_KEY_CIV_TURKIC_NAME_BYZANTIUM",
	},
	iNorse : {
		iFrance: "TXT_KEY_CIV_NORSE_NAME_FRANCE",
		iSpain: "TXT_KEY_CIV_NORSE_NAME_SPAIN",
		iHolyRome: "TXT_KEY_CIV_NORSE_NAME_HOLY_ROME",
		iRus: "TXT_KEY_CIV_NORSE_NAME_RUS",
		iPoland: "TXT_KEY_CIV_NORSE_NAME_POLAND",
		iItaly: "TXT_KEY_CIV_NORSE_NAME_ITALY",
		iRussia: "TXT_KEY_CIV_NORSE_NAME_RUSSIA",
	},
	iArabia : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_ARABIAN_NAME_TURKS",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iJava : "TXT_KEY_CIV_ARABIAN_NAME_JAVA",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iMorocco : {
 		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
 		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
 		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
 		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
 		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
 		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
 		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
 		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
 		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
 		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
 		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
 	},
 	iTunis : {
 		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
 		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
 		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
 		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
 		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
 		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
 		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
 		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
 		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
 		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
 		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
 	},
	iTibet : {
		iChina : "TXT_KEY_CIV_TIBETAN_NAME_CHINA",
		iIndia : "TXT_KEY_CIV_TIBETAN_NAME_INDIA",
		iTurks : "TXT_KEY_CIV_TIBETAN_NAME_TURKS",
		iMongols : "TXT_KEY_CIV_TIBETAN_NAME_MONGOLIA",
	},
	iMoors : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iSpain : {
		iKhmer : "TXT_KEY_CIV_SPANISH_NAME_KHMER",
		iAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
		iTimurids : "TXT_KEY_CIV_SPANISH_NAME_MUGHALS",
	},
	iFrance : {
		iKhmer : "TXT_KEY_CIV_FRENCH_NAME_KHMER",
		iTimurids : "TXT_KEY_CIV_FRENCH_NAME_MUGHALS",
	},
	iEngland : {
		iKhmer : "TXT_KEY_CIV_ENGLISH_NAME_KHMER",
		iTimurids : "TXT_KEY_CIV_ENGLISH_NAME_MUGHALS",
	},
	iRussia : {
		iPersia : "TXT_KEY_CIV_RUSSIAN_NAME_PERSIA",
	},
	iMongols : {
		iTurks : "TXT_KEY_CIV_MONGOL_NAME_TURKS",
		iRussia : "TXT_KEY_CIV_MONGOL_NAME_RUSSIA",
	},
	iOttomans : {
		iPoland : "TXT_KEY_CIV_OTTOMAN_NAME_POLAND",
		iGermany : "TXT_KEY_CIV_OTTOMAN_NAME_GERMANY",
	},
	iGermany : {
		iMoors : "TXT_KEY_CIV_GERMAN_NAME_MOORS",
	},
})

lRepublicOf = [iEgypt, iIndia, iChina, iPersia, iCelts, iJapan, iEthiopia, iKorea, iNorse, iTurks, iTibet, iKhmer, iJava, iHolyRome, iMali, iVietnam, iBenin, iHausa, iGhana, iKanemBornu, iPoland, iSweden, iTimurids, iOttomans, iThailand, iIran, iAshanti, iMorocco, iSaudis]
lRepublicAdj = [iBabylonia, iAssyria, iHittites, iRome, iMoors, iToltecs, iSpain, iFrance, iRus, iPortugal, iInca, iItaly, iAztecs, iArgentina, iSaudis, iBelgium]

lSocialistRepublicOf = [iEgypt, iCelts, iMoors, iHolyRome, iVietnam, iBrazil, iNorse, iSweden, iColombia, iHausa, iMorocco]
lSocialistRepublicAdj = [iHittites, iPersia, iToltecs, iTurks, iItaly, iAztecs, iIran, iArgentina, iMisr]

lPeoplesRepublicOf = [iIndia, iChina, iPolynesia, iJapan, iTibet, iMali, iJava, iSonghai, iGhana, iPoland, iTimurids, iThailand, iCongo, iKanemBornu]
lPeoplesRepublicAdj = [iDravidia, iByzantium, iRus, iMongols]

lIslamicRepublicOf = [iIndia, iPersia, iMali, iTimurids, iIran, iSaudis, iHausa]

dEmpireThreshold = {
	iKhmer : 3,
	iToltecs: 2,
	iHittites: 2,
	iBabylonia: 2,
	iSouthAfrica: 10,
	iOman : 3,
	iHausa : 3,
	iSwahili : 2,
	iSamanids : 3,
	iTunis : 2,
	iBuyids : 10,
	iMisr : 3,
	iParthia : 6,
	iArmenia : 4,
	iScythia : 8,
	iNumidia : 5,
	iVandals : 5,
	iHuns : 5,
	iGoths : 5,
	iGermania : 5,
	iMacedon : 6,
	iAssyria : 2,
	iSumeria : 2,
	iMinoa : 3,
	iElam : 2,
	iMycenae : 4,
	iSparta : 3,
	iPhoenicia : 4,
	iPolynesia : 3,
	iDravidia : 3,
	iKorea : 4,
	iTibet : 2,
	iMoors : 3,
	iHolyRome : 3,
	iPoland : 3,
	iInca : 3,
	iMongols : 8,
	iTimurids : 6,
	iItaly : 7,
	iTatars: 3,
	iRussia : 8,
	iIran : 4,
	iGermany : 5,
	iBelgium : 5,
	iSaudis : 6,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lInitialNameChanges = [iMisr, iSaudis]
lRespawnNameChanges = [iHolyRome, iInca, iAztecs, iTimurids, iNumidia, iGreece] # TODO: this should be covered by period
lVassalNameChanges = [iInca, iAztecs, iTimurids] # TODO: this should be covered by period
lChristianityNameChanges = [iInca, iAztecs] # TODO: this should be covered by period

lColonies = [iMali, iSonghai, iGhana, iKanemBornu, iBenin, iHausa, iAshanti, iEthiopia, iCongo, iSwahili, iToltecs, iAztecs, iInca, iMaya, iZulu, iBoers, iZimbabwe, iKatanga, iBuganda, iSomalia, iFunj, iAdal, iMadagascar] # TODO: could be covered by more granular continental regions

dReplacementCivs = {
	iManchuria: iChina,
}

dNameChanges = { # TODO: this should be covered by period
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_SHORT_DESC",
	iAztecs : "TXT_KEY_CIV_MEXICO_SHORT_DESC",
	iInca : "TXT_KEY_CIV_PERU_SHORT_DESC",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_SHORT_DESC",
	iMisr : "TXT_KEY_CIV_FATIMIDS_SHORT_DESC",
	#iMoors : "TXT_KEY_CIV_MOROCCO_SHORT_DESC",
	iTurks : "TXT_KEY_CIV_UZBEKS_SHORT_DESC",
	iTimurids : "TXT_KEY_CIV_MUGHALS_SHORT_DESC",
	iNumidia : "TXT_KEY_CIV_ALGERIA_SHORT_DESC",
	iGreece : "TXT_KEY_CIV_MGREECE_SHORT_DESC",
	iSparta : "TXT_KEY_CIV_MGREECE_SHORT_DESC",
	#iHausa : "TXT_KEY_CIV_SOKOTO",
	#iSwahili : "TXT_KEY_CIV_TANZANIA_SHORT_DESC",
	iCelts : "TXT_KEY_CIV_IRELAND_SHORT_DESC",
	#iNubia : "TXT_KEY_CIV_NUBIA_SOUTH_SUDAN", Not on revival
	#iFunj : "TXT_KEY_CIV_FUNJ_SUDAN",
	iManchuria: "TXT_KEY_CIV_CHINA_SHORT_DESC",
	iSaudis : "TXT_KEY_CIV_ARABIA_SHORT_DESC",

}

dAdjectiveChanges = {
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_ADJECTIVE",
	iAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_ADJECTIVE",
	iMisr : "TXT_KEY_CIV_FATIMIDS_ADJECTIVE",
	#iMoors : "TXT_KEY_CIV_MOROCCO_ADJECTIVE",
	iTurks : "TXT_KEY_CIV_UZBEKS_ADJECTIVE",
	iTimurids : "TXT_KEY_CIV_MUGHALS_ADJECTIVE",
	iNumidia : "TXT_KEY_CIV_ALGERIA_ADJECTIVE",
	iGreece : "TXT_KEY_CIV_MGREECE_ADJECTIVE",
	iSparta : "TXT_KEY_CIV_MGREECE_ADJECTIVE",
	#iHausa : "TXT_KEY_CIV_SOKOTO_ADJECTIVE",
	#iSwahili : "TXT_KEY_CIV_TANZANIA_ADJECTIVE",
	iCelts : "TXT_KEY_CIV_IRELAND_ADJECTIVE",
	#iNubia : "TXT_KEY_CIV_NUBIA_SOUTH_SUDANESE",
	#iFunj : "TXT_KEY_CIV_FUNJ_SUDANESE",
	iManchuria : "TXT_KEY_CIV_CHINA_ADJECTIVE",
	iSaudis : "TXT_KEY_CIV_ARABIA_ADJECTIVE",
}

dStartingLeaders = [ 
# 3000 BC
{
	iIndependent : iIndependentLeader,
	iIndependent2 : iIndependentLeader,
	iNative : iNativeLeader,
	iEgypt : iDjoser,
	iSumeria : iSargon,
	iIndia : iAsoka,
	iBabylonia : iHammurabi,
	iHarappa : iWentAntu,
	iMinoa : iMinos,
	iElam : iKindattu,
	iAssyria : iAshurbanipal,
	iNubia : iTaharqa,
	iChina : iWu,
	iHittites : iMursili,
	iMycenae : iAgamemnon,
	iGreece : iPericles,
	iPersia : iCyrus,
	iCarthage : iHiram,
	iJudah : iDavid,
	iPolynesia : iAhoeitu,
	iScythia : iTomyris,
	iRome : iScipio,
	iGermania : iJuliusCivilis,
	iSparta : iLeonidas,
	iCelts : iBrennus,
	iMaya : iPacal,
	iJapan : iKammu,
	iNumidia : iMasinissa,
	iMacedon : iAlexanderTheGreat,
	iArmenia : iTigranes,
	iDravidia : iRajendra,
	iEthiopia : iEzana,
	iVietnam: iLeLoi,
	iParthia: iMithridates,
	iToltecs : iTopiltzin,
	iVandals : iGaiseric,
	iKushans: iKanishka,
	iKorea : iWangKon,
	iGoths : iAlaric,
	iGhana : iDinghaCisse,
	iByzantium : iConstantine,
	iHuns : iAttila,
	iMalays : iSriJayanasa,
	iNorse : iCanute,
	iTurks : iAlpArslan,
	iGokturks : iBumin,
	iArabia : iHarun,
	iTibet : iSongtsen,
	iKhazars: iBulan,
	iKanemBornu: iDunamaDabbalemi,
	iKhmer : iNeangNeak,
	iMoors : iRahman,
	iJava : iHayamWuruk,
	iSpain : iIsabella,
	iFrance : iCharlemagne,
	iGeorgia : iTamar,
	iEngland : iAlfred,
	iYemen : iArwaAlSulayhi,
	iOman : iAbiBinOmar,
	iHolyRome : iBarbarossa,
	iBurma : iAnawrahta,
	iHausa : iAmina,
	iRus : iYaroslav,
	iSamanids : iIsmaelSamani,
	iMorocco : iYaqub,
	iBenin : iEwuare,
	iMisr : iAlMuiz,
	iBuyids : iAdudAlDawla,
	iSwahili : iDawud,
	iSomalia: iFakrAdDin,
	iMali : iMansaMusa,
	iBuganda: iKakamaTwale,
	iPoland : iCasimir,
	iJerusalem: iBaldwin,
	iPortugal : iAfonso,
	iInca : iHuaynaCapac,
	iItaly : iLorenzo,
	iMongols : iGenghisKhan,
	iAztecs : iMontezuma,
	iZimbabwe: iMatope,
	iTunis : iAbuAmrUthman,
	iTimurids : iTamerlane,
	iGhorids : iSabuktigin,
	iTatars : iUzbeg,
	iThailand : iNaresuan,
	iSweden : iGustav,
	iRussia : iIvan,
	iAdal: iAhmadIbnIbrahim,
	iOttomans : iMehmed,
	iCongo : iMbemba,
	iSonghai : iSunniAli,
	iFunj: iAmaraDunqas,
	iIran : iAbbas,
	iMadagascar: iAndrianampoinimerina,
	iNetherlands : iWillemVanOranje,
	iManchuria : iKangxi,
	iKatanga: iChibindaIlunga,
	iAshanti : iOsei,
	iGermany : iFrederick,
	iSaudis : iIbnSaud,
	iAmerica : iWashington,
	iBoers: iPaulKruger,
	iArgentina : iSanMartin,
	iMexico : iJuarez,
	iColombia : iBolivar,
	iZulu: iShaka,
	iBrazil : iPedro,
	iBelgium : iLeopold,
	iAustralia : iCurtin,
	iCanada : iMacDonald,
	iSouthAfrica: iBotha,
},
# 600 AD
{
	iChina : iTaizong,
	iParthia : iKhosrow,
	iByzantium : iJustinian,
	iNubia : iMerkurios,
	iCelts : iBrianBoru,
},
# 1100 AD
{
	iByzantium : iBasil,
	iArabia : iQatadaIbnIdris,
	iEthiopia : iZaraYaqob,
	iFrance : iPhilipAugustus,
},
# 1500 AD
{
	iChina : iHongwu,
	iDravidia : iKrishnaDevaRaya,
	iEthiopia : iZaraYaqob,
	iKorea : iSejong,
	iMali : iMansaMusa,
	iFrance : iLouis,
	iMalays : iTunPerak,
	iJapan : iOdaNobunaga,
	iNorse : iChristian,
	iTurks : iTamerlane,
	iMoors : iYaqub,
	iJava : iHayamWuruk,
	iSpain : iPhilip,
	iEngland : iElizabeth,
	iHolyRome : iCharles,
	iBurma : iBayinnaung,
	iVietnam : iLeLoi,
	iMisr : iBaibars,
	iPoland : iSobieski,
	iPortugal : iJoao,
	iInca : iHuaynaCapac,
	iItaly : iLorenzo,
	iAztecs : iMontezuma,
	iMughals : iAkbar,
	iGhorids: iTughluq,
	iThailand : iNaresuan,
	iSweden : iGustav,
	iRussia : iIvan,
	iOttomans : iSuleiman,
	iCongo : iMbemba,
	iIran : iAbbas,
},
# 1700 AD
{
	iChina : iHongwu,
	iIndia : iShivaji,
	iDravidia : iKrishnaDevaRaya,
	iEthiopia : iZaraYaqob,
	iKorea : iSejong,
	iNorse : iChristian,
	iJapan : iOdaNobunaga,
	iTurks : iShaybaniKhan,
	iSpain : iPhilip,
	iFrance : iLouis,
	iEngland : iVictoria,
	iHolyRome : iFrancis,
	iBurma : iBayinnaung,
	iVietnam : iLeLoi,
	iPoland : iSobieski,
	iOman: iBarghash,
	iPortugal : iJoao,
	iZimbabwe: iChangamire,
	iTimurids : iAkbar,
	iSweden : iGustav,
	iRussia : iPeter,
	iOttomans : iSuleiman,
	iNetherlands : iWilliam,
	iMorocco : iAhmad,
	iYemen : iAlQasim,
},
# 1815 AD
{
	iIndia: iShivaji,
	iKorea: iSejong,
	iJapan: iOdaNobunaga,
	iNorse: iChristian,
	iTurks: iShaybaniKhan,
	iSpain: iPhilip,
	iFrance: iNapoleon,
	iEngland: iVictoria,
	iHolyRome: iFrancis,
	iBurma: iBayinnaung,
	iVietnam: iLeLoi,
	iMisr: iMuhammadAli,
	iItaly: iCavour,
	iSweden: iGustav,
	iRussia: iAlexanderI,
	iOttomans: iSuleiman,
	iThailand: iMongkut,
	iCongo: iMbemba,
	iIran: iAbbas,
	iManchuria: iKangxi,
	iNetherlands: iWilliam,
	iGermany: iFrederick,
	iAmerica: iWashington,
	iArgentina: iSanMartin,
	iMexico: iSantaAnna,
	iColombia: iBolivar,
	iHausa: iUsumanDanFodio,
	iBuganda: iMutesa,
},
]

### Event handlers

@handler("GameStart")
def setup():
	iScenario = scenario()
	
	if iScenario == i600AD:
		data.civs[iChina].iAnarchyTurns += 3
		
	elif iScenario in [i1700AD, i1815AD]:
		checkReplacementName(iManchuria)
	
@handler("playerCivAssigned")
def initName(iPlayer):
	if not is_minor(iPlayer) and player(iPlayer).getNumCities() == 0: 
		setDesc(iPlayer, peoplesName(iPlayer))
		checkName(iPlayer)
		checkLeader(iPlayer)

	if civ(iPlayer) in lInitialNameChanges:
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)

@handler("resurrection")
def onResurrection(iPlayer):
	onRespawn(iPlayer)

def onRespawn(iPlayer):
	data.civs[civ(iPlayer)].iResurrections += 1
	
	if civ(iPlayer) in lRespawnNameChanges:
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)

@handler("vassalState")	
def onVassalState(iMaster, iVassal):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv == iTimurids and iMasterCiv not in dCivGroups[iCivGroupEurope]: 		return
	
	data.civs[iVassalCiv].iResurrections += 1
	checkNameChange(iVassal)
	checkAdjectiveChange(iVassal)
		
	checkName(iVassal)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if is_minor(iPlayer):
		return

	if civ(iPlayer) in lChristianityNameChanges and iReligion in lChristianity:
		data.civs[civ(iPlayer)].iResurrections += 1
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	checkName(iPlayer)

@handler("revolution")
def onRevolution(iPlayer):
	if is_minor(iPlayer):
		return

	data.civs[civ(iPlayer)].iAnarchyTurns += 1
	
	if civ(iPlayer) == iTimurids and isRepublic(iPlayer):
		checkNameChange(iPlayer)
	
	checkName(iPlayer)
	
	for iLoopPlayer in players.vassals(iPlayer):
		checkName(iLoopPlayer)
	
@handler("setPlayerAlive")
def onSetPlayerAlive(iPlayer, bAlive):
	if bAlive:
		checkName(iPlayer)

@handler("cityAcquired")
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)

	checkReplacementName(iPreviousOwner)
	checkReplacementName(iNewOwner)

@handler("cityRazed")
def onCityRazed(city):
	iPreviousOwner = slot(Civ(city.getPreviousCiv()))
	if iPreviousOwner >= 0:
		checkName(iPreviousOwner)

@handler("cityBuilt")	
def onCityBuilt(city):
	checkName(city.getOwner())
	
@handler("playerPeriodChange")
def onPeriodChange(iPlayer, iPeriod):
	iCiv = civ(iPlayer)


	if iCiv == iByzantium:
		if iPeriod == iPeriodByzantiumRoman:
			setShort(iPlayer, text("TXT_KEY_CIV_MEDIOLANUM_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_MEDIOLANUM_ADJECTIVE"))

	
	if iCiv == iPhoenicia:
		if iPeriod == iPeriodCarthage:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)

	if iCiv == iCelts:
		if iPeriod == iPeriodInsularCelts:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)

	if iCiv == iOman:
		if iPeriod == iPeriodZanzibar:
			setShort(iPlayer, text("TXT_KEY_CIV_ZANZIBAR_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_ZANZIBAR_ADJECTIVE"))
		elif iPeriod == -1:
			setShort(iPlayer, text("TXT_KEY_CIV_OMAN_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_OMAN_ADJECTIVE"))


	
	if iCiv == iNorse:
		if iPeriod == iPeriodDenmark:
			setShort(iPlayer, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
		elif iPeriod == iPeriodNorway:
			setShort(iPlayer, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))

	if iCiv == iMacedon:
		if iPeriod == iPeriodSeleucids:
			setShort(iPlayer, text("TXT_KEY_CIV_SELEUCIA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_SELEUCIA_ADJECTIVE"))

	if iCiv == iSwahili:
		if iPeriod == iPeriodTanzania:
			setShort(iPlayer, text("TXT_KEY_CIV_TANZANIA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_TANZANIA_ADJECTIVE"))

	if iCiv == iNubia:
		if iPeriod == iPeriodSouthSudan:
			setShort(iPlayer, text( "TXT_KEY_CIV_NUBIA_SOUTH_SUDAN"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_NUBIA_SOUTH_SUDANESE"))

	if iCiv == iFunj:
		if iPeriod == iPeriodSudan:
			setShort(iPlayer, text("TXT_KEY_CIV_FUNJ_SUDAN"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_FUNJ_SUDANESE"))

	if iCiv == iZimbabwe:
		if iPeriod == iPeriodMutapa:
			setShort(iPlayer, text("TXT_KEY_CIV_MUTAPA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_MUTAPA_ADJECTIVE"))
		elif iPeriod == iPeriodRozwi:
			setShort(iPlayer, text("TXT_KEY_CIV_ROZWI_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_ROZWI_ADJECTIVE"))
		elif iPeriod == iPeriodRhodesia:
			setShort(iPlayer, text("TXT_KEY_CIV_RHODESIA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_RHODESIA_ADJECTIVE"))
		elif iPeriod == -1:
			setShort(iPlayer, text("TXT_KEY_CIV_ZIMBABWE_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_ZIMBABWE_MODERN_ADJECTIVE"))

	if iCiv == iBuganda:
		if iPeriod == iPeriodBuganda:
			setShort(iPlayer, text("TXT_KEY_CIV_BUGANDA_NEW_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_BUGANDA_NEW_ADJECTIVE"))
		elif iPeriod == iPeriodUganda:
			setShort(iPlayer, text("TXT_KEY_CIV_UGANDA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_UGANDA_ADJECTIVE"))


	if iCiv == iMisr:
		if iPeriod == iPeriodMisrEgypt:
			setShort(iPlayer, text("TXT_KEY_CIV_EGYPT_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_EGYPT_ADJECTIVE"))

	if iCiv == iHausa:
		if iPeriod == iPeriodNigeria:
			setShort(iPlayer, text("TXT_KEY_CIV_NIGERIA"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_NIGERIA_ADJECTIVE"))
		elif iPeriod == iPeriodSokoto:
			setShort(iPlayer, text("TXT_KEY_CIV_SOKOTO"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_SOKOTO_ADJECTIVE"))


	if iCiv == iArabia:
		if iPeriod == iPeriodHejaz:
			setShort(iPlayer, text("TXT_KEY_CIV_HEJAZ"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_HEJAZ_ADJECTIVE"))
		else:
			setShort(iPlayer, text("TXT_KEY_CIV_ARABIA_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_ARABIA_ADJECTIVE"))


	
	if iCiv == iTurks:
		if iPeriod == iPeriodUzbeks:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)

	if iCiv == iNumidia:
		if iPeriod == iPeriodAlgeria:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
	
	if iCiv == iGreece:
		if iPeriod == iPeriodModernGreece or iPeriod == iPeriodUnitedGreece:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)

	if iCiv == iSparta:
		if iPeriod == iPeriodUnitedGreece:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
			
	if iCiv == iHolyRome:
		if iPeriod == iPeriodAustria:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)


	if iCiv == iTimurids:
		if iPeriod == iPeriodMughals:
			setShort(iPlayer, text("TXT_KEY_CIV_MUGHALS_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_MUGHALS_ADJECTIVE"))

	if iCiv == iGhorids:
		if iPeriod == iPeriodDelhi:
			setShort(iPlayer, text("TXT_KEY_CIV_DELHI_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_DELHI_ADJECTIVE"))

	if iCiv == iRus:
		if iPeriod == iPeriodUkraine:
			setShort(iPlayer, text("TXT_KEY_CIV_UKRAINE_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_UKRAINE_ADJECTIVE"))
	
	if iPeriod == -1:
		revertNameChange(iPlayer)
		revertAdjectiveChange(iPlayer)
	
	checkName(iPlayer)
	checkLeader(iPlayer)
	

@handler("religionFounded")
def onReligionFounded(_, iPlayer):
	if turn() == scenarioStartTurn():
		return

	checkName(iPlayer)


@handler("capitalMoved")
def onCapitalMoved(city):
	checkName(city.getOwner())


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
	if every(10):
		for iPlayer in players.major():
			checkName(iPlayer)
			checkLeader(iPlayer)

		
def checkName(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	if player(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if player(iPlayer).isHuman(): return
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	try:
		player(iPlayer).setCivDescription(sName)
	except:
		pass
	
def setShort(iPlayer, sShort):
	player(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	player(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if player(iPlayer).isHuman(): return
	if player(iPlayer).getLeader() == iLeader: return
	player(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if infos.leader(player(iPlayer)).getText() != sName:
		player(iPlayer).setLeaderName(sName)

### Utility methods ###

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_%s" % sSuffix
	return "TXT_KEY_CIV_%s%s" % (civ_name(civ(iPlayer)).upper(), sSuffix)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if team(iPlayer).isAVassal():
		return text(latin1(sTextKey), name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True))
	return text(latin1(sTextKey), name(iPlayer), adjective(iPlayer))

def capitalName(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: 
		translatedCapital = cn.getTranslation(iEngland, capital)
		if translatedCapital:
			return translatedCapital.name
		
		return capital.getName()
	
	return short(iPlayer)

def isCurrentCapital(iPlayer, *names):
	capital = player(iPlayer).getCapitalCity()
	if not capital: return False
	
	return cn.getBaseName(capital) in names
	
def checkNameChange(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iCiv]))
	
def checkAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iCiv]))
		
def revertNameChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dNameChanges:
		setShort(iPlayer, infos.civ(iCiv).getShortDescription(0))

def revertAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, infos.civ(iCiv).getAdjective(0))
	
def getColumn(iPlayer):
	lTechs = [infos.tech(iTech).getGridX() for iTech in range(iNumTechs) if team(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
def getColumn(iPlayer):
	lTechs = [infos.tech(iTech).getGridX() for iTech in range(iNumTechs) if team(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)

def checkReplacementName(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dReplacementCivs:
		iReplacementCiv = dReplacementCivs[iCiv]
		
		if player(iReplacementCiv).isExisting():
			revertNameChange(iPlayer)
			revertAdjectiveChange(iPlayer)
		else:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)

### Utility methods for civilization status ###
	
def isCapitulated(iPlayer):
	return team(iPlayer).isAVassal() and team(iPlayer).isCapitulated()
	
def isEmpire(iPlayer):
	if team(iPlayer).isAVassal(): return False

	return player(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dEmpireThreshold: 
		return dEmpireThreshold[iCiv]
	
	if iCiv == iEthiopia and not game.isReligionFounded(iIslam):
		return 4
	
	if iCiv == iRome and not player(iByzantium).isExisting():
		return 7
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in players.major():
		if team(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def capitalCoords(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: return location(capital)
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = game.getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, (x, y)):
	plot = plot_(x, y)
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer) and not bIgnoreVassal:
		sVassalName = vassalName(iPlayer, master(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = dDefaultInsertNames.get(iCiv)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if iMasterCiv == iRome and player(iPlayer).getPeriod() == iPeriodCarthage:
		return "TXT_KEY_CIV_ROMAN_NAME_CARTHAGE"
		
	if iCiv == iNetherlands:
		return short(iPlayer)

	sSpecificName = dForeignNames[iMasterCiv].get(iCiv)
	if sSpecificName:
		return sSpecificName
	
	return None
	
def republicName(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in [iMoors, iEngland]: return None
	
	if iCiv == iInca and data.civs[iCiv].iResurrections > 0: return None
	
	if iCiv == iNetherlands and isCommunist(iPlayer): return "TXT_KEY_CIV_NETHERLANDS_ARTICLE"
	
	if iCiv == iTurks: return "TXT_KEY_CIV_TURKS_UZBEKISTAN"

	if iCiv == iSwahili: return specificName(iPlayer)

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or (civic.iGovernment in [iRepublic, iElective] and civic.iReligion == iFanaticism)
	bResurrected = data.civs[iCiv].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iCiv].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)

	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	if iCiv == iSouthAfrica:
		if iNumCities <= 3 and location(capital) == location(plots.capital(iCiv)):
			return "TXT_KEY_CIV_SOUTH_AFRICA_CAPE"

	if iCiv == iMoors:
		if isCurrentCapital(iPlayer, "Al-Garnatah"):
			return "TXT_KEY_CIV_GRANADA"
		if isCurrentCapital(iPlayer, "Al-Garnatah") and player(iMoors).getNumCities() == 1 and year() > year(1200):
			return "TXT_KEY_CIV_GRANADA"

	elif iCiv == iSonghai:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_NIGER"

	elif iCiv == iAdal:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ADAL_SOMALILAND"
		elif iEra >= iRenaissance:
			return "TXT_KEY_CIV_ADAL_HARAR"
		elif year() < year(1400):
			return "TXT_KEY_CIV_ADAL_IFAT"

	elif iCiv == iSomalia:
		if iEra == iRenaissance:
			return "TXT_KEY_CIV_SOMALIA_GELEDI"
		elif iEra == iMedieval:
			return "TXT_KEY_CIV_SOMALIA_AJURAN"
		elif iEra <= iClassical:
			return "TXT_KEY_CIV_SOMALIA_MOGADISHU"

	elif iCiv == iKatanga:
		if iEra >= iIndustrial:
			return
		if iAnarchyTurns > 5:
			return "TXT_KEY_CIV_KATANGA_CHOKWE"
		elif iAnarchyTurns > 3:
			return "TXT_KEY_CIV_KATANGA_LUNDA"
		elif iAnarchyTurns > 2:
			return "TXT_KEY_CIV_KATANGA_KUBA"
		else:
			return "TXT_KEY_CIV_KATANGA_LUBA"

	elif iCiv == iMadagascar:
		if iEra <= iRenaissance:
			return "TXT_KEY_CIV_MADAGASCAR_IMERINA"


	elif iCiv == iAshanti:
		if bResurrected and not player(iGhana).isExisting():
			return "TXT_KEY_CIV_GHANA"

	elif iCiv == iBenin:
		if getColumn(iPlayer) <= 5:
			return "TXT_KEY_CIV_IGODOMIGODO"


	elif iCiv == iKanemBornu:
		if iEra >= iGlobal:
			setShort(iPlayer, text("TXT_KEY_CIV_CIV_CHAD"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_CHAD_ADJECTIVE"))
		elif iEra < iMedieval:
			return "TXT_KEY_CIV_KANEM"
		else: return "TXT_KEY_CIV_BORNU"

	elif iCiv == iHausa:
		if iEra <= iGlobal and not bEmpire:
			return "TXT_KEY_CIV_HAUSA_KATSINA"

	elif iCiv == iGhana:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_MAURITANIA"

	elif iCiv == iMisr:
		if not bResurrected and year() <= year(1700) and not player(iMisr).getPeriod() == -1:
			if getColumn(iPlayer) >= 13 or bCapitulated:
				return "TXT_KEY_CIV_MISR_MAMLUK"
			elif iReligion == iShia:
				return "TXT_KEY_CIV_MISR_FATIMID"
			elif getColumn(iPlayer) >= 10:
					return "TXT_KEY_CIV_MISR_MAMLUK"
			else:
				return "TXT_KEY_CIV_MISR_AYYUBID"

			#if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			#	return "TXT_KEY_CIV_EGYPT_COPTIC"

	elif iCiv == iSwahili:
		if iEra <= iIndustrial:
			return "TXT_KEY_CIV_KILWA_SHORT_DESC"


	elif iCiv == iYemen:
		if bMonarchy:
			if iReligion == iShia and getColumn(iPlayer) <= 11:
				return "TXT_KEY_CIV_YEMEN_SULAYHIDS"
			elif iReligion == iShia and getColumn(iPlayer) <= 14:
				return "TXT_KEY_CIV_YEMEN_QASIMIDS"
			elif getColumn(iPlayer) == 7:
				return "TXT_KEY_CIV_YEMEN_ZIYADIDS"
			elif getColumn(iPlayer) <= 10:
				return "TXT_KEY_CIV_YEMEN_ZURAYIDS"
			elif getColumn(iPlayer) <= 11:
				return "TXT_KEY_CIV_YEMEN_RASULIDS"
			elif getColumn(iPlayer) <= 14:
				return "TXT_KEY_CIV_YEMEN_TAHIRIDS"

	elif iCiv == iOman:
		if getColumn(iPlayer) == 10:
				return "TXT_KEY_CIV_OMAN_HORMUZ"
		if iEra == iMedieval:
			return "TXT_KEY_CIV_OMAN_SOHAR"


	elif iCiv == iChina:
		if bEmpire and turn() <= year(1800): # Aeons - No Ming after 1800, just be named China
			if bResurrected and turn() >= year(1300):
				return "TXT_KEY_CIV_CHINA_MING"
			
			if iEra == iRenaissance and turn() >= year(1300):
				return "TXT_KEY_CIV_CHINA_MING"

	elif iCiv == iHittites:
		return "TXT_KEY_CIV_HITTITES_HATTI"

	elif iCiv == iMinoa:
		if iEra >= iClassical:
			return "TXT_KEY_CIV_MINOA_CRETE"

	elif iCiv == iGermania:
		if capital in plots.region(rBritain):
			return "TXT_KEY_CIV_GERMANIA_WESSEX"


	elif iCiv == iSumeria:
		if bEmpire:
			return "TXT_KEY_CIV_SUMERIA_AKKAD"
		if turn() >= year(-2000):
			return "TXT_KEY_CIV_SUMERIA_SEALAND"
	
	elif iCiv == iNubia:
		if iEra == iMedieval or iReligion == iOrthodoxy:
			if isCurrentCapital(iPlayer, "Para"):
				return "TXT_KEY_CIV_NUBIA_NOBATIA"
			
			if isCurrentCapital(iPlayer, "Soba"):
				return "TXT_KEY_CIV_NUBIA_ALODIA"

			return "TXT_KEY_CIV_NUBIA_MAKURIA"
		if iEra <= iClassical:
			return "TXT_KEY_CIV_NUBIA_KUSH"


	elif iCiv == iBuyids:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_BUYIDS_FARS"
			
	if iCiv == iGreece:
		if player(iGreece).getPeriod() == -1 and not controlsCity(iPlayer, location(plots.capital(iGreece))):
			return "TXT_KEY_CIV_THESSALLONIKI"

	elif iCiv == iJudah:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_JUDAH_PALESTINE"
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_CIV_JUDAH_JERUSALEM"
		if iReligion == iJudaism:
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_JUDAH_ISRAEL"

	elif iCiv == iJerusalem:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_JERUSALEM_PALESTINE"
		if iReligion == iJudaism:
				return "TXT_KEY_CIV_JERUSALEM_ISRAEL"

	elif iCiv == iGhorids:
		if turn() <= year(1150) and period(iCiv) == -1:
			return "TXT_KEY_CIV_GHAZNAVIDS"


	elif iCiv == iGoths:
		if capital in plots.regions(rIberia):
			return "TXT_KEY_CIV_GOTHS_VISIGOTHS"
	
		if capital in plots.region(rItaly):
			return "TXT_KEY_CIV_GOTHS_OSTROGOTHS"

	elif iCiv == iNumidia:
		if not tPlayer.isHasTech(iCurrency):
			return "TXT_KEY_CIV_NUMIDIA_MASSAESYLI"
		elif iEra >= iIndustrial and not bMonarchy:
			return "TXT_KEY_CIV_NUMIDIA_ALGERIA"
		elif iReligion == iIslam or iReligion == iShia:
			return "TXT_KEY_CIV_NUMIDIA_ZAYYANIDS"

	elif iCiv == iParthia:
		if iEra == iMedieval:
			return "TXT_KEY_CIV_PARTHIA_SASSANID"

	elif iCiv == iSamanids:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_SAMANIDS_TAJIKISTAN"

	elif iCiv == iGokturks:
		if getColumn(iPlayer) >= 7:
			return "TXT_KEY_CIV_GOKTURKS_KYRGYZSTAN"

	elif iCiv == iGeorgia:
		if turn() <= year(1000):
			return "TXT_KEY_CIV_GEORGIA_ABKHAZIA"

	

	elif iCiv == iTunis:
		if bMonarchy:
			return "TXT_KEY_CIV_TUNIS_HAFSIDS"
		elif iEra >= iIndustrial:
			return "TXT_KEY_CIV_TUNIS_TUNISIA"


	elif iCiv == iPersia:

		if bResurrected and game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_PERSIA_SAFFARIDS"

		if year() < year(-550):
			return "TXT_KEY_CIV_PERSIA_MEDES"

			
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Lihu'e", "Honolulu", "Hilo"):
			return "TXT_KEY_CIV_POLYNESIA_HAWAII"
			
		if isCurrentCapital(iPlayer, "Aga'e"):
			return "TXT_KEY_CIV_POLYNESIA_SAMOA"
			
		if isCurrentCapital(iPlayer, "Alofi"):
			return "TXT_KEY_CIV_POLYNESIA_NIUE"
			
		return "TXT_KEY_CIV_POLYNESIA_TONGA"

	elif iCiv == iCelts:
		if player(iPlayer).getPeriod() == iPeriodInsularCelts:
			if capital in cities.region(rIreland):
				return "TXT_KEY_CIV_CELTS_IRELAND"
			
			if isCurrentCapital(iPlayer, "Cardiff", "Caernarfon"):
				return "TXT_KEY_CIV_CELTS_WALES"
			
			return "TXT_KEY_CIV_CELTS_GAELS"
		
		if capital in cities.region(rIberia):
			return "TXT_KEY_CIV_CELTS_CELTIBERIA"
		
		if capital in cities.regions(rBritain, rIreland):
			return "TXT_KEY_CIV_CELTS_BRITAIN"
		
		if cities.owner(iPlayer).count() == cities.owner(iPlayer).region(rFrance).count():
			return "TXT_KEY_CIV_CELTS_GAUL"
		
	elif iCiv == iDravidia:
		if getColumn(iPlayer) >= 12 or scenario() == i1700AD:
			return "TXT_KEY_CIV_DRAVIDIA_MYSORE"
			
		if getColumn(iPlayer) >= 10:
			return "TXT_KEY_CIV_DRAVIDIA_VIJAYANAGARA"
			
	elif iCiv == iEthiopia:
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUM"

	elif iCiv == iToltecs:
		return capital.getName()

	elif iCiv == iKushans:
		if not cities.regions(*lIndia):
			return "TXT_KEY_CIV_KUSHANS_TOCHARIAN"
			
	elif iCiv == iKorea:
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_CIV_KOREA_GOGURYEO"
				
		if iEra <= iMedieval:
			return "TXT_KEY_CIV_KOREA_GORYEO"
			
		return "TXT_KEY_CIV_KOREA_JOSEON"
		
	elif iCiv == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_BYZANTIUM_RUM"
	
		if not bEmpire:
			if isCurrentCapital(iPlayer, "Epidamnos", "Apollonia"):
				return "TXT_KEY_CIV_BYZANTIUM_EPIRUS"
			
			if isCurrentCapital(iPlayer, "Athenai"):
				return "TXT_KEY_CIV_BYZANTIUM_MOREA"
	
			if not isCurrentCapital(iPlayer, "Byzantion"):
				return capitalName(iPlayer)

		elif iCiv == iMalays:
			if iEra >= iGlobal:
				return short(iPlayer)
		
		if iReligion == iIslam:
			if capital in cities.rectangle(tMalaya):
				return "TXT_KEY_CIV_MALAYA_MALACCA"
			
			if capital in cities.rectangle(tKalimantan):
				return "TXT_KEY_CIV_MALAYA_BRUNEI"
			
			if capital in cities.rectangle(tSulawesi):
				return "TXT_KEY_CIV_MALAYA_GOWA"
			
			return "TXT_KEY_CIV_MALAYA_ACEH"
		
		if bEmpire:
			return "TXT_KEY_CIV_MALAYA_SRIVIJAYA"
		
		if capital in cities.region(tMalaya):
			return "TXT_KEY_CIV_MALAYA_SINGAPURA"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_MALAYA_PAGARUYUNG"
		
		return "TXT_KEY_CIV_MALAYA_MELAYU"
			
	elif iCiv == iNorse:
		if iEra >= iIndustrial and bEmpire and (not player(iSweden).isAlive() or team(iSweden).isVassal(iPlayer)):
			return "TXT_KEY_CIV_NORSE_SCANDINAVIA"

		if pPlayer.getPeriod() == -1:
			if not player(iSweden).isAlive() and capital in cities.birth(iSweden):
				return "TXT_KEY_CIV_NORSE_SWEDEN"
			
			if capital in cities.rectangle(tNorway):
				return "TXT_KEY_CIV_NORSE_NORWAY"
		
	elif iCiv == iTurks:
		if not player(iOttomans).isExisting() or master(iOttomans) == iPlayer:
			if not player(iGokturks).isExisting() or master(iGokturks) == iPlayer:
				if not player(iGhorids).isExisting() or master(iGhorids) == iPlayer:
					if not player(iTimurids).isExisting() or master(iTimurids) == iPlayer:
						if bEmpire:
							return "TXT_KEY_CIV_TURKS_PAN_TURKESTAN"
	
		if capital in plots.region(rAnatolia):
			return "TXT_KEY_CIV_TURKS_RUM"
		
		if capital in cities.regions(rTransoxiana):
			return "TXT_KEY_CIV_TURKS_KHWARAZMIAN"
			
		if iEra >= iRenaissance and not tPlayer.isAVassal():
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_UZBEKISTAN"
				
			return capitalName(iPlayer)

		# Added and removed by Aeons, emirate of "Seljuks" sounds odd.
		#return "TXT_KEY_CIV_TURKS_SELJUKS"

		
	#elif iCiv == iArabia:
	#	if bResurrected and getColumn(iPlayer) >= 13:
	#		return "TXT_KEY_CIV_ARABIA_SAUDI"
			
	elif iCiv == iKhmer:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_KHMER_CAMBODIA"

		if iEra >= iMedieval:
			return "TXT_KEY_CIV_KHMER_KAMBUJA"
		
		if getColumn(iPlayer) >= 6:
			return "TXT_KEY_CIV_KHMER_CHENLA"
		
		return "TXT_KEY_CIV_KHMER_FUNAN"
			
	elif iCiv == iMoors:	
		if isCurrentCapital(iPlayer, "Qurtubah"):
			return "TXT_KEY_CIV_MOORS_CORDOBA"
			
		return "TXT_KEY_CIV_MOORS_ANDALUSIA"

	elif iCiv == iGhorids:
		# around 1200, rule breaks down into "Emirate/Sultanate of X" realms
		if year() > year(dBirth[iMongols]) and cities.regions(lIndia).owner(iPlayer) > 0:
			return capitalName(iPlayer)
			
	elif iCiv == iJava:
		if iEra >= iIndustrial:
			if isControlled(iPlayer, plots.rectangle(tSumatra).without(plots.rectangle(tMalaya))) and isControlled(iPlayer, plots.rectangle(tKalimantan)):
				if civic.iSociety == iEgalitarianism:
					return "TXT_KEY_CIV_JAVA_NUSANTARA"
				
				return "TXT_KEY_CIV_JAVA_INDONESIA"

		if iReligion == iIslam:
			return "TXT_KEY_CIV_JAVA_DEMAK"
			
		if iEra <= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_JAVA_MAJAPAHIT"
		
		if getColumn(iPlayer) >= 8:
			return "TXT_KEY_CIV_JAVA_SINGHASARI"
		
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_JAVA_KEDIRI"
			
		if iEra == iClassical:
			return "TXT_KEY_CIV_JAVA_KALINGGA"
		
	elif iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
	
		bSpain = not player(iMoors).isExisting() or not player(iMoors).getCapitalCity() in plots.region(rIberia)
	
		if bSpain:
			if not player(iPortugal).isExisting() or not player(iPortugal).getCapitalCity() in plots.region(rIberia):
				return "TXT_KEY_CIV_SPAIN_IBERIA"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Tarragona", "Valencia", "Zaragoza"):
			return "TXT_KEY_CIV_SPAIN_ARAGON"

		if period(iCiv) == -1 and year() >= year(1050):
			return "TXT_KEY_CIV_SPAIN_LEON"
			
		if period(iCiv) == -1:
			return "TXT_KEY_CIV_SPAIN_ASTURIAS"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iCiv == iFrance:
		if iEra == iMedieval and not player(iHolyRome).isExisting():
			return "TXT_KEY_CIV_FRANCE_FRANCIA"
		if iEra == iClassical:
			return "TXT_KEY_CIV_FRANCE_FRANKS"
			
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 12 and 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iCiv == iHolyRome:
		if isCurrentCapital(iPlayer, "Buda", "Pest"):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARY"
	
		if not bEmpire:
			if year() < year(dBirth[iGermany]):
				return "TXT_KEY_CIV_HOLY_ROME_GERMANY"
			else:
				return "TXT_KEY_CIV_AUSTRIA_SHORT_DESC"

	elif iCiv == iBurma:
		if iEra >= iGlobal:
			if civic.iSociety == iTotalitarianism or civic.iTerritory == iIsolationism:
				return "TXT_KEY_CIV_BURMA_MYANMAR"
			
			return short(iPlayer)
		
		if iEra >= iIndustrial:
			if bEmpire:
				return "TXT_KEY_CIV_BURMA_KONBAUNG"
			
			return short(iPlayer)
		
		if iEra >= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_BURMA_TOUNGOO"
			
			if capital in cities.birth(iBurma).coastal():
				return "TXT_KEY_CIV_BURMA_HANTHAWADDY"
			
			return "TXT_KEY_CIV_BURMA_AVA"
		
		if bCityStates:
			return "TXT_KEY_CIV_BURMA_PYU"
		
		if capital in cities.birth(iBurma).coastal():
			return "TXT_KEY_CIV_BURMA_HANTHAWADDY"
		
		return "TXT_KEY_CIV_BURMA_BAGAN"

	elif iCiv == iRus:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_RUS_UKRAINE"
		
		if isCurrentCapital(iPlayer, "Drohiczyn", "Lviv", "Stanislaviv"):
			return "TXT_KEY_CIV_RUS_GALICIA_VOLHYNIA"
		
		if isCurrentCapital(iPlayer, "Vladimir", "Suzdal"):
			return "TXT_KEY_CIV_RUS_VLADIMIR_SUZDAL"
		
		return capitalName(iPlayer)
	
	elif iCiv == iSwahili:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_SWAHILI_TANZANIA"
		
		return capitalName(iPlayer)

	elif iCiv == iVietnam:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_VIETNAM_DAI_NAM"

	elif iCiv == iInca:
		if not bEmpire:
			return capitalName(iPlayer)
			
	elif iCiv == iItaly:
		if not bResurrected and not bEmpire and not bCityStates:
			if isCurrentCapital(iPlayer, "Florentia"):
				return "TXT_KEY_CIV_ITALY_TUSCANY"
				
			return capitalName(iPlayer)
		if cities.region(rItaly).any(lambda city: city.getOwner() != iPlayer):
			return "TXT_KEY_CIV_ITALY_SARDINIA_PIEDMONT"
	
	elif iCiv == iPortugal:
		if isControlled(iPlayer, plots.core(iMoors)):
			return "TXT_KEY_CIV_PORTUGAL_ALGARVE"
			
	elif iCiv == iRussia:
		if not (bEmpire and iEra >= iRenaissance) and not isControlled(iPlayer, plots.regions(rRuthenia, rPonticSteppe, rEuropeanArctic), 5):
			if not bCityStates and isCurrentCapital(iPlayer, "Moskva"):
				return "TXT_KEY_CIV_RUSSIA_MUSCOVY"
				
			if not tPlayer.isAVassal():
				return capitalName(iPlayer)
			
	elif iCiv == iThailand:
		if getColumn(iPlayer) < 10 and scenarioStartYear() < 1500:
			return "TXT_KEY_CIV_THAILAND_SUKHOTHAI"

		if getColumn(iPlayer) <= 11:
			return "TXT_KEY_CIV_THAILAND_AYUTTHAYA"

	elif iCiv == iTatars:
		if capital.getRegionID() == rVolga:
			return capitalName(iPlayer)
		
		if capital.getRegionID() == rPonticSteppe and capital.isCoastal(20):
			return "TXT_KEY_CIV_TATARS_CRIMEA"
			
		if bEmpire:
			return "TXT_KEY_CIV_TATARS_GOLDEN_HORDE"
		
		return "TXT_KEY_CIV_TATARS_GREAT_HORDE"
			
	elif iCiv == iNetherlands:
		if bCityStates:
			return short(iPlayer)
			
		if isCurrentCapital(iPlayer, "Bruges", "Antwerpen", "Gent", "Bruxelles"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIUM"
			
	elif iCiv == iManchuria:
		if player(iPlayer).getPeriod() == iPeriodQing:
			return "TXT_KEY_CIV_MANCHURIA_GREAT_QING"
		
		if bEmpire:
			return "TXT_KEY_CIV_MANCHURIA_GREAT_JIN"

	elif iCiv == iGermany:
		if getColumn(iPlayer) <= 15 and pPlayer.isExisting() and (not player(iHolyRome).isExisting() or not team(iHolyRome).isVassal(iPlayer)):
			return "TXT_KEY_CIV_GERMANY_PRUSSIA"

	elif iCiv == iSaudis:	
		if capital.isHolyCityByType(iIslam):
			if bEmpire and getColumn(iPlayer) >= 15:
				return "TXT_KEY_CIV_SAUDIS_HASHEMITE_ARABIA"
			
			return "TXT_KEY_CIV_SAUDIS_HEJAZ"
			
		if bEmpire and getColumn(iPlayer) >= 15:
			return "TXT_KEY_CIV_SAUDIS_SAUDI_ARABIA"
		
		if getColumn(iPlayer) >= 12:
			return "TXT_KEY_CIV_SAUDIS_NAJD"
		
		return "TXT_KEY_CIV_SAUDIS_DIRIYAH"
	
def adjective(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer):
		iMaster = master(iPlayer)
	
		sForeignAdjective = dForeignAdjectives[civ(iMaster)].get(iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return adjective(iMaster)
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	sDefaultInsertAdjective = dDefaultInsertAdjectives.get(iCiv)
	if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return player(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iRome:
		if player(iByzantium).isExisting(): return None

	if iCiv == iByzantium:
		if player(iRome).isExisting(): return None
		
	if iCiv in [iMoors, iEngland]: return None
	
	if iCiv == iInca and data.civs[iCiv].iResurrections > 0: return None
	
	if iCiv == iHolyRome and player(iPlayer).getPeriod() == -1: return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
		
	return player(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return player(iPlayer).getCivilizationAdjective(0)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or civic.iReligion == iFanaticism
	bResurrected = data.civs[iCiv].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iCiv].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	if iCiv == iSouthAfrica:
		if iNumCities <= 3 and location(capital) == location(plots.capital(iCiv)):
			return "TXT_KEY_CIV_SOUTH_AFRICA_CAPE"

	if iCiv == iMoors:
		if isCurrentCapital(iPlayer, "Al-Garnatah"):
			return "TXT_KEY_CIV_GRANADA_ADJECTIVE"
		if isCurrentCapital(iPlayer, "Al-Garnatah") and player(iMoors).getNumCities() == 1 and year() > year(1200):
			return "TXT_KEY_CIV_GRANADA_ADJECTIVE"

	elif iCiv == iSonghai:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_NIGER_ADJECTIVE"

	elif iCiv == iAdal:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ADAL_SOMALI"
		elif iEra >= iRenaissance:
			return "TXT_KEY_CIV_ADAL_HARARI"
		elif iEra <= iClassical:
			return "TXT_KEY_CIV_ADAL_IFAT"

	elif iCiv == iSomalia:
		if iEra == iRenaissance:
			return "TXT_KEY_CIV_SOMALIA_GELEDI"
		elif iEra == iMedieval:
			return "TXT_KEY_CIV_SOMALIA_AJURAN"
		elif iEra <= iClassical:
			return "TXT_KEY_CIV_SOMALIA_MOGADISHU"

	elif iCiv == iKatanga:
		if iEra >= iIndustrial:
			return
		if iAnarchyTurns > 5:
			return "TXT_KEY_CIV_KATANGA_CHOKWE"
		elif iAnarchyTurns > 3:
			return "TXT_KEY_CIV_KATANGA_LUNDA"
		elif iAnarchyTurns > 2:
			return "TXT_KEY_CIV_KATANGA_KUBAN"
		else:
			return "TXT_KEY_CIV_KATANGA_LUBAN"

	elif iCiv == iAshanti:
		if bResurrected and not player(iGhana).isExisting():
			return "TXT_KEY_CIV_GHANA_ADJECTIVE"

	elif iCiv == iBenin:
		if getColumn(iPlayer) <= 5:
			return "TXT_KEY_CIV_IGODOMIGODO_ADJECTIVE"

	elif iCiv == iKanemBornu:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_CHAD_ADJECTIVE"

	elif iCiv == iGhana:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_MAURITANIA_ADJECTIVE"

	elif iCiv == iMisr:
		if not bResurrected and year() <= year(1700):
			if getColumn(iPlayer) >= 13 or bCapitulated:
				return "TXT_KEY_CIV_MAMLUKS_EGYPTIAN"
			elif iReligion == iShia:
				return "TXT_KEY_CIV_MAMLUKS_FATIMID"
			elif getColumn(iPlayer) >= 10:
					return "TXT_KEY_CIV_MAMLUKS_MAMLUK"
			else:
				return "TXT_KEY_CIV_MAMLUKS_AYYUBID"

	elif iCiv == iSwahili:
		if iEra <= iIndustrial:
			return "TXT_KEY_CIV_KILWA_ADJECTIVE"

	elif iCiv == iYemen:
		if bMonarchy:
			if iReligion == iShia and getColumn(iPlayer) <= 10:
				return "TXT_KEY_CIV_YEMEN_SULAYHID"
			elif iReligion == iShia and getColumn(iPlayer) <= 14:
				return "TXT_KEY_CIV_YEMEN_QASIMID"
			elif getColumn(iPlayer) == 7:
				return "TXT_KEY_CIV_YEMEN_ZIYADID"
			elif getColumn(iPlayer) <= 9:
				return "TXT_KEY_CIV_YEMEN_ZURAYID"
			elif getColumn(iPlayer) == 10:
				return "TXT_KEY_CIV_YEMEN_RASULID"
			elif getColumn(iPlayer) <= 13:
				return "TXT_KEY_CIV_YEMEN_TAHIRID"

	elif iCiv == iOman:
		if getColumn(iPlayer) == 10:
				return "TXT_KEY_CIV_OMAN_HORMUZI"
		if iEra == iMedieval:
			return "TXT_KEY_CIV_OMAN_SOHARI"

	elif iCiv == iNubia:
		if iEra == iMedieval or iReligion == iOrthodoxy:
			if isCurrentCapital(iPlayer, "Para"):
				return "TXT_KEY_CIV_NUBIA_NOBATIAN"
			
			if isCurrentCapital(iPlayer, "Soba"):
				return "TXT_KEY_CIV_NUBIA_ALODIAN"

			return "TXT_KEY_CIV_NUBIA_MAKURIAN"
		if iEra <= iClassical:
			return "TXT_KEY_CIV_NUBIA_KUSHITE"

	elif iCiv == iHittites:
		if bMonarchy and not bEmpire:
			return capitalName(iPlayer)

	elif iCiv == iBuyids:
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_BUYIDS_FARSI"

	#elif iCiv == iKhazars:
	#	if bResurrected:
	#		return "TXT_KEY_CIV_TATARS_ADJECTIVE"

	elif iCiv == iMorocco:
 		if year() < year(1150):
 			return "TXT_KEY_CIV_MOROCCO_ALMORAVID"
 		elif year() < year(1250):
 			return "TXT_KEY_CIV_MOROCCO_ALMOHAD"
 		elif year() < year(1470):
 			return "TXT_KEY_CIV_MOROCCO_MARINID"
 		elif year() < year(1560):
 			return "TXT_KEY_CIV_MOROCCO_WATTASID"
 		elif getColumn(iPlayer) < 12:
 			return "TXT_KEY_CIV_MOROCCO_SAADI"

	elif iCiv == iEgypt:
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_CIV_EGYPT_COPTIC"
			
	elif iCiv == iIndia:
		if bMonarchy and not bCityStates and (iEra >= iMedieval or bEmpire):
			if iEra >= iRenaissance:
				return "TXT_KEY_CIV_INDIA_MARATHA"
			
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_INDIA_PALA"
			
			if iReligion == iBuddhism:
				return "TXT_KEY_CIV_INDIA_MAURYA"
			
			if iReligion == iHinduism:
				return "TXT_KEY_CIV_INDIA_GUPTA"

	elif iCiv == iMinoa:
		if iEra >= iClassical:
			return "TXT_KEY_CIV_MINOA_CRETAN"

	elif iCiv == iGermania:
		if capital in plots.region(rBritain):
			return "TXT_KEY_CIV_GERMANIA_ANGLO_SAXON"
	

	elif iCiv == iSumeria:
		if bEmpire:
			return "TXT_KEY_CIV_SUMERIA_AKKADIAN"
		if turn() >= year(-2000):
			return "TXT_KEY_CIV_SUMERIA_SEALANDER"

	elif iCiv == iAssyria:
		if bEmpire:
			if iEra >= iClassical:
				return "TXT_KEY_CIV_ASSYRIA_NEO"
			
			if getColumn(iPlayer) >= 3:
				return "TXT_KEY_CIV_ASSYRIA_MIDDLE"
			
			return "TXT_KEY_CIV_ASSYRIA_OLD"



	elif iCiv == iJudah:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_JUDAH_PALESTINIAN"
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_CIV_JUDAH_JERUSALEMITE"
		if iReligion == iJudaism:
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_JUDAH_ISRAELI"

	elif iCiv == iJerusalem:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_JERUSALEM_PALESTINIAN"
		if iReligion == iJudaism:
				return "TXT_KEY_CIV_JERUSALEM_ISRAELI"

	elif iCiv == iGoths:
		if capital in plots.regions(rIberia):
			return "TXT_KEY_CIV_GOTHS_VISIGOTHIC"
	
		if capital in plots.region(rItaly):
			return "TXT_KEY_CIV_GOTHS_OSTROGOTHIC"

	
	elif iCiv == iGreece:
		if player(iGreece).getPeriod() == -1 and not controlsCity(iPlayer, location(plots.capital(iGreece))):
			return "TXT_KEY_CIV_THESSALLONIKI_ADJECTIVE"

	elif iCiv == iNumidia:
		if not tPlayer.isHasTech(iCurrency):
			return "TXT_KEY_CIV_NUMIDIA_MASSAESYLIAN"
		elif iEra >= iIndustrial and not bMonarchy:
			return "TXT_KEY_CIV_NUMIDIA_ALGERIAN"
		elif iReligion == iIslam or iReligion == iShia:
			return "TXT_KEY_CIV_NUMIDIA_ZAYYANID"


	elif iCiv == iParthia:
		if iEra == iMedieval:
			return "TXT_KEY_CIV_PARTHIA_SASSANIAN"

	elif iCiv == iSamanids:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_SAMANIDS_TAJIKISTANI"
	
	elif iCiv == iGokturks:
		if getColumn(iPlayer) >= 7:
			return "TXT_KEY_CIV_GOKTURKS_KYRGYZ"

	elif iCiv == iGeorgia:
		if turn() <= year(1000):
			return "TXT_KEY_CIV_GEORGIA_ABKHAZIAN"

	elif iCiv == iTunis:
		if bMonarchy:
			return "TXT_KEY_CIV_TUNIS_HAFSID"

			
	elif iCiv == iChina:
		if bMonarchy:
			if iEra >= iMedieval:
				if tPlayer.isHasTech(iPaper) and tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_CHINA_SONG"
			
				if year() >= year(600):
					return "TXT_KEY_CIV_CHINA_TANG"
				
				return "TXT_KEY_CIV_CHINA_SUI"
			
			if iEra == iClassical:
				if year() >= year(0):
					return "TXT_KEY_CIV_CHINA_HAN"
				
				return "TXT_KEY_CIV_CHINA_QIN"
			
			return "TXT_KEY_CIV_CHINA_ZHOU"
			
	elif iCiv == iBabylonia:
		if bEmpire:
			if iEra >= iClassical:
				return "TXT_KEY_CIV_BABYLONIA_NEO"
			
			if getColumn(iPlayer) >= 3:
				return "TXT_KEY_CIV_BABYLONIA_KASSITE"
		
		if bCityStates and not bEmpire:
			return "TXT_KEY_CIV_BABYLONIA_MESOPOTAMIAN"
			
			
	elif iCiv == iIran:
		if bEmpire:
			if iEra >= iGlobal:
				return "TXT_KEY_CIV_PERSIA_PAHLAVI"
		
			if getColumn(iPlayer) >= 12:
				return "TXT_KEY_CIV_PERSIA_QAJAR"
		
			return "TXT_KEY_CIV_PERSIA_SAFAVID"
		
	elif iCiv == iPersia:
		if iEra >= iGlobal:
				return "TXT_KEY_CIV_PERSIA_PAHLAVI"
			
		if getColumn(iPlayer) >= 12:
				return "TXT_KEY_CIV_PERSIA_QAJAR"
		
		if iEra >= iRenaissance:
				return "TXT_KEY_CIV_PERSIA_SAFAVID"

		if bResurrected and game.isReligionFounded(iIslam): 
			return "TXT_KEY_CIV_PERSIA_SAFFARID"

		if year() < year(-550):
			return "TXT_KEY_CIV_PERSIA_MEDIAN"
	
		if bEmpire:
			if iEra >= iClassical:				
				if getColumn(iPlayer) < 6:
					return "TXT_KEY_CIV_PERSIA_ACHAEMENID"

	
				
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Manu'a"):
			return "TXT_KEY_CIV_POLYNESIA_TUI_MANUA"
			
		return "TXT_KEY_CIV_POLYNESIA_TUI_TONGA"

	elif iCiv == iCelts:
		if player(iPlayer).getPeriod() == iPeriodInsularCelts:
			if capital in cities.region(rIreland):
				return "TXT_KEY_CIV_CELTS_IRISH"
			
			if isCurrentCapital(iPlayer, "Cardiff", "Caernarfon"):
				return "TXT_KEY_CIV_CELTS_WELSH"
			
			return "TXT_KEY_CIV_CELTS_GAELIC"
		
		if capital in cities.region(rIberia):
			return "TXT_KEY_CIV_CELTS_CELTIBERIAN"
		
		if capital in cities.regions(rBritain, rIreland):
			return "TXT_KEY_CIV_CELTS_BRITTONIC"
		
		if cities.owner(iPlayer).count() == cities.owner(iPlayer).region(rFrance).count():
			return "TXT_KEY_CIV_CELTS_GALLIC"
		
	elif iCiv == iRome:
		if player(iByzantium).isExisting() and not team(iByzantium).isVassal(team(iCiv).getID()):
			return "TXT_KEY_CIV_ROME_WESTERN"
			
	elif iCiv == iDravidia:
		if iReligion == iIslam:
			if iEra in [iMedieval, iRenaissance]:
				return "TXT_KEY_CIV_DRAVIDIA_BAHMANI"
	
		if iEra <= iMedieval:
			if isCurrentCapital(iPlayer, "Madurai", "Vizhinjam", "Yapanaya"):
				return "TXT_KEY_CIV_DRAVIDIA_PANDYAN"
				
			if isCurrentCapital(iPlayer, "Desinganadu", "Kallikkottai", "Mangalapuram"):
				return "TXT_KEY_CIV_DRAVIDIA_CHERA"
				
			return "TXT_KEY_CIV_DRAVIDIA_CHOLA"
			
	elif iCiv == iEthiopia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_ETHIOPIA_ADAL"
			
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUMITE"

	elif iCiv == iToltecs:
		if iEra == iAncient:
			return capital.getName()
			
	elif iCiv == iByzantium:
		iMediterraneanHegemon = data.iMediterraneanHegemon
		if player(iMediterraneanHegemon).isExisting() and player(iMediterraneanHegemon).getNumCities() > 0 and not team(iMediterraneanHegemon).isVassal(team(iCiv).getID()):
			return infos.civ(iMediterraneanHegemon).getAdjective(0)

		if bEmpire and controlsCity(iPlayer, location(plots.capital(iMediterraneanHegemon))):
			return infos.civ(iMediterraneanHegemon).getAdjective(0)
			
	elif iCiv == iTurks:
		if not player(iOttomans).isExisting() or master(iOttomans) == iPlayer:
			if not player(iGokturks).isExisting() or master(iGokturks) == iPlayer:
				if not player(iGhorids).isExisting() or master(iGhorids) == iPlayer:
					if not player(iTimurids).isExisting() or master(iTimurids) == iPlayer:
						if bEmpire:
							return "TXT_KEY_CIV_TURKS_PAN_TURKIC"


		if period(iCiv) == iPeriodUzbeks:
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_SHAYBANID"

			return "TXT_KEY_CIV_TURKS_UZBEK"
		
		if period(iCiv) == -1:
			#if cities.owner(iPlayer).all(lambda city: city.getX() < iTurkicEastWestBorder):
			#	return "TXT_KEY_CIV_TURKS_WESTERN_TURKIC"
			#
			#if cities.owner(iPlayer).all(lambda city: city.getY() >= iTurkicEastWestBorder):
			#	return "TXT_KEY_CIV_TURKS_EASTERN_TURKIC"

			return "TXT_KEY_CIV_TURKS_SELJUK"

	elif iCiv == iMalays:
		if iEra >= iGlobal:
			return civAdjective(iPlayer)
		
		if iReligion == iIslam:
			if capital in cities.rectangle(tMalaya):
				return "TXT_KEY_CIV_MALAYA_MALACCAN"
			
			if capital in cities.rectangle(tKalimantan):
				return "TXT_KEY_CIV_MALAYA_BRUNEIAN"
			
			if capital in cities.rectangle(tSulawesi):
				return "TXT_KEY_CIV_MALAYA_GOWAN"
			
			return "TXT_KEY_CIV_MALAYA_ACEHNESE"
		
		if bEmpire:
			return "TXT_KEY_CIV_MALAYA_SRIVIJAYAN"
		
		if capital in cities.region(tMalaya):
			return "TXT_KEY_CIV_MALAYA_SINGAPURAN"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CIV_MALAYA_PAGARUYUNG"
		
		return "TXT_KEY_CIV_MALAYA_MELAYU"

	elif iCiv == iNorse:
		if iEra >= iIndustrial and bEmpire and (not player(iSweden).isAlive() or team(iSweden).isVassal(iPlayer)):
			return "TXT_KEY_CIV_NORSE_SCANDINAVIAN"

	elif iCiv == iArabia:
		if (bTheocracy or controlsHolyCity(iPlayer, iIslam)) and iReligion == iIslam and year() <= year(1700):
			if not bEmpire and year() <= year(700):
				return "TXT_KEY_CIV_ARABIA_RASHIDUN"
				
			if bEmpire and year() >= year(750):
				return "TXT_KEY_CIV_ARABIA_ABBASID"
			
			if bEmpire:	
				return "TXT_KEY_CIV_ARABIA_UMMAYAD"
		
	elif iCiv == iJava:
		if iEra >= iIndustrial:
			if isControlled(iPlayer, plots.rectangle(tSumatra).without(plots.rectangle(tMalaya))) and isControlled(iPlayer, plots.rectangle(tKalimantan)):
				if civic.iSociety == iEgalitarianism:
					return "TXT_KEY_CIV_JAVA_NUSANTARAN"
					
				return "TXT_KEY_CIV_JAVA_INDONESIAN"
		
		return "TXT_KEY_CIV_JAVA_JAVAN"

	elif iCiv == iSpain:
		bSpain = not player(iMoors).isExisting() or not player(iMoors).getCapitalCity() in plots.region(rIberia)
	
		if bSpain:
			if not player(iPortugal).isExisting() or master(iPortugal) == iPlayer or not cities.owner(iPortugal).region(rIberia):
				return "TXT_KEY_CIV_SPAIN_IBERIAN"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Tarragon", "Valencia", "Zaragoza"):
			return "TXT_KEY_CIV_SPAIN_ARAGONESE"
		
		if period(iCiv) == -1 and year() >= year(1050):
			return "TXT_KEY_CIV_SPAIN_LEONESE"		

		if period(iCiv) == -1: return "TXT_KEY_CIV_SPAIN_ASTURIAN"
	
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILIAN"
			
	elif iCiv == iFrance:
		if iEra <= iMedieval and not player(iHolyRome).isExisting():
			return "TXT_KEY_CIV_FRANCE_FRANKISH"
	
	elif iCiv == iKhmer:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_KHMER_CAMBODIAN"
		
		if iEra >= iMedieval or bEmpire:
			return civAdjective(iPlayer)
		
		if getColumn(iPlayer) >= 6:
			return "TXT_KEY_CIV_KHMER_CHENLA"
		
		return "TXT_KEY_CIV_KHMER_FUNANESE"
			
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 12 and 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iCiv == iHolyRome:
		if isCurrentCapital(iPlayer, "Buda", "Pest"):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARIAN"
	
		if player(iGermany).isExisting() and civic.iLegitimacy == iConstitution:
			return "TXT_KEY_CIV_HOLY_ROME_AUSTRO_HUNGARIAN"
			
		iVassals = 0
		for iLoopCiv in dCivGroups[iCivGroupEurope]:
			iLoopPlayer = slot(iLoopCiv)
			if iLoopPlayer >= 0 and master(iLoopPlayer) == iPlayer:
				iVassals += 1
				
		if iVassals >= 2:
			return "TXT_KEY_CIV_HOLY_ROME_HABSBURG"
			
		if not bEmpire and year() < year(dBirth[iGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMAN"

	elif iCiv == iBurma:
		if iEra >= iGlobal:
			return civAdjective(iPlayer)
		if iEra >= iIndustrial and not bEmpire:
			return civAdjective(iPlayer)
			
	elif iCiv == iRus:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_RUS_UKRAINIAN"
		
		if isCurrentCapital(iPlayer, "Drohiczyn", "Lviv", "Stanislaviv"):
			return "TXT_KEY_CIV_RUS_GALICIAN"
		
		if isCurrentCapital(iPlayer, "Kyiv"):
			return "TXT_KEY_CIV_RUS_KIEVAN"
		
		if isCurrentCapital(iPlayer, "Moskva"):
			return "TXT_KEY_CIV_RUS_MUSCOVITE"
		
		return capitalName(iPlayer)
	
	elif iCiv == iSwahili:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_SWAHILI_TANZANIAN"
				
	elif iCiv == iItaly:
		if bCityStates and bWar:
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_LOMBARD"
				
	elif iCiv == iMongols:
		if not bEmpire and iEra <= iRenaissance:
			if capital.getRegionID() == rPersia:
				return "TXT_KEY_CIV_MONGOLIA_HULAGU"
				
			if location(capital) != location(plots.capital(iMongols)) and capital.getRegionID() in [rCentralAsianSteppe, rTarimBasin, rKhorasan]:
				return "TXT_KEY_CIV_MONGOLIA_CHAGATAI"
				
			if 2 * cities.regions(rNorthChina, rSouthChina).owner(iPlayer).count() >= cities.regions(rNorthChina, rSouthChina).count():
				return "TXT_KEY_CIV_MONGOLIA_YUAN"

		if bResurrected and year() <= year(1750):
			return "TXT_KEY_CIV_MONGOLIA_NORTHERN_YUAN"
				
		if bMonarchy:
			return "TXT_KEY_CIV_MONGOLIA_MONGOL"
	
	elif iCiv == iGhorids:
		if turn() <= year(1150) and period(iCiv) == -1:
			return "TXT_KEY_CIV_GHAZNAVIDS_ADJECTIVE"
				
	elif iCiv == iTatars:
		if capital.getRegionID() in [rUrals, rSiberia]:
			return "TXT_KEY_CIV_TATARS_SIBIR"
		
		elif capital.getRegionID() == rPonticSteppe and capital.isCoastal(20):
			return "TXT_KEY_CIV_TATARS_CRIMEAN"

	elif iCiv == iOttomans:
		return "TXT_KEY_CIV_OTTOMANS_OTTOMAN"
			
	elif iCiv == iNetherlands:
		if isCurrentCapital(iPlayer, "Bruges", "Antwerpen", "Gent", "Bruxelles"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIAN"
			
	elif iCiv == iGermany:
		if getColumn(iPlayer) <= 15 and player(iHolyRome).isExisting() and not team(iHolyRome).isVassal(iPlayer):
			return "TXT_KEY_CIV_GERMANY_PRUSSIAN"
	
### Title methods ###

def title(iPlayer):
	if isCapitulated(iPlayer):
		sVassalTitle = vassalTitle(iPlayer, master(iPlayer))
		if sVassalTitle: return sVassalTitle

	if isCommunist(iPlayer):
		sCommunistTitle = communistTitle(iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iPlayer):
		sFascistTitle = fascistTitle(iPlayer)
		if sFascistTitle: return sFascistTitle
		
	if isRepublic(iPlayer):
		sRepublicTitle = republicTitle(iPlayer)
		if sRepublicTitle: return sRepublicTitle

	# don't need to check for islam, the function will do this
	sIslamicTitle = islamicTitle(iPlayer)
	if sIslamicTitle: return sIslamicTitle
		
	sSpecificTitle = specificTitle(iPlayer)
	if sSpecificTitle: return sSpecificTitle
	
	return defaultTitle(iPlayer)

def islamicTitle(iPlayer):
	pPlayer = player(iPlayer)
	civic = civics(iPlayer)
	iCiv = civ(iPlayer)
	iReligion = pPlayer.getStateReligion()
	bEmpire = isEmpire(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or (civic.iGovernment in [iRepublic, iElective] and civic.iReligion == iFanaticism)

	# some civs have their own nomenclature, like Shahdom for Iran/Persia
	if iCiv in [iIran, iPersia, iOttomans, iMongols, iTimurids, iKhazars, iMali, iKanemBornu, iGhana, iSonghai, iGhorids, iBuyids, iSamanids, iOman]:
		return

	if iReligion == iIslam or iReligion == iShia:
		if iCiv in [iAssyria, iMisr, iArabia, iTunis, iNumidia, iTurks] or (iCiv == iMorocco and getColumn(iPlayer) < 12):
			if bTheocracy and bEmpire or iCiv == iArabia:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
			if bEmpire:
				return "TXT_KEY_SULTANATE_ADJECTIVE"
			elif bTheocracy:
				return "TXT_KEY_IMAMATE_ADJECTIVE"
			else:
				return "TXT_KEY_EMIRATE_ADJECTIVE"
		elif iCiv in [iFunj, iYemen]:	# Non Empire requiring civs
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
			else:
				return "TXT_KEY_SULTANATE_ADJECTIVE"
		elif iCiv in [iHausa]:	# No Sultanate title for Hausa - only Caliphate
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
		elif iCiv in [iSomalia, iAdal, iSwahili]:	# Non Empire requiring civs
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_NAME"
			else:
				return "TXT_KEY_SULTANATE_NAME"
		else:
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_OF"
			if bEmpire:
				return "TXT_KEY_SULTANATE_OF"
			elif bTheocracy:
				return "TXT_KEY_IMAMATE_OF"
			else:
				return "TXT_KEY_EMIRATE_OF"
	
def vassalTitle(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if isCommunist(iMaster):
		sCommunistTitle = dCommunistVassalTitles[iMasterCiv].get(iCiv)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = dCommunistVassalTitlesGeneric.get(iMasterCiv)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = dFascistVassalTitles[iMasterCiv].get(iCiv)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = dFascistVassalTitlesGeneric.get(iMasterCiv)
		if sFascistTitle: return sFascistTitle
				
	if player(iMaster).getPeriod() == iPeriodAustria and iCiv in [iPoland, iRus]:
		return "TXT_KEY_CIV_AUSTRIAN_POLAND"
		
	if iMasterCiv == iEngland and iCiv == iTimurids:
		if not player(iIndia).isExisting():
			return dSpecificVassalTitles[iEngland][iIndia]
	
	if iMasterCiv == iEgypt and player(iMasterCiv).getStateReligion() == iIslam:
		return dMasterTitles[iArabia]#
	
	if iMasterCiv == iMongols and iCiv == iRussia:
		if not player(iRus).isExisting():
			return dSpecificVassalTitles[iMongols][iRus]

	sSpecificTitle = dSpecificVassalTitles[iMasterCiv].get(iCiv)
	if sSpecificTitle: return sSpecificTitle

	sMasterTitle = dMasterTitles.get(iMasterCiv)
	if sMasterTitle: return sMasterTitle

	# if no specific title and master is islamic, use the generic "emirate of"
	if player(iMasterCiv).getStateReligion() == iIslam or player(iMasterCiv).getStateReligion() == iShia:
		return dMasterTitles[iArabia]

	if iCiv in lColonies and iMasterCiv not in lColonies:
		return "TXT_KEY_COLONY_OF"

	if player(iMasterCiv).getCurrentEra() <= iClassical:
		return "TXT_KEY_CLIENT_KINGDOM"

	if player(iMasterCiv).getCurrentEra() <= iRenaissance and iMasterCiv in dCivGroups[iCivGroupEurope]:
		return "TXT_KEY_DUCHY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iVietnam and player(iPlayer).getCurrentEra() <= iGlobal:
		return "TXT_KEY_CIV_VIETNAM_DEMOCRATIC_REPUBLIC"

	if iCiv in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iCiv in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iCiv in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iCiv in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if iCiv == iCelts and pPlayer.getPeriod() == iPeriodInsularCelts and pPlayer.getCurrentEra() <= iIndustrial:
		return "TXT_KEY_CIV_CELTS_FREE_STATE"

	if iCiv == iHolyRome and pPlayer.getPeriod() == -1:
		return "TXT_KEY_CIV_HOLY_ROME_CONFEDERATION"
	
	if iCiv == iPoland:
		if pPlayer.getCurrentEra() <= iIndustrial:
			return key(iPlayer, "COMMONWEALTH")
	
	if iCiv == iEngland:
		iEra = pPlayer.getCurrentEra()
		if isEmpire(iPlayer) and iEra == iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	if iCiv == iMisr:
		if isControlled(iPlayer, plots.regions(rLevant, rArabia)):
			return "TXT_KEY_CIV_MISR_UNITED_ARAB_STATES"
		
		if isControlled(iPlayer, plots.regions(rLevant)):
			return "TXT_KEY_CIV_MISR_UNITED_ARAB_REPUBLIC"

	if iCiv == iSaudis:
		if isControlled(iPlayer, plots.regions(rLevant, rEgypt)):
			return "TXT_KEY_CIV_SAUDIS_UNITED_ARAB_STATES"
		
		if isControlled(iPlayer, plots.region(rLevant)):
			return "TXT_KEY_CIV_SAUDIS_UNITED_ARAB_REPUBLIC"

	if iCiv == iAmerica:
		if civics(iPlayer).iSociety in [iManorialism, iSlavery]:
			return key(iPlayer, "CSA")
			
	if iCiv == iColombia:
		if isControlled(iPlayer, plots.regions(rNewGranada, rAndes)):
			return "TXT_KEY_CIV_COLOMBIA_FEDERATION_ANDES"
			
	if pPlayer.getStateReligion() == iIslam:
		if iCiv in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"

		if iCiv == iOttomans: return key(iPlayer, "ISLAMIC_REPUBLIC")
		
	if iCiv in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iCiv in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or (civic.iGovernment in [iRepublic, iElective] and civic.iReligion == iFanaticism)
	bResurrected = data.civs[iCiv].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iCiv].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))

	if iCiv == iZimbabwe:
		if period(iCiv) != -1:
			return "TXT_KEY_EMPIRE_ADJECTIVE"

	if iCiv == iHausa:
		if period(iCiv) == -1 and bCityStates:
			return "TXT_KEY_CIV_HAUSA_SEVEN_KINGDOMS"

	if iCiv == iEgypt:
		if bResurrected or scenario() >= i600AD:
			if iReligion == iIslam:
				if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
				return "TXT_KEY_SULTANATE_ADJECTIVE"
			return "TXT_KEY_KINGDOM_ADJECTIVE"
			
		if player(iPlayer).getPeriod() == iPeriodPtolemaicEgypt or slot(iMacedon) in lPreviousOwners:
			return "TXT_KEY_CIV_EGYPT_PTOLEMAIC"
			
		if bCityStates and not bResurrected:
			return "TXT_KEY_CIV_EGYPT_NOMES"
		
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
		
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_CIV_EGYPT_COPTIC"
				
		if iEra == iAncient:
			if iAnarchyTurns == 0: return "TXT_KEY_CIV_EGYPT_OLD_KINGDOM"
			if iAnarchyTurns <= turns(1): return "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM"
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
		
		if iEra == iClassical:
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"

	#elif iCiv == iKhazars:
	#	if bResurrected:
	#		return "TXT_KEY_CIV_GOLDEN_HORDE"

	elif iCiv == iZulu:
		if year() <= year(1816):
			return "TXT_KEY_CIV_ZULU_MTETWA"
		if period(iCiv) == iPeriodSouthAfricaUnion:
			return "TXT_KEY_CIV_ZULU_EMPIRE"

	elif iCiv == iBoers:
		if period(iCiv) == iPeriodSouthAfricaUnion:
			return "TXT_KEY_CIV_BOERS_EMPIRE"
		elif isControlled(iPlayer, plots.regions(rCape), 3):
			return "TXT_KEY_CIV_BOERS_TRANSVAAL"
		elif isControlled(iPlayer, plots.regions(rCape), 2):
			return "TXT_KEY_CIV_BOERS_ORANGE"

	elif iCiv == iSouthAfrica:
		if period(iCiv) == -1 and team(iSouthAfrica).isAVassal():
			return "TXT_KEY_CIV_ENGLISH_SOUTH_AFRICA"
		#if bEmpire and bCapitulated:
		#	return "TXT_KEY_CIV_SOUTH_AFRICA_EMPIRE"
		if iNumCities >= 4:
			return "TXT_KEY_CIV_SOUTH_AFRICA_UNION_OF"

			
	elif iCiv == iIndia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CONFEDERACY_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_INDIA_GANA_SANGHAS"
		
		if iEra <= iClassical:
			return "TXT_KEY_CIV_INDIA_MAHAJANAPADAS"

	elif iCiv == iMinoa:	
		if bEmpire:
			return "TXT_KEY_CIV_MINOA_DORIC_EMPIRE"
		if iEra >= iMedieval and civic.iGovernment == iDespotism:
			return "TXT_KEY_CIV_MINOA_DESPOTATE"
		if civic.iGovernment == iRepublic:
			return "TXT_KEY_CIV_MINOA_CITY_STATES"

	elif iCiv == iBuyids:	
		if civic.iGovernment == iElective:
			return "TXT_KEY_CIV_BUYIDS_EMIRATE"

	elif iCiv == iSumeria:	
		if iEra >= iClassical and bEmpire:
			return "TXT_KEY_CIV_SUMERIA_NEOEMPIRE"
		if bEmpire:
			return "TXT_KEY_CIV_SUMERIA_EMPIRE"

	elif iCiv == iElam:	
		if bEmpire:
			return "TXT_KEY_CIV_ELAM_EMPIRE"

	elif iCiv == iMacedon:	
		if bEmpire:
			return "TXT_KEY_CIV_MACEDON_EMPIRE"

	elif iCiv == iSamanids:	
		if bEmpire:
			return "TXT_KEY_CIV_SAMANIDS_EMPIRE"

	elif iCiv == iMycenae:	
		if bEmpire:
			return "TXT_KEY_CIV_MYCENAE_EMPIRE"

	elif iCiv == iSparta:	
		if bEmpire:
			return "TXT_KEY_CIV_SPARTA_EMPIRE"
		if iNumCities >= 2:
			return "TXT_KEY_CIV_SPARTA_LEAGUE"
		if not period(iCiv) == -1: 
		    return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iGoths:
		if bEmpire:
			return "TXT_KEY_CIV_GOTHS_EMPIRE"
		if iEra >=  iMedieval or scenario() == i600AD:
			return "TXT_KEY_CIV_GOTHS_KINGDOM"

	elif iCiv == iHuns:
		if bEmpire:
			return "TXT_KEY_CIV_HUNS_EMPIRE"

	elif iCiv == iNumidia:
		if bEmpire:
			return "TXT_KEY_CIV_NUMIDIA_EMPIRE"

	elif iCiv == iVandals:
		if capital in plots.regions(rMaghreb):
			return "TXT_KEY_CIV_VANDALS_KINGDOM"

	elif iCiv == iArmenia:
		if bEmpire:
			return "TXT_KEY_CIV_ARMENIA_EMPIRE"
		if bResurrected:
			return "TXT_KEY_CIV_ARMENIA_BAGRATID"

	elif iCiv == iParthia:
		if bEmpire:
			return "TXT_KEY_CIV_PARTHIA_EMPIRE"


	elif iCiv == iScythia:
		if capital in plots.regions(rPonticSteppe):
			return "TXT_KEY_CIV_SCYTHIA_PONTIC_KINGDOM"
		if bEmpire:
			return "TXT_KEY_CIV_SCYTHIA_EMPIRE"
		if iEra >= iMedieval:
			return "TXT_KEY_CIV_SCYTHIA_KINGDOM"

	elif iCiv == iMisr:
		if iReligion == iIslam:
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			if iEra >= iIndustrial:
				return "TXT_KEY_SULTANATE_OF"
			
			if not tPlayer.isHasTech(iGunpowder) and controlsHolyCity(iPlayer, iIslam):
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
			return "TXT_KEY_SULTANATE_ADJECTIVE"
		
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_KINGDOM_ADJECTIVE"
		
		return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iBuganda:
		if not period(iCiv) == -1: 
		    return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iTunis:
		if iReligion in lChristianity:
			return "TXT_KEY_CIV_TUNIS_KINGDOM"
		elif bEmpire and bTheocracy: 
			return "TXT_KEY_CIV_TUNIS_CALIPHATE"
		elif bEmpire and bMonarchy:
			return "TXT_KEY_CIV_TUNIS_EMPIRE"

	elif iCiv == iYemen:
		if bEmpire and bTheocracy:
			return "TXT_KEY_CIV_YEMEN_CALIPHATE"
		elif bEmpire:
			return "TXT_KEY_CIV_YEMEN_EMPIRE"
		elif bMonarchy:
			if iReligion == iShia and getColumn(iPlayer) <= 11:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"
			elif getColumn(iPlayer) == 7:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"
			elif getColumn(iPlayer) <= 9:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"
			elif getColumn(iPlayer) == 10:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"
			elif getColumn(iPlayer) == 11:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"
			elif getColumn(iPlayer) <= 14:
				return "TXT_KEY_CIV_YEMEN_DYNASTIC_SULTAN"


	elif iCiv == iOman:
		if  bTheocracy:
			return "TXT_KEY_CIV_OMAN_IMAMATE"
		elif bEmpire and period(iCiv) == -1:
			return "TXT_KEY_CIV_OMAN_EMPIRE"
		else:
			return "TXT_KEY_SULTANATE_OF"



	elif iCiv == iJudah:	
		if iReligion == iIslam: 
				return "TXT_KEY_SULTANATE_ADJECTIVE"
		if iReligion == iCatholicism:
			if bTheocracy:
				return "TXT_KEY_CIV_JUDAH_HOLYKINGDOM"

	elif iCiv == iJerusalem:	
		if bTheocracy:
			return "TXT_KEY_CIV_JERUSALEM_HOLYKINGDOM"
		if capital in plots.region(rEgypt):
			return "TXT_KEY_CIV_JERUSALEM_COPTIC"

	elif iCiv == iGeorgia:	
		if bEmpire:
			return "TXT_KEY_CIV_GEORGIA_EMPIRE"

	elif iCiv == iGhorids:
		if not period(iCiv) == -1: 
			return "TXT_KEY_CIV_DELHI_SULTANATE"

	elif iCiv == iGermania:	
		if bEmpire:
			return "TXT_KEY_CIV_GERMANIA_EMPIRE"
		if civic.iGovernment == iElective:
			return "TXT_KEY_CIV_GERMANIA_HIGH_ELECTIVE"
		if iEra == iMedieval:
			return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iGokturks:	
		if bEmpire:
			return "TXT_KEY_CIV_GOKTURKS_EMPIRE"

			
	elif iCiv == iChina:
		if bEmpire:
			if iEra >= iIndustrial or scenario() == i1700AD:
				return "TXT_KEY_EMPIRE_OF"
			
			if iEra == iRenaissance and year() >= year(1400):
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iBabylonia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
		if bEmpire and iEra > iAncient:
			return "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE"
	
	elif iCiv == iAssyria:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"

	elif iCiv == iNubia:
		if bEmpire:
			if iEra <= iMedieval:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if iReligion == iIslam:
			if iEra >= iIndustrial and civic.iReligion == iFanaticism:
				return "TXT_KEY_CIV_NUBIA_MAHDIYYA"
			
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
	elif iCiv == iHittites:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iGreece:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
		if bCityStates and player(iPlayer).getPeriod() == -1:				
			if bWar:
				return "TXT_KEY_CIV_GREECE_LEAGUE"
				
			return "TXT_KEY_GREECE_CITY_STATE_OF"
			
	elif iCiv == iPersia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iPhoenicia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Lihu'e", "Honolulu", "Hilo"):
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iCelts:
		if player(iPlayer).getPeriod() == iPeriodInsularCelts:
			if capital in cities.region(rIreland):
				return "TXT_KEY_KINGDOM_OF"
			
			if isCurrentCapital(iPlayer, "Cardiff", "Caernarfon"):
				return "TXT_KEY_KINGDOM_OF"
			
			return "TXT_KEY_KINGDOM_ADJECTIVE"

	elif iCiv == iRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_REPUBLIC_ADJECTIVE"
			
	elif iCiv == iColombia:
		if bEmpire:
			if isControlled(iPlayer, plots.regions(rNewGranada, rAndes)):
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE_ANDES"
		
			return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iCiv == iJapan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
		if civic.iLegitimacy == iBureaucracy:
			return "TXT_KEY_EMPIRE_OF"
			
		if iEra >= iIndustrial:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iCiv == iDravidia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if getColumn(iPlayer) >= 10:
			if bEmpire:
				return "TXT_KEY_EMPIRE_NAME"
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iEthiopia:
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
	
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"

	elif iCiv == iToltecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if bCityStates:
			return "TXT_KEY_TOLTECS_ALTEPETL"
			
		if iEra == iAncient:
			return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iKushans:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
	elif iCiv == iKorea:
		if iEra >= iIndustrial:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
		if bCityStates:
			return "TXT_KEY_CIV_KOREA_SAMHAN"
				
		if iReligion >= 0:
			return "TXT_KEY_KINGDOM_OF"
			
	elif iCiv == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if not bEmpire and location(capital) != location(plots.capital(iCiv)):
			if capital.getRegionID() == rAnatolia:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_CIV_BYZANTIUM_DESPOTATE"

		iMediterraneanHegemon = data.iMediterraneanHegemon
		if player(iMediterraneanHegemon).isExisting() and player(iMediterraneanHegemon).getNumCities() > 0 and not team(iMediterraneanHegemon).isVassal(team(iCiv).getID()):
			if player(iByzantium).getPeriod() == -1:
				return "TXT_KEY_CIV_BYZANTIUM_EASTERN_EMPIRE"
			if player(iByzantium).getPeriod() == iPeriodByzantiumRoman:
				return "TXT_KEY_CIV_BYZANTIUM_WESTERN_EMPIRE"

	elif iCiv == iMalays:
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_MALAYA_FEDERATION_OF"
		
		if iReligion == iIslam:
			if capital in cities.rectangle(tKalimantan):
				if bEmpire:
					return "TXT_KEY_EMPIRE_ADJECTIVE"
					
				return "TXT_KEY_SULTANATE_OF"
			
			if capital in cities.rectangle(tSulawesi):
				return "TXT_KEY_SULTANATE_OF"
			
			return "TXT_KEY_SULTANATE_NAME"
			
		if bEmpire:
			return "TXT_KEY_KINGDOM_OF"
		
		if capital in cities.region(tMalaya):
			return "TXT_KEY_KINGDOM_OF"
		
		if iEra >= iRenaissance:
			return "TXT_KEY_KINGDOM_ADJECTIVE"

			
	elif iCiv == iNorse:
		if bCityStates:
			return "TXT_KEY_CIV_NORSE_THINGS"
		
		if isControlled(iPlayer, plots.region(rBritain)):
			return "TXT_KEY_CIV_NORSE_NORTH_SEA_EMPIRE"
				
		if iReligion < 0 and iEra < iRenaissance:
			return "TXT_KEY_CIV_NORSE_NORSE_KINGDOMS"

		if player(iPlayer).getPeriod() == -1:
			return "TXT_KEY_CIV_NORSE_NORSE_KINGDOMS"
			
		if isControlled(iPlayer, plots.core(iSweden)) or team(iSweden).isVassal(iPlayer):
			return "TXT_KEY_CIV_NORSE_KALMAR_UNION"
		
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
				
	elif iCiv == iTurks:			
		if iReligion >= 0:
			if bEmpire:
				if isControlled(iPlayer, plots.core(iPersia)) and not bResurrected:
					return "TXT_KEY_CIV_TURKS_GREAT_EMPIRE"
			
				return "TXT_KEY_EMPIRE_ADJECTIVE"
			
			if not isControlled(iPlayer, plots.core(iPersia)):
				return "TXT_KEY_CIV_TURKS_KHANATE_OF"
				
			if iReligion == iIslam:
				if isControlled(iPlayer, plots.core(iPersia)):
					return "TXT_KEY_SULTANATE_ADJECTIVE"
			
				return "TXT_KEY_SULTANATE_OF"
				
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_CIV_TURKS_KHAGANATE"
			
	elif iCiv == iArabia:
		if bResurrected:
			return "TXT_KEY_KINGDOM_OF"
			
		if iReligion == iIslam and (bTheocracy or controlsHolyCity(iPlayer, iIslam)):
			return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
	elif iCiv == iTibet:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iKhmer:
		if bEmpire and getColumn(iPlayer) >= 6:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
			
	elif iCiv == iMoors:
		if bCityStates:
			return "TXT_KEY_CIV_MOORS_TAIFAS"
			
			
	elif iCiv == iJava:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_NAME"
		
		if bEmpire:
			if iEra >= iIndustrial:
				if isControlled(iPlayer, plots.rectangle(tSumatra).without(plots.rectangle(tMalaya))) and isControlled(iPlayer, plots.rectangle(tKalimantan)):
					if civic.iSociety == iEgalitarianism:
						return "TXT_KEY_EMPIRE_OF"
					
					return "TXT_KEY_EMPIRE_ADJECTIVE"
			return "TXT_KEY_EMPIRE_NAME"
			
	elif iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire and iEra > iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iMedieval and isCurrentCapital(iPlayer, "Barcelona", "Tarragona", "Valencia", "Zaragoza"):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iCiv == iFrance:
		if not capital in cities.region(rFrance):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if civic.iLegitimacy == iStratocracy:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not player(iHolyRome).isExisting() and iEra == iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"

		if iEra == iClassical:
			return "TXT_KEY_CIV_FRANCE_FRANKS_TITLE"
			
	elif iCiv == iEngland:
		if capital not in cities.core(iEngland):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iMedieval and player(iFrance).isExisting() and team(iFrance).isAVassal() and civ(master(iFrance)) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 12:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iCiv == iHolyRome:
		if bCityStates and player(iPlayer).getPeriod() == -1:
			return "TXT_KEY_CIV_HOLY_ROME_FREE_CITIES"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCurrentCapital(iPlayer, "Buda", "Pest"):
			return "TXT_KEY_KINGDOM_OF"
			
		if player(iGermany).isExisting():
			return "TXT_KEY_CIV_HOLY_ROME_ARCHDUCHY_OF"
	
	elif iCiv == iBurma:
		if bCityStates:
			return "TXT_KEY_CIV_BURMA_CITY_STATES"
		
		if iEra >= iRenaissance:
			if bEmpire or getColumn(iPlayer) >= 11:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
			
			if capital in cities.birth(iBurma).coastal():
				return "TXT_KEY_KINGDOM_NAME"
			
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_NAME"

		elif iCiv == iRus:
			if bResurrected:
				return "TXT_KEY_CIV_RUS_COSSACK_HETMANATE"
		
		if iReligion == -1:
			return "TXT_KEY_CIV_RUS_RUS"
		
		if iEra <= iMedieval:
			if (civic.iGovernment == iRepublic and civic.iLegitimacy in [iVassalage, iCitizenship]) or (civic.iGovernment == iElective and civic.iLegitimacy == iCitizenship):
				if isCurrentCapital(iPlayer, "Novgorod"):
					return "TXT_KEY_CIV_RUS_NOVGOROD"
				
				return "TXT_KEY_REPUBLIC_NAME"
		
		if isCurrentCapital(iPlayer, "Drohiczyn", "Lviv", "Stanislaviv"):
			return "TXT_KEY_KINGDOM_OF"
	
	elif iCiv == iVietnam:
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_VIETNAM_DAI_NAM"
	
	elif iCiv == iSwahili:
		if iEra >= iIndustrial and not player(iBuganda).isExisting():
			return "TXT_KEY_CIV_EAST_AFRICA_FEDERATION"
		if civic.iGovernment == iRepublic:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
		
		if iReligion != iIslam:
			return "TXT_KEY_KINGDOM_ADJECTIVE"
		
		if iEra >= iIndustrial:
			return "TXT_KEY_SULTANATE_OF"
	
	if iCiv == iBuganda:
		if iEra >= iIndustrial and not player(iSwahili).isExisting():
			return "TXT_KEY_CIV_EAST_AFRICA_FEDERATION"
			
	# Nothing for Mali
	
	elif iCiv == iPoland:
		if iEra >= iRenaissance and bEmpire:
			return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		if scenario() == i1700AD and turn() < year(1790):
			return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		if isCurrentCapital(iPlayer, "Kaunas", "Klaipeda", "Vilnius", "Riga"):
			return "TXT_KEY_CIV_POLAND_GRAND_DUCHY_OF"
			
	elif iCiv == iPortugal:
		if capital in cities.core(iBrazil) and not player(iBrazil).isExisting():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not capital in plots.region(rIberia):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iInca:
		if not bResurrected:
			if bEmpire:
				return "TXT_KEY_CIV_INCA_FOUR_REGIONS"
				
	elif iCiv == iItaly:
		if bCityStates:
			if bWar:
				return "TXT_KEY_CIV_ITALY_LEAGUE"
				
			return "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS"
			
		if not bResurrected:
			if iReligion == iCatholicism:
				if isCurrentCapital(iPlayer, "Roma"):
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
					
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_DUCHY_OF"
				
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iMongols:
		if capital.getRegionID() == rPersia:
			return "TXT_KEY_CIV_MONGOLIA_ILKHANATE"
	
		if bEmpire and not bResurrected:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra <= iRenaissance:
			if iNumCities <= 3 and not bResurrected:
				return "TXT_KEY_CIV_MONGOLIA_KHAMAG"
				
		if iEra <= iIndustrial:
			return "TXT_KEY_CIV_MONGOLIA_KHANATE"
			
	elif iCiv == iAztecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_AZTECS_ALTEPETL"
				
	elif iCiv == iTimurids:
		if bResurrected:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if not bEmpire and not tPlayer.isHasTech(iFirearms):
			return "TXT_KEY_SULTANATE_ADJECTIVE"
		
	elif iCiv == iSweden:
		if cities.owner(iPlayer).any(lambda city: plot(city).getRegionID() != rScandinavia):
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if cities.rectangle(tNorway).all(lambda city: city.getOwner() == iPlayer):
			return "TXT_KEY_CIV_SWEDEN_SWEDEN_NORWAY"

	elif iCiv == iTatars:
		if capital.getRegionID() == rVolga:
			return "TXT_KEY_CIV_TATARS_KHANATE_OF"
		
		if capital.getRegionID() == rPonticSteppe:
			if not capital.isCoastal(20):
				if bEmpire or year() >= year(1300):
					return "TXT_KEY_CIV_TATARS_KHANATE_OF"
			
			if bEmpire:
				return "TXT_KEY_CIV_TATARS_THRONE_OF"


	elif iCiv == iRussia:
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if iEra <= iMedieval:
			if (civic.iGovernment == iRepublic and civic.iLegitimacy in [iVassalage, iCitizenship]) or (civic.iGovernment == iElective and civic.iLegitimacy == iCitizenship):
				return "TXT_KEY_REPUBLIC_NAME"
			
		if isControlled(iPlayer, plots.regions(rRuthenia, rPonticSteppe, rEuropeanArctic), 5):
			return "TXT_KEY_CIV_RUSSIA_TSARDOM_OF"


	elif iCiv == iTimurids: # similar structure to Ottoman nomenclature
		if iReligion == iShia:
			if bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"

		if iReligion == iIslam:
			if bTheocracy and game.getHolyCity(iIslam) and game.getHolyCity(iIslam).getOwner() == iPlayer:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"

		if iReligion == iShia or iReligion == iIslam:		
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"

			return "TXT_KEY_SULTANATE_ADJECTIVE"

		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iOttomans:
		if iReligion == iIslam:
			if bTheocracy and game.getHolyCity(iIslam) and game.getHolyCity(iIslam).getOwner() == iPlayer:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_SULTANATE_ADJECTIVE"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iThailand:
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_OF"
		if getColumn(iPlayer) >= 11:
			return "TXT_KEY_KINGDOM_OF"

	elif iCiv == iNetherlands:
		if bCityStates:
			return "TXT_KEY_CIV_NETHERLANDS_REPUBLIC"
		
		if capital not in cities.core(iNetherlands):
			return "TXT_KEY_CIV_NETHERLANDS_EXILE"
			
		if bEmpire:
			if iEra >= iIndustrial:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM_OF"

	elif iCiv == iManchuria:
		if iReligion in (iOrthodoxy, iCatholicism, iProtestantism):
			return "TXT_KEY_CIV_MANCHURIA_HEAVENLY_KINGDOM"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iCiv == iGermany:
		if getColumn(iPlayer) >= 16 and bEmpire:
			if player(iHolyRome).isExisting() and team(iHolyRome).isExisting() and civ(master(iHolyRome)) == iGermany:
				return "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iSaudis:
		if bEmpire:
			if getColumn(iPlayer) >= 15:
				return "TXT_KEY_KINGDOM_OF"
			
			return "TXT_KEY_SULTANATE_OF"

	elif iCiv == iAmerica:
		if civic.iSociety in [iSlavery, iManorialism]:
			if isControlled(iPlayer, plots.region(rMesoamerica)) and isControlled(iPlayer, plots.region(rCaribbean)):
				return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iCiv == iArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not at(capital, plots.capital(iCiv)):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
	
	elif iCiv == iMexico:
		if bEmpire or iDespotism in civic:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"

	elif iCiv == iBelgium:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if isControlled(iPlayer, plots.core(iBelgium)) and isControlled(iPlayer, plots.core(iNetherlands)):
			return "TXT_KEY_CIV_BELGIUM_UNITED_KINGDOM_OF"
			
	return None
			
### Leader methods ###

def startingLeader(identifier):
	if not isinstance(identifier, Civ):
		identifier = civ(identifier)
		
	return dStartingLeaders[scenario()].get(identifier, dStartingLeaders[i3000BC][identifier])
	
def leader(iPlayer):
	iCiv = civ(iPlayer)

	if is_minor(iPlayer): return None
	
	if not player(iPlayer).isAlive(): return None
	
	if player(iPlayer).isHuman(): return None
	
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	civic = civics(iPlayer)
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or (civic.iGovernment in [iRepublic, iElective] and civic.iReligion == iFanaticism)
	bResurrected = data.civs[iCiv].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.civs[iCiv].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	
	if iCiv == iEgypt:
		if player(iPlayer).getPeriod() == iPeriodPtolemaicEgypt: return iPtolemy
		if getColumn(iPlayer) >= 3: return iRamesses
		if year() >= year(-1600): return iHatshepsut

	elif iCiv == iZimbabwe:
		if iEra >= iIndustrial: return iIanSmith

		elif tPlayer.isHasTech(iGeneralship): return iChangamire

	elif iCiv == iBuganda:
		if iEra >= iIndustrial: return iIdiAmin

		if getColumn(iPlayer) >= 7: return iMutesa

	elif iCiv == iSomalia:
		if iEra >= iRenaissance: return iAbdillaiDeria	

	elif iCiv == iCongo:
		if iEra >= iGlobal or year() >= year(1900): return iMobutu

	elif iCiv == iMali:
		if iEra >= iGlobal or year() >= year(1900): return iTraore	
	
	elif iCiv == iMadagascar:
		if iEra >= iGlobal or year() >= year(1900): return iTsiranana	
	
	elif iCiv == iSwahili:
		if iEra >= iGlobal or year() >= year(1900): return iNyerere	


	elif iCiv == iNubia:
		if year() >= year(600) or iReligion == iOrthodoxy: return iMerkurios
		if getColumn(iPlayer) >= 5: return iAmanirena
	
	elif iCiv == iFunj:
		if player(iPlayer).getPeriod() == iPeriodSudan: return iAlBashir

	elif iCiv == iMisr:

		if not bMonarchy and iEra >= iGlobal: return iNasser
		
		if getColumn(iPlayer) >= 13: return iMuhammadAli

		if getColumn(iPlayer) >= 10: return iBaibars

		if year() >= year(1140):  return iSaladin


	elif iCiv == iBabylonia:
		if year() >= year(-660): return iNebuchadnezzar
		
	elif iCiv == iIndia:
		if not bMonarchy and iEra >= iGlobal: return iGandhi
		
		if iEra >= iRenaissance: return iShivaji
		
		if getColumn(iPlayer) >= 5: return iChandragupta
		
	elif iCiv == iChina:
		if isCommunist(iPlayer) or isRepublic(iPlayer) and iEra >= iIndustrial: return iMao
			
		if iEra >= iRenaissance and year() >= year(1400): return iHongwu
	
		if bResurrected and year() >= year(1300): return iHongwu
		
		if scenario() >= i1700AD: return iHongwu
		
		if iEra >= iMedieval: return iTaizong
		
		
	elif iCiv == iGreece:
		if iEra >= iIndustrial: return iGeorge
		
		if bResurrected and getColumn(iPlayer) >= 12: return iGeorge
	
		
	elif iCiv == iIran:
		if iEra >= iGlobal: return iKhomeini

		
	elif iCiv == iPersia:
		
		if bResurrected or getColumn(iPlayer) >= 8: return iAlSaffar

		if bEmpire: return iDarius

		
	elif iCiv == iParthia:
		if getColumn(iPlayer) >= 7: return iKhosrow
			
			
	elif iCiv == iPhoenicia:
		if not bCityStates: return iHannibal
		
		if capital.getRegionID() not in [rLevant, rMesopotamia, rAnatolia]: return iHannibal
		
	elif iCiv == iRome:
		if year() >= year(180): return iMarcusAurelius
		if not bCityStates: return iAugustus
		
		if tPlayer.isHasTech(iGeneralship): return iJuliusCaesar
		
	elif iCiv == iKorea:		
		if iEra >= iRenaissance: return iSejong
		
		if scenario() >= i1700AD: return iSejong

	elif iCiv == iKhmer:
		if iEra >= iMedieval: return iSuryavarman
		
	elif iCiv == iJapan:
		if iEra >= iIndustrial: return iMeiji
		
		if tPlayer.isHasTech(iFeudalism): return iOdaNobunaga
		
	elif iCiv == iEthiopia:
		if iEra >= iGlobal or year() >= year(1960): return iSelassie

		if iEra >= iIndustrial: return iMenelik
		
		if year() >= year(1000): return iZaraYaqob
		
	elif iCiv == iDravidia:
		if iEra >= iRenaissance: return iKrishnaDevaRaya
		if scenarioStartYear() >= 1500: return iKrishnaDevaRaya
		
	elif iCiv == iByzantium:
		if year() >= year(1000): return iBasil
		if year() >= year(520): return iJustinian
		
	elif iCiv == iMalays:
		if iEra >= iRenaissance: return iTunPerak

	elif iCiv == iNorse:
		if iEra >= iGlobal: return iGerhardsen
		elif iEra >= iRenaissance: return iChristian
		if scenarioStartYear() >= 1500: return iChristian
		if getColumn(iPlayer) >= 8 and capital in cities.rectangle(tNorway): return iHaakon

	elif iCiv == iTurks:
		if bResurrected:
			return iShaybaniKhan
		
	elif iCiv == iArabia:
		if bResurrected or getColumn(iPlayer) >= 10:
			return iQatadaIbnIdris

		
	elif iCiv == iTibet:
		if year() >= year(1500): return iLobsangGyatso
		
	elif iCiv == iMorocco:
		if iEra >= iGlobal: return iMohammedV
		
		if iEra >= iRenaissance: return iAhmad
		
	elif iCiv == iJava:
		if iEra >= iGlobal: return iSuharto
		
		
	elif iCiv == iSpain:
		if isFascist(iPlayer): return iFranco
		
		if any(data.dFirstContactConquerors.values()): return iPhilip

	# Aeons - Goths get Spanish/Italian leaders if no Spain/Italy
	elif iCiv == iGoths:
		if not player(iSpain).isExisting() and year() > year(1000) and player(iPlayer).getPeriod() == iPeriodVisigoths:
			if isFascist(iPlayer): return iFranco
		
			if any(data.dFirstContactConquerors.values()): return iPhilip

			return iIsabella
		if not player(iItaly).isExisting() and year() > year(1250) and player(iPlayer).getPeriod() == iPeriodOstrogoths:
			if isFascist(iPlayer): return iMussolini
	
			if iEra >= iIndustrial: return iCavour

			return iLorenzo
		
	elif iCiv == iFrance:
		if iEra >= iGlobal: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if iEra >= iRenaissance: return iLouis

		if year() >= year(840): return iPhilipAugustus
		
	elif iCiv == iEngland:
		if iEra >= iGlobal: return iChurchill
		
		if iEra >= iIndustrial: return iVictoria
		
		if scenario() == i1700AD: return iVictoria
		
		if iEra >= iRenaissance: return iElizabeth
		
	elif iCiv == iHolyRome:
		if iEra >= iIndustrial: return iFrancis
		
		if scenario() == i1700AD: return iFrancis
		
		if iEra >= iRenaissance: return iCharles

	# Aeons - Potential German leaders for Germania if HRE doesn't spawn
	elif iCiv == iGermania:
		if not player(iHolyRome).isExisting() and year() > year(900):
			if iEra >= iIndustrial: return iFrancis
		
			if scenario() == i1700AD: return iFrancis
		
			if iEra >= iRenaissance: return iCharles

			return iBarbarossa

	elif iCiv == iBurma:
		if iEra >= iRenaissance: return iBayinnaung

	elif iCiv == iRus:
		if iEra >= iRenaissance: return iKhmelnytsky
	
	elif iCiv == iVietnam:
		if isCommunist(iPlayer) or isRepublic(iPlayer): return iHoChiMinh

	elif iCiv == iHausa:
		if iEra >= iGlobal: return iObasanjo
		
		elif tPlayer.isHasTech(iDoctrine): return iUsumanDanFodio


	elif iCiv == iCelts:
		if capital.getRegionID() == rBritain:
			return iBoudica

		if year() >= year(580): return iBrianBoru

		if player(iPlayer).getPeriod() == iPeriodInsularCelts:
			return iBrianBoru

	elif iCiv == iMacedon:
		if player(iPlayer).getPeriod() == iPeriodSeleucids:
			return iSeleucus
			
	elif iCiv == iPoland:
		if iEra >= iGlobal: return iWalesa
		
		if isFascist(iPlayer) or isCommunist(iPlayer): return iPilsudski
	
		if iEra >= iRenaissance: return iSobieski
		
		if scenario() == i1700AD: return iSobieski
		
	elif iCiv == iPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iCartography): return iJoao
		
	elif iCiv == iInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and year() >= year(1600): return iCastilla

	elif iCiv == iOman:
		if iEra >= iIndustrial: return iBarghash

		if player(iOman).getPeriod() == iPeriodZanzibar: return iBarghash
		
		if year() >= year(1850): return iBarghash

	
	elif iCiv == iItaly:
		if isFascist(iPlayer): return iMussolini
	
		if iEra >= iIndustrial: return iCavour
		
	elif iCiv == iMongols:
		if year() >= year(1400): return iKublaiKhan
		
	elif iCiv == iMexico:
		if bMonarchy: return iSantaAnna
		
		if isFascist(iPlayer): return iSantaAnna
		
		if iEra >= iGlobal: return iCardenas
			
	elif iCiv == iTimurids:
		if year() > year(dBirth[iIran]): return iAkbar

	elif iCiv == iSweden:
		if iEra >= iGlobal: return iErlander

	elif iCiv == iGhorids:
		if year() > year(1220): return iTughluq

	elif iCiv == iTunis:
		if not bMonarchy and iEra >= iIndustrial: return iBourguiba
		
	elif iCiv == iRussia:
		if iEra >= iIndustrial:
			if not bMonarchy: return iStalin
			
			return iAlexanderI
			
		if iEra >= iRenaissance:
			if year() >= year(1750): return iCatherine
			
			return iPeter
		
	elif iCiv == iOttomans:
		if not bMonarchy and iEra >= iIndustrial: return iAtaturk

		if getColumn(iPlayer) >= 13: return iMahmudII	

		if iEra >= iRenaissance: return iSuleiman
		if scenarioStartYear() >= 1500: return iSuleiman
				
	elif iCiv == iThailand:
		if iEra >= iIndustrial: return iMongkut
		
	elif iCiv == iNetherlands:
		if year() >= year(1650): return iWilliam

	elif iCiv == iAshanti:
		if iEra >= iIndustrial: return iYaaAsantewa

	elif iCiv == iGermany:
		if isFascist(iPlayer): return iHitler
		
		if getColumn(iPlayer) >= 15: return iBismarck
		
	elif iCiv == iAmerica:
		if iEra >= iGlobal: return iRoosevelt
		
		if year() >= year(1850): return iLincoln
		
	elif iCiv == iArgentina:
		if iEra >= iGlobal: return iPeron
	
	elif iCiv == iBrazil:
		if iEra >= iGlobal: return iVargas
		
	elif iCiv == iCanada:
		if iEra >= iGlobal: return iTrudeau

	elif iCiv == iArmenia:
		if not bMonarchy and iEra >= iIndustrial: return iAndranik
		if getColumn(iPlayer) >= 7: return iAshot
		elif bResurrected: return iAshot

	elif iCiv == iNumidia:
		if not bMonarchy and iEra >= iIndustrial: return iBourguiba
		if bResurrected: return iYaghmurasen
		if iReligion == iIslam or iReligion == iShia:  return iYaghmurasen

	elif iCiv == iYemen:
		if getColumn(iPlayer) >= 11: return iAlQasim
		if not bMonarchy and iEra >= iIndustrial: return iAlSallal

		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	iLeader = pPlayer.getLeader()
				
	if iCiv == iDravidia:
		if iLeader == iKrishnaDevaRaya:
			if year() >= year(1700):
				return "TXT_KEY_LEADER_TIPU_SULTAN"
				
	return None