from Core import *
from RFCUtils import *
from Locations import *
from Events import events, handler
from DynamicCivs import isCurrentCapital


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
}

dPeriods600AD = {
	iPhoenicia : iPeriodCarthage,
	iCelts : iPeriodInsularCelts,
	iGoths : iPeriodVisigoths,
	iNubia : iPeriodMakuria,
}

dPeriods1100AD = {
	iCelts : iPeriodInsularCelts,
	iNorse : iPeriodDenmark,
	iArabia : iPeriodHejaz,
	iSpain : iPeriodCastile,
	iNumidia : iPeriodAlgeria,
	iMisr : iPeriodMisrEgypt,
}

dPeriods1500AD = {
	iOttomans : iPeriodOttomanConstantinople,
	iZimbabwe : iPeriodMutapa,
	iChina : iPeriodMing,
	iDravidia : iPeriodVijayanagara,
	iNorse : iPeriodDenmark,
	iTurks : iPeriodUzbeks,
	iSpain : iPeriodModernSpain,
	iBuganda : iPeriodBuganda,
	iNumidia : iPeriodAlgeria,
	iTimurids : iPeriodMughals,
	iGhorids : iPeriodDelhi,
	iMisr : iPeriodMisrEgypt,
}

dPeriods1700AD = {
	iIndia : iPeriodMaratha,
	iCelts : iPeriodInsularCelts,
	iHolyRome : iPeriodAustria,
	iInca : iPeriodPeru,
	iZimbabwe : iPeriodRozwi,
	iBuganda : iPeriodBuganda,
	iManchuria : iPeriodQing,
	iTimurids : iPeriodMughals,
	iEngland : iPeriodUnitedKingdom,
	iOman : iPeriodZanzibar,
}

dPeriods1815AD = {
	iChina : iPeriodMing,
	iIndia : iPeriodMaratha,
	iFrance : iPeriodNationalFrance,
	iNorse : iPeriodDenmark,
	iTurks : iPeriodUzbeks,
	iSpain : iPeriodModernSpain,
	iHolyRome : iPeriodAustria,
	iEngland : iPeriodUnitedKingdom,
	iOttomans : iPeriodOttomanConstantinople,
	iManchuria : iPeriodQing,
	iZimbabwe : iPeriodRozwi,
}

dScenarioPeriods = {
	-3000: {},
	600: dPeriods600AD,
	1100: dPeriods1100AD,
	1500: dPeriods1500AD,
	1700: dPeriods1700AD,
	1815: dPeriods1815AD,
}


dPeriodNames = {
	iPeriodPtolemaicEgypt:			"Ptolemaic_Egypt",
	iPeriodMakuria:					"Makuria",
	iPeriodMing:					"Ming",
	iPeriodMaratha:					"Maratha",
	iPeriodUnitedGreece:			"United_Greece",
	iPeriodModernGreece:			"Modern_Greece",
	iPeriodCarthage:				"Carthage",
	iPeriodInsularCelts:			"Insular_Celts",
	iPeriodVijayanagara:			"Vijayanagara",
	iPeriodByzantineConstantinople:	"Byzantine_Constantinople",
	iPeriodNationalFrance:			"National_France",
	iPeriodMeiji:					"Meiji",
	iPeriodDenmark:					"Denmark",
	iPeriodNorway:					"Norway",
	iPeriodUzbeks:					"Uzbeks",
	iPeriodAustria:					"Austria",
	iPeriodYuan:					"Yuan",
	iPeriodPeru:					"Peru",
	iPeriodLateInca:				"Late_Inca",
	iPeriodModernItaly:				"Modern_Italy",
	iPeriodPakistan:				"Pakistan",
	iPeriodOttomanConstantinople:	"Ottoman_Constantinople",
	iPeriodQing:					"Qing",
	iPeriodModernGermany:			"Modern_Germany",
	iPeriodVisigoths: 			"Visigoths",
	iPeriodOstrogoths: 			"Ostrogoths",
	iPeriodVandalAfrica: 			"Vandal_Africa",
	iPeriodAngloSaxons:			"Anglo_Saxons",
	iPeriodPonticScythia:			"Pontic_Scythians",
	iPeriodMisrEgypt:			"Misr_Egypt",
	iPeriodMughals:				"Mughals",
	iPeriodCastile:				"Castile",
	iPeriodModernSpain:			"Modern_Spain",
	iPeriodDelhi:				"Delhi",
	iPeriodBuyidBaghdad:			"Buyid_Baghdad",
	iPeriodAlgeria:				"Algeria",
	iPeriodSeleucids:			"Seleucids",
	iPeriodModernBenin:			"Modern Benin",	
	iPeriodSokoto:				"Sokoto",
	iPeriodNigeria:				"Nigeria",
	iPeriodUnitedKingdom:			"United_Kingdom",
 	iPeriodGreatBritain:			"Great_Britain",
	iPeriodArabiaMesopotamia:		"Arabia_Mesopotamia",
	iPeriodTanzania:			"Tanzania",
	iPeriodSudan:				"Sudan",
	iPeriodSouthSudan:			"South_Sudan",
	iPeriodMutapa:				"Mutapa",
	iPeriodRozwi:				"Rozwi",
	iPeriodRhodesia:			"Rhodesia",
	iPeriodBuganda:				"Buganda",
	iPeriodUganda:				"Uganda",
	iPeriodSouthAfricaUnion:			"South_Africa_Union",
	iPeriodZanzibar:			"Zanzibar",
	iPeriodHejaz:				"Hejaz",
	iPeriodByzantiumRoman:			"Roman_Byzantium"
}
	


