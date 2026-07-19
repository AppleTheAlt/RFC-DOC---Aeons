from Core import *
from Locations import *
from RFCUtils import *
from Events import handler
from Secession import *
from Civics import * #Aeons - Needed for immigration
#from Plague import * #Aeons - Needed for immigration plague spread


### CONSTANTS ###

dRelocatedCapitals = {
	(iChina, iMedieval): tBeijing,
	(iDravidia, iRenaissance): tVijayanagara,
	(iJapan, iIndustrial): tTokyo,
	(iNorse, iRenaissance): tCopenhagen,
	(iHolyRome, iRenaissance): tVienna,
	(iPoland, iRenaissance): tWarsaw,
	(iItaly, iIndustrial): tRome,
	(iIran, iIndustrial): tTehran,
}


### CITY ACQUIRED ###

@handler("cityAcquired")
def resetSlaves(iOwner, iPlayer, city):
	if player(iPlayer).canUseSlaves():
		freeSlaves(city, iPlayer)
	else:
		city.setFreeSpecialistCount(iSpecialistSlave, 0)
		

@handler("cityAcquired")
def resetAdminCenter(iOwner, iPlayer, city):
	if city.isCapital() and city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)


@handler("cityAcquired")
def restoreCapital(iOwner, iPlayer, city):
	if player(iPlayer).isHuman() or is_minor(iPlayer):
		return
	
	capital = plots.capital(iPlayer)
	
	if data.civs[civ(iPlayer)].iResurrections > 0 or player(iPlayer).getPeriod() != -1:
		capital = plots.respawnCapital(iPlayer)
		
	if at(city, capital):
		relocateCapital(iPlayer, city)


