from Resources import setupScenarioResources

from Scenario import *
from Locations import *
from RFCUtils import *
from Core import *

	

lCivilizations = [
	Civilization(
		iChina,
		iGold=200,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iTheocracy, iManorialism, iMerchantTrade, iSyncretism, iIsolationism],
		techs=techs.column(9).including(iPrinting).without(iDoctrine, iReligiousOrders, iDiscipline),
		dAttitudes={iKorea: 1}
	),
	Civilization(
		iCelts,
		iGold=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iManorialism, iRedistribution, iMonasticism],
		techs=techs.column(6).including(iCivilService),
	),
	Civilization(
		iMaya,
		iGold=50,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iDeification],
		techs=techs.column(4).including(iAesthetics, iLaw).without(iSeafaring, iRiding, iShipbuilding, iCement, iNavigation),
	),
	Civilization(
		iEthiopia,
		iStateReligion=iOrthodoxy,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iClergy],
		techs=techs.column(6).without(iSteel),
	),
	Civilization(
		iDravidia,
		iGold=300,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(8).including(iCommune),
	),
	Civilization(
		iKorea,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iRedistribution, iSyncretism],
		techs=techs.column(9).without(iReligiousOrders, iDoctrine, iCommune, iCompass, iDiscipline, iPatronage),
		dAttitudes={iChina: 1}
	),
	Civilization(
		iKhmer,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iRedistribution, iSyncretism],
		techs=techs.column(7).including(iMachinery).without(iFeudalism),
	),
	Civilization(
		iGhana,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6)
	),
	Civilization(
		iByzantium,
		iGold=300,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iCitizenship, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).without(iCropRotation, iSelectiveBreeding, iAlchemy)
	),
	Civilization(
		iFrance,
		iGold=400,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iPaper, iEducation, iDiscipline),
		dAttitudes={iEngland: -3, iHolyRome: -1}
	),
	Civilization(
		iMalays,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(6).without(iPolitics),
	),
	Civilization(
		iJava,
		iGold=100,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(6),
	),
	Civilization(
		iJapan,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iManorialism, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(8).including(iEducation).without(iFeudalism, iAlchemy, iGuilds),
	),
	Civilization(
		iNorse,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade],
		techs=techs.column(8).including(iCompass).without(iDoctrine, iTheology, iCropRotation),
	),
	Civilization(
		iArabia,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iClergy],
		techs=techs.column(8)
	),
	Civilization(
 		iMorocco,
 		iGold=200,
 		iStateReligion=iIslam,
 		lCivics=[iDespotism, iSlavery, iMerchantTrade, iFanaticism, iVassalage, iHegemony],
 		techs=techs.column(7).including(iDoctrine, iMachinery, iGuilds, iReligiousOrders)
 	),
	Civilization(
		iSpain,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(8).including(iPaper, iReligiousOrders, iEducation),
		dAttitudes={iMorocco: -4}
	),
	Civilization(
		iKanemBornu,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iSlavery, iClergy],
		techs=techs.column(5).without(iCement),
	),
	Civilization(
		iGeorgia,
		iGold=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iDoctrine, iReligiousOrders, iLimbProtection, iSelectiveBreeding),
	),
	Civilization(
		iEngland,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iCompass),
		dAttitudes={iFrance: -3}
	),
	Civilization(
		iYemen,
		iGold=100,
		iStateReligion=iShia,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iSyncretism],
		techs=techs.column(7).including(iDoctrine, iLimbProtection, iSelectiveBreeding)
	),
	Civilization(
		iHolyRome,
		iGold=150,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iEducation, iReligiousOrders),
		dAttitudes={iFrance: -2}
	),
	Civilization(
		iRus,
		iGold=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iElective, iMerchantTrade, iVassalage, iHegemony, iClergy],
		techs=techs.column(7).including(iGuilds),
	),
	Civilization(
		iBurma,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iVassalage, iCasteSystem, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(8).without(iGuilds, iMachinery),
	),
	Civilization(
		iHausa,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iClergy],
		techs=techs.column(5).without(iEngineering, iAesthetics),
	),
	Civilization(
		iBenin,
		iGold=200,
		lCivics=[iDespotism, iSlavery, iRedistribution],
		techs=techs.column(4).including(iGeneralship).without(iLiterature),
	),
	Civilization(
		iMisr,
		iGold=200,
		iStateReligion=iShia,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iReligiousOrders, iEducation, iPaper),
	),
	Civilization(
		iGhorids,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(8).including(iReligiousOrders, iPaper),
	),
	Civilization(
		iSomalia,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iElective, iCitizenship, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(5).including(iRecurveBow, iScholarship, iArtisanry, iSteel)
	),
	Civilization(
		iSwahili,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iIslam,
		lCivics=[iElective, iCitizenship, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(6).including(iLateenSails, iAlchemy, iFeudalism, iNobility)
	),
	Civilization(
		iVietnam,
		iGold=150,
		iStateReligion=iConfucianism,
		lCivics=[iMonarchy, iCitizenship, iCasteSystem, iRegulatedTrade, iSyncretism, iThalassocracy],
		techs=techs.column(8).including(iEducation),
	),
	Civilization(
		iBuganda,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(2).including(iAlloys, iBloomery)
	),
	Civilization(
		iTurks,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(8).including(iDiscipline, iEducation),
	),
	Civilization(
		iPoland,
		iGold=200,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iSyncretism],
		techs=techs.column(7).including(iLimbProtection, iSelectiveBreeding).without(iTheology),
	),
	Civilization(
		iJerusalem,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(8).including(iReligiousOrders)
	),
	Civilization(
		iNative,
		iGold=300,
		techs=techs.column(4),
	),
	Civilization(
		iIndependent2,
		iGold=500,
		techs=techs.column(7),
	),
	Civilization(
		iIndependent,
		iGold=500,
		techs=techs.column(7),
	),
]

