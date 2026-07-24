from Core import *
from Civilizations import *
from DynamicCivs import *
from Locations import *
from RFCUtils import *
from Slots import *
from Scenarios import *
from Periods import * # Aeons - For dynamic Byzantium spawn
from Files import *
from Periods import *

from Events import events, handler
from Collapse import completeCollapse
from Popups import popup

import Logging as log

import BugCore
import CvScreensInterface


MainOpt = BugCore.game.MainInterface


lExpandedFlipCivs = [
	#iByzantium
]

lExpansionCivs = [
	iPersia,
	iRome,
	iMacedon,
	iKushans,
	iTurks,
	iArabia,
	iMongols,
	iTimurids,
	iOttomans,
	iBuyids,
	iSamanids,
	iGhorids,
	iManchuria,
]

# Aeons - These civs can only spawn if their birth area is empty - These are essentially civs that must spawn from the ground up
lNoCitySpawns = [
	iGhana,
	iHausa,
	iBenin,
	iSomalia,
	iSwahili,
	iBuganda,
	iZimbabwe,
	iCongo,
	iKatanga,
	iAshanti,
]

#Aeons - independence civs list expanded considerably
lIndependenceCivs = [
	iByzantium,
	iTatars,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iAustralia,
	iCanada,
	iFrance,
	iTimurids,
	iGhorids,
	iBuyids,
	iMoors,
	iMisr,
	iSouthAfrica,
]

lDynamicReligionCivs = [
	iByzantium,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iAustralia,
	iCanada,
	iSouthAfrica
]

lInvasionCivs = [
	iOttomans,
]

dClearedForBirth = {
	iIndia: iHarappa,
	iGreece: iMycenae,
	iByzantium: iGreece,
	iItaly: iRome,
	iAztecs: iToltecs,
	iRussia: iRus,
	iMexico: iAztecs,
	iBelgium: iNetherlands,
	iParthia: iPersia,
	iBuyids: iParthia,
	iSpain: iGoths,
	iMoors: iGoths,
	iArmenia: iMacedon,	# Macedon can destroy a player Armenia or Parthia...
	iParthia: iMacedon,
}

lAlwaysClear = [
	iHarappa,
	iToltecs,
]

lBirthWars = [
	(iPersia, iElam),
	(iMacedon, iSparta),
	(iMacedon, iGreece),
	(iArabia, iEgypt),
	(iArabia, iBabylonia),
	(iArabia, iPersia),
	(iMongols, iChina),
	(iOttomans, iByzantium),
	(iManchuria, iChina),
	(iParthia, iMacedon),
	(iBuyids, iArabia),
	(iSamanids, iArabia),
	(iSamanids, iPersia),
	(iTurks, iArabia),
	(iTurks, iBuyids),
	(iTurks, iSamanids),
	(iTurks, iGhorids),
	(iSouthAfrica, iBoers),
	(iSouthAfrica, iZulu),
]


### Event Handlers ###


@handler("BeginGameTurn")
def showDawnOfMan(iGameTurn):
	if iGameTurn == scenarioStartTurn() and game.getAIAutoPlay() > 0 and data.iBeforeObserverSlot == -1:
		CvScreensInterface.dawnOfMan.interfaceScreen()
			

@handler("GameStart")
def initBirths():
	data.births = [Birth(iCiv) for iCiv in lBirthOrder]
	
	for birth in data.births:		
		birth.check()


@handler("GameStart")
def initCamera():
	city = capital(active())
	if city:
		unit = units.at(city).owner(active()).land().first()
		if unit:
			interface.selectUnit(unit, True, False, False)
			
		plot(city).cameraLookAt()
		return
	plots.capital(active()).cameraLookAt()


@handler("GameStart")
def cleanupGreatWall():
 	getScenario().greatWall.cleanup()

@handler("BeginGameTurn")
def checkBirths():
	for birth in data.births:
		birth.check()

@handler("playerCivAssigned")
def updateMapsOnActive(iPlayer, iCivilization):
	if iCivilization in lBirthOrder:
		applyMaps(iCivilization)


@handler("periodChange")
def updateMapsOnPeriodChange(iCivilization, iPeriod):
	applyMaps(iCivilization, iPeriod)