def setPeriod(iCiv, iPeriod):
	if game.getPeriod(iCiv) == iPeriod:
		return

	game.setPeriod(iCiv, iPeriod)
	
	events.fireEvent("periodChange", iCiv, iPeriod)
	
	iPlayer = slot(iCiv)
	if iPlayer >= 0:
		events.fireEvent("playerPeriodChange", iPlayer, iPeriod)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		iCiv = civ(iPlayer)
		if iCiv in dEvacuatePeriods:
			setPeriod(iCiv, dEvacuatePeriods[iCiv])
			
			if cities.core(iPlayer).owner(iPlayer) > 0:
				return True
			else:
				setPeriod(iCiv, -1)
	return False


@handler("birth")
def onBirth(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iFrance:
		setPeriod(iCelts, iPeriodInsularCelts)
	elif iCiv == iGermany:
		setPeriod(iHolyRome, iPeriodAustria)
	elif iCiv == iIran:
		setPeriod(iTurks, iPeriodUzbeks)
 

@handler("collapse")
def onCollapse(iPlayer):
	if civ(iPlayer) == iArabia:
		setPeriod(iArabia, iPeriodHejaz)

	if civ(iPlayer) == iChina:
		setPeriod(iMongols, iPeriodYuan)

		if cities.regions(rNorthChina, rSouthChina).owner(iManchuria).count() > 1:
			setPeriod(iManchuria, iPeriodQing)


@handler("resurrection")
def onResurrection(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iEgypt:
		#if player(iPlayer).getStateReligion() == -1 and cities.owner(iPlayer).any(lambda city: city.getPreviousCiv() == iGreece or city.getPreviousCiv() == iSparta or city.getPreviousCiv() == iMacedon):
		if cities.owner(iPlayer).any(lambda city: city.getPreviousCiv() == iGreece or city.getPreviousCiv() == iSparta or city.getPreviousCiv() == iMacedon):
			setPeriod(iEgypt, iPeriodPtolemaicEgypt)
	
	if iCiv == iZimbabwe:
		setPeriod(iZimbabwe, iPeriodRhodesia)

	if iCiv == iNumidia:
		setPeriod(iNumidia, iPeriodAlgeria)

	if iCiv == iOman:
		setPeriod(iOman, -1)

	if iCiv == iFunj:
		if year() > year(1900):
			setPeriod(iFunj, iPeriodSudan)

	if iCiv == iHausa:
		if year() > year(1900):
			setPeriod(iHausa, iPeriodNigeria)

	if iCiv == iGreece:
		if year() > year(500):
			setPeriod(iGreece, iPeriodModernGreece)
	
	if iCiv == iChina:
		if year() > year(dBirth[iMongols]):
			setPeriod(iChina, iPeriodMing)

		setPeriod(iManchuria, -1)

	if iCiv == iSpain:
		setPeriod(iSpain, iPeriodModernSpain)

	if iCiv == iEngland:
 		if player(iPlayer).getCurrentEra() == iIndustrial and city in cities.regions(rBritain, rIreland) and cities.regions(rBritain, rIreland).all(lambda city: city.getOwner() == iPlayer):
 			setPeriod(iEngland, iPeriodGreatBritain)
 		elif player(iPlayer).getCurrentEra() >= iRenaissance and city in cities.region(rBritain) and cities.region(rBritain).all(lambda city: city.getOwner() == iPlayer):
 			setPeriod(iEngland, iPeriodUnitedKingdom)
	
	if iCiv == iIndia:
		if year() < year(1900):
			setPeriod(iIndia, iPeriodMaratha)
		else:
			setPeriod(iIndia, -1)

	if iCiv == iTurks:
		if year() < year(1450):
			setPeriod(iTurks, iPeriodUzbeks)
	
	if iCiv == iCelts:
		setPeriod(iCelts, iPeriodInsularCelts)
	
	if iCiv == iArabia:
		setPeriod(iArabia, iPeriodHejaz)
		
	if iCiv == iMongols:
		setPeriod(iCiv, -1)

	if iCiv == iManchuria:
		setPeriod(iCiv, -1)
	
	if iCiv == iRus:
		# Ukraine needs a modern leader too
		setPeriod(iCiv, iPeriodUkraine)

	if iCiv == iBenin:
		if year() > year(1800):
			setPeriod(iBenin, iPeriodModernBenin)


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	iCiv = civ(iPlayer)
	iOwnerCiv = civ(iOwner)

	if iCiv == iSpain:
		if city.at(*tMadrid) and player(iSpain).getPeriod() == -1:
			setPeriod(iSpain, iPeriodCastile)

	if iCiv == iOttomans:
		if city.at(*tConstantinople):
			setPeriod(iOttomans, iPeriodOttomanConstantinople)

	if iCiv == iManchuria:
		chineseCities = cities.regions(rNorthChina, rSouthChina)
		if chineseCities.owner(iManchuria) > 1 and chineseCities.owner(iManchuria) > chineseCities.owner(iChina):
			setPeriod(iManchuria, iPeriodQing)

	if iCiv == iBuyids:
		if city.at(*tBabylon):
			setPeriod(iBuyids, iPeriodBuyidBaghdad)
			
	if iOwnerCiv == iByzantium:
		if iOwnerCiv == iByzantium or city.getPreviousCiv() == iByzantium:
			if bConquest and player(iByzantium).getNumCities() <= 3 and year() >= year(dBirth[iOttomans]) and player(iByzantium).getPeriod() == -1:
				setPeriod(iByzantium, iPeriodByzantineConstantinople)
	
	if iOwnerCiv == iCelts:
		if player(iCelts).getNumCities() > 0 and cities.core(iCelts).owner(iCelts).count() == 0:
			setPeriod(iCelts, iPeriodInsularCelts)

	if iCiv == iBoers:
		if cities.region(rCape).owner(iBoers).count() >= 4 and cities.regions(rCape).all(lambda city: city.getOwner() == iPlayer):
			setPeriod(iBoers, iPeriodSouthAfricaUnion)

	if iCiv == iZulu:
		if cities.region(rCape).owner(iZulu).count() >= 4 and cities.regions(rCape).all(lambda city: city.getOwner() == iPlayer):
			setPeriod(iZulu, iPeriodSouthAfricaUnion)
	
	if iCiv == iSouthAfrica:
		if cities.region(rCape).owner(iSouthAfrica).count() >= 4 and not player(iZulu).isExisting() and cities.regions(rCape).all(lambda city: city.getOwner() == iPlayer):
			setPeriod(iSouthAfrica, iPeriodSouthAfricaUnion)

	
	if iOwnerCiv == iTimurids: #Timmies become Mughals if they lose all Persian cities after 1500 and conquer India
		if player(iTimurids).getNumCities() > 0 and cities.regions(lIndia).owner(iTimurids).count() > 0 and year() > year(dBirth[iIran]):
			setPeriod(iTimurids, iPeriodMughals)

	
@handler("firstCity")
def onCityBuilt(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)

	if iOwnerCiv == iPhoenicia:
		if city.getRegionID in lEurope + lAfrica:
			setPeriod(iPhoenicia, iPeriodCarthage)


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)
	
	if bVassal:
		if iVassalCiv == iInca:
			setPeriod(iInca, iPeriodPeru)
		
		if iVassalCiv == iChina:
			if bCapitulated and iMasterCiv == iMongols:
				setPeriod(iMongols, iPeriodYuan)

		if iVassalCiv == iEgypt:
			if iMasterCiv in [iGreece, iRome, iSparta, iMacedon]:
				setPeriod(iEgypt, iPeriodPtolemaicEgypt)
			

@handler("capitalMoved")
def onCapitalMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)


	if iOwnerCiv == iOman:
		if city.getRegionID() == rSwahiliCoast:
			setPeriod(iOman, iPeriodZanzibar)

	if iOwnerCiv == iMacedon:
		if city.getRegionID() in [rPersia, rMesopotamia, rKhorasan, rLevant]:
			setPeriod(iMacedon, iPeriodSeleucids)

	if iOwnerCiv == iMisr:
		if city.getRegionID() == rEgypt:
			setPeriod(iMisr, iPeriodMisrEgypt)

	if iOwnerCiv == iGhorids:
		if city.getRegionID() == rHindustan:
			setPeriod(iGhorids, iPeriodDelhi)

	if iOwnerCiv == iArabia:
		if city.getRegionID() == rMesopotamia:
			setPeriod(iArabia, iPeriodArabiaMesopotamia)
	
	if iOwnerCiv == iPhoenicia:
		if city.getRegionID() in lEurope + lAfrica:
			setPeriod(iPhoenicia, iPeriodCarthage)
		else:
			setPeriod(iPhoenicia, -1)
	
	if iOwnerCiv == iNorse:
		if player(iOwner).getLastStateReligion() != -1:
			setPeriod(iNorse, getNorsePeriod(iOwner))
	
	if iOwnerCiv == iMoors:
		if player(iOwner).getCurrentEra() >= iIndustrial and city.getRegionID() != rIberia:
			setPeriod(iSpain, iPeriodModernSpain)
	
	if iOwnerCiv == iGoths:
		if city.getRegionID() == rIberia:
			setPeriod(iGoths, iPeriodVisigoths)
		elif city.getRegionID() == rItaly:
			setPeriod(iGoths, iPeriodOstrogoths)

	if iOwnerCiv == iVandals:
		if city.getRegionID() == rMaghreb:
			setPeriod(iVandals, iPeriodVandalAfrica)
	
	if iOwnerCiv == iGermania:
		if city.getRegionID() == rBritain:
			setPeriod(iGermania, iPeriodAngloSaxons)

	if iOwnerCiv == iScythia:
		if city.getRegionID() == rPonticSteppe:
			setPeriod(iScythia, iPeriodPonticScythia)



