from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from Core import periodic as core_periodic
from StoredData import data # edead
import Stability # Aeons - For Funj
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler

from Locations import *
from Core import *


#Free camel lancer with each conquered city
@handler("cityAcquired")
def MoroccanPower(iOwner, iPlayer, city, bConquest):
 	if civ(iPlayer) == iMorocco and bConquest and player(iPlayer).getCurrentEra() < iRenaissance:
 		makeUnits(iMorocco, iCamelLancer, city, 1, UnitAITypes.UNITAI_ATTACK_CITY)

@handler("cityAcquired")
def ghoridUP(iOwner, iPlayer, city):
	if civ(iPlayer) != iGhorids:
		return

	iStateReligion = player(iGhorids).getStateReligion()
	for iReligion in range(iNumReligions):
			if iReligion != iStateReligion and city.isHasReligion(iReligion) and city.getID() != game.getHolyCity(iReligion).getID():		
					removeReligion(city, iReligion)
					player(iPlayer).changeGold(50)

@handler("cityAcquired") #Free Flotilla with each conquered city.
def VandalPower(iOwner, iPlayer, city, bConquest):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iVandals and bConquest and iEra < iMedieval:
		if city.plot().isCoastalLand():
			makeUnits(iVandals, iFlotilla, city, 1, UnitAITypes.UNITAI_SETTLER_SEA)


@handler("cityAcquired") #2 free companions when you conquer a city.
def MacedonianPower(iOwner, iPlayer, city, bConquest):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMacedon and bConquest and iEra < iMedieval:
		makeUnits(iMacedon, iCompanion, city, 2, UnitAITypes.UNITAI_ATTACK_CITY)


@handler("cityAcquired") # Next tech comes with a bonus tech after conquering a city until the medieval era
def babylonianPower(iOwner, iPlayer, city, bConquest):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iBabylonia and bConquest and iEra < iMedieval:
		player(city).setFreeTechsOnDiscovery(1)


@handler("firstCity")
def initSumerianUP(city):
	# Sumerian UP: receive a free tech after discovering the first five techs
	iCivilization = civ(city)
	if iCivilization == iSumeria:
		player(city).setFreeTechsOnDiscovery(5)

@handler("BeginGameTurn")
def funjUPStartTurn():
	if stability(slot(iFunj)) == iStabilityStable or stability(slot(iFunj)) == iStabilitySolid:
		player(iFunj).setFreeTechsOnDiscovery(1)
	else:
		player(iFunj).setFreeTechsOnDiscovery(0)

@handler("EndGameTurn")
def funjUPEndTurn():
	if stability(slot(iFunj)) == iStabilityStable or stability(slot(iFunj)) == iStabilitySolid:
		player(iFunj).setFreeTechsOnDiscovery(1)
	else:
		player(iFunj).setFreeTechsOnDiscovery(0)

@handler("techAcquired")
def funjUPTechGain(iTech, iTeam, iPlayer):
    if civ(iPlayer) == iFunj and player(iPlayer).isHuman():
		if stability(slot(iFunj)) == iStabilityStable or stability(slot(iFunj)) == iStabilitySolid:
			player(iFunj).setFreeTechsOnDiscovery(1)
		else:
			player(iFunj).setFreeTechsOnDiscovery(0)



@handler("cityAcquired")
def arabianUP(iOwner, iPlayer, city):
	if civ(iPlayer) != iArabia:
		return

	iStateReligion = player(iArabia).getStateReligion()

	if iStateReligion >= 0:
		if not city.isHasReligion(iStateReligion):
			city.spreadReligion(iStateReligion)
		if not city.hasBuilding(temple(iStateReligion)):
			city.setHasRealBuilding(temple(iStateReligion), True)


@handler("cityAcquired")
def mongolUP(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) != iMongols:
		return
	
	if not bConquest:
		return
		
	if player(iPlayer).isHuman():
		return

	if city.getPopulation() >= 7:
		makeUnits(iMongols, iKeshik, city, 2, UnitAITypes.UNITAI_ATTACK_CITY)
	elif city.getPopulation() >= 4:
		makeUnit(iMongols, iKeshik, city, UnitAITypes.UNITAI_ATTACK_CITY)

	if city.getPopulation() >= 4:
		message(slot(iMongols), 'TXT_KEY_UP_MONGOL_HORDE')


#Gothic UP, gain money from defeating units.
@handler("combatResult")
def GothUP(winningUnit, losingUnit):
	iWinner = winningUnit.getOwner()
	if (civ(iWinner) == iGoths) or winningUnit.getUnitType() == iRozwiWarrior:
		iGold = scale(infos.unit(losingUnit).getProductionCost() / 3)
		player(iWinner).changeGold(iGold)
		message(iWinner, 'TXT_KEY_GOTH_VICTORY_UP', iGold, adjective(losingUnit), losingUnit.getName())
			
		events.fireEvent("combatGold", iWinner, iGold)