lTribalVillages = [
	((130, 20), (141, 23)), # Northern Australia
	((138, 9), (143, 17)), # Eastern Australia
	((0, 6), (2, 12)), # New Zealand
	((69, 29), (78, 33)), # Central Africa
	((137, 59), (140, 62)), # Hokkaido
	((99, 65), (119, 72)), # Siberia
]
	


scenario1100AD = Scenario(
	iStartYear = 1100,
	fileName = "RFC_1100AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	dCivilizationDescriptions = {
		iNorse: "TXT_KEY_CIV_DENMARK_DESC",
		iCelts: "TXT_KEY_CIV_IRELAND_DESC",
		iArabia: "TXT_KEY_CIV_HEJAZ_DESC",
		iMisr: "TXT_KEY_CIV_EGYPT_DESC",
	},
	iCultureTurns = 100,
	
	dRevealed = {
		iCivGroupEurope: Revealed(
			lLandRegions= lEurope + lNorthAfrica + [rAnatolia, rArabia], 
			lCoastRegions=[rMesopotamia, rPersia],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupEastAsia: Revealed(
			lLandRegions=lEastAsia + [rTransoxiana],
		),
		iCivGroupSouthAsia: Revealed(
			lLandRegions=lIndia + [rIndochina, rIndonesia, rPersia, rKhorasan, rTransoxiana, rTibet, rArabia, rMesopotamia],
			lCoastRegions=[rEthiopia],
			lSeaAreas=[((79, 23), (97, 32))],
		),
		iCivGroupMiddleEast: Revealed(
			lLandRegions=lMiddleEast + lIndia + lNorthAfrica + [rSahel, rSahara, rEthiopia, rHornOfAfrica, rIberia, rItaly, rBalkans, rGreece],
			lCoastRegions=lEastAsia + [rBritain, rIreland, rFrance, rPonticSteppe, rSwahiliCoast],
			lSeaAreas=[((79, 23), (97, 32))],
		),
	},
	
	dGreatPeopleCreated = {
		iChina: 8,
		iDravidia: 3,
		iKorea: 3,
		iJapan: 3,
		iNorse: 2,
		iTurks: 2,
		iSpain: 3,
		iFrance: 3,
		iEngland: 2,
		iHolyRome: 3,
	},
	dGreatGeneralsCreated = {
		iChina: 2,
		iDravidia: 1,
		iKorea: 1,
		iJapan: 1,
		iNorse: 1,
		iTurks: 1,
		iMorocco: 1,
		iSpain: 1,
		iFrance: 1,
		iEngland: 1,
		iHolyRome: 1,
	},
	
	
	
	lAllGoalsFailed = [iChina, iKorea, iCelts],
	
	greatWall = GreatWall(
		tGraphicsTL = (118, 54),
		tGraphicsBR = (128, 58),
		lGraphicsExceptions = [(118, 55), (118, 56), (118, 57), (118, 58), (119, 55), (119, 56), (119, 57), (119, 58), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (122, 58), (123, 58)],
		lClearCulture = [(127, 59), (128, 59), (129, 57), (129, 58)],
		
		lEffectAreas = [((118, 46), (129, 53)), ((124, 54), (128, 58)), ((121, 54), (123, 55)), ((119, 54), (120, 54)), ((123, 56), (123, 57))],
	),

)