@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	iEra = player(iPlayer).getCurrentEra()
	iColumn = getColumn(iPlayer)
	tPlayer = team(iPlayer)
	
	if iCiv == iHausa:
		if iEra == iGlobal:
				setPeriod(iHausa, iPeriodNigeria)
		elif player(iCiv).getPeriod() == -1 and tPlayer.isHasTech(iDoctrine):
				setPeriod(iHausa, iPeriodSokoto)

	elif iCiv == iZimbabwe:
		if iEra == iDigital:
				setPeriod(iZimbabwe, -1)
		elif iEra == iClassical:
				if tPlayer.isHasTech(iGeneralship):
					setPeriod(iZimbabwe, iPeriodRozwi)
				elif player(iCiv).getPeriod() == -1:
					setPeriod(iZimbabwe, iPeriodMutapa)
	
	elif iCiv == iBuganda:
		if iEra == iGlobal:
				setPeriod(iBuganda, iPeriodUganda)
		elif tPlayer.isHasTech(iGeneralship):
				setPeriod(iBuganda, iPeriodBuganda)	


	elif iCiv == iDravidia:
		if iEra == iMedieval:
			setPeriod(iDravidia, iPeriodVijayanagara)

	elif iCiv == iSwahili:
		if iEra == iIndustrial:
			setPeriod(iSwahili, iPeriodTanzania)

	elif iCiv == iNubia:
		if iEra == iIndustrial and bResurrected:
			setPeriod(iNubia, iPeriodSouthSudan)
		elif iEra == iMedieval:
			setPeriod(iNubia, iPeriodMakuria)
    
	elif iCiv == iGreece:
		if iColumn >= 6:
			if not player(iSparta).isExisting():
				setPeriod(iGreece, iPeriodUnitedGreece)
			if  player(iSparta).isExisting() and cities.owner(iSparta).region(rGreece).none():
				setPeriod(iGreece, iPeriodUnitedGreece)

	elif iCiv == iSparta:
		if iColumn >= 6:
			if not player(iGreece).isExisting():
				setPeriod(iSparta, iPeriodUnitedGreece)
			if  player(iGreece).isExisting() and cities.owner(iGreece).region(rGreece).none():
				setPeriod(iSparta, iPeriodUnitedGreece)


	elif iCiv == iSpain:
		if iEra == iRenaissance:
			if player(iMoors).isExisting() and player(iMoors).getPeriod() == -1 and cities.owner(iMoors).region(rIberia).none():	
				setPeriod(iSpain, iPeriodModernSpain)
			if not player(iMoors).isExisting():
				setPeriod(iSpain, iPeriodModernSpain)
	
	elif iCiv == iFrance:
		if iEra == iIndustrial:
			setPeriod(iFrance, iPeriodNationalFrance)

	elif iCiv == iJapan:
		if iColumn == 13:
			setPeriod(iJapan, iPeriodMeiji)

	elif iCiv == iEngland:
 		if iEra == iRenaissance:
 			if cities.region(rBritain).all(lambda city: city.getOwner() == iPlayer):
 				setPeriod(iEngland, iPeriodUnitedKingdom)
 		
 		elif iEra == iIndustrial:
 			if cities.regions(rBritain, rIreland).all(lambda city: city.getOwner() == iPlayer):
 				setPeriod(iEngland, iPeriodGreatBritain)
 		
 		elif iEra == iGlobal:
 			if player(iPlayer).getPeriod() == iPeriodGreatBritain:
 				setPeriod(iEngland, iPeriodUnitedKingdom)
	
	elif iCiv == iInca:
		if player(iPlayer).getPeriod() == -1:
			if iEra == iRenaissance:
				setPeriod(iInca, iPeriodLateInca)
	
	elif iCiv == iItaly:
		if iEra == iIndustrial:
			setPeriod(iItaly, iPeriodModernItaly)
	
	elif iCiv == iGermany:
		if iEra == iDigital:
			setPeriod(iGermany, iPeriodModernGermany)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer, iReligion):
	iCiv = civ(iPlayer)
	
	# Aeons - Remove religion req because sometimes Egypt goes Zoroastrian
	if iCiv == iEgypt: #and iReligion >= 0: 
		if player(iPlayer).getPeriod() == iPeriodPtolemaicEgypt:
			setPeriod(iEgypt, -1)

	elif iCiv == iNorse and iReligion >= 0:
		setPeriod(iNorse, getNorsePeriod(iPlayer))
			
@handler("changeWar")
def onChangeWar(bWar, iPlayer, iOtherPlayer):
	if not bWar:
		if civ(iPlayer) == iEgypt and civ(iOtherPlayer) in [iGreece, iRome, iMacedon, iEgypt]:
			if cities.region(rEgypt).owner(iOtherPlayer):
				setPeriod(iEgypt, iPeriodPtolemaicEgypt)

def getNorsePeriod(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	
	if capital:
		if capital in cities.rectangle(tNorway): # Aeons - Loosen Norway conditions a bit
			return iPeriodNorway
		return iPeriodDenmark
	
	return -1