#Huns UP - Gain double gold from city conquest.
@handler("cityCaptureGold")
def HunsUP(city, iPlayer, iGold):
	if iGold > 0:
		player(iPlayer).changeGold(iGold)



# Aeons - Hausa UP: Native Spawn within borders.
@handler("BeginGameTurn")
def hausaNativeSpawn():
	iEra = player(iHausa).getCurrentEra()
	if iEra <= iIndustrial:
		for city in cities.owner(player(iHausa)):
			spawnPlot = plots.surrounding(city).without(city).land().passable().no_enemies(iNative).random()
			iUnitType = iLightSwordsman
			iUnitTypeRange = iArcher
			iUnitTypeSpears = iSpearman
			if(year() >= year(1800)):
				iUnitType = iArquebusier
				iUnitTypeRange = iArquebusier
				iUnitTypeSpears = iPikeman
			elif(year() >= year(1600)):
				iUnitType = iHeavySwordsman
				iUnitTypeRange = iLongbowman
				iUnitTypeSpears = iHeavySpearman
			elif(year() >= year(1300)):
				iUnitType = iSwordsman
				iUnitTypeRange = iShortbowman
			if(rand(turns(15)) == 1):
				created_unit = makeUnit(iNative, iUnitType, spawnPlot, UnitAITypes.UNITAI_ATTACK)
				set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_HAUSA")
			elif(rand(turns(15))  == 1):
				created_unit = makeUnit(iNative, iUnitTypeRange, spawnPlot, UnitAITypes.UNITAI_ATTACK)
				set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_HAUSA")
			elif(rand(turns(15))  == 1):
				created_unit = makeUnit(iNative, iUnitTypeSpears, spawnPlot, UnitAITypes.UNITAI_ATTACK)
				set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_HAUSA")


@handler("combatResult")
def norseUP(winningUnit, losingUnit):
	iWinner = winningUnit.getOwner()
	if (civ(iWinner) == iNorse and year() <= year(1500)) or winningUnit.getUnitType() == iCorsair or winningUnit.getUnitType() == iBaghlah or winningUnit.getUnitType() == iPirogue:
		if infos.unit(losingUnit).getDomainType() == DomainTypes.DOMAIN_SEA:
			iGold = scale(infos.unit(losingUnit).getProductionCost() / 2)
			player(iWinner).changeGold(iGold)
			message(iWinner, 'TXT_KEY_NORSE_NAVAL_UP', iGold, adjective(losingUnit), losingUnit.getName())
			
			events.fireEvent("combatGold", iWinner, iGold)

#Songhai UP: Great Engineer points in capital when you defeat a unit next to a river.
@handler("combatResult")
def songhaiUP(winningUnit, losingUnit):
	iWinner = winningUnit.getOwner()
	if (civ(iWinner) == iSonghai and losingUnit.plot().isRiver()):
		city = capital(winningUnit)
		if city:
			iGreatPeoplePoints = 12
				
			city.changeGreatPeopleProgress(iGreatPeoplePoints)
			city.changeGreatPeopleUnitProgress(iGreatEngineer, iGreatPeoplePoints)

#Ashanti UP: Culture in capital from losing units
@handler("combatResult")
def ashantiUP(winningUnit, losingUnit):
	iLoser = losingUnit.getOwner()
	if (civ(iLoser) == iAshanti):
		city = cities.owner(player(iLoser)).building(iPalace).one()
		if city:
			iCost = infos.unit(losingUnit).getProductionCost()
			city.changeCulture(city.getOwner(), iCost, True)

# Jerusalem UP: receives 50% of building cost as culture when completing catholic buildings or wonders.
@handler("buildingBuilt")
def jerusalemUP(city, iBuilding):
	if civ(city) == iJerusalem:
		if iCatholicism in [infos.building(iBuilding).getPrereqReligion(), infos.building(iBuilding).getOrPrereqReligion()]:
			iCost = player(city).getBuildingProductionNeeded(iBuilding)
			city.changeCulture(city.getOwner(), iCost * 2, True)


# Timurid UP: receives 50% of building cost as culture when building is completed
@handler("buildingBuilt")
def mughalUP(city, iBuilding):
	if civ(city) == iTimurids:
		iCost = player(city).getBuildingProductionNeeded(iBuilding)
		city.changeCulture(city.getOwner(), iCost / 2, True)

# Numidian UP: gain 10 food when a unit is produced, until the medieval era.
@handler("unitBuilt")
def numidianUP(city, iUnit):
	iPlayer = civ(city)
	iEra = player(iPlayer).getCurrentEra()
	if iPlayer == iNumidia and iEra < iMedieval:
		city.changeFood(scale(10))