@handler("cityAcquired")
def resetNationalWonders(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade:
		for iNationalWonder in range(iNumBuildings):
			if iNationalWonder != iPalace and isNationalWonderClass(infos.building(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
				city.setHasRealBuilding(iNationalWonder, False)


@handler("cityAcquired")
def spreadTradingCompanyCulture(iOwner, iPlayer, city, bConquest, bTrade):
	if bTrade and civ(iPlayer) in lTradingCompanyCivs and city.getRegionID() in lAsia + lSubSaharanAfrica:
		for plot in plots.surrounding(city):
			if location(plot) == location(city):
				convertPlotCulture(plot, iPlayer, 51, False)
			elif plot.isCity():
				pass
			elif distance(plot, city) == 1:
				convertPlotCulture(plot, iPlayer, 65, True)
			elif pPlot.getOwner() == iPreviousOwner:
				convertPlotCulture(plot, iPlayer, 15, False)


@handler("cityAcquired")
def downgradeCottages(iOwner, iPlayer, city, bConquest, bTrade):
	if bConquest and player(iPlayer).getCurrentEra() <= iRenaissance:
		downgradeCityCottages(city)


### CITY ACQUIRED AND KEPT ###
	
@handler("cityAcquiredAndKept")
def spreadCultureOnConquest(iPlayer, city):
	for plot in plots.surrounding(city):
		if at(plot, city):
			convertTemporaryCulture(plot, iPlayer, 25, False)
		elif civ(plot) == city.getPreviousCiv():
			convertTemporaryCulture(plot, iPlayer, 50, True)
		else:
			convertTemporaryCulture(plot, iPlayer, 25, True)

@handler("cityAcquiredAndKept")
def revealCity(iPlayer, city):
	"""Sometimes birth flips can flip a city before its tile is revealed."""
	city.setRevealed(player(iPlayer).getTeam(), True)

### CITY BUILT ###

@handler("cityBuilt")
def clearMinorCulture(city):
	for iMinor in players.minor():
		plot(city).setCulture(iMinor, 0, True)


@handler("cityBuilt")
def spreadCulture(city):
	if not is_minor(city):
		spreadMajorCulture(city.getOwner(), location(city))


@handler("cityBuilt")
def updateFoundValues(city):
	if not is_minor(city) and player(city).getNumCities() <= 1:
		player(city).AI_updateFoundValues(False)


@handler("cityBuilt")
def createColonialDefenders(city):
	iPlayer = city.getOwner()
	if not player(iPlayer).isHuman():
		if civ(iPlayer) in dCivGroups[iCivGroupEurope] and city.getRegionID() not in lEurope:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


@handler("cityBuilt")
def americanPioneerAbility(city):
	iPlayer = city.getOwner()
	if civ(iPlayer) == iAmerica:
		if city.getRegionID() in lNorthAmerica:
			createGarrisons(city, iPlayer, 1)
			createRoleUnit(iPlayer, city, iWork, 1)


### CITY GIFTED ###
 
 
@handler("cityGifted")
def giftedCityDefenders(city):
 	if not player(city).isHuman():
 		iNumDefenders = max(2, 1 + player(city).getCurrentEra() / 2)
 		createGarrisons(city, city.getOwner(), iNumDefenders)

### COMBAT RESULT ###
		
@handler("combatResult")
def captureSlaves(winningUnit, losingUnit):
	if plot(winningUnit).isWater() and freeCargo(winningUnit, winningUnit) <= 0:
		return

	if civ(winningUnit) == iAztecs:
		captureUnit(losingUnit, winningUnit, iAztecSlave, 50)
		return

	
	iSlaveType = iSlave
	if civ(winningUnit) == iGhana:
		iSlaveType = iJonow
	if civ(winningUnit) == iBenin:
		iSlaveType = iBenineseSlave

	if civ(losingUnit) == iNative and winningUnit.getUnitType() == iBandeirante or winningUnit.getUnitType() == iSlaveHunter or winningUnit.getUnitType() == iAbambowa:
		if player(winningUnit).canUseSlaves():
			captureUnit(losingUnit, winningUnit, iSlaveType, 100)
			return
	
	# Can now capture slaves without compass.
	#if players.major().existing().none(lambda p: team(p).isHasTech(iCompass)):
	#	return
		
	if civ(losingUnit) == iNative:
		if civ(winningUnit) not in lBioNewWorld or any(data.dFirstContactConquerors.values()):
			if player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
				captureUnit(losingUnit, winningUnit, iSlaveType, 50)
				return

	# also enslave barbarians but at a lesser rate - Credit - Cross Overhaul
	if civ(losingUnit) == iBarbarian:

		if civ(winningUnit) == iGokturks:	#Gokturk UP - Won't capture slaves from barb light and heavy cavalry.
			if losingUnit.getUnitCombatType() == 2 or losingUnit.getUnitCombatType() == 3:
					return
		elif player(winningUnit).isSlavery() or player(winningUnit).isColonialSlavery():
			captureUnit(losingUnit, winningUnit, iSlaveType, 15)
			return

	# Small general chance of capturing slaves if slavery is enabled (eg. Roman, Middle Eastern slavery.)
	if player(winningUnit).isSlavery():
		#Can't capture slaves of same religion, unless pagan.
		if player(winningUnit).getStateReligion() > 0 and player(winningUnit).getStateReligion() == player(losingUnit).getStateReligion():
			return
		else:
			if winningUnit.getUnitType() == iBarbaryPirate: 
				captureUnit(losingUnit, winningUnit, iSlaveType, 100)
				return
			else:
				captureUnit(losingUnit, winningUnit, iSlaveType, 10)
				return


@handler("combatResult")
def mayanHolkanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iHolkan:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city and distance(winningUnit, city) <= 10:
				iFood = scale(5)
				city.changeFood(iFood)
				
				message(iWinner, 'TXT_KEY_MAYA_HOLKAN_EFFECT', adjective(losingUnit), losingUnit.getName(), iFood, city.getName())
				
				events.fireEvent("combatFood", iWinner, winningUnit, iFood)

@handler("combatResult")
def assegaiAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iAssegaiWielder:
		iWinner = winningUnit.getOwner()
		if player(iWinner).getNumCities() > 0:
			city = closestCity(winningUnit, iWinner)
			if city and distance(winningUnit, city) <= 10:
				iProduction = scale(5)
				city.changeProduction(iProduction)
				
				message(iWinner, 'TXT_KEY_ZIMBABWEAN_ASSEGAI_WIELDER_EFFECT', adjective(losingUnit), losingUnit.getName(), iProduction, city.getName())
				
				#events.fireEvent("combatFood", iWinner, winningUnit, iProduction)


@handler("combatResult")
def manchuBannermanAbility(winningUnit, losingUnit):
	if winningUnit.getUnitType() == iBannerman and not is_minor(winningUnit) and losingUnit.canFight():
		iWinner = winningUnit.getOwner()
		iLoser = losingUnit.getOwner()
		
		if is_minor(iLoser):
			return
		
		if player(iWinner).getPower() < player(iLoser).getPower():
			losingUnit.setDamage(losingUnit.maxHitPoints() * 8 / 10, iWinner)
			
			capturedUnit = makeUnit(iWinner, losingUnit.getUnitType(), winningUnit)
			capturedUnit.convert(losingUnit)
			capturedUnit.finishMoves()
			
			city = closestCity(losingUnit)
			
			message(iWinner, "TXT_KEY_MANCHU_BANNERMAN_EFFECT", adjective(iLoser), losingUnit.getName(), city.getName())
			message(iLoser, "TXT_KEY_MANCHU_BANNERMAN_EFFECT_TARGET", losingUnit.getName(), adjective(iWinner), city.getName())

# Aeons - Zulu UP: 50% chance to capture military units whose tech you haven't discovered
@handler("combatResult")
def zuluUP(winningUnit, losingUnit):
	if civ(winningUnit) == iZulu and losingUnit.canFight() and not team(player(winningUnit)).isHasTech(infos.unit(losingUnit).getPrereqAndTech()):
		iWinner = winningUnit.getOwner()
		iLoser = losingUnit.getOwner()
		
		if rand(0, 2) == 0: # 50/50 chance
			losingUnit.setDamage(losingUnit.maxHitPoints() * 8 / 10, iWinner)
			
			capturedUnit = makeUnit(iWinner, losingUnit.getUnitType(), winningUnit)
			capturedUnit.convert(losingUnit)
			capturedUnit.finishMoves()
			
			city = closestCity(losingUnit)
			
			message(iWinner, "TXT_KEY_ZULU_UP_EFFECT", adjective(iLoser), losingUnit.getName(), city.getName())
			message(iLoser, "TXT_KEY_ZULU_UP_EFFECT_TARGET", losingUnit.getName(), adjective(iWinner), city.getName())

# Aeons - Hausa UP: 50% chance to capture natives
@handler("combatResult")
def hausaUP(winningUnit, losingUnit):
	if civ(winningUnit) == iHausa and losingUnit.canFight() and civ(losingUnit) == iNative:
		iWinner = winningUnit.getOwner()
		iLoser = losingUnit.getOwner()
		
		if rand(0, 2) == 0: # 50/50 chance
			losingUnit.setDamage(losingUnit.maxHitPoints() * 8 / 10, iWinner)
			
			capturedUnit = makeUnit(iWinner, losingUnit.getUnitType(), winningUnit)
			capturedUnit.convert(losingUnit)
			capturedUnit.finishMoves()
			
			city = closestCity(losingUnit)
			
			message(iWinner, "TXT_KEY_HAUSA_UP_EFFECT", adjective(iLoser), losingUnit.getName(), city.getName())



### REVOLUTION ###

@handler("revolution")
def validateSlaves(iPlayer):
	if not player(iPlayer).canUseSlaves():
		if player(iPlayer).getImprovementCount(iSlavePlantation) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlavePlantation):
				plot.setImprovementType(iPlantation)
		
		if player(iPlayer).getImprovementCount(iSlaveMine) > 0:
			for plot in plots.owner(iPlayer).where(lambda plot: plot.getImprovementType() == iSlaveMine):
				plot.setImprovementType(iMine)
		
		for city in cities.owner(iPlayer):
			city.setFreeSpecialistCount(iSpecialistSlave, 0)
				
		for slave in units.owner(iPlayer).where(lambda unit: base_unit(unit) == iSlave):
			slave.kill(False, iPlayer)


### UNIT BUILT ###

@handler("unitBuilt")
def moveSlavesToNewWorld(city, unit):
	if base_unit(unit) == iSlave and city.getRegionID() in lEurope + [rMaghreb, rAnatolia] and not city.isHuman():	
		colony = cities.owner(iPlayer).regions(*(lAmerica + lSubSaharanAfrica)).random()
		if colony:
			move(unit, colony)


### CAPITAL MOVED ###

@handler("capitalMoved")
def resetAdminCenterOnPalaceBuilt(city):
	if city.isHasRealBuilding(iAdministrativeCenter):
		city.setHasRealBuilding(iAdministrativeCenter, False)



### PLOT FEATURE REMOVED ###


@handler("plotFeatureRemoved")
def brazilianMadeireiroAbility(plot, city, iFeature):
	dFeatureGold = defaultdict({
		iForest : 15,
		iSavanna : 15,
		iJungle : 20,
		iRainforest : 20,
	}, 0)
	
	if civ(plot) == iBrazil:
		iGold = dFeatureGold[iFeature]
		
		if iGold > 0:
			player(plot).changeGold(iGold)
			message(plot.getOwner(), 'TXT_KEY_DEFORESTATION_EVENT', infos.feature(iFeature).getText(), city.getName(), iGold, type=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.commerce(0).getButton(), location=plot)


### BEGIN GAME TURN ###

@handler("BeginGameTurn")
def checkImmigration(iGameTurn):
	#AEONS - Immigration now starts from year -1000
	if iGameTurn < year(-1000):
		return

	data.iImmigrationTimer -= 1
	
	if data.iImmigrationTimer == 0:
		immigration()
		data.iImmigrationTimer = turns(5 + rand(10)) # Aeons - immigration on average every 10 turns.


### TECH ACQUIRED ###

@handler("techAcquired")
def relocateCapitals(iTech, iTeam, iPlayer):
	if not player(iPlayer).isHuman():
		iCiv = civ(iPlayer)
		iEra = infos.tech(iTech).getEra()
		if (iCiv, iEra) in dRelocatedCapitals:
			relocateCapital(iPlayer, dRelocatedCapitals[iCiv, iEra])


### END GAME TURN ###

@handler("EndGameTurn")
def startTimedConquests():
	for iConqueror, tPlot in data.lTimedConquests:
		colonialConquest(iConqueror, tPlot)
	
	data.lTimedConquests = []


### BEGIN PLAYER TURN ###

@handler("setPlayerAlive")
def updateLastTurnAlive(iPlayer, bAlive):
	if turn() == scenarioStartTurn():
		return

	if not bAlive and not (player(iPlayer).isHuman() and autoplay()):
		data.civs[civ(iPlayer)].iLastTurnAlive = game.getGameTurn()

### INTEGRATE ###

@handler("playerIntegrate")
def secedeIntegratedPlayerCities(iPlayer1, iPlayer2):
	for city in cities.owner(iPlayer1):
		secedeCity(city, iPlayer2, 0, 0)

	


### IMPLEMENTATIONS ###

def isBribableUnit(iPlayer, unit):
	if not unit.canFight():
		return False
	
	if unit.isInvisible(player(iPlayer).getTeam(), False):
		return False
	
	if unit.getDomainType() != DomainTypes.DOMAIN_LAND:
		return False
	
	return True


def getPossibleBribes(iPlayer, location):
	iTreasury = player(iPlayer).getGold()
	targets = [(unit, infos.unit(unit).getProductionCost() * 3 / 2) for unit in units.at(location).owner(iBarbarian)]
	return [(unit, iCost) for unit, iCost in targets if isBribableUnit(iPlayer, unit) and iCost <= iTreasury]


def canBribeUnits(spy):
	if not player(spy).canHurry(1):
		return False
	
	if plot(spy).isOwned() and plot(spy).getOwner() != spy.getOwner():
		return False

	if spy.getMoves() >= spy.maxMoves(): 
		return False
		
	if not getPossibleBribes(spy.getOwner(), location(spy)):
		return False
	
	return True


def applyUnitBribes(iChoice, iPlayer, x, y):
	targets = getPossibleBribes(iPlayer, (x, y))
	unit, iCost = targets[iChoice]
	
	newUnit = makeUnit(iPlayer, unit.getUnitType(), closestCity(unit, owner=iPlayer))
	player(iPlayer).changeGold(-iCost)

	unit.kill(False, -1)
	
	if newUnit:
		interface.selectUnit(newUnit, True, True, False)


def doUnitBribes(spy):
	# only once per turn
	spy.finishMoves()
			
	# launch popup
	bribePopup = unit_bribe_popup.launcher()
	
	for unit, iCost in getPossibleBribes(spy.getOwner(), location(spy)):
		bribePopup.text().applyUnitBribes(unit.getName(), unit.currHitPoints(), unit.maxHitPoints(), iCost, button=unit.getButton())
	
	x, y = location(spy)
	bribePopup.cancel().launch(spy.getOwner(), x, y)

# AEONS - Immigration overhaul - No longer requires New World. More dynamic conditions.
def immigration():
	selectPlayers = players.major().existing().where(lambda p: not player(p).isBirthProtected())
	
	# Number of migraations is the total number of players * 2/3
	# In other words, with 40 players this is 20 migrations on average every 10 turns or so
	iNumMigrations = selectPlayers.count() / 2

	sourceCities = selectPlayers.cities().where(lambda city: city.getPopulation() > 1).lowest(iNumMigrations, getImmigrationValue)
	
	for sourceCity in sourceCities:
		iSourcePlayer = sourceCity.getOwner()

		
		iDistance = 999 # In other words, infinite...

		if player(iSourcePlayer).getCurrentEra() == iAncient:
			iDistance = 10
		elif player(iSourcePlayer).getCurrentEra() == iClassical:
			iDistance = 20
		elif player(iSourcePlayer).getCurrentEra() == iMedieval:
			iDistance = 20
		elif player(iSourcePlayer).getCurrentEra() == iRenaissance:
			iDistance = 50

		validPlayers = players.major().existing().where(lambda p: (team(player(sourceCity)).isOpenBorders(p) and team(player(sourceCity)).canContact(p)) or p == iSourcePlayer)
		targetCity = validPlayers.cities().where(lambda p: distance(p, sourceCity)<iDistance).maximum(getImmigrationValue)
		

		iTargetPlayer = targetCity.getOwner()	
		selectedTarget = targetCity
		selectedSource = sourceCity

		bInternalMigration = false
		bForcedKillMigrant = false
		#bBroughtPlague = false

		if iTargetPlayer == iSourcePlayer:
			bInternalMigration = true

		# If the target city doesn't have open borders, choose an internal city instead - encourages more internal migration in the early game.
		if not bInternalMigration:
			if not player(sourceCity).canExternalMigrate():	
				bForcedKillMigrant = true
			elif not player(targetCity).canExternalMigrate():
				selectedTarget = cities.owner(iSourcePlayer).maximum(getImmigrationValue)
				bInternalMigration = true


		# Cancel if same city or if immigration value difference isn't large enough.
		if selectedTarget.getID() == selectedSource.getID():
			continue
		if getImmigrationValue(selectedTarget) - getImmigrationValue(selectedSource) < 10:
			continue


		iTargetPlayer = selectedTarget.getOwner()
		iSourcePlayer = selectedSource.getOwner()

		iPopulation = getMigrantNum(selectedSource, iTargetPlayer)
	
		selectedSource.changePopulation(-iPopulation)


		if not bForcedKillMigrant:
			selectedTarget.changePopulation(iPopulation)
			
			# extra cottage growth for target city's vicinity
			for pCurrent in plots.surrounding(selectedTarget, radius=2):
				if pCurrent.getWorkingCity() == selectedTarget:
					pCurrent.changeUpgradeProgress(turns(10))
					
			# migration brings culture
			targetPlot = plot(selectedTarget)

			# It can also bring plagues...
			# Test this to make sure that this doesn't perpetuate plagues forever...
			#if selectedSource.isHasRealBuilding(iPlague) and not selectedTarget.isHasRealBuilding(iPlague):
			#	infectCity(selectedSource)
			#	bBroughtPlague = true

			iCultureChange = 0

			iCultureChange += targetPlot.getCulture(iTargetPlayer) / selectedTarget.getPopulation()
			targetPlot.changeCulture(iSourcePlayer, iCultureChange, False)

			iCultureChange = 0
			
			iCultureChange += selectedTarget.getCulture(iTargetPlayer) / selectedTarget.getPopulation()
			selectedTarget.changeCulture(iSourcePlayer, iCultureChange, False)
		
			# chance to spread religions in source city
			lReligions = [iReligion for iReligion in range(iNumReligions) if selectedSource.isHasReligion(iReligion) and not selectedTarget.isHasReligion(iReligion)]
			if player(iSourcePlayer).getStateReligion() in lReligions:
				lReligions.append(player(iSourcePlayer).getStateReligion())
		
			if rand(1, 10) <= len(lReligions):	# Aeons - Bring back religion immigration as 1/10, rather than 1/4.
				selectedTarget.setHasReligion(random_entry(lReligions), True, True, True)
			
			# Aeons - Boer UP: Get Trekker Specialsit
			if civ(iTargetPlayer) == iBoers:
				iNumTrekkers = selectedTarget.getFreeSpecialistCount(iSpecialistTrekker)
				selectedTarget.setFreeSpecialistCount(iSpecialistTrekker, iNumTrekkers+1)

			if bInternalMigration:
				message(iSourcePlayer, 'TXT_KEY_UP_INTERNAL_MIGRATION_AEONS', selectedSource.getName(), selectedTarget.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button='Art/Interface/Buttons/Actions/migrationbutton.dds', color=iYellow, location=selectedSource)


			else: 
				message(iSourcePlayer, 'TXT_KEY_UP_EMIGRATION_AEONS', selectedSource.getName(), selectedTarget.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button='Art/Interface/Buttons/Actions/emmigrationbutton.dds', color=iYellow, location=selectedSource)
				message(iTargetPlayer, 'TXT_KEY_UP_IMMIGRATION_AEONS', selectedSource.getName(), selectedTarget.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button='Art/Interface/Buttons/Actions/immigrationbutton.dds', color=iYellow, location=selectedTarget)


			#if bBroughtPlague:
			#	message(iTargetPlayer, 'TXT_KEY_UP_IMMIGRATION_PLAGUE', selectedSource.getName(), selectedTarget.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSettler).getButton(), color=iYellow, location=selectedTarget)


		if bForcedKillMigrant:
			iCultureChange = 0
			message(iSourcePlayer, 'TXT_KEY_UP_EMIGRATION_AEONS_DIRTY_TRAITORS', selectedSource.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.unit(iSpy).getButton(), color=iYellow, location=selectedSource)


		events.fireEvent("immigration", selectedSource, selectedTarget, iPopulation, iCultureChange)


def getMigrantNum(city, iTargetPlayer):
	iPopulation = 1
	if city.getPopulation() >= 9:
		iPopulation += 1
	if player(city).getCurrentEra() >= iIndustrial:
		iPopulation += 1
	#if player(city).getCurrentEra() >= iGlobal:
	#	iPopulation += 1

	# Boers UP: Double pop from migration
	#if civ(iTargetPlayer) == iBoers:	
	#		iPopulation *= 2

	if iPopulation >= city.getPopulation():
		iPopulation = city.getPopulation() - 1


	return iPopulation

def getImmigrationValue(city):
	iImmigrationDesire = city.immigrationDesire(true)
	return iImmigrationDesire

def getEmigrationValue(city):
	iImmigrationDesire = city.immigrationDesire(false)
	return iImmigrationDesire
	

### CHANGE STATE RELIGION ### Aeons

# Aeons - Remove religious UU's when changing religion and replace with normal variants
@handler("playerChangeStateReligion")
def replaceReligiousUnits(iPlayer):
	bFoundReligionFlipUnit = false
	for unit in units.owner(iPlayer): 
		if unit.getUnitType() == iCrusader or unit.getUnitType() == iHospitaller and not player(iPlayer).getStateReligion() == iCatholicism:
			if not bFoundReligionFlipUnit: message(iPlayer, "TXT_KEY_MESSAGE_RELIGION_FLIP_UNIT")
			tPlot = plot(unit)
			unit.kill(-1, False)
			bFoundReligionFlipUnit = true
			makeUnits(iPlayer, iLancer, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
		if unit.getUnitType() == iMujahid and not player(iPlayer).getStateReligion() == iIslam:
			if not bFoundReligionFlipUnit: message(iPlayer, "TXT_KEY_MESSAGE_RELIGION_FLIP_UNIT")
			tPlot = plot(unit)
			unit.kill(-1, False)
			makeUnits(iPlayer, iHeavySwordsman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			bFoundReligionFlipUnit = true
		if unit.getUnitType() == iKshatriya and not player(iPlayer).getStateReligion() == iHinduism:
			if not bFoundReligionFlipUnit: message(iPlayer, "TXT_KEY_MESSAGE_RELIGION_FLIP_UNIT")
			tPlot = plot(unit)
			unit.kill(-1, False)
			makeUnits(iPlayer, iShortbowman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			bFoundReligionFlipUnit = true
		if unit.getUnitType() == iWarriorMonk and not player(iPlayer).getStateReligion() == iBuddhism:
			if not bFoundReligionFlipUnit: message(iPlayer, "TXT_KEY_MESSAGE_RELIGION_FLIP_UNIT")
			tPlot = plot(unit)
			unit.kill(-1, False)
			makeUnits(iPlayer, iSwordsman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			bFoundReligionFlipUnit = true
		if unit.getUnitType() == iFidai and not player(iPlayer).getStateReligion() == iShia:
			if not bFoundReligionFlipUnit: message(iPlayer, "TXT_KEY_MESSAGE_RELIGION_FLIP_UNIT")
			tPlot = plot(unit)
			unit.kill(-1, False)
			makeUnits(iPlayer, iSwordsman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			bFoundReligionFlipUnit = true


### AEONS - CHANGE WAR ###

# Aeons - Release vassals who declare war on their overlord
@handler("changeWar")
def independenceWar(bWar, iAttacker, iDefender, bFromDefensivePact):
	if team(iAttacker).isVassal(player(iDefender).getTeam()):
		team(iAttacker).setVassal(iDefender, False, False)
		message(iAttacker, 'TXT_KEY_INDEPENDENCE_WAR', adjective(iDefender))
		message(iDefender, 'TXT_KEY_INDEPENDENCE_WAR_DEFENDER', adjective(self.iPlayer))


### POPUPS ###

unit_bribe_popup = popup.text("TXT_KEY_BRIBE_UNITS_POPUP") \
						.selection(applyUnitBribes, "TXT_KEY_BRIBE_UNITS_BUTTON") \
						.cancel("TXT_KEY_BRIBE_UNITS_BUTTON_NONE") \
						.build()