@handler("changeWar")
def ensureAdditionalDefenders(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	iNumDefenders = 1 + (player(iDefender).getCurrentEra() + 1) / 2
	for city in cities.owner(iDefender).where(lambda city: plot(city).getBirthProtected() == iDefender):
		defenders = ensureDefenders(iDefender, city, iNumDefenders)
		for defender in defenders:
			mission(defender, MissionTypes.MISSION_FORTIFY)


@handler("changeWar")
def spawnWarUnits(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iDefender).isBirthProtected():
		return
		
	if team(iAttacker).isAVassal():
		return
		
	city = capital(iDefender)
	
	if city:
		createRoleUnits(iDefender, city, getAdditionalUnits(iDefender))
		for iUnit, iAmount in getSpecificAdditionalUnits(iDefender):
			makeUnits(iDefender, iUnit, city, iAmount)


@handler("changeWar")
def balanceMilitary(bWar, iAttacker, iDefender, bFromDefensivePact):
	if not bWar:
		return
	
	if bFromDefensivePact:
		return
	
	if not player(iAttacker).isHuman():
		return
	
	if player(iDefender).isHuman():
		return

	if not player(iDefender).isBirthProtected():
		return
	
	iAttackerPower = player(iAttacker).getPower()
	iDefenderPower = player(iDefender).getPower()
	
	if not iAttackerPower:
		return
	
	iPowerRatioThreshold = player(iAttacker).isHuman() and 80 or 50
	iPowerRatio = 100 * iDefenderPower / iAttackerPower
	
	iMaxAdditionalPower = 50
	
	if iPowerRatio < iPowerRatioThreshold:
		iPowerRatioDifference = iPowerRatioThreshold - iPowerRatio
		iPowerRequired = iPowerRatioDifference * iAttackerPower / 100
		
		iPowerRequired = min(iPowerRequired, iMaxAdditionalPower * iDefenderPower / 100)
		
		additionalUnits = getAdditionalUnits(iDefender)
		iUnitsPower = sum(infos.unit(iUnit).getPowerValue() * iAmount for iRole, iAmount in additionalUnits for iUnit, _ in getUnitsForRole(iDefender, iRole))
		
		specificAdditionalUnits = getSpecificAdditionalUnits(iDefender)
		iUnitsPower += sum(infos.unit(iUnit).getPowerValue() * iAmount for iUnit, iAmount in specificAdditionalUnits)
		
		iAdditionalUnitsRequired = iUnitsPower > 0 and iPowerRequired / iUnitsPower or 1
		
		for _ in range(iAdditionalUnitsRequired):
			createRoleUnits(iDefender, capital(iDefender), additionalUnits).promotion(iVolunteer)
			for iUnit, iAmount in specificAdditionalUnits:
				lExperiences = [iRoleExperience for iRole, iRoleExperience in dStartingExperience[iDefender].items() if isUnitOfRole(iUnit, iRole)]
				iExperience = lExperiences and max(lExperiences) or 0
				makeUnits(iDefender, iUnit, capital(iDefender), iAmount).experience(iExperience).promotion(iVolunteer)


@handler("changeWar")
def moveOutAttackers(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if not player(iDefender).isBirthProtected():
		return
	
	aroundCities = cities.owner(iDefender).plots().expand(2)
	birthProtected = plots.all().where(lambda p: p.getBirthProtected() == iDefender and not p.isPlayerCore(iAttacker) and not p.getOwner() == iAttacker)
	for plot in aroundCities.including(birthProtected):
		attackers = units.at(plot).owner(iAttacker)
		if attackers:
			destination = cities.owner(iAttacker).closest(plot)
			for unit in attackers:
				if destination:
					move(unit, destination)
				else:
					unit.kill(-1, False)
			
			if destination:
				message(iAttacker, "TXT_KEY_MESSAGE_ATTACKERS_EXPELLED", attackers.count(), adjective(iDefender), city(destination).getName(), button=attackers.first().getButton(), location=plot)


@handler("changeWar")
def createExpansionArmies(bWar, iAttacker, iDefender):
	if not bWar:
		return
	
	if player(iAttacker).isHuman():
		return
		
	if player(iDefender).isBirthProtected():
		return
	
	if is_minor(iDefender):
		return
	
	attackerCities = cities.owner(iAttacker)
	defenderCities = cities.owner(iDefender)
	expansionCities = defenderCities.where(lambda city: plot(city).getExpansion() == iAttacker)
	
	bLessPowerful = player(iAttacker).getPower() < player(iDefender).getPower()
	
	if expansionCities and attackerCities:
		target, attacker_closest = expansionCities.closest_pair(attackerCities)
		defender_closest = defenderCities.closest(attacker_closest)
		
		iDistance = player(iDefender).isHuman() and 3 or 2
		spawn = possibleSpawnsBetween(attacker_closest, defender_closest, iDistance).closest(defender_closest)
		
		iExtraAI = 0
		iExtraTargets = 0
		if bLessPowerful and not player(iDefender).isHuman():
			iExtraTargets = expansionCities.count()-1
			
			if not player(iAttacker).isHuman():
				iExtraAI = 1

		createExpansionUnits(iAttacker, iDefender, spawn, defender_closest, iExtraAI, iExtraTargets)

def createExpansionUnits(iAttacker, iDefender, tile, closest, iExtraAI, iExtraTargets):
		
	dExpansionUnits = {
		iCityAttack: 2 + iExtraAI + iExtraTargets,
		iSiege: 1 + 2*iExtraAI + iExtraTargets,
	}
	createRoleUnits(iAttacker, tile, dExpansionUnits.items()).promotion(iVolunteer)
	
	message(iDefender, "TXT_KEY_MESSAGE_EXPANSION_UNITS", player(iAttacker).getCivilizationDescription(0), closest.getName(), color=iRed, location=tile, button=infos.civ(player(iAttacker).getCivilizationType()).getButton())

def deleteExpansionUnits(iPlayer):
	if players.major().existing().any(lambda p: team(player(iPlayer)).isAtWar(player(p).getTeam())):
		return
	
	if players.minor().cities().any(lambda city: plot_(city).getExpansion() == iPlayer):
		return
	
	for unit in units.owner(iPlayer).where(lambda u: u.isHasPromotion(iVolunteer)):
		unit.kill(False, -1)

@handler("changeWar")
def endExpansionOnPeace(bWar, iPlayer1, iPlayer2):
	if not bWar:
		for plot in plots.owner(iPlayer1).where(lambda plot: plot.getExpansion() == iPlayer2):
			plot.resetExpansion()
		
		for plot in plots.owner(iPlayer2).where(lambda plot: plot.getExpansion() == iPlayer1):
			plot.resetExpansion()

		deleteExpansionUnits(iPlayer1)
		deleteExpansionUnits(iPlayer2)


#@handler("collapse")
def endExpansionOnCollapse(iPlayer):
	for plot in plots.all().where(lambda plot: plot.getExpansion() == iPlayer):
		plot.resetExpansion()


@handler("firstCity")
def createStartingWorkers(city):
	iPlayer = city.getOwner()
	iNumStartingWorkers = dStartingUnits[iPlayer].get(iWork, 0)
	
	if iNumStartingWorkers > 0:
		createRoleUnit(iPlayer, city, iWork, iNumStartingWorkers)
	

@handler("firstCity")
def createInvaderSettlers(city):
	iPlayer = city.getOwner()
	if not civ(iPlayer) in lInvasionCivs:
		return
	
	iNumSettlers = dStartingUnits[iPlayer].get(iSettler, 0)
	if iNumSettlers > 0:
		createSettlers(iPlayer, iNumSettlers, bGrantCapital=False)


@handler("firstCity")
def restorePreservedWonders(city):
	while data.players[city.getOwner()].lPreservedWonders:
		iWonder = data.players[city.getOwner()].lPreservedWonders.pop(0)
		if city.isValidBuildingLocation(iWonder):
			city.setHasRealBuilding(iWonder, True)


@handler("playerDestroyed")
def preserveCivilizationAttributes(iPlayer):
	iCiv = civ(iPlayer)
	data.civs[iCiv].iGreatGeneralsCreated = player(iPlayer).getGreatGeneralsCreated()
	data.civs[iCiv].iGreatPeopleCreated = player(iPlayer).getGreatPeopleCreated()
	data.civs[iCiv].iGreatSpiesCreated = player(iPlayer).getGreatSpiesCreated()
	data.civs[iCiv].iNumUnitGoldenAges = player(iPlayer).getNumUnitGoldenAges()
	

### MAPS ###


def applyMaps(iCivilization, iPeriod=-1):
	for p in plots.all().land():
		p.setSettlerValue(iCivilization, 0)
		p.setWarValue(iCivilization, 0)

	for (x, y), iValue in FileMap.read("Settler/%s.csv" % civ_name(iCivilization)):
		if iValue and not plot(x, y).isWater():
			plot(x, y).setSettlerValue(iCivilization, iValue)

	for (x, y), iValue in FileMap.read("War/%s.csv" % civ_name(iCivilization)):
		if iValue and not plot(x, y).isWater():
			plot(x, y).setWarValue(iCivilization, iValue)
	
	if iPeriod != -1:
		for (x, y), iValue in FileMap.read("Settler/Period/%s.csv" % dPeriodNames[iPeriod], bIgnoreMissing=True):
			if not plot(x, y).isWater():
				plot(x, y).setSettlerValue(iCivilization, iValue)
				
		for (x, y), iValue in FileMap.read("War/Period/%s.csv" % dPeriodNames[iPeriod], bIgnoreMissing=True):
			if not plot(x, y).isWater():
				plot(x, y).setWarValue(iCivilization, iValue)
		
def initMaps():
	for iCivilization in lBirthOrder:
		applyMaps(iCivilization)


### BIRTH ###

def getBirth(iCiv):
	return next(birth for birth in data.births if birth.iCiv == iCiv)
	


class Birth(object):

	def __init__(self, iCiv):
		self.iCiv = iCiv
		self.iTurn = year(dBirth[iCiv])
		
		self.iPlayer = None
		self.area = None
		
		self.civ = next((civ for civ in lCivilizations if civ.iCiv == self.iCiv), Civilization(self.iCiv))
		
		self.location = location(plots.capital(self.iCiv))
		
		self.protectionEnd = None
		self.canceled = until(self.iTurn) < 0
		
		self.bFlip = False
		self.bSwitch = False
		
		self.iExpansionDelay = 0
		self.iExpansionTurns = 0
		
		if self.isHuman():
			self.startAutoplay()
	
	@property
	def player(self):
		if self.iPlayer is None:
			return None
		return player(self.iPlayer)
	
	@property
	def team(self):
		if self.iPlayer is None:
			return None
		return team(self.player.getTeam())
	
	@property
	def data(self):
		return data.players[self.iPlayer]
	
	@property
	def name(self):
		if self.iPlayer is None:
			return "Unassigned civ: %s" % infos.civ(self.iCiv).getText()
		return name(self.iPlayer)

	@property
	def spawn(self):
		return plot_(self.location)
		
	@property
	def flipPopup(self):
		return popup.text("TXT_KEY_POPUP_FLIP").cancel("TXT_KEY_POPUP_FLIP_CANCEL", button='Art/Interface/Buttons/Actions/Join.dds').option(self.declareWarOnFlip, "TXT_KEY_POPUP_FLIP_WAR", button='Art/Interface/Buttons/Actions/Fortify.dds').build()
	
	@property
	def switchPopup(self):
		return popup.text("TXT_KEY_POPUP_SWITCH").option(self.noSwitch, "TXT_KEY_POPUP_NO").option(self.yesSwitch, "TXT_KEY_POPUP_YES").build()
	
	def isHuman(self):
		if self.iPlayer is None:
			return game.getActiveCivilizationType() == self.iCiv
		return self.player.isHuman()
	
	def isIndependence(self):
		return self.iCiv in lIndependenceCivs

	def isNoCity(self):
		return self.iCiv in lNoCitySpawns
	
	def startAutoplay(self):
		iAutoplayTurns = self.iTurn - scenarioStartTurn()
		if iAutoplayTurns > 0:
			game.setAIAutoPlay(iAutoplayTurns)
			
	def reset(self):
		# reset AI
		self.player.AI_reset()
		
		# reset stability
		self.data.resetStability()
	
		# reset diplomatic relations
		self.resetDiplomacy()
	
		# reset espionage against
		self.resetEspionage()
	
		# reset great people
		self.resetGreatPeople()
	
	def resetDiplomacy(self):
		for iOtherPlayer in players.major().without(self.iPlayer):
			self.team.makePeace(player(iOtherPlayer).getTeam())
			
			if self.team.isVassal(player(iOtherPlayer).getTeam()):
				team(iOtherPlayer).freeVassal(self.player.getTeam())
			
			if team(iOtherPlayer).isVassal(self.player.getTeam()):
				self.team.freeVassal(player(iOtherPlayer).getTeam())
				
			self.team.cutContact(player(iOtherPlayer).getTeam())
	
	def resetEspionage(self):
		player().setEspionageSpendingWeightAgainstTeam(self.player.getTeam(), 0)
		
		for iOtherPlayer in players.all():
			team(player(iOtherPlayer).getTeam()).setEspionagePointsAgainstTeam(self.player.getTeam(), 0)
	
	def resetGreatPeople(self):
		self.player.resetGreatPeopleCreated()
		
		self.player.changeGreatPeopleCreated(data.civs[self.iCiv].iGreatPeopleCreated)
		self.player.changeGreatGeneralsCreated(data.civs[self.iCiv].iGreatGeneralsCreated)
		self.player.changeGreatSpiesCreated(data.civs[self.iCiv].iGreatSpiesCreated)
		
		self.player.setNumUnitGoldenAges(data.civs[self.iCiv].iNumUnitGoldenAges)
		
	def updateCivilization(self):
		updateCivilization(self.iPlayer, self.iCiv, iBirthTurn=self.iTurn)

	def updateStartingLocation(self):
		startingPlot = plots.capital(self.iCiv)
		self.player.setStartingPlot(startingPlot, False)
	
	def updateNames(self):
		setLeader(self.iPlayer, startingLeader(self.iPlayer))
		
		if self.player.getNumCities() == 0:
			setDesc(self.iPlayer, peoplesName(self.iPlayer))
		
	def updateArea(self):
		if self.iCiv in lExpandedFlipCivs:
			owners = self.area.cities().owners().major()
			ownerCities = cities.all().area(self.location).where(lambda city: city.getOwner() in owners).where(lambda city: not plot(city).isPlayerCore(city.getOwner())).where(lambda city: plot(city).getSettlerValue(self.iCiv) > 0 or plot(city).getPlayerSettlerValue(city.getOwner()) == 0)
			closerCities = ownerCities.where(lambda city: real_distance(city, self.location) <= real_distance(city, capital(city)))
			
			additionalPlots = closerCities.plots().expand(1) + closerCities.plots().expand(2).where(lambda p: p.getSettlerValue(self.iCiv) > 0)
			
			self.area += additionalPlots.where(lambda p: p.getOwner() in owners and none(p.isPlayerCore(iPlayer) for iPlayer in players.major().existing().without(self.iPlayer)))
			self.area = self.area.unique()
		
		if self.iCiv == iTatars:
			if player(iMongols).isExisting():
				self.area += plots.owner(iMongols).regions(*lEurope)
				self.area = self.area.unique()

		if self.iCiv == iManchuria:
			if player(iChina).isExisting() and player(iChina).isHuman() and stability(iChina) >= iStabilityStable:
				self.area = self.area.where(lambda p: p not in plots.core(iChina))

		if self.iCiv == iMexico:
			self.area = self.area.where(lambda p: p.isPlayerCore(self.iPlayer) or not owner(p, iAmerica))
		
		if self.iCiv == iCanada:
			self.area += cities.regions(rOntario, rQuebec, rMaritimes).where(lambda city: city.getX() < plots.capital(iCanada).getX()).where(lambda city: civ(city) in [iFrance, iEngland, iAmerica]).plots().expand(2).regions(rOntario, rQuebec, rMaritimes).where(lambda p: not p.isCore(p.getOwner()))
			self.area = self.area.unique()
		
		self.excludeForeignCapitals()
			
	def excludeForeignCapitals(self):
		areaCapitals = self.area.cities().where(CyCity.isCapital).where(lambda city: city.atPlot(plots.capital(city.getOwner())))
		excludedPlots = areaCapitals.plots().expand(1).where_surrounding(lambda p: p in areaCapitals or p not in self.area or not p.isCity())
	
		self.area = self.area.without(excludedPlots)
	
		for plot in plots.all():
			if plot in self.area:
				plot.setBirthProtected(self.iPlayer)
			elif plot.getBirthProtected() == self.iPlayer:
				plot.resetBirthProtected()
				
	def assignAdditionalTechs(self):
		if self.iCiv == iChina and scenario() == i3000BC and not self.isHuman():
			self.team.setHasTech(iAlloys, True, self.iPlayer, False, False)
	
	def assignAttributes(self):
		# civilization attributes
		self.civ.apply()
		
		# dynamic starting religion
		if self.iCiv in lDynamicReligionCivs:
			iPrevalentReligion = getPrevalentReligion(self.area, self.iPlayer)
			if iPrevalentReligion >= 0:
				self.player.setLastStateReligion(iPrevalentReligion)
		
		# allow free civic changes in the birth and flip turn
		self.player.changeNoAnarchyTurns(2)
		
	def closeNeighbourPlots(self, iNeighbour):
		neighbourPlots = plots.owner(iNeighbour).areas(self.location, capital(iNeighbour)).land()
		closest = neighbourPlots.without(self.area).closest(self.location)
		furthest = find_max(neighbourPlots.entities(), lambda p: distance(self.location, p)).result
		
		if not closest:
			return plots.none()
		
		closePlots, farPlots = neighbourPlots.split(lambda p: distance(closest, p) <= distance(furthest, p))
		return closePlots
	
	def revealTerritory(self):
		# reset visibility
		for plot in plots.all():
			plot.setRevealed(self.player.getID(), False, False, -1)

		# reveal birth area
		revealed = self.area.land()
		
		# if independence civ, revealed by civs controlling cities in birth area
		independenceRevealed = plots.none()
		if self.isIndependence():
			independenceRevealed = plots.sum(plots.owner(iOwner) for iOwner in self.area.cities().owners().major())
		
		# revealed by enough neighbours
		neighbours = self.area.expand(3).owners().major().without(self.iPlayer)
		neighbourRevealed = plots.sum(self.closeNeighbourPlots(iNeighbour) for iNeighbour in neighbours)
		
		# revealed by enough civilizations in your tech group
		iTechGroup = next(iGroup for iGroup in dTechGroups if self.iCiv in dTechGroups[iGroup])
		peers = players.major().existing().without(self.iPlayer).where(lambda p: civ(p) in dTechGroups[iTechGroup])
		peerRevealed = plots.none()
		
		def isPeerRevealed(plot):
			iRequiredPeers = (plot.isWater() and self.team.isMapTrading()) and peers.count() / 2 or peers.count() * 2 / 3
			return count(peer for peer in peers if plot.isRevealed(player(peer).getTeam(), False)) >= min(iRequiredPeers, peers.count()-1)
		
		if peers.count() > 2:
			peerRevealed += plots.all().where(isPeerRevealed).expand(1)
		
		bCanNeighbourReveal = revealed.intersect(neighbourRevealed) 
		bCanPeerReveal = revealed.intersect(peerRevealed)
		
		revealed += independenceRevealed
		
		if bCanNeighbourReveal:
			revealed += neighbourRevealed
			
		iVisionRange = self.player.getCurrentEra() / 2 + 1
		revealed = revealed.expand(iVisionRange)
		
		if bCanPeerReveal:
			revealed += peerRevealed
		
		# for AI, reveal nearby settler and expansion targets to improve settler AI and help with expansion
 		if not self.isHuman():
 			region_plots = plots.all().land().where(lambda p: (p.getRegionID() in lNewWorld) == (self.spawn.getRegionID in lNewWorld))
 			revealed += region_plots.where(lambda p: p.getSettlerValue(self.iCiv) >= 10).where(lambda p: distance(self.location, p) <= 15).expand(2)
 			revealed += region_plots.where(lambda p: p.getExpansion() == self.iPlayer).expand(1)
		
		# reveal tiles
		for plot in revealed:
			plot.setRevealed(self.team.getID(), True, False, -1)
	
	def createUnits(self):
		bInvasionCiv = self.iCiv in lInvasionCivs
		

		# Aeons - Add Byzantium due to dynamic capital.
		createRoleUnits(self.iPlayer, self.location, getStartingUnits(self.iPlayer), bCreateSettlers=not bInvasionCiv and not self.iCiv == iByzantium) 
		
		# if invader but no cities in birth, still grant a settler now
		if bInvasionCiv and not cities.birth(self.iPlayer):
			createRoleUnit(self.iPlayer, self.location, iSettle)

		# Aeons - Dynamic capital Byzantium
		if self.iCiv == iByzantium:
			makeUnit(self.iPlayer, iSettler, self.location, UnitAITypes.UNITAI_SETTLE)
		
		# only create units if coming from autoplay, otherwise after the switch
		if self.iPlayer == active():
			createSpecificUnits(self.iPlayer, self.location)
		
		# select a settler if available
		if self.isHuman():
			settler = units.at(self.location).owner(self.iPlayer).where(lambda unit: unit.isFound()).last()
			if settler:
				interface.selectUnit(settler, True, False, False)
		
		# update revealed owners
		for plot in plots.all():
			plot.updateRevealedOwner(self.team.getID())
	
	def setCommonwealth(self):
		if self.iCiv in [iCanada, iAustralia, iSouthAfrica]:
			iMaster = self.getMajorityCiv()
			if iMaster is not None:
				if self.iCiv == iBoers and iMaster == iSouthAfrica:
					return
				self.team.setVassal(iMaster, True, False)
				#setDesc(self.iPlayer, desc(self.iPlayer, title(self.iPlayer))) # Set vassal title here since it doesn't set during peoples stage

	# If more than half of the cities in the birth area are controlled by a Civ
	# Canada/Australia/South Africa will become a vassal to that civ
	def getMajorityCiv(self):
		for iPlayer in players.major().without(self.iPlayer):
			if cities.birth(self.iCiv).proportion(lambda city: city.getOwner() == iPlayer) > 0.5:
				return iPlayer
			

	def prepareCapital(self):
		expelUnits(self.iPlayer, plots.surrounding(self.location), self.flippedArea())
	
		if plot_(self.location).isCity():
			completeCityFlip(self.location, self.iPlayer, city_(self.location).getOwner(), 100, bCreateGarrisons=False)
		
		if self.iCiv not in lInvasionCivs:
			for city in cities.ring(self.location):
				if city.isHolyCity():
					completeCityFlip(city, self.iPlayer, city.getOwner(), 100)
				else:
					self.data.lPreservedWonders += [iWonder for iWonder in infos.buildings() if isWonder(iWonder) and city.isHasRealBuilding(iWonder)]
				
					plot_(city).eraseAIDevelopment()
					plot_(city).setImprovementType(iCityRuins)
		
		for plot in plots.surrounding(self.location):
			convertPlotCulture(plot, self.iPlayer, 100, bOwner=True)
		
	def resetPlague(self):
		self.data.iPlagueCountdown = -10
		clearPlague(self.iPlayer)
	
	def removeMinors(self):
		cities = self.area.cities()
		edge = self.area.expand(1).edge().where_surrounding(lambda p: not p.isCity()).where(lambda p: not p.isOwned() or is_minor(p)).passable()
		
		for unit in self.area.units().minor():
			if unit.isAnimal():
				unit.kill(False, -1)
				continue
			
			if cities.owner(unit.getOwner()):
				closest = cities.owner(unit.getOwner()).closest(unit)
			elif unit.getDomainType() == DomainTypes.DOMAIN_SEA or unit.isCargo():
				if edge.sea():
					closest = edge.sea().closest(unit)
				else:
					closest = plots.all().sea().without(self.area).closest(unit)
			else:
				closest = edge.land().area(unit).closest(unit)
			
			if closest:
				move(unit, closest)
			else:
				unit.kill(False, -1)
	
	def check(self):
		
		
		if self.canceled:
			return
		
		if self.isHuman() and data.iBeforeObserverSlot != -1:
			return
	
		iUntilBirth = until(self.iTurn)
	
		
		if iUntilBirth == turns(3) or (scenarioStart() and self.iTurn - turns(3) < scenarioStartTurn()):
			if not self.canSpawn():
				self.canceled = True
				return
			if self.lowImpactCancel():
				self.canceled = True
				return
			
			self.activate()

			if self.canceled:
				return
			
			self.prepare()
			self.protect()
			self.expansion()
			self.announce()
		
		elif iUntilBirth == 2:
			if self.cancelSpawn():
				self.cancel()
				return
			self.askSwitch()
		elif iUntilBirth == 1:
			self.checkSwitch()
			self.birth()

		#elif iUntilBirth == 0 and not scenarioStart():
		#	self.flip()
		#	self.wars()

		elif -turns(3) <= iUntilBirth <= 0 and not scenarioStart():
			self.checkFlip()
			
		if iUntilBirth < 0:
			self.checkExpansion()
			
		if turn() == self.protectionEnd:
			self.resetProtection()
			
		self.checkIncompatibleCivs()
		
	def canSpawn(self):
		if self.isHuman() and not data.iBeforeObserverSlot != -1:
			return True
		
		if not infos.civ(self.iCiv).isAIPlayable():
			return False

		# Aeons - Certain civs can't spawn if their birth area is occupied
		if self.isNoCity():
			if cities.birth(self.iCiv):
				return False

		# Aeons - Rome is opposite and requires at least one city in birth area
		if self.iCiv == iRome:
			if not cities.birth(self.iCiv):
				return False
		

		if autoplay():
			if getImpact(self.iCiv) <= iImpactLimited:
				if year(dBirth[civ(active())]) > year(dFall[self.iCiv]) + turns(20):
					return False
		
		
		# Byzantium requires Rome to be alive and Greece to be dead (human Rome can avoid Byzantine spawn by being solid)
		# Aeons - Remove due to Dynamic Byzantium
		#if self.iCiv == iByzantium:
			#if not player(iRome).isExisting():
				#return False
			#elif player(iGreece).isExisting():
				#return False
			#elif player(iSparta).isExisting():
				#return False
			#elif player(iMycenae).isExisting():
				#return False
			#elif player(iRome).isHuman() and stability(iRome) == iStabilitySolid:
				#return False

		# Aeons - Byzantium requires that the Mediterranean hegemon holds land in Italy/Greece
		if self.iCiv == iByzantium:
			validHegemons = players.major().existing().where(lambda p: plots.capital(p) in plots.region(rMediterraneanSea).expand(2))
			if validHegemons == None:
				return False
			else:
				data.iMediterraneanHegemon = civ(validHegemons.maximum(lambda p: player(p).getNumMilitaryUnits()))
				if player(data.iMediterraneanHegemon).isHuman() and stability(data.iMediterraneanHegemon) == iStabilitySolid:
					return False
				if plots.capital(data.iMediterraneanHegemon).getX() >= 73:
					if cities.region(rItaly).none(lambda city: data.iMediterraneanHegemon in [city.getCivilizationType()]):
						return False
				else:
					if cities.region(rGreece).none(lambda city: data.iMediterraneanHegemon in [city.getCivilizationType()]):
						return False


		# Athens requires Mycenae to be dead
		if self.iCiv == iGreece:
			if player(iMycenae).isExisting():
				return False

		# Sparta requires Mycenae to be dead
		if self.iCiv == iSparta:
			if player(iMycenae).isExisting():
				return False

		# Moors, Morocco, Spain requires Arabia to take an Iberian city.
		if self.iCiv == iMorocco or self.iCiv == iSpain:
			if not cities.regions(rIberia).ever_owned(iArabia):
				return False

		# Holy Rome requires that the French managed to conquer at least one city in Germany and that Rome doesn't exist.
		if self.iCiv == iHolyRome and not self.isHuman() and not player(iFrance).isHuman():
			if not cities.region(rLowerGermany).owner(iFrance):
				return False
			if player(iRome).isExisting():
				return False

		# Arabia must've conquered a city in Persia for Samanids
		if self.iCiv == iSamanids:
			if not cities.regions(rPersia).ever_owned(iArabia):
				return False

		# If Gokturks own a city in Persia or Khorasan, Turks won't spawn.
		if self.iCiv == iTurks:
			if cities.regions(rPersia, rKhorasan).owner(iGokturks):
				return False

		# Arabia must've conquered a Persian city for Buyids
		if self.iCiv == iBuyids:
			if not cities.regions(rPersia).ever_owned(iArabia):
				return False


		# Arabia must've conquered an Egyptian or Maghrebi city for Misr and Carthage must not exist
		if self.iCiv == iMisr:
			if not cities.regions(rMaghreb, rEgypt).ever_owned(iArabia):
				return False
			if player(iCarthage).isExisting():
				if player(iCarthage).getPeriod() == iPeriodCarthage:
					return False
			if self.iCiv == iMisr:
				if player(iEgypt).isExisting():
					return False
	

		# Fatimids must've moved beyond Tunisia for Tunis
		# And Carthage must not exist
		if self.iCiv == iTunis:
			if player(iMisr).isExisting():
				if player(iMisr).getPeriod() == iPeriodMisrEgypt:
					return False
			if player(iCarthage).isExisting():
				if player(iCarthage).getPeriod() == iPeriodCarthage:
					return False

		
		# Italy requires Rome to be dead and sufficient minor or HRE cities in Italy
		if self.iCiv == iItaly:
			if player(iRome).isExisting():
				return False
			if cities.region(rItaly).proportion(lambda city: city.getOwner() in players.minor() or civ(city) == iHolyRome) < 0.5:
				return False
			#if player(iGoths).isExisting():
			#	return False
			#if cities.region(rItaly).proportion(lambda city: is_minor(city) or city.getOwner() == iHolyRome) < 0.5:
			#	return False
			#if cities.regions(rItaly).none(lambda city: iByzantium in [city.getCivilizationType()]):
			#	return False
		
		# Aztecs require Toltecs to be dead
		if self.iCiv == iAztecs:
			iRequiredStability = player(iToltecs).isHuman() and iStabilityUnstable or iStabilityShaky
			if player(iToltecs).isExisting() and stability(iToltecs) >= iRequiredStability:
				return False
		
		# Ottomans require that the Turks managed to conquer at least one city in Anatolia
		# Aeons - Was previously Anatolia, Caucasus, Levant and Mesopotamia, but loosened to help Byzantium a bit
		if self.iCiv == iOttomans:
			if cities.birth(iOttomans).none(CyCity.isHuman) and not cities.regions(rAnatolia).ever_owned(iTurks):
				return False
			#if cities.birth(iOttomans).none(CyCity.isHuman) and cities.regions(rAnatolia, rCaucasus).none(lambda city: iTurks in [city.getCivilizationType(), city.getPreviousCiv()] or iMongols in [city.getCivilizationType(), city.getPreviousCiv()]): return False
		
		# Parthia requires Persia to be dead or unstable
		if self.iCiv == iParthia:
			if player(iPersia).isExisting() and stability(iPersia) >= iStabilityShaky:
				return False

		# Iran requires Persia, Parthia, Buyids to be dead
		if self.iCiv == iIran:
			if player(iPersia).isExisting():
				return False
			if player(iParthia).isExisting():
				return False
			if player(iBuyids).isExisting():
				return False
		
		# Saudis require Arabia to be dead and no player in its birth area to be stable
		if self.iCiv == iSaudis:
			if player(iArabia).isExisting():
				return False
			
			if cities.birth(iSaudis).owners().major().all_if_any(lambda p: stability(p) >= iStabilityStable):
				return False

		# Argentina requires any Old World civilization in Andes or Southern Cone
		if self.iCiv == iArgentina:
			if not cities.regions(rAndes, rSouthernCone).ever_owned(lBioOldWorld):
				return False
		
		# Mexico requires Aztecs to be dead and any Old World civilization in Mesoamerica or Central America
		if self.iCiv == iMexico:
			if player(iAztecs).isExisting():
				return False

			if not cities.regions(rMesoamerica, rCentralAmerica).ever_owned(lBioOldWorld):
				return False
		
		# Colombia requires any Old World civilization in New Granada or Andes
		if self.iCiv == iColombia:
			if not cities.regions(rNewGranada, rAndes).ever_owned(lBioOldWorld):
				return False
		
		# Brazil requires any Old World civilization in Brazil or Amazonia
		if self.iCiv == iBrazil:
			if not cities.regions(rBrazil, rAmazonia).ever_owned(lBioOldWorld):
				return False

		# Belgium requires Netherlands not to exist, not controlling its core, or being collapsing
		if self.iCiv == iBelgium:
			if not player(iCongo).isHuman() and not player(iKatanga).isHuman(): # Aeons - Always spawn Belgium if human owned Congo.
				if player(iNetherlands).isExisting() and cities.core(iNetherlands).owner(iNetherlands) and stability(iNetherlands) > iStabilityCollapsing:
					return False

		# Australia requires any cities in Australia
		if self.iCiv == iAustralia:
			if not cities.region(rAustralia):
				return False

		# Jerusalem requires a Catholic owner for a Levantine city
		if self.iCiv == iJerusalem:
			if cities.region(rLevant).none(lambda city: player(city).getStateReligion()==iCatholicism):
				return False

		# Boers/Zulu must not be in South African Union period for South Africa to spawn
		if self.iCiv == iSouthAfrica:
			if player(iBoers).isExisting():
				if player(iBoers).getPeriod() == iPeriodSouthAfricaUnion:
					return False
			if player(iZulu).isExisting():
				if player(iZulu).getPeriod() == iPeriodSouthAfricaUnion:
					return False

		# Buyids and Ghurids always spawn so long as Persia exists, as Saffarids respawn at high stability.
		if self.iCiv == iBuyids or self.iCiv == iGhorids:
			if player(iPersia).isExisting():
				return True

	
		# independence civs require all players controlling cities in their area to be stable or worse, solid or worse from 1750 onwards
		if self.isIndependence():
			birthCities = plots.birth(self.iCiv).cities()
			if players.major().where(lambda p: civ(p) != self.iCiv).where(lambda p: birthCities.owner(p).any()).all_if_any(lambda p: stability(p) >= iStabilitySolid) and year(dBirth[self.iCiv]>=1750):
				return False
			if players.major().where(lambda p: civ(p) != self.iCiv).where(lambda p: birthCities.owner(p).any()).all_if_any(lambda p: stability(p) >= iStabilityStable):
				return False
		
		return True

	def cancelSpawn(self):
		if self.isHuman():
			return False
		if self.iCiv == iTatars:
			if not cities.owner(iMongols).regions(*lEurope):
				return True
		
		return False
	
	def announce(self):
		if scenarioStart():
			return
	
		if game.getAIAutoPlay() > 0:
			return
	
		if plots.owner(active()).closest_distance(self.location) <= 10:
			key = "TXT_KEY_MESSAGE_RISE_%s" % infos.civ(self.iCiv).getIdentifier()
			text = text_if_exists(key, adjective(self.iPlayer), otherwise="TXT_KEY_MESSAGE_RISE_GENERIC")
			message(active(), latin1(text), location=self.location, color=iRed, button=infos.civ(self.iCiv).getButton())
	
	def activate(self):
		if self.iPlayer is None:
			if self.sharesLimitedSlot():
				self.canceled = True
				log.rise("BIRTH CANCELED: skipping %s slot to keep it free", infos.civ(self.iCiv).getText())
				return
			self.iPlayer = findSlot(self.iCiv)
			
		if self.iPlayer < 0:
			self.canceled = True
			log.rise("BIRTH CANCELED: no free slot found for %s", infos.civ(self.iCiv).getText())
			return
		
		self.updateCivilization()
		self.updateStartingLocation()
		self.updateNames()
		
		self.player.setInitialBirthTurn(self.iTurn)
		
		if not self.isHuman():
			self.player.setAlive(True, True)
		
		self.area = plots.birth(self.iPlayer) + plots.core(self.iPlayer)
		self.area = self.area.unique()

	def prepare(self):
		events.fireEvent("prepareBirth", self.iCiv)
	
	def protect(self):
		# 5 turns of protection after it spawns since this event fires 2 turns before true birth
		self.protectionEnd = self.iTurn + turns(7)
		self.player.setBirthProtected(True)
	
		for plot in self.area:
			plot.setBirthProtected(self.iPlayer)
	
		self.removeMinors()
	
	def resetProtection(self):
		self.player.setBirthProtected(False)
		
		for plot in self.area:
			plot.resetBirthProtected()

	def cancel(self):
		self.canceled = True
		self.resetProtection()
	
	def expansion(self):
		for plot in plots.all().where(lambda p: p.getExpansion() == self.iPlayer):
			plot.resetExpansion()
	
		if self.iCiv in lExpansionCivs:
			capital_continent = plot_(self.location).getContinentArea()
			
			for plot in plots.all().without(self.area).land().where(self.isExpansionPlot):
				plot.setExpansion(self.iPlayer)

			self.iExpansionDelay = rand(turns(5)) + 1
			self.iExpansionTurns = turns(30)

	def isExpansionPlot(self, plot):
		if plot.isPeak():
			return False

		if plot.getPlayerWarValue(self.iPlayer) < 5:
			return False

		if plot.getContinentArea() == self.spawn.getContinentArea():
			return True

		if distance(plot, self.location) > 32:
			return False

		return (plot.getRegionID() in lNewWorld) == (self.spawn.getRegionID() in lNewWorld)
	
	def checkExpansion(self):
		if not self.player.isExisting():
			return
		
		if self.player.getNumCities() == 0:
			return
				
		if self.iExpansionTurns < 0:
			return
		
		expansionPlots = plots.all().where(lambda p: p.getExpansion() == self.iPlayer and p.isRevealed(self.player.getTeam(), False))
		expansionCities = expansionPlots.cities().notowner(self.iPlayer)
		
		if expansionCities.owner(self.iPlayer).any(lambda city: since(city.getGameTurnAcquired()) <= 1):
			self.iExpansionTurns = max(self.iExpansionTurns, turns(10))
		
		if self.iExpansionTurns == 0:
			for plot in expansionPlots:
				plot.resetExpansion()

		deleteExpansionUnits(self.iPlayer)
		
		self.iExpansionDelay -= 1
		self.iExpansionTurns -= 1

		if self.team.isAVassal():
 			return
		
		if self.iExpansionDelay >= 0:
			return
		
		if not self.isHuman() and expansionCities:
			minors, majors = expansionCities.owners().without(self.iPlayer).split(is_minor)
 			
 			majors = majors.where(self.team.canDeclareWar).where(self.player.canContact).where(lambda p: not player(p).isBirthProtected())
		
			for iMinor in minors.where(lambda p: not self.team.isAtWar(p)):
				self.team.declareWar(player(iMinor).getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)
	
			if majors and self.team.getAtWarCount(True) > 0:
				target = expansionCities.where(lambda city: not is_minor(city)).closest_all(cities.owner(self.iPlayer))
				self.team.declareWar(target.getTeam(), True, WarPlanTypes.WARPLAN_TOTAL)

				self.iExpansionDelay = rand(turns(5)) + 1
 			
 			elif minors:
 				target, attacker_closest = expansionCities.where(is_minor).where_surrounding(lambda city: not units.at(city).owner(self.iPlayer)).where_maximum(lambda city: plot_(city).getPlayerWarValue(self.iPlayer)).closest_pair(cities.owner(self.iPlayer))
 				
 				if target:
 					spawn = possibleSpawnsBetween(attacker_closest, target, 1).closest(target)
 		
 					createExpansionUnits(self.iPlayer, target.getOwner(), spawn, target, iExtraAI=0, iExtraTargets=0)
 				
 					self.iExpansionDelay = 2

	def checkIncompatibleCivs(self):
		if self.iCiv not in dClearedForBirth:
			return
		
		iClearedCiv = dClearedForBirth[self.iCiv]
		
		if not self.isHuman() and iClearedCiv not in lAlwaysClear:
			return
			
		if not player(iClearedCiv).isExisting():
			return
		
		if player(iClearedCiv).isHuman():
			return
		
		if turn() == year(dFall[iClearedCiv]).deviate(10, data.iSeed):
			completeCollapse(slot(iClearedCiv))
	
	def sharesLimitedSlot(self):
		currentUnassignedBirths = getBirthsForTurn(self.iTurn).where(lambda iCiv: iCiv not in players.all().civs())
		iAvailableSlots = countAvailableSlots()
		if currentUnassignedBirths.count() <= iAvailableSlots:
			return False
			
		return currentUnassignedBirths.any(lambda iCiv: getImpact(iCiv) > getImpact(self.iCiv)) and self.iCiv not in currentUnassignedBirths.limit(iAvailableSlots)
	
	def askSwitch(self):
		if not self.canSwitch():
			self.assignAdditionalTechs()
			return

		self.switchPopup.text(adjective(self.iPlayer)).noSwitch().yesSwitch().launch()

	def lowImpactCancel(self):
		
		if civ() == self.iCiv:
			return False

		#Aeons - Prevent super-marginal impact civs from spawning if not neighbours or influences
		if not civ() in dNeighbours[self.iCiv] and not civ() in dInfluences[self.iCiv] and infos.civ(self.iCiv).getImpact() <= iImpactSuperMarginal:
			return True

		#Aeons - Prevent marginal impact civs from spawning if not neighbours, influences or same civ group.
		if not civ() in dNeighbours[self.iCiv] and not civ() in dInfluences[self.iCiv] and infos.civ(self.iCiv).getImpact() <= iImpactMarginal:
			if civ() in dCivGroups[iCivGroupEurope] and self.iCiv in dCivGroups[iCivGroupEurope]:
				return False
			if civ() in dCivGroups[iCivGroupEastAsia] and self.iCiv in dCivGroups[iCivGroupEastAsia]:
				return False
			if civ() in dCivGroups[iCivGroupSouthAsia] and self.iCiv in dCivGroups[iCivGroupSouthAsia]:
				return False
			if civ() in dCivGroups[iCivGroupMiddleEast] and self.iCiv in dCivGroups[iCivGroupMiddleEast]:
				return False
			if civ() in dCivGroups[iCivGroupMediterranean] and self.iCiv in dCivGroups[iCivGroupMediterranean]:
				return False
			if civ() in dCivGroups[iCivGroupAfrica] and self.iCiv in dCivGroups[iCivGroupAfrica]:
				return False
			if civ() in dCivGroups[iCivGroupAmerica] and self.iCiv in dCivGroups[iCivGroupAmerica]:
				return False
			if civ() in dCivGroups[iCivGroupOceania] and self.iCiv in dCivGroups[iCivGroupOceania]:
				return False
			if civ() in dCivGroups[iCivGroupNorthAfrica] and self.iCiv in dCivGroups[iCivGroupNorthAfrica]:
				return False
			return True		

		return False
		
	
	def canSwitch(self):
		if not MainOpt.isSwitchPopup():
			return False
	
		if game.getAIAutoPlay() > 0:
			return False

		if scenarioStart():
			return False
		
		if civ() in dNeighbours[self.iPlayer] and since(year(dBirth[civ(active())])) < turns(25):
			return False
	
		return True
	
	def yesSwitch(self):
		self.bSwitch = True
		
		game.doControl(ControlTypes.CONTROL_FORCEENDTURN)
	
	def noSwitch(self):
		if not self.isHuman():
			self.assignAdditionalTechs()
			createRoleUnits(self.iPlayer, self.location, getAIStartingUnits(self.iPlayer))
		
		createSpecificUnits(self.iPlayer, self.location)
	
	def checkSwitch(self):
		if self.bSwitch:
			self.bSwitch = False
			self.switch()
	
	def switch(self):
		iPreviousPlayer = active()
		iOldHandicap = player(iPreviousPlayer).getHandicapType()
		
		game.setActivePlayer(self.iPlayer, False)
		
		player(iPreviousPlayer).setHandicapType(self.player.getHandicapType())
		self.player.setHandicapType(iOldHandicap)
		
		iMaster = master(self.iPlayer)
		if iMaster:
			self.team.setVassal(iMaster, False, False)
		
		self.player.setPlayable(True)
		
		if game.getWinner() == iPreviousPlayer:
			game.setWinner(-1, -1)
		
		data.resetHumanStability()
		
		for city in cities.owner(self.iPlayer):
			city.setInfoDirty(True)
			city.setLayoutDirty(True)
		
		if player(iPreviousPlayer).getAdvancedStartPoints() > 0:
			player(iPreviousPlayer).AI_doAdvancedStart()
		
		for iOtherPlayer in players.major():
			self.player.setEspionageSpendingWeightAgainstTeam(player(iOtherPlayer).getTeam(), 0)
		
		# update statistics offsets
		
		statistics = CyStatistics()
		
		dUnitsBuilt = dict((iUnit, statistics.getPlayerNumUnitsBuilt(self.iPlayer, iUnit)) for iUnit in infos.units())
		dUnitsKilled = dict((iUnit, statistics.getPlayerNumUnitsKilled(self.iPlayer, iUnit)) for iUnit in infos.units())
		dUnitsLost = dict((iUnit, statistics.getPlayerNumUnitsLost(self.iPlayer, iUnit)) for iUnit in infos.units())
		dBuildingsBuilt = dict((iBuilding, statistics.getPlayerNumBuildingsBuilt(self.iPlayer, iBuilding)) for iBuilding in infos.buildings())
		
		data.dUnitsBuilt = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsBuilt.items() if iNumUnits > 0)
		data.dUnitsKilled = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsKilled.items() if iNumUnits > 0)
		data.dUnitsLost = dict((iUnit, iNumUnits) for iUnit, iNumUnits in dUnitsLost.items() if iNumUnits > 0)
		data.dBuildingsBuilt = dict((iBuilding, iNumBuildings) for iBuilding, iNumBuildings in dBuildingsBuilt.items() if iNumBuildings > 0)
	
	def birth(self):
		# reset AI
		self.reset()
		
		# set initial birth turn
		self.player.setInitialBirthTurn(self.iTurn)
		
		# update area
		self.updateArea()
		
		# assign civilization attributes
		self.assignAttributes()
		

		#Aeons - Dynamic Byzantium starting plot
		if self.iCiv == iByzantium:
			validHegemons = players.major().existing().where(lambda p: plots.capital(p) in plots.region(rMediterraneanSea).expand(2))
			if validHegemons == None:
				area = plots.birth(self.iPlayer)
			else:
				data.iMediterraneanHegemon = civ(validHegemons.maximum(lambda p: player(p).getNumMilitaryUnits()))
				if plots.capital(data.iMediterraneanHegemon).getX() >= 73:
					setPeriod(iByzantium, iPeriodByzantiumRoman)
					startingPlot = plots.capital(iRome)
					self.player.setStartingPlot(startingPlot, False)
					self.location = location(plots.capital(iRome))

		# reveal territory
		self.revealTerritory()		

		# Aeons - Set Australia, Canada, South Africa as vassals of their previous owner
		self.setCommonwealth()

		# flip capital
		self.prepareCapital()
		
		# create starting units
		self.createUnits()
		
		# reset plague
		self.resetPlague()
		
		# send event
		events.fireEvent("birth", self.iPlayer)
		
	def warOnFlip(self, iOwner, cityNames):
		if player(iOwner).isHuman():
			self.flipPopup.text(cityNames, name(self.iPlayer)).cancel().declareWarOnFlip().launch(iOwner)
			return
		
		if team(iOwner).isAtWar(self.player.getTeam()):
			team(iOwner).AI_setAtWarCounter(self.player.getTeam(), 0)
			self.team.AI_setAtWarCounter(player(iOwner).getTeam(), 0)
			return
		
		iRefusalModifier = dWarOnFlipProbability[iOwner]
		if chance(dWarOnFlipProbability[iOwner]):
 			player(iOwner).AI_changeMemoryCount(self.iPlayer, MemoryTypes.MEMORY_STOPPED_TRADING_RECENT, 1)
	
	def declareWarOnFlip(self, iOwner):
		team(iOwner).declareWar(self.player.getTeam(), False, WarPlanTypes.WARPLAN_ATTACKED_RECENT)

	def checkFlip(self):
		if not self.bFlip and (self.player.getNumCities() > 0 or self.iCiv in lInvasionCivs):
			self.flip()
			self.wars()
			
			self.bFlip = True
	
	def flippedArea(self):
		if self.iCiv == iEngland and not self.isHuman():
 			area = plots.birth(self.iPlayer) + plots.region(rBritain).where(lambda p: not p.isOwned() or is_minor(p.getOwner()))
 			return area.unique()

		#Aeons - remove Byzantium from expanded flips, but make it flip all of Rome east of Italy
		if self.iCiv == iByzantium:
			validHegemons = players.major().existing().where(lambda p: plots.capital(p) in plots.region(rMediterraneanSea).expand(2))
			if validHegemons == None:
				area = plots.birth(self.iPlayer)
				return area.unique()
			else:
				data.iMediterraneanHegemon = civ(validHegemons.maximum(lambda p: player(p).getNumMilitaryUnits()))
				if plots.capital(data.iMediterraneanHegemon).getX() >= 73:
					setPeriod(iByzantium, iPeriodByzantiumRoman)
					startingPlot = plots.capital(iRome)
					self.player.setStartingPlot(startingPlot, False)
					self.location = location(plots.capital(iRome))
					area = plots.birth(iRome) + plots.all().where(lambda p: p.getX() < 73 and p.isOwned() and civ(p.getOwner()) == data.iMediterraneanHegemon)
 					return area.unique()
				else:
 					area = plots.birth(self.iPlayer) + plots.all().where(lambda p: p.getX() >= 73 and p.isOwned() and civ(p.getOwner()) == data.iMediterraneanHegemon)
 					return area.unique()
			
		# Aeons - Holy Rome birth area is the French birth area in Germany, Central Europe and Italy
		# Ignore for human player
		if self.iCiv == iHolyRome and not self.isHuman() and not player(iFrance).isHuman():
			area = plots.regions(rLowerGermany, rCentralEurope, rItaly).where(lambda p: p.isOwned() and civ(p.getOwner()) == iFrance)
			return area.unique()
		
		# Flip all of western Timurid land as Iran.
		# Technically it was controlled by the Aq Qoyunlu before the Safavids
		# But we can't really fit such a civ in the timeline
		# This will force the Timurids out into India
		if self.iCiv == iIran:
			area = plots.birth(self.iPlayer) + plots.all().where(lambda p: p.getX() <= 98 and p.isOwned() and civ(p.getOwner()) == iTimurids)
			return area.unique()
		

	
		return self.isIndependence() and self.area or plots.birth(self.iPlayer)
	
	def flip(self):
		flippedPlots = self.flippedArea()
		
		excludedPlots = flippedPlots.where(lambda p: p.isCity() and city_(p).isCapital() and p.isPlayerCore(p.getOwner()))
		excludedPlots = excludedPlots.expand(1).where(lambda p: cities.surrounding(p).all(lambda city: city in excludedPlots))
		
		flippedPlots = flippedPlots.without(excludedPlots)
		
		flippedCities = flippedPlots.cities().notowner(self.iPlayer)
		flippedCityPlots = flippedCities.plots()
	
		flippedPlayerCities = dict((p, format_separators(flippedCities.owner(p), ",", text("TXT_KEY_AND"), CyCity.getName)) for p in flippedCities.owners().major())
		
		expelUnits(self.iPlayer, flippedPlots)
		
		for city in flippedCities:
			city = completeCityFlip(city, self.iPlayer, city.getOwner(), 100, bFlipUnits=True)
			city.rebuild(-1)
			
			iMinPopulation = self.player.getCurrentEra() + 1
			city.setPopulation(max(iMinPopulation, city.getPopulation()))
			
			if since(scenarioStartTurn()):
				ensureDefenders(self.iPlayer, city, 2)
		
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots.land())
		convertSurroundingPlotCulture(self.iPlayer, flippedPlots.water().where(lambda p: p.getPlayerCityRadiusCount(self.iPlayer) > 0))
		
		if self.player.getCurrentEra() <= iRenaissance:
			downgradeAreaCottages(self.iPlayer, flippedPlots.land())
		
		for iOwner, cityNames in flippedPlayerCities.items():
			self.warOnFlip(iOwner, cityNames)
		
		flipped_names = format_separators(flippedCityPlots.cities(), ",", text("TXT_KEY_AND"), CyCity.getName)
		if flippedCities:
			message(self.iPlayer, 'TXT_KEY_MESSAGE_CITIES_FLIPPED', flipped_names, color=iGreen)
		
		self.civ.advancedStart()
		
		events.fireEvent("flip", self.iPlayer)
	
	def wars(self):
		if self.isHuman():
			return
	
		expansionArea = plots.all().where(lambda p: p.getExpansion() == self.iPlayer)
		expansionTargets = expansionArea.owners()
		
		for iTarget in expansionTargets:
			if (self.iCiv, civ(iTarget)) in lBirthWars:
				self.team.declareWar(player(iTarget).getTeam(), True, WarPlanTypes.WARPLAN_TOTAL)
				
				if player(iTarget).isHuman():
					for plot in expansionArea.owner(iTarget).core(iTarget):
						plot.resetExpansion()

		