# Scythian UP: Gain an extra Aspabarata every time you build a cavalry unit.
@handler("unitBuilt")
def scythianUP(city, iUnit):
	iPlayer = civ(city)
	iEra = player(iPlayer).getCurrentEra()
	if iPlayer == iScythia and iEra < iMedieval:
		if infos.unit(iUnit).getUnitCombatType() == UnitCombatTypes.UNITCOMBAT_LIGHT_CAVALRY or infos.unit(iUnit).getUnitCombatType() == UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY:
			makeUnit(iScythia, iAspabarata, city, UnitAITypes.UNITAI_ATTACK_CITY)


@handler("BeginGameTurn")
def resetBabylonianPower():
	data.bBabyloniaTechReceived = False


@handler("cityAcquired")
def colombianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if city in cities.regions(*(lCentralAmerica + lSouthAmerica)):
			city.setOccupationTimer(0)


@handler("techAcquired")
def mayanPower(iTech, iTeam, iPlayer):
	iEra = player(iPlayer).getCurrentEra()
	if civ(iPlayer) == iMaya and iEra < iMedieval:
		iNumCities = player(iPlayer).getNumCities()
		if iNumCities > 0:
			iFood = scale(20) / iNumCities
			for city in cities.owner(iPlayer):
				city.changeFood(iFood)
			
			message(iPlayer, 'TXT_KEY_MAYA_UP_EFFECT', infos.tech(iTech).getText(), iFood)


@handler("changeWar")
def resetMongolPower(bWar, iTeam, iOtherTeam):
	if not bWar and iMongols in civs.of(iTeam, iOtherTeam):
		for city in cities.owner(iMongols):
			city.setMongolUP(False)


@handler("improvementBuilt")
def americanImprovementPower(iImprovement, x, y):
	if scenarioStart():
		return
	improved = plot(x, y)
	if iImprovement >= 0 and improved.isOwned() and civ(improved) == iAmerica and not improved.isWater():
		if improved.getBonusType(improved.getTeam()) >= 0 and infos.improvement(iImprovement).isImprovementBonusTrade(improved.getBonusType(improved.getTeam())) and not infos.improvement(iImprovement).isActsAsCity():
			improved_city = improved.getWorkingCity()
			if not improved_city or improved_city.isNone():
				closest = closestCity(improved, owner=improved.getOwner())
				if closest and not closest.isNone() and distance(closest, improved) <= 3:
					improved_city = closest
			
			if improved_city and not improved_city.isNone():
				improved_city.changePopulation(1)
				improved_city.changeHappinessTimer(turns(10))
				
				message(improved.getOwner(), "TXT_KEY_UP_MANIFEST_DESTINY_IMPROVEMENT", infos.bonus(improved.getBonusType(improved.getTeam())).getText(), improved_city.getName())


@handler("immigration")
def americanImmigrationPower(_, city):
	if civ(city) == iAmerica:
		city.changePopulation(1)
		city.changeHappinessTimer(turns(10))
		
		message(city.getOwner(), "TXT_KEY_UP_MANIFEST_DESTINY_IMMIGRATION", city.getName())


@handler("cityAcquired")
def assyrianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iAssyria and bConquest:
		city.setOccupationTimer(0)

@handler("unitSpreadReligionAttempt")
def judahPower(unit, iReligion, bSuccess):
	if civ(unit.getOwner()) == iJudah and bSuccess:
		spread_city = city(unit)
		capital_city = capital(unit)
		if spread_city and capital_city:
			if(iReligion == iJudaism):
				capital_city.changeCulture(capital_city.getOwner(), 500, True)
				


@handler("unitSpreadReligionAttempt")
def kushanPower(unit, iReligion, bSuccess):
	if civ(unit.getOwner()) == iKushans and bSuccess:
		spread_city = city(unit)
		capital_city = capital(unit)
		if spread_city and capital_city:
			if player(spread_city.getOwner()).getStateReligion() != iReligion:
				iGold = scale(20 + distance(capital_city, spread_city))
				message(unit.getOwner(), "TXT_KEY_UP_SYNCRETISM_EFFECT", iGold, infos.religion(iReligion).getText(), spread_city.getName(), location=spread_city, button=infos.religion(iReligion).getButton())
				player(unit.getOwner()).changeGold(iGold)

@handler("unitPillage")
def tatarPillagePower(unit, iImprovement):
	if civ(unit.getOwner()) == iTatars and iImprovement >= 0:
		unit.changeExperience(1, 1000, True, False, True)


@handler("unitCaptured")
def tatarCapturePower(iOwner, iUnit, unit):
	iPlayer = unit.getOwner()
	if civ(iPlayer) == iTatars:
		iGold = scale(20)
		message(iPlayer, "TXT_KEY_UP_DESPOILMENT_EFFECT", iGold, adjective(iOwner), unit.getName(), location=unit, button=unit.getButton())
		player(iPlayer).changeGold(iGold)
		
		events.fireEvent("combatGold", iPlayer, iGold)
