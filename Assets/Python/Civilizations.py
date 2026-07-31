from Core import *

from Events import events, handler


### Unit spawn functions ###

def getStartingUnits(iPlayer):
	return [(iSettle, dStartingUnits[iPlayer].get(iSettle, 0))] + [(iRole, iAmount) for iRole, iAmount in dStartingUnits[iPlayer].items() if iRole not in (iWork, iSettle)]

def getAIStartingUnits(iPlayer):
	return dExtraAIUnits[iPlayer].items()
	
def getAdditionalUnits(iPlayer):
	return dAdditionalUnits[iPlayer].items()

def getSpecificAdditionalUnits(iPlayer):
	return dSpecificAdditionalUnits[iPlayer].items()

### Tech preference functions ###

def getTechPreferences(iPlayer):
	dPreferences = defaultdict({}, 0)
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = dPreferences[iPrereqTech]
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	player(iPlayer).resetTechPreferences()

	for iTech, iValue in dPreferences.items():
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.resetBuildingClassPreferences()
	
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingClassPreference(infos.building(iBuilding).getBuildingClassType(), iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingClassPreference(infos.building(iWonder).getBuildingClassType(), iDefaultPreference)


### General functions ###
		
@handler("playerCivAssigned")
def onPlayerCivAssigned(iPlayer):
	initPlayerTechPreferences(iPlayer)
	initBuildingPreferences(iPlayer)
	

### Civilization starting attributes ###

class Civilization(object):

	def __init__(self, iCiv, **kwargs):
		self.iCiv = iCiv
	
		self.iLeader = kwargs.get("iLeader")
		self.iGold = kwargs.get("iGold")
		self.iStateReligion = kwargs.get("iStateReligion")
		self.iAdvancedStartPoints = kwargs.get("iAdvancedStartPoints")
		
		self.lCivics = kwargs.get("lCivics", [])
		self.lEnemies = kwargs.get("lEnemies", []) + [iNative, iBarbarian]
		
		self.dAttitudes = kwargs.get("dAttitudes", {})
		self.dMemories = kwargs.get("dMemories", {})
		
		self.sLeaderName = kwargs.get("sLeaderName")
		
		self.techs = kwargs.get("techs", techs.none())
	
	@property
	def player(self):
		return player(self.iCiv)
	
	@property
	def team(self):
		return team(self.player.getTeam())
	
	@property
	def info(self):
		return infos.civ(self.iCiv)
	
	def isPlayable(self):
		return self.info.getStartingYear() != 0
	
	def apply(self):
		if not self.player.isHuman():
			if self.iLeader is not None:
				self.player.setLeader(self.iLeader)
		
			if self.sLeaderName is not None:
				self.player.setLeaderName(text(self.sLeaderName))
		
		if self.iGold is not None:
			self.player.changeGold(scale(self.iGold))
		
		if self.iStateReligion is not None:
			iOldStateReligion = self.player.getStateReligion()
			iNewStateReligion = self.iStateReligion
			
			if iNewStateReligion == iProtestantism and not game.isReligionFounded(iProtestantism):
				iNewStateReligion = iCatholicism
			
			if iNewStateReligion == iCatholicism and not game.isReligionFounded(iCatholicism):
				iNewStateReligion = iOrthodoxy
			
			if game.isReligionFounded(iNewStateReligion) or self.canFoundReligion(iNewStateReligion):
				self.player.setLastStateReligion(iNewStateReligion)
				events.fireEvent("playerChangeStateReligion", self.player.getID(), iNewStateReligion, iOldStateReligion)
		
		if self.techs:
			for iTech in self.techs:
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)
			
			self.player.setStartingEra(self.player.getCurrentEra())
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
			
		for iEnemy in self.lEnemies:
			iEnemyPlayer = slot(iEnemy)
			if iEnemyPlayer >= 0 and self.iCiv != iEnemy:
				team(iEnemyPlayer).declareWar(self.player.getTeam(), False, WarPlanTypes.NO_WARPLAN)
		
		for iCiv, iAttitude in self.dAttitudes.items():
			self.player.AI_changeAttitudeExtra(slot(iCiv), iAttitude)

		for iCiv, entries in self.dMemories.items():
			for iMemory, iChange in entries.items():
				self.player.AI_changeMemoryCount(slot(iCiv), iMemory, iChange)
	
	def canFoundReligion(self, iReligion):
		return infos.religion(iReligion).getTechPrereq() in self.techs
	
	def advancedStart(self):
		if self.iAdvancedStartPoints is not None:
			self.player.setAdvancedStartPoints(scale(self.iAdvancedStartPoints))
			
			if not self.player.isHuman():
				self.player.AI_doAdvancedStart()

lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iPottery, iAgriculture, iMythology)
	),
	Civilization(
		iSumeria,
		techs=techs.of(iPottery, iPastoralism, iAgriculture, iMythology)
	),
	Civilization(
		iBabylonia,
		lCivics=[iMonarchy, iSlavery, iDeification],
		techs=techs.column(1).including(iMasonry, iSmelting, iProperty, iDivination, iWriting, iCeremony, iLeverage)
	),
	Civilization(
		iHarappa,
		techs=techs.of(iTanning, iMining, iPottery, iAgriculture)
	),
	Civilization(
		iMinoa,
		techs=techs.of(iMining, iPottery, iAgriculture, iSailing)
	),
	Civilization(
		iElam,
		techs=techs.of(iMining, iPottery, iAgriculture, iPastoralism, iSailing, iTanning)
	),
	Civilization(
		iAssyria,
		iGold=100,
		iAdvancedStartPoints=60,
		lCivics=[iDespotism, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys, iWriting)
	),
	Civilization(
		iChina,
		iGold=50,
		lCivics=[iDespotism],
		techs=techs.column(1).without(iSailing).including(iSmelting, iLeverage, iProperty, iCeremony)
	),
	Civilization(
		iHittites,
		iGold=40,
		lCivics=[iMonarchy, iSlavery],
		techs=techs.column(2).without(iRiding, iSeafaring).including(iAlloys)
	),
	Civilization(
		iNubia,
		iGold=100,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(1).including(iMasonry, iProperty)
	),
	Civilization(
		iMycenae,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys, iWriting)
	),
	Civilization(
		iIndia,
		iGold=80,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iDeification],
		techs=techs.column(2).including(iAlloys, iWriting).without(iSeafaring)
	),
	Civilization(
		iPhoenicia,
		iGold=200,
		iAdvancedStartPoints=60,
		lCivics=[iRepublic, iSlavery],
		techs=techs.column(2).including(iAlloys, iWriting, iShipbuilding)
	),
	Civilization(
		iJudah,
		iGold=150,
		iStateReligion=iJudaism,
		lCivics=[iMonarchy, iSlavery],
		techs=techs.column(2).including(iAlloys, iWriting, iArithmetics, iCalendar, iLiterature)
	),
	Civilization(
		iGreece,
		iGold=150,
		iAdvancedStartPoints=200,
		lCivics=[iRepublic, iSlavery, iDeification, iRedistribution, iThalassocracy],
		techs=techs.column(4).including(iPhilosophy).without(iRiding, iContract)
	),
	Civilization(
		iPolynesia,
		techs=techs.of(iTanning, iMythology, iSailing, iSeafaring)
	),
	Civilization(
		iScythia,
		iGold=100,
		lCivics=[iDespotism, iSlavery, iDeification],
		techs=techs.column(2).including(iRiding, iAlloys, iBloomery, iCalendar).without(iShipbuilding)
	),

	Civilization(
		iPersia,
		iGold=200,
		iAdvancedStartPoints=600,
		lCivics=[iMonarchy, iManorialism, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iPriesthood, iMathematics).without(iSeafaring, iShipbuilding)
	),
	Civilization(
		iSparta,
		iAdvancedStartPoints=100,
		lCivics=[iDespotism, iSlavery, iDeification, iRedistribution],
		techs=techs.column(3).including(iBloomery, iContract).without(iRiding)
	),

	Civilization(
		iCelts,
		techs=techs.column(2).including(iAlloys),
		lCivics=[iMonarchy],
	),
	Civilization(
		iRome,
		iGold=100,
		iAdvancedStartPoints=300,
		lCivics=[iRepublic, iSlavery, iRedistribution],
		techs=techs.column(4).including(iGeneralship, iCurrency, iEngineering).without(iRiding, iShipbuilding, iNavigation)
	),
	Civilization(
		iGermania,
		iGold=50,
		lCivics=[iDespotism],
		techs=techs.column(2).including(iAlloys, iBloomery, iCalendar).without(iMasonry, iSeafaring)
	),
	Civilization(
		iMaya,
		iGold=100,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(1).including(iProperty, iMasonry, iSmelting, iCeremony).without(iSailing)
	),
	Civilization(
		iMacedon,
		iGold=1000,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iCitizenship, iSyncretism, iHegemony],
		iAdvancedStartPoints=150,
		techs=techs.column(4).including(iPhilosophy, iGeneralship, iCurrency)
	),
	Civilization(
		iNumidia,
		iGold=100,
		lCivics=[iDespotism, iSlavery, iRedistribution],
		iAdvancedStartPoints=100,
		techs=techs.column(4).without(iPriesthood)
	),
	Civilization(
		iArmenia,
		iGold=100,
		iAdvancedStartPoints=100,
		iStateReligion=iZoroastrianism,
		lCivics=[iMonarchy, iRedistribution, iClergy],
		techs=techs.column(4).including(iGeneralship,iCurrency,iAesthetics).without(iNavigation)
	),

	Civilization(
		iDravidia,
		iGold=200,
		iAdvancedStartPoints=80,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iMathematics, iContract, iPriesthood)
	),
	Civilization(
		iEthiopia,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys, iWriting, iCalendar, iPriesthood)
	),
	Civilization(
		iToltecs,
		iGold=50,
		lCivics=[iRedistribution, iDeification],
		techs=techs.column(2).including(iConstruction, iArithmetics).without(iSeafaring)
	),
	Civilization(
		iVandals,
		iGold=100,
		lCivics=[iDespotism],
		techs=techs.column(3).without(iConstruction, iWriting)
	),
	Civilization(
		iParthia,
		iGold=300,
		iStateReligion=iZoroastrianism,
		lCivics=[iMonarchy, iMerchantTrade, iClergy, iHegemony],
		iAdvancedStartPoints=150,
		techs=techs.column(4).including(iGeneralship, iCurrency, iEngineering)
	),
	Civilization(
		iKushans,
		iGold=100,
		iAdvancedStartPoints=120,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iSyncretism, iHegemony],
		techs=techs.column(4).including(iGeneralship, iCurrency, iPhilosophy).without(iNavigation)
	),
	Civilization(
		iKorea,
		iGold=200,
		iAdvancedStartPoints=60,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCasteSystem, iRedistribution, iSyncretism],
		techs=techs.column(4).without(iNavigation).including(iPhilosophy)
	),
	Civilization(
		iKhmer,
		iGold=50,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(4).without(iNavigation).including(iEngineering)
	),
	Civilization(
		iGoths,
		iGold=150,
		lCivics=[iMonarchy, iSlavery],
		techs=techs.column(4).including(iGeneralship, iRecurveBow, iCurrency, iSteel),
	),
	Civilization(
		iGhana,
		iGold=200,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(3).including(iBloomery, iRiding, iContract)
	),
	Civilization(
		iByzantium,
		iGold=400,
		iAdvancedStartPoints=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iCitizenship, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).without(iArchitecture, iArtisanry, iEthics)
	),
	Civilization(
		iHuns,
		iGold=300,
		iAdvancedStartPoints=100,
		lCivics=[iDespotism, iSlavery, iHegemony],
		techs=techs.column(4).including(iGeneralship, iRecurveBow, iSteel).without(iSeafaring, iNavigation)
	),
	Civilization(
		iFrance,
		iGold=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(5).including(iRecurveBow, iEthics)
	),
	Civilization(
		iMalays,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(5).including(iEthics).without(iGeneralship, iEngineering)
	),
	Civilization(
		iJapan,
		iGold=100,
		iAdvancedStartPoints=60,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iCasteSystem, iRedistribution, iDeification, iThalassocracy],
		techs=techs.column(5).including(iNobility, iRecurveBow, iSteel, iArchitecture, iArtisanry)
	),
	Civilization(
		iNorse,
		iGold=150,
		lCivics=[iElective, iSlavery, iMerchantTrade, iThalassocracy],
		techs=techs.column(6).without(iScholarship, iEthics)
	),
	Civilization(
		iGokturks,
		iGold=100,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(5).including(iSteel, iRecurveBow).without(iNavigation, iMedicine, iPhilosophy)
	),
	Civilization(
		iArabia,
		iGold=300,
		iAdvancedStartPoints=150,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		lEnemies=[iIndependent, iIndependent2],
		techs=techs.column(6).including(iAlchemy, iTheology, iLateenSails, iNobility, iSpringSteel)
	),
	Civilization(
		iTibet,
		iGold=50,
		iAdvancedStartPoints=25,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(5).including(iRecurveBow, iScholarship, iEthics)
	),
	Civilization(
		iKhazars,
		iGold=100,
		iStateReligion=iJudaism,
		lCivics=[iElective, iSlavery, iMerchantTrade],
		techs=techs.column(5).including(iRecurveBow, iSteel, iPolitics).without(iEngineering, iAesthetics, iLaw, iPhilosophy, iShipbuilding, iNavigation)
	),
	Civilization(
		iKanemBornu,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iDeification],
		techs=techs.column(4).without(iNavigation, iPriesthood)
	),
	Civilization(
		iMoors,
		iGold=400,
		iAdvancedStartPoints=150,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iAlchemy)
	),
	Civilization(
		iJava,
		iGold=300,
		iAdvancedStartPoints=100,
		iStateReligion=iHinduism,
		lCivics=[iDespotism, iCitizenship, iCasteSystem, iMerchantTrade, iDeification, iThalassocracy],
		techs=techs.column(6).without(iRecurveBow, iPolitics, iScholarship)
	),
	Civilization(
		iSpain,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iGuilds).without(iTheology)
	),
	Civilization(
		iGeorgia,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7).including(iGuilds).without(iSpringSteel, iLateenSails)
	),
	Civilization(
		iEngland,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7)
	),
	Civilization(
		iYemen,
		iGold=100,
		iAdvancedStartPoints=50,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iAlchemy).without(iSpringSteel)
	),
	Civilization(
		iHolyRome,
		iGold=150,
		iAdvancedStartPoints=150,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iTheocracy, iManorialism, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).without(iCivilService)
	),
	Civilization(
		iBurma,
		iGold=100,
		iAdvancedStartPoints=80,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iHegemony],
		techs=techs.column(6).including(iFeudalism, iTheology, iNobility)
	),
	Civilization(
		iHausa,
		iGold=200,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(3).including(iBloomery, iRiding, iPriesthood).without(iNavigation)
	),
	Civilization(
		iRus,
		iGold=200,
		iAdvancedStartPoints=50,
		lCivics=[iElective, iMerchantTrade],
		techs=techs.column(7).including(iGuilds).without(iCivilService, iSpringSteel, iTheology)
	),
	Civilization(
		iSamanids,
		iGold=100,
		iAdvancedStartPoints=100,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		lEnemies=[iArabia, iParthia, iPersia, iIndependent, iIndependent2],
		techs=techs.column(7).including(iAlchemy, iMachinery, iLimbProtection)
	),
	Civilization(
		iBenin,
		iGold=200,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(3).including(iBloomery, iRiding, iContract, iPriesthood).without(iNavigation)
	),
	Civilization(
		iMisr,
		iGold=250,
		iAdvancedStartPoints=150,
		iStateReligion=iShia,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iAlchemy, iDoctrine, iLimbProtection, iSelectiveBreeding)
	),
	Civilization(
		iBuyids,
		iGold=250,
		iAdvancedStartPoints=100,
		iStateReligion=iShia,
		lEnemies=[iArabia],
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(7).including(iMachinery, iLimbProtection)
	),
	Civilization(
		iSomalia,
		iGold=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iCitizenship, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(5).including(iRecurveBow, iScholarship)
	),
	Civilization(
		iVietnam,
		iGold=200,
		iStateReligion=iConfucianism,
		lCivics=[iMonarchy, iCasteSystem, iRedistribution, iMonasticism, iThalassocracy],
		techs=techs.column(7).including(iAlchemy, iLimbProtection)
	),
	Civilization(
		iSwahili,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iIslam,
		lCivics=[iElective, iCitizenship, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(6).including(iLateenSails, iAlchemy)
	),
	Civilization(
		iGhorids,
		iGold=150,
		iStateReligion=iIslam,
		lEnemies=[iIndependent, iIndependent2, iSamanids, iBuyids, iArabia],
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(7).including(iLimbProtection, iSelectiveBreeding, iDoctrine)
	),
	Civilization(
		iBuganda,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(2).including(iAlloys)
	),
	Civilization(
		iPoland,
		iGold=100,
		iAdvancedStartPoints=80,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7).including(iLimbProtection).without(iTheology)
	),
	Civilization(
 		iMorocco,
 		iGold=150,
 		iStateReligion=iIslam,
 		lEnemies=[iSpain, iMoors],
 		lCivics=[iDespotism, iSlavery, iMerchantTrade, iFanaticism, iVassalage, iHegemony],
 		techs=techs.column(7).including(iDoctrine, iMachinery, iGuilds, iReligiousOrders)
 	),
	Civilization(
		iTurks,
		iGold=250,
		iStateReligion=iIslam,
		lEnemies=[iPersia, iParthia, iGhorids, iBuyids, iArabia, iSamanids],
		lCivics=[iMonarchy, iSlavery, iClergy, iMerchantTrade, iHegemony],
		techs=techs.column(7).including(iSelectiveBreeding, iLimbProtection).without(iFortification)
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
		iPortugal,
		iGold=200,
		iAdvancedStartPoints=60,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(8).including(iPatronage)
	),
	Civilization(
		iInca,
		iGold=700,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iDeification],
		techs=techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood).without(iSeafaring, iRiding, iShipbuilding)
	),
	Civilization(
		iOman,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iSlavery, iMerchantTrade, iClergy, iThalassocracy],
		techs=techs.column(7).including(iAlchemy, iSelectiveBreeding).without(iFeudalism)
	),
	Civilization(
		iItaly,
		iGold=350,
		iAdvancedStartPoints=250,
		iStateReligion=iCatholicism,
		lCivics=[iRepublic, iCitizenship, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(8).including(iCommune)
	),
	Civilization(
		iMongols,
		iGold=250,
		iAdvancedStartPoints=50,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(8).including(iPaper, iCompass).without(iDoctrine, iTheology)
	),
	Civilization(
		iAztecs,
		iGold=200,
		iAdvancedStartPoints=30,
		lCivics=[iMonarchy, iCitizenship, iSlavery, iRedistribution, iDeification, iHegemony],
		techs=techs.column(4).including(iGeneralship, iAesthetics, iCurrency, iLaw).without(iSeafaring, iRiding, iShipbuilding, iCement, iNavigation)
	),
	Civilization(
		iZimbabwe,
		iGold=100,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(2).including(iAlloys).without(iSeafaring, iShipbuilding)
	),
	Civilization(
		iTunis,
		iGold=200,
		iAdvancedStartPoints=150,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(8).including(iCommune, iCompass)
	),
	Civilization(
		iThailand,
		iGold=250,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iMonasticism, iThalassocracy],
		techs=techs.column(9).without(iCompass, iReligiousOrders, iDoctrine)
	),
	Civilization(
		iMali,
		iGold=300,
		iStateReligion=iIslam,
		lEnemies=[iGhana],
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(6).including(iFeudalism, iTheology, iLateenSails, iAlchemy, iGuilds)
	),
	Civilization(
		iSweden,
		iGold=200,
		iAdvancedStartPoints=800,
		iStateReligion=iProtestantism,
		lCivics=[iElective, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iPatronage).including(iCompanies)
	),
	Civilization(
		iTatars,
		iGold=200,
		iAdvancedStartPoints=200,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iMonasticism, iHegemony],
		techs=techs.column(8).including(iCommune, iPaper, iCompass, iGunpowder).without(iTheology)
	),
	Civilization(
		iRussia,
		iGold=300,
		iAdvancedStartPoints=200,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iVassalage, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(9).without(iPaper,iReligiousOrders)
	),
	Civilization(
		iAdal,
		iGold=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(7)
	),
	Civilization(
		iOttomans,
		iGold=300,
		iAdvancedStartPoints=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iTheocracy, iSlavery, iMerchantTrade, iSyncretism, iHegemony],
		techs=techs.column(8).including(iCommune, iPaper, iReligiousOrders, iGunpowder)
	),
	Civilization(
		iCongo,
		iGold=300,
		lCivics=[iSlavery, iRedistribution],
		techs=techs.column(4).including(iGeneralship).without(iCement, iNavigation, iWriting, iLiterature)
	),
	Civilization(
		iTimurids,
		iGold=300,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iRegulatedTrade, iSyncretism, iHegemony],
		lEnemies=[iIndependent, iIndependent2, iPersia, iGhorids, iArmenia, iOttomans, iMongols, iParthia, iTurks],
		techs=techs.column(8).including(iCommune, iCropRotation, iPaper, iGunpowder)
	),
	Civilization(
		iSonghai,
		iGold=400,
		iStateReligion=iIslam,
		lEnemies=[iMali, iGhana],
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iClergy, iHegemony],
		techs=techs.column(7).including(iCropRotation, iLimbProtection, iSelectiveBreeding, iMachinery, iGuilds)
	),
	Civilization(
		iFunj,
		iGold=200,
		iStateReligion=iIslam,
		lEnemies=[iNubia],
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iSyncretism, iHegemony],
		techs=techs.column(8).including(iGuilds, iCommune, iGunpowder, iCropRotation, iPaper)
	),
	Civilization(
		iIran,
		iGold=600,
		iAdvancedStartPoints=250,
		iStateReligion=iShia,
		lEnemies=[iTimurids],
		lCivics=[iMonarchy, iTheocracy, iSlavery, iMerchantTrade, iFanaticism, iHegemony],
		techs=techs.column(10).including(iHeritage, iFirearms)
	),
	Civilization(
		iMadagascar,
		iGold=100,
		lCivics=[iDespotism, iSlavery, iRedistribution, iDeification, iThalassocracy],
		techs=techs.column(8).including(iCompanies, iPatronage, iCommune, iDiscipline, iCompass)
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iAdvancedStartPoints=300,
		iStateReligion=iProtestantism,
		lCivics=[iRepublic, iBureaucracy, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(11).without(iHeritage)
	),
	Civilization(
		iKatanga,
		iGold=200,
		techs=techs.column(1).including(iCeremony, iSmelting).without(iSailing)
	),
	Civilization(
		iAshanti,
		iGold=300,
		lCivics=[iMonarchy, iSlavery, iMerchantTrade, iHegemony],
		techs=techs.column(7).including(iLimbProtection)
	),
	Civilization(
		iManchuria,
		iGold=800,
		iAdvancedStartPoints=300,
		iStateReligion=iConfucianism,
		lCivics=[iDespotism, iBureaucracy, iSlavery, iMerchantTrade, iSyncretism, iIsolationism],
		techs=techs.column(11).without(iOptics, iExploration, iAcademia).including(iCombinedArms, iHorticulture)
	),
	Civilization(
		iGermany,
		iGold=800,
		iAdvancedStartPoints=300,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iBureaucracy, iManorialism, iRegulatedTrade, iClergy, iHegemony],
		techs=techs.column(12).without(iCivilLiberties, iHorticulture)
	),
	Civilization(
		iSaudis,
		iGold=50,
		iAdvancedStartPoints=200,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iTheocracy, iSlavery, iMerchantTrade, iFanaticism],
		techs=techs.column(11).including(iCombinedArms, iGeography, iHorticulture).without(iAcademia)
	),
	Civilization(
		iAmerica,
		iGold=1500,
		iAdvancedStartPoints=500,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iIsolationism],
		techs=techs.column(13).including(iRepresentation, iChemistry)
	),
	Civilization(
		iZulu,
		iGold=200,
		lCivics=[iDespotism, iSlavery, iRedistribution],
		techs=techs.column(3).including(iBloomery).without(iWriting, iNavigation, iShipbuilding)
	),
	Civilization(
		iBoers,
		iGold=500,
		iAdvancedStartPoints=200,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iClergy, iNationhood],
		techs=techs.column(13).including(iNationalism, iChemistry, iRepresentation)
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iAdvancedStartPoints=400,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(13).including(iBiology, iRepresentation, iNationalism)
	),
	Civilization(
		iMexico,
		iGold=500,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(13).including(iRepresentation, iNationalism)
	),
	Civilization(
		iColombia,
		iGold=750,
		iAdvancedStartPoints=200,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(13).including(iRepresentation, iNationalism)
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iAdvancedStartPoints=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iConstitution, iSlavery, iFreeEnterprise, iClergy, iColonialism],
		techs=techs.column(13).including(iRepresentation, iNationalism, iBiology)
	),
	Civilization(
		iBelgium,
		iGold=600,
		iAdvancedStartPoints=800,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iConstitution, iIndividualism, iFreeEnterprise, iClergy, iNationhood],
		techs=techs.column(14).without(iBiology, iRepresentation)
	),
	Civilization(
		iAustralia,
		iGold=600,
		iAdvancedStartPoints=200,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(14).including(iRailroad)
	),
	Civilization(
		iSouthAfrica,
		iGold=1000,
		iAdvancedStartPoints=400,
		iStateReligion=iProtestantism,
		lEnemies=[iBoers, iZulu],
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(14).including(iRailroad, iEngine, iBallistics)
	),
	Civilization(
		iCanada,
		iGold=1000,
		iAdvancedStartPoints=250,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iSecularism, iNationhood],
		techs=techs.column(14).including(iBallistics, iEngine, iRailroad, iJournalism)
	),
]

### Starting units ###

dStartingUnits = CivDict({

	iBabylonia: {
		iSettle: 1,
		iWork: 2,
		iAttack: 2,
		iBase: 1,
		iDefend: 1,
	},


	iMinoa: {
		iSettle: 1,
		iWork: 1,
		iBase: 1,
	},

	iElam: {
		iSettle: 1,
		iWork: 1,
		iBase: 1,
	},


	iAssyria: {
		iSettle: 1,
		iWork: 2,
		iBase: 1,
		iSiege: 2,
		iCounter: 4,
	},
	iChina: {
		iSettle: 1,
		iWork: 2,
		iBase: 1,
		iDefend: 2,
		iAttack: 1,
	},
	iHittites: {
		iSettle: 1,
		iWork: 1,
		iBase: 1,
		iDefend: 1,
		iAttack: 2,
		iHarass: 1,
	},
	iNubia: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iBase: 2,
	},

	iMycenae: {
		iSettle: 1,
		iWork: 2,
		iAttack: 3,
		iFerry: 1,
	},

	iGreece: {
		iSettle: 2,
		iWork: 2,
		iAttack: 3,
		iDefend: 2,
		iFerry: 1,
	},
	iIndia: {
		iSettle: 2,
		iWork: 2,
		iDefend: 1,
		iCounter: 1,
		iAttack: 1,
		iHarass: 1,
	},
	iPhoenicia: {
		iSettle: 1,
		iWork: 2,
		iDefend: 1,
		iCounter: 1,
		iSettleSea: 1,
		iFerry: 1,
		iEscort: 1,
	},
	iJudah: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iAttack: 3,
	},

	iPolynesia: {
		iSettle: 1,
		iSettleSea: 1,
		iWorkerSea: 1,
	},
	iScythia: {
		iSettle: 3,
		iDefend: 3,
		iHarass: 6,
	},

	iPersia: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iShock: 4,
		# 1 War Elephant
	},
	iSparta: {
		iSettle: 1,
		iWork: 1,
		iBase: 2,
		iAttack: 2,
		iCityAttack: 1,
		iSkirmish: 1,
	},
	iCelts: {
		iSettle: 3,
		iDefend: 3,
		iAttack: 4,
		iExplore: 1,
	},
	iRome: {
		iSettle: 2,
		iWork: 3,
		iDefend: 3,
		iAttack: 10,
		iSiege: 2,
		iSettleSea: 2,
		iFerry: 1,
		iWorkerSea: 1,
	},
	iGermania: {
		iSettle: 4,
		iDefend: 4,
	},
	iMaya: {
		iSettle: 1,
		iWork: 1,
		iSkirmish: 2,
	},
	iMacedon: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iShock: 12,
	},
	iNumidia: {
		iSettle: 2,
		iWork: 1,
		iShock: 3,
	},
	iArmenia: {
		iSettle: 1,
		iWork: 1,
		iShock: 2,
		iDefend: 1,
		iMissionary: 1,
	},
	iDravidia: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 2,
		iDefend: 1,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
		# 1 War Elephant
	},
	iEthiopia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 2,
		iAttack: 1,
		iWorkerSea: 1,
		iEscort: 1,
		# 1 Shotelai
	},
	iParthia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 5,
		iAttack: 10,
		iSiege: 4,
		iShock: 8,
	},
	iToltecs: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iAttack: 2,
	},
	iVandals: {
		iSettle: 2,
		iDefend: 6,
	},

	iKushans: {
		iSettle: 3,
		iWork: 3,
		iDefend: 2,
		iShockCity: 4,
		iCityAttack: 2,
		iSkirmish: 2,
		iCitySiege: 2,
	},
	iKorea: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iAttack: 1,
		iShock: 1,
		iMissionary: 1,
	},
	iKhmer: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iAttack: 1,
		iMissionary: 1,
		iWorkerSea: 1,
	},
	iGoths: {
		iSettle: 3,
		iWork: 1,
		iDefend: 4,
		iHarass: 2,
		iAttack: 2,
	},
	iGhana: {
		iSettle: 1,
		iWork: 1,
		iCounter: 1,
		iSkirmish: 1,
		iDefend: 1,
	},
	iByzantium: {
		iSettle: 4,
		iWork: 2,
		iAttack: 4,
		iCounter: 2,
		iDefend: 2,
		iMissionary: 1,
		iFerry: 2,
		iEscort: 2,
	},
	iHuns: {
		iSettle: 3,
		iWork: 2,
		iHarass: 16,
		iDefend: 3,
	},
	iFrance: {
		iSettle: 2,
		iWork: 1,
		iDefend: 2,
		iCounter: 2,
		iAttack: 2,
		iMissionary: 1,
	},
	iMalays: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 2,
		iWorkerSea: 1,
		iDefend: 1,
		iAttack: 1,
		iMissionary: 2,
		iEscort: 1,
	},
	iJapan: {
		iSettle: 3,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 2,
	},
	iNorse: {
		iSettle: 1,
		iWork: 2,
		iSettleSea: 2,
		iDefend: 2,
		iExplore: 1,
		iAssaultSea: 1,
		iWorkerSea: 2,
	},
	iGokturks: {
		iSettle: 6,
		iWork: 3,
		iDefend: 3,
		iHarass: 7,
		iExplore: 1,
	},
	iArabia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 1,
		iShock: 2,
		iAttack: 2,
		iWork: 1,
		iWorkerSea: 1,
	},
	iTibet: {
		iSettle: 2,
		iWork: 1,
		iDefend: 3,
		iHarass: 4,
		iMissionary: 2,
	},
	iKhazars: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
 		iCounter: 1,
 		iHarass: 2,
 		iShock: 4,
		iMissionary: 2,
	},
	iKanemBornu: {
		iSettle: 1,
		iWork: 1,
		iDefend: 3,
		iCounter: 1,
		iAttack: 1,
	},
	iMoors: {
		iSettle: 2,
		iWork: 1,
		iDefend: 1,
		iMissionary: 2,
		iWorkerSea: 1,
		iFerry: 1,
		iEscort: 1,
	},
	iJava : {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iCityAttack: 2,
		iFerry: 2,
		iEscort: 1,
 		iExploreSea: 1,
		iWorkerSea: 1,
		iMissionary: 1,
	},
	iSpain: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 6,
		iShock: 2,
		iMissionary: 1,
	},
	iGeorgia: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iSiege: 1,
		iAttack: 4,
		iShock: 2,
		iMissionary: 1,
	},
	iEngland: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iShockCity: 1,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
		iFerry: 1,
	},
	iYemen: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iExploreSea: 1,
		iMissionary: 1,

	},
	iHolyRome: {
		iSettle: 4,
		iWork: 2,
		iDefend: 3,
		iCityAttack: 3,
		iShockCity: 3,
		iCitySiege: 4,
		iMissionary: 1,
	},
	iBurma: {
		iSettle: 2,
		iWork: 2,
		iDefend: 3,
		iCounter: 2,
		iAttack: 2,
		iMissionary: 1,
	},
	iVietnam: {
		iSettle: 1,
		iWork: 2,
		iDefend: 1,
		iSkirmish: 4,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
	},
	iHausa: {
		iSettle: 1,
		iAttack: 2,
		iDefend: 2,
	},
	iRus: {
		iSettle: 3,
		iWork: 2,
		iDefend: 3,
		iAttack: 2,
		iCounter: 1,
	},
	iSamanids: {
		iSettle: 2,
		iWork: 3,
		iAttack: 8,
		iHarass: 6,
		iSiege: 4,
		iMissionary: 2,
	},
	iBenin: {
		iSettle: 1,
		iCounter: 2,
		iDefend: 3,
	},
	iMisr: {
		iSettle: 2,
		iWork: 3,
		iDefend: 2,
		iAttack: 1,
		iShock: 1,
		iMissionary: 2,
	},
	iBuyids: {
		iSettle: 1,
		iWork: 3,
		iDefend: 2,
		iAttack: 6,
		iCounter: 6,
		iShock: 2,
		iSiege: 3,
		iMissionary: 2,
	},
	iSomalia: {
		iSettle: 1,
		iWork: 1,
		iDefend: 3,
		iCounter: 2,
		iExploreSea: 2,
		iMissionary: 1,
	},
	iSwahili: {
		iSettle: 1,
		iWork: 3,
		iWorkerSea: 2,
		iDefend: 2,
		iSkirmish: 2,
		iExploreSea: 1,
		iSettleSea: 1,
		iFerry: 1,
		iMissionary: 1,
	},
	iGhorids: {
		iSettle: 4,
		iWork: 3,
		iDefend: 3,
		iShockCity: 4,
		iAttack: 8,
		iSiege: 4,
		iMissionary: 3,
	},
	iBuganda: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iCounter: 1,
	},
	iPoland: {
		iSettle: 2,
		iWork: 2,
		iDefend: 1,
		iAttack: 2,
		iShock: 2,
		iSiege: 1,
		iMissionary: 1,
	},
	iTurks: {
		iSettle: 2,
		iWork: 3,
		iDefend: 5,
		iHarass: 12,
		iSiege: 5,
		iShock: 5,
		iExplore: 1,
		iMissionary: 2,
	},
	iMorocco: {
 		iSettle: 2,
 		iWork: 1,
 		iSiege: 2,
 		iAssaultSea: 2,
 		iEscort: 1,
 		iCounter: 2,
 		iAttack: 4,
 	},
	iJerusalem: {
		iSettle: 1,
		iWork: 1,
		iDefend: 2,
		iAttack: 3,
		iSiege: 1,
		iMissionary: 3,
	},
	iPortugal: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 1,
		iDefend: 4,
		iCounter: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iEscort: 2,
	},
	iInca: {
		iSettle: 1,
		iWork: 4,
		iCityAttack: 4,
		iDefend: 2,
		# if not human: 1 Settler
	},
	iOman: {
		iSettle: 1,
		iWork: 2,
		iCounter: 1,
		iCityAttack: 2,
		iDefend: 2,
		iMissionary: 1,
		iExploreSea: 2,
	},
	iItaly: {
		iSettle: 1,
		iWork: 2,
		iDefend: 1,
		iMissionary: 1,
		iWorkerSea: 1,
		iFerry: 1,
		iEscort: 1,
	},
	iMongols: {
		iSettle: 3,
		iWork: 4,
		iDefend: 4,
		iAttack: 3,
		iHarass: 5,
		iShock: 8,
		iSiege: 4,
		iExplore: 2,
	},
	iAztecs: {
		iSettle: 1,
		iWork: 2,
		iAttack: 4,
		iDefend: 2,
		iWorkerSea: 1,
	},
	iTimurids: {
		iSettle: 3,
		iWork: 2,
		iSiege: 8,
		iAttack: 8,
		iHarass: 8,
		iShock: 20,
		iDefend: 8,
		iMissionary: 2,
	},
	iZimbabwe: {
		iSettle: 1,
		iDefend: 2,
		iCounter: 2,
		iWork: 1,
	},
	iTunis: {
		iSettle: 1,
		iWork: 2,
		iWorkerSea: 1,
		iDefend: 3,
		iMissionary: 2,
		iExploreSea: 3,
		iAssaultSea: 3,
	},
	iThailand: {
		iSettle: 1,
		iWork: 2,
		iCounter: 2,
		iShock: 2,
		iMissionary: 1,
	},
	iMali: {
		iSettle: 1,
		iWork: 2,
		iSkirmish: 3,
		iAttack: 4,
		iShock: 6,
		iDefend: 3,
		iMissionary: 2,
		iSiege: 2,
	},
	iSweden: {
		iSettle: 2,
		iWork: 3,
		iCounter: 3,
		iDefend: 2,
		iAttack: 2,
		iMissionary: 2,
		iSettleSea: 1,
		iEscort: 2,
		iWorkerSea: 1,
	},
	iTatars: {
		iSettle: 3,
		iWork: 2,
		iSiege: 3,
		iShock: 6,
		iHarass: 6,
		iDefend: 2,
	},
	iRussia: {
		iSettle: 4,
		iWork: 5,
		iDefend: 4,
		iAttack: 3,
		iCounter: 4,
		iSiege: 3,
		iExplore: 2,
		iMissionary: 3,
	},
	iAdal: {
		iSettle: 1,
		iWork: 2,
		iDefend: 3,
		iShock: 2,
		iAttack: 2,
		iExploreSea: 1,
		iMissionary: 1,
	},
	iOttomans: {
		iSettle: 3,
		iWork: 3,
		iAttack: 4,
		iDefend: 2,
		iShock: 3,
		iSiege: 4,
		iMissionary: 2,
	},
	iCongo: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
		iExplore: 1,
	},
	iSonghai: {
		iSettle: 2,
		iWork: 2,
		iAttack: 8,
		iHarass: 2,
		iDefend: 4,
		iMissionary: 1,
		iSiege: 2,
	},
	iFunj: {
		iSettle: 1,
		iWork: 1,
		iAttack: 3,
		iCounter: 2,
		iShock: 2,
		iDefend: 2,
		iSiege: 2,
		iMissionary: 1,
	},
	iIran: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 3,
	},
	iMadagascar: {
		iSettle: 1,
		iWork: 2,
		iCounter: 2,
		iDefend: 2,
		iExploreSea: 1,
		iAssaultSea: 1,
	},
	iNetherlands: {
		iSettle: 2,
		iSettleSea: 2,
		iWork: 2,
		iAttack: 6,
		iCounter: 2,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iExploreSea: 2,
	},
	iKatanga: {
		iSettle: 1,
		iWork: 1,
		iAttack: 1,
		iCounter: 1,
		iDefend: 1,
	},
	iAshanti: {
		iSettle: 1,
		iAttack: 3,
		iDefend: 3,
		iWork: 1,
	},
	iManchuria: {
		iSettle: 3,
		iWork: 4,
		iDefend: 3,
		iCityAttack: 6,
		iCitySiege: 6,
		iShockCity: 10,
		iExplore: 1,
	},
	iGermany: {
		iSettle: 4,
		iWork: 2,
		iAttack: 3,
		iDefend: 2,
		iSiege: 3,
		iMissionary: 2,
	},
	iSaudis: {
		iSettle: 4,
		iWork: 2,
		iDefend: 2,
		iMissionary: 2,
		# 6 Camel Gunners
	},
	iAmerica: {
		iSettle: 6,
		iWork: 4,
		iSkirmish: 2,
		iAttack: 3,
		iSiege: 2,
		iExplore: 1,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 1,
	},
	iBoers: {
		iSettle: 1,
		iWork: 2,
		iAttack: 3,
		iDefend: 2,
		iShock: 2,
		iSiege: 3,
		iMissionary: 2,
	},
	iArgentina: {
		iSettle: 2,
		iWork: 3,
		iAttack: 3,
		iDefend: 2,
		iSiege: 2,
		iShock: 2,
		iMissionary: 1,
		iFerry: 1,
		iEscort: 2,
	},
	iMexico: {
		iSettle: 1,
		iWork: 2,
		iShock: 4,
		iDefend: 3,
		iAttack: 2,
		iSkirmish: 2,
		iMissionary: 1,
	},
	iColombia: {
		iSettle: 4,
		iWork: 2,
		iDefend: 2,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 1,
		iFerry: 1,
		iAttackSea: 1,
	},
	iZulu: {
		iSettle: 1,
		iWork: 1,
		iCounter: 4,
		iDefend: 1,
	},
	iBrazil: {
		iSettle: 5,
		iWork: 3,
		iSkirmish: 3,
		iDefend: 3,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iFerry: 2,
		iEscort: 3,
	},
	iBelgium: {
		iSettle: 1,
		iWork: 3,
		iExplore: 1,
		iSkirmish: 4,
		iDefend: 5,
		iSiege: 3,
		iMissionary: 1,
		iFerry: 2,
		iExploreSea: 1,
	},
	iAustralia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 4,
		iMissionary: 2,
		iHarass: 2,
		iWorkerSea: 2,
		iFerry: 2,
		iLightEscort: 1,
	},
	iSouthAfrica: {
		iSettle: 2,
		iWork: 3,
		iAttack: 3,
		iDefend: 2,
		iShock: 1,
		iSiege: 2,
		iMissionary: 2,
		iFerry: 1,
		iAttackSea: 1,
	},
	iCanada: {
		iSettle: 5,
		iWork: 3,
		iShock: 3,
		iDefend: 5,
		iMissionary: 1,
		iFerry: 2,
		iEscort: 1,
		iLightEscort: 1,
	},
}, {})

dExtraAIUnits = CivDict({
	iMorocco: {
		iAttack: 3,
	},
	iArabia: {
		iAttack: 5,

	},
	iTimurids: {
		iSiege: 4,
		iAttack: 4,
		iHarass: 2,
		iShock: 15,
	},
	iIndia : {
		iHarass: 1,
		iAttack: 1,
		iDefend: 1,
	},
	iRome: {
		iDefend: 2,
		iAttack: 2,
	},
	iFrance: {
		iDefend: 2,
	},
	iJapan: {
		iDefend: 2,
		iAttack: 3,
	},
	iDravidia: {
		iShock: 1,
		iMissionary: 1,
	},
	iKushans: {
		iShockCity: 4,
		iCityAttack: 2,
		iSiege: 3,
	},
	iKorea: {
		iCounter: 2,
		iDefend: 2,
	},
	iMalays: {
		iDefend: 2,
	},
	iNorse: {
		iExploreSea: 1,
		iAssaultSea: 1,
	},
	iJava: {
		iCityAttack: 2,
	},
	iKanemBornu: {
		iDefend: 2,
	},
	iGeorgia: {
		iShock: 6,
	},
	iEngland: {
		iAttack: 2,
		iShock: 2,
	},
	iSamanids: {
		iAttack: 8,
		iDefend: 4,
		iSiege: 5,
	},
	iHolyRome: {
		iCityAttack: 2,
		iSiege: 1,
	},
	iPoland: {
		iCounter: 2,
	},
	iMongols: {
		iDefend: 2,
		iAttack: 2,
		iShock: 10,
		iSiege: 6,
		iHarass: 5,
		iExplore: 2,
	},
	iInca: {
		iCityAttack: 2,
	},
	iAztecs: {
		iAttack: 1,
		iSkirmish: 1,
		iDefend: 1,
	},
	iTatars: {
		iWork: 2,
	},
	iCongo: {
		iSettle: 1,
		iWork: 1,
		iDefend: 1,
		iAttack: 2,
	},
	iMali: {
		iAttack: 3,
		iSiege: 2,
	},
	iSonghai: {
		iAttack: 6,
		iShock: 4,
		iSiege: 3,
	},
	iFunj: {
		iAttack: 2,
	},
	iIran: {
		iAttack: 6,
		iSiege: 3,
	},
	iKatanga: {
		iDefend: 2,
	},
	iTurks: {
		iDefend: 3,
		iHarass: 6,
	},
	iManchuria: {
		iCityAttack: 4,
		iCitySiege: 6,
		iShockCity: 8,
	},
	iGermany: {
		iAttack: 10,
		iSiege: 5,
	},
	iAmerica: {
		iDefend: 1,
		iAttack: 4,
 		iSiege: 2,
 		iDefend: 4,
	},
	iArgentina: {
		iDefend: 3,
		iShock: 2,
		iSiege: 2,
	},
	iZulu: {
		iDefend: 2,
		iCounter: 3,
	},
	iSouthAfrica: {
		iAttack: 2,
		iDefend: 2,
		iSiege: 4,
		iShock: 1,
	},
	iBrazil: {
		iDefend: 1,
	}
}, {})

dAdditionalUnits = CivDict({
	iIndia: {
		iDefend: 2,
		iAttack: 1,
	},
	iGreece: {
		iDefend: 1,
	},
	iPersia: {
		iAttack: 7,
	},
	iPhoenicia: {
		iHarass: 1,
		iShock: 1
	},
	iPolynesia: {
		iBase: 2,
	},
	iRome: {
		iAttack: 4,
	},
	iJapan: {
		iDefend: 2,
		iAttack: 2,
	},
	iDravidia: {
		iAttack: 2,
		iShock: 1,
	},
	iEthiopia: {
		iDefend: 2,
		# 2 Shotelai
	},
	iKorea: {
		iHarass: 2,
		# 2 Crossbowmen
	},
	iMaya: {
		iDefend: 2,
		iAttack: 2,
	},
	iByzantium: {
		iShock: 2,
		iAttack: 3,
		iCounter: 1,
	},
	iFrance: {
		iDefend: 3,
		iAttack: 3,
	},
	iNorse: {
		# 3 Huscarls
	},
	iTurks: {
		iHarass: 4,
	},
	iArabia: {
		iAttack: 2,
		iShock: 1,
	},
	iTibet: {
		iHarass: 2,
	},
	iKhazars: {
		iShock: 2,
	},
	iKhmer: {
		iAttack: 3,
		iShockCity: 2,
	},
	iMali: {
		iSkirmish: 2,
		iAttack: 2,
	},
	iMoors: {
		# 2 Camel Archers
	},
	iSpain: {
		iDefend: 3,
		iAttack: 3,
	},
	iEngland: {
		iDefend: 3,
		iAttack: 3,
	},
	iHolyRome: {
		iDefend: 3,
		iAttack: 3,
	},
	iPoland: {
		iDefend: 2,
		iShock: 2,
	},
	iMorocco: {
		iDefend: 2,
		iAttack: 3,
	},
	iPortugal: {
		iDefend: 3,
		iCounter: 3,
	},
	iInca: {
		iAttack: 5,
		iDefend: 3,
	},
	iItaly: {
		iDefend: 2,
		iCounter: 2,
	},
	iMongols: {
		iDefend: 2,
		iHarass: 2,
		iShock: 4,
	},
	iAztecs: {
		iAttack: 5,
		iDefend: 3,
	},
	iGhorids: {
		iShockCity: 4,
		iHarass: 4,
	},
	iThailand: {
		iCounter: 2,
		iShock: 2,
	},
	iTatars: {
		iShock: 2,
		iHarass: 3,
	},
	iRussia: {
		iAttack: 4,
		iDefend: 3,
	},
	iOttomans: {
		iDefend: 3,
		iHarass: 3,
	},
	iCongo: {
		iAttack: 3,
	},
	iIran: {
		iAttack: 2,
		iHarass: 1,
		iSiege: 1,
	},
	iNetherlands: {
		iAttack: 3,
		iCounter: 3,
	},
	iManchuria: {
		iShock: 4,
		iAttack: 4,
		iSiege: 3,
	},
	iGermany: {
		iAttack: 5,
		iSiege: 3,
	},
	iAmerica: {
		iAttack: 3,
		iSkirmish: 3,
		iSiege: 3,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 4,
	},
	iMexico: {
		iShock: 4,
		iSiege: 2,
	},
	iColombia: {
		iAttack: 4,
		iSkirmish: 4,
		iSiege: 2,
	},
	iBrazil: {
		iAttack: 3,
		iSkirmish: 2,
		iSiege: 2,
	},
	iBelgium: {
		iSkirmish: 3,
		iDefend: 3,
		iSiege: 3,
	},
	iAustralia: {
		iAttack: 4,
		iEscort: 3,
	},
	iCanada: {
		iAttack: 4,
		iShock: 2,
		iSiege: 2,
	},
}, {})

dStartingExperience = CivDict({
	iCelts: {
		iAttack: 2,
	},
	iKushans: {
		iCityAttack: 3,
		iShockCity: 3,
		iCitySiege: 2,
	},
	iBuganda: {
		iDefend: 2,
	},
	iGhorids: {
		iAttack: 2,
	},
	iMorocco: {
		iAttack: 2,
		iSiege: 2,
	},
	iTimurids: {
		iAttack: 2,
	},
	iTatars: {
		iShock: 3,
		iHarass: 3,
	},
	iRussia: {
		iExplore: 2,
	},
	iSonghai: {
		iSiege: 5,
		iAttack: 2,
	},
	iManchuria: {
		iShockCity: 3,
		iShock: 3,
	},
	iGermany: {
		iAttack: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iMexico: {
		iShock: 2,
		iDefend: 2,
		iAttack: 2,
		iSkirmish: 2,
	},
	iBoers: {
		iAttack: 3,
		iSiege: 2,
		iDefend: 2,
		iShock: 3,
	},
	iZulu: {
		iAttack: 5,
		iCounter: 5,
	},
	iColombia: {
		iAttack: 2,
		iSkirmish: 2,
		iSiege: 2,
	},
	iSouthAfrica: {
		iAttack: 5,
		iSiege: 5,
		iDefend: 3,
		iShock: 3,
	},
}, {})

dAlwaysTrain = CivDict({
	iGeorgia: [iMonaspa],
	iHuns: [iHeavyHorseArcher],
	iGermania: [iGermanicWarrior],
	iGoths: [iKontosCavalry],
	iAssyria: [iAzmaru, iSiegeRam],
	iGreece: [iHoplite, iCatapult],
	iPhoenicia: [iNumidianCavalry],
	iDravidia: [iWarElephant],
	iByzantium: [iLegion, iDromon],
	iArabia: [iMobileGuard, iGhazi],
	iVietnam: [iRattanArcher],
	iAztecs: [iJaguar],
	iOttomans: [iJanissary, iGreatBombard],
	iMexico: [iGrenadier],
	iColombia: [iAlbionLegion],
	iBrazil: [iGrenadier],
	iZulu: [iImpi],
	iMorocco: [iCamelLancer],
}, [])

dAIAlwaysTrain = CivDict({
	iNorse: [iCrossbowman],
	iSpain: [iCrossbowman],
	iFrance: [iCrossbowman],
	iEngland: [iCrossbowman],
	iHolyRome: [iCrossbowman],
	iPoland: [iCrossbowman],
	iTurks: [iOghuz],
}, [])

dNeverTrain = CivDict({
	iCongo: [iCrossbowman],
}, [])

def createSpecificUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	bHuman = player(iPlayer).isHuman()


	if iCiv == iSamanids:
		makeUnits(iPlayer, iDehqanArcher, tile, 6, UnitAITypes.UNITAI_ATTACK_CITY)
	elif iCiv == iAshanti:
		makeUnits(iPlayer, iTwafo, tile, 2, UnitAITypes.UNITAI_ATTACK).experience(5)
	elif iCiv == iSonghai:
		makeUnits(iPlayer, iGuy, tile, 5, UnitAITypes.UNITAI_ATTACK).experience(5)
	elif iCiv == iMali:
		makeUnits(iPlayer, iFarari, tile, 2, UnitAITypes.UNITAI_ATTACK).experience(5)
	elif iCiv == iKanemBornu:
		makeUnits(iPlayer, iCaravan, tile, 1, UnitAITypes.UNITAI_MERCHANT)
	elif iCiv == iJerusalem:
		makeUnits(iPlayer, iHospitaller, tile, 4, UnitAITypes.UNITAI_MERCHANT).experience(2)
	elif iCiv == iPersia:
		makeUnits(iPlayer, iImmortal, tile, 5, UnitAITypes.UNITAI_ATTACK)
		makeUnits(iPlayer, iWarElephant, tile, 5)
	elif iCiv == iKorea:
		makeUnit(iPlayer, iConfucianMissionary, tile)
	elif iCiv == iSwahili:
		makeUnit(iPlayer, iShiaMissionary, tile)
	elif iCiv == iDravidia:
		makeUnit(iPlayer, iWarElephant, tile)
	elif iCiv == iEthiopia:
		makeUnit(iPlayer, iShotelai, tile)
	elif iCiv == iMalays:
		makeUnit(iPlayer, iHinduMissionary, tile)
	elif iCiv == iNorse:
		if bHuman:
			makeUnits(iPlayer, iHuscarl, tile, 2)
	elif iCiv == iJava:
		makeUnit(iPlayer, iBuddhistMissionary, tile)
	elif iCiv == iSpain:
		if not bHuman:
			makeUnit(iPlayer, iSettler, tile)
			makeUnits(iPlayer, iLancer, tile, 2)
	elif iCiv == iInca:
		if not bHuman:
			makeUnit(iPlayer, iSettler, tile)
	elif iCiv == iSaudis:
		makeUnits(iPlayer, iCamelGunner, tile, 6)
	elif iCiv == iColombia:
		makeUnits(iPlayer, iAlbionLegion, tile, 5).experience(2)
	elif iCiv == iBelgium:
		makeUnit(iPlayer, iGreatArtist, tile)
		makeUnit(iPlayer, iGreatScientist, tile)
		makeUnit(iPlayer, iGreatEngineer, tile)
	elif iCiv == iGermania:
		makeUnits(iPlayer, iGermanicWarrior, tile, 4)
	elif iCiv == iVandals:
		makeUnits(iPlayer, iGermanicWarrior, tile, 4)
	elif iCiv == iGoths:
		makeUnits(iPlayer, iKontosCavalry, tile, 6).experience(2)
	elif iCiv == iNumidia:
		makeUnits(iPlayer, iJavelineer, tile, 4)
	elif iCiv == iMorocco:
 		makeUnits(iPlayer, iCamelLancer, tile, 5)
 		if not bHuman:
 			makeUnits(iPlayer, iCamelLancer, tile, 3)


dSpecificAdditionalUnits = CivDict({
	iEthiopia: {
		iShotelai: 2,
	},
	iKorea: {
		iCrossbowman: 2,
	},
	iNorse: {
		iHuscarl: 3,
	},
	iMoors: {
		iCamelArcher: 2,
	},
}, {})


### Tech Preferences ###

dTechPreferences = {

	iElam : {
		iSailing: 40,
		iSeafaring: 30,
		iMasonry: 40,
		iWriting: 30,
		iLeverage: 20,
		iRiding: 20,
		iDivination: 20,
		iCeremony: 10,

		
		iAlloys: -20,

	},


	iSumeria : {
		iWriting: 40,
		iContract: 30,
		iConstruction: 30,
		iProperty: 20,
		iDivination: 20,
		iMasonry: 20,
	
		iCalendar: -10,
		iArithmetics: -20,
		iMathematics: -50,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
		iLiterature: -40,
	},

	iJudah : {
		iAlloys: 50,
		iConstruction: 50,
		iEthics: 30,
		iTheology: 30,

		iShipbuilding: -30,

	},


	iMinoa : {
		iDivination: 30,
		iCeremony: 30,
		iPhilosophy: 40,
		iShipbuilding: 50,

		iMasonry: -10,
		iAlloys: -10,

	},

	iEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		iNavigation: 20,
		iShipbuilding: 20,
		iArithmetics: 20,
		
		iAlloys: -20,
		iBloomery: -50,
		iRiding: -50,
	},
	iBabylonia : {
		iLaw: 50,
		iWriting: 30,
		iContract: 30,
		iCalendar: 30,
		iMasonry: 20,
		iProperty: 20,
		iDivination: 20,
		iConstruction: 20,
		iArithmetics: 20,
	
		iMathematics: -50,
		iLiterature: -50,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
	},
	iHarappa : {
		iMasonry: 20,
		
		iAlloys: -50,
		iDivination: -50,
		iCeremony: -50,
	},
	iAssyria : {
		iMasonry: 40,
		iLeverage: 40,
		iAlloys: 30,
		iCeremony: 20,
		iWriting: 20,
		iArithmetics: 20,
		
		iRiding: -40,
		iSeafaring: -20,
	},
	iChina : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,	
	},
	iHittites: {
		iBloomery: 50,
		iContract: 20,
		iConstruction: 20,
	},
	iNubia: {
		iPriesthood: 20,
		iEthics: 20,
		iGeneralship: -50,
	},
	iMycenae : {
		iPriesthood: 50,
		iMathematics: 40,
		iNavigation: 40,
		iBloomery: 40,
		iMathematics: 30,
		iPhilosophy: 20,
		iCalendar: 20,
		iWriting: 20,
		iShipbuilding: 20,
		iMedicine: 20,
		iAesthetics: 20,
		
		iLiterature: -20,	# Avoid founding Judaism
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iGreece : {
		iPhilosophy: 50,
		iPriesthood: 40,
		iLiterature: 40,
		iMathematics: 40,
		iNavigation: 40,
		iBloomery: 40,
		iMathematics: 30,
		iCalendar: 20,
		iWriting: 20,
		iShipbuilding: 20,
		iMedicine: 20,
		iAesthetics: 20,
		
		iNobility: -30,
		iEthics: -30,
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iCarthage : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iScythia : {
		iContract: 30,

		iPriesthood: -20,	
		iWriting: -20,
	},
	iPersia : {
		iPriesthood: 200,
		iFission: 15,
	
		iTheology: -40,
	},
	iCelts : {
		iLaw: 30,
		iEthics: 20,
		iBloomery: 20,
	},
	iRome : {
		iEthics: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
		iMachinery: -50,
		iTheology: -60,
		iAlchemy: -60,
	},
	iGermania : {
		iFeudalism: 30,
		iWriting: 20,
		iCivilService: 10,
		
		iMasonry: -40,
	},
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iDravidia : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iToltecs : {
		iMathematics: 30,
		iWriting: 20,
		iCalendar: 20,
		iContract: 20,
	},
	iVandals : {
		iLaw: 60,
		iCement: 50,
		iCurrency: 30,
		iGuilds: 20,
		iFeudalism: 20,
	},
	iParthia : {
		iNobility: 30,
		iFission: 15,
		
		iEthics: -15,
		iTheology: -40,
	},
	iKushans : {
		iAesthetics: 20,
		iEngineering: 20,
		iArchitecture: 20,
		iMedicine: 20,
	},
	iKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iGoths : {
		iLaw: 50,
		iFeudalism: 50,
		iCivilService: 40,
		
		iPhilosophy: -20,
		iMedicine: -20,
	},
	iGhana : {
		iCurrency: 50,
		iTheology: 40,
		iScholarship: 40,
		iDoctrine: 30,
		iFeudalism: 20,
	},
	iByzantium : {
		iAlchemy: -60,
		iTheology: -60,
		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iHuns : {
		iFeudalism: 90,
		iCivilService: 30,
		
		iPhilosophy: -40,
		iEthics: -20,
		iCurrency: -20,
		iMedicine: -10,
	},
	iMali : {
		iScholarship: 40,
		iDoctrine: 30,
		iPolitics: 30,
		iFeudalism: 20,
		iTheology: 20,
	},
	iFrance : {
		iFirearms: 20,
		iExploration: 20,
		iGeography: 20,
		iLogistics: 20,
		iPatronage: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iFeudalism: 15,
		iChemistry: 15,
		iSociology: 15,
		iFission: 12,
	},
	iMalays : {
		iEcology: 40,
		iCompass: 30,
		iPolitics: 20,
		iArtisanry: 20,
	},
	iJapan : {
		iFeudalism: 40,
		iFortification: 40,
		iRobotics: 40,
	
		iOptics: -40,
		iExploration: -40,
		iFirearms: -30,
		iMachinery: -20,
		iGuilds: -20,
		iGeography: -20,
		iReplaceableParts: -20,
		iScientificMethod: -20,
	},
	iNorse : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
	},
	iTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iKhazars : {
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
		iCompass: -30,
	},
	iKanemBornu : {
		iCurrency: 40,
		iFirearms: 20,
		iGunpowder: 10,
		iCompass: -10,
		iExploration: -30,
	},
	iJava : {
		iPolitics: 30,
		iGunpowder: 30,
		iCompass: 20,
		iCivilService: 20,
	
		iExploration: -20,
	},
	iMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
	},
	iSpain : {
		iMachinery: 25,
		iCartography: 50,
		iExploration: 50,
		iGunpowder: 50,
		iCompass: 30,
		iFirearms: 25,
		iPatronage: 25,
		iReplaceableParts: 30,
		iGuilds: 15,
		iChemistry: 15,
	},
	iGeorgia : {
		iPaper: 30,
		iCivilService: 20,
		iFirearms: -20,
		iExploration: -20,
	},
	iEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iAcademia: 20,
		iCivilLiberties: 20,
		iEducation: 15,
		iGuilds: 15,
		iChemistry: 15,
	},
	iYemen : {
		iCropRotation: 15,
		iDoctrine: 15,
		
		iFinance: -30,
		iFirearms: -30,
		iCompanies: -30,
		iPaper: -30,
	},
	iHolyRome : {
		iPrinting: 50,
		iAcademia: 30,
		iFirearms: 20,
		iReplaceableParts: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
	},
	iBurma : {
		iLogistics: 20,
		iCombinedArms: 20,
	},
	iHausa : {
		iCurrency: 50,
		iDoctrine: 20,
		iGuilds: 20,

		iFirearms: -30,
		iGunpowder: -50,
	},
	iRus : {
		iCompass: 30,
		iCommune: 20,
	},
	iBenin : {
		iFortification: 50,
		iDoctrine: 20,
		iGuilds: 20,

		iFirearms: -30,
		iGunpowder: -40,
	},
	iMisr : {
		iGunpowder: 40,
		iFortification: 30,
		
		iFinance: -50,
		iFirearms: -40,
		iCompanies: -50,
		iPaper: -20,
	},
	iVietnam : {
		iPrinting: 20,
		iHeritage: 20,
		iStatecraft: 20,
		iCollectivism: 20,
	},
	iSomalia : {
		iLateenSails: 50,
		iCompass: 30,
		iCivilService: 20,
		iExploration: 20,
		iTheology: 20,

		iFirearms: -20,
		iGunpowder: -20,
	},
	iSwahili : {
		iCompass: 30,
		iFortification: 20,
		iExploration: 20,
		
		iCartography: -40,
	},
	iBuganda : {
		iGeneralship: 50,
		iCivilService: 30,
		iNobility: 20,

		iWriting: -30,
	},
	iMorocco : {
 		iExploration: -30,
 		iCartography: -30,
 		iAlchemy: 10,
 		iReplaceableParts: -10,
 	},
	iPoland : {
		iCombinedArms: 30,
		iCivilLiberties: 30,
		iSocialContract: 20,
		iOptics: 20,
	},
	iPortugal : {
		iCartography: 50,
 		iExploration: 50,
 		iGeography: 50,
		iFirearms: 30,
 		iCompass: 25,
 		iGunpowder: 25,
		iCompanies: 20,
		iPatronage: 20,
		iReplaceableParts: 20,
	},
	iJerusalem : {
		iPaper: 30,
		iGunpowder: 10,
	},

	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,

	},
	iOman : {
		iExploration: 40,
		iCartography: 20,
		iGunpowder: 30,
		iGeography: 20,
		
		iFirearms: -10,
		iPaper: -30,
	},
	iItaly : {
		iRadio: 20,
		iPsychology: 20,
		iFinance: 25,
		iOptics: 25,
		iPatronage: 30,
		iHumanities: 30,
		iHumanities: 30,
		iAcademia: 25,
		iFission: 12,
		iCartography: -20,
	},
	iZimbabwe : {
		iFortification: 50,
		iAesthetics: 30,
		iCivilService: 20,

		iPolitics: -20,
		iHumanities: -20,
	},
	iTunis : {
		iCivilService: 20,
	
		iPaper: -20,
		iExploration: -40,
		iGuilds: -40,
	},
	iGhorids : {
		iHumanities: 30,
		iPhilosophy: 20,
		iEducation: 20,
		iPaper: 20,
		iPatronage: 20,
		iEngineering: 15,
	
		iReplaceableParts: -30,
		iScientificMethod: -30,
		iCombinedArms: -30,
		iExploration: -30,
	},
	iTimurids : {
		iHumanities: 30,
		iPhilosophy: 20,
		iEducation: 20,
		iPaper: 20,
		iHorticulture: 20,
		iUrbanPlanning: 20,
		iPatronage: 20,
		iEngineering: 15,
	
		iReplaceableParts: -30,
		iScientificMethod: -30,
		iCombinedArms: -30,
		iExploration: -30,
		iCivilLiberties: -30,
	},
	iMongols : {
		iGunpowder: 100,
		iLogistics: 40,
		iStatecraft: 20,
		iPrinting: 20,
		
		iExploration: -100,
		iOptics: -100,
		iFirearms: -40,
		iCombinedArms: -40,
	},
	iAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iSweden : {
		iCombinedArms: 40,
		iFirearms: 30,
		iLogistics: 30,
		iRefining: 30,
		iCivilLiberties: 20,
		iBiology: 20,
	},
	iRussia : {
		iMacroeconomics: 30,
		iCollectivism: 30,
		iCombinedArms: 30,
		iReplaceableParts: 30,
		iHeritage: 15,
		iPatronage: 15,
		iUrbanPlanning: 15,
		iFission: 12,
		
		iPhilosophy: -20,
		iPrinting: -20,
		iCivilLiberties: -20,
		iSocialContract: -20,
		iRepresentation: -20,
	},
	iAdal : {
		iGunpowder: 30,
		iCivilService: 20,

		iExploration: -30,
	},
	iOttomans : {
		iGunpowder: 30,
		iFirearms: 30,
		iCombinedArms: 30,
		iJudiciary: 20,
	},
	iThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iSonghai : {
		iDoctrine: 50,
		iCartography: -10,
		iExploration: -20,
		iGunpowder: -30,
		iFirearms: -30,
	},
	iPersia : {
		iFission: 15,
		iRepresentation: -40,
	},
	iFunj : {
		iPaper: 30,

		iReplaceableParts: -20,
		iGunpowder: -50,
		iFirearms: -50,
	},
	iMadagascar : {
		iGuilds: 20,
		iExploration: 20,
		iFinance: 20,
	},
	iNetherlands : {
		iAcademia: 30,
		iExploration: 20,
		iFirearms: 20,
		iOptics: 20,
		iGeography: 20,
		iReplaceableParts: 20,
		iLogistics: 20,
		iEconomics: 20,
		iCivilLiberties: 20,
		iHumanities: 20,
		iChemistry: 15,
	},
	iKatanga : {
		iWriting: -30,
		iLiterature: -30,
	},
	iAshanti : {
		iFirearms: 60,
		iGunpowder: 40,
		iReplaceableParts: 20,

		iCartography: -30,
		iExploration: -40,
	},
	iGermany : {
		iEngine: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iSaudis: {
		iEngine: 40,
		iRefining: 40,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iBoers : {
		iFlight: 35,
		iAssemblyLine: 20,
		iPowerProjection: 20,
		iFission: 10,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBelgium: {
		iRailroad: 50,
		iFission: 30,
		iGlobalism: 30,
	},
	iZulu : {
		iFirearms: 50,
		iGeneralship: 50,
		iGunpowder: 50,
		
		iWriting: -20,
		iRiding: -50,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
	iAustralia : {
		iTelevision: 40,
		iGenetics: 40,
		iEcology: 20,
	},
	iSouthAfrica : {
		iPowerProjection: 30,
		iFission: 30,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iSonghai: 40, # Aeons - Makes these guys wonder hungry so that they get the Sub-Saharan wonders done.
	iMali: 30,
	iGhana: 15,
	iEgypt: -15,
	iBabylonia: -15,
	iHittites: -50,
	iNubia: -50,
	iIndia: -15,
	iRome: -20,
	iArabia: -15,
	iJava: -15,
	iFrance: -12,
	iKhmer: -15,
	iEngland: -12,
	iYemen: -15,
	iRussia: -12,
	iThailand: -15,
	iCongo: -20,
	iNetherlands: -12,
	iAmerica: -12,
	iNumidia: -15,
	iScythia: -30,
	iArmenia: -15,
	iMorocco: -10,
	iMinoa: -30,
}

dBuildingPreferences = {
	iHarappa : {
		iGreatBath: 100,
		iPyramids: -30,
		iGreatSphinx: -20,
	},

	iEgypt : {
		iPyramids: 100,
		iAbuSimbel: 50,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,
		iTempleOfAmun: 20,
		iNuri: 20,
	},
	iBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: -10,
		iGreatSphinx: -10,
		
		iAbuSimbel: -30,
		iTempleOfAmun: -30,
		iNuri: -30,
		iOracle: -60,
	},
	iSumeria : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: -30,
		iGreatSphinx: -30,
		
		iAbuSimbel: -30,
		iTempleOfAmun: -30,
		iNuri: -30,
		iOracle: -60,
	},
	iMinoa: {
		iKnossosPalace: 50,
		iOracle: 10,
		iPyramids: -50,
		iAbuSimbel: -50,
		iGreatCothon: -50,
		iColossus: -50,
		iTempleOfAmun: -50,
	},
	iAssyria : {
		iHangingGardens: 30,
		iIshtarGate: 30,
	},
	iChina : {
		iGreatWall: 80,
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iTiananmenSquare: 40,
		iDujiangyan: 30,
		iTerracottaArmy: 30,
		iPorcelainTower: 30,
		
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
		iTempleOfAmun: -30,
	},
	iMycenae : {
		iOracle: 100,
		iColossus: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		iGreatLibrary: 15,
		iGreatLighthouse: 15,
		
		iIshtarGate: -20,
		iTempleOfAmun: -30,
		iPyramids: -100,
		iGreatCothon: -100,
	},
	iNubia : {
		iNuri: 50,
		iTempleOfAmun: 50,
		iAbuSimbel: 30,
 		iPyramids: 20,
 		iGreatSphinx: 20,
		iOuadaneKsar: -20,
 		iGreatAdobeMosque: -20,
		iUniversityOfSankore: -30,
		iTombOfAskia: -30,
 		iHangingGardens: -30,
		iAquaAppia: -40,
		iFlavianAmphitheatre: -40,
		iParthenon: -30,
 	},
	iGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iGreatLibrary: 15,
		iGreatLighthouse: 15,
		iStatueOfZeus: 5,

		iAlKhazneh: -15,
		iTempleOfAmun: -30,
		iPyramids: -100,
		iGreatCothon: -100,
	},
	iIndia : {
		iKhajuraho: 30,
		iIronPillar: 30,
		iVijayaStambha: 30,
		iNalanda: 30,
		iLotusTemple: 30,
		iTajMahal: 20,
		iWatPreahPisnulok: 20,
		iShwedagonPaya: 20,
		iHarmandirSahib: 20,
		iJetavanaramaya: 20,
		iSalsalBuddha: 20,
		iPotalaPalace: 20,
		iBorobudur: 15,
		iPrambanan: 15,
		
		iTempleOfAmun: -30,
		iParthenon: -30,
		iStatueOfZeus: -20,
	},
	iCarthage : {
		iGreatCothon: 30,
		iColossus: 15,
		
		iTempleOfAmun: -20,
		iGreatLighthouse: -30, # Aeons - Stop stealing Macedon UHV!
		iPyramids: -50,
	},
	iPolynesia : {
		iMoaiStatues: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iSparta : {
		iStatueOfZeus: 30,
		iColossus: 30,
		iOracle: 20,
		iParthenon: 10,
		iTempleOfArtemis: 10,
		iGreatMausoleum: 10,
		iMountAthos: 5,
		iHagiaSophia: 5,
		iGreatLibrary: 5,
		iGreatLighthouse: 5,

		iAlKhazneh: -20,
		iPyramids: -100,
		iGreatCothon: -100,
	},

	iRome : {
		iTrajansColumn: 50,
		iCircusMaximus: 50,
		iFlavianAmphitheatre: 50,
		iAquaAppia: 50,
		iPantheon: 50,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iMaya : {
		iTempleOfKukulkan: 40,
	},
	iMacedon : {
		iStatueOfZeus: 10,
		iColossus: 10,
		iOracle: 10,
		iParthenon: 20,
		iTempleOfArtemis: 20,
		iGreatMausoleum: 40,
		iMountAthos: 15,
		iHagiaSophia: 15,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,	
		iAlKhazneh: 30,

		iTrajansColumn: -30,
		iCircusMaximus: -30,
		iGreatCothon: -100,
	},
	iNumidia : {
		iGreatCothon: 20,
	},
	iArmenia : {
		iNarekavank: 80,
		iMonolithicChurch: 20,
		iHagiaSophia: -25,
	},

	iDravidia : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iEthiopia : {
		iMonolithicChurch: 40,

		iTheodosianWalls: -30,
		iHagiaSophia: -20,
		iSaintBasilsCathedral: -20,
		iSaintSophia: -20,
		iKremlin: -20,
	},
	iToltecs : {
		iPyramidOfTheSun: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 15,
		iGondeshapur: 50,
		iAlamut: 35,
		iHangingGardens: 15,
		iOracle: 15,
		iCircusMaximus: -20,
	},
	iKushans : {
		iSalsalBuddha: 30,
		iNalanda: 20,
		iKhajuraho: 20,
	},
	iKorea : {
		iCheomseongdae: 30,
		iShwedagonPaya: 0,
		iPrambanan: 0,
		iBorobudur: 0,
	},
	iKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iGhana : {
		iOuadaneKsar: 100,
		iUniversityOfSankore: 40,
		iGreatAdobeMosque: 40,
		iTombOfAskia: 30,
		iAitBenhaddou: -20,
	},
	iMali : {
		iOuadaneKsar: 50,
		iUniversityOfSankore: 75,
		iGreatAdobeMosque: 50,
		iTombOfAskia: 40,
		iAitBenhaddou: -20,
	},
	iSonghai : {
		iOuadaneKsar: 80,
		iUniversityOfSankore: 80,
		iGreatAdobeMosque: 80,
		iTombOfAskia: 80,
		iAitBenhaddou: -20,
	},
	iKanemBornu : {
		iOuadaneKsar: 80,
		iUniversityOfSankore: 20,
		iGreatAdobeMosque: 20,
		iAitBenhaddou: -20,
	},

	iByzantium : {
		iCircusMaximus: 50,
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		iTrajansColumn: 10,
		
		iNotreDame: -20,
		iSistineChapel: -20,
		iSaintSophia: -50,
		iNarekavank: -60,
	},
	iFrance : {
		iTradingCompanyBuilding: 40,
		iNotreDame: 40,
		iEiffelTower: 30,
		iVersailles: 30,
		iLouvre: 30,
		iTriumphalArch: 30,
		iMetropolitain: 30,
		iCERN: 30,
		iKrakDesChevaliers: 30,
		iChannelTunnel: 30,
		iPalaceOfNations: 20,
		iBerlaymont: 20,
		iLargeHadronCollider: 20,
		iITER: 20,
		iOldSynagogue: -20,
	},
	iMalays : {
		iGardensByTheBay: 40,
		iPrambanan: 20,
		iBorobudur: 20,
	},
	iJapan : {
		iItsukushimaShrine: 50,
		iHimejiCastle: 50,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iBorobudur: 0,
		iPrambanan: 0,
		iShwedagonPaya: 0,
		iGreatWall: -100,
	},
	iGokturks : {
		iItchanKhala: 50,
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
		
		iShwedagonPaya: -30,
	},
	iTurks : {
		iItchanKhala: 70,
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
		
		iShwedagonPaya: -30,
	},
	iNorse : {
		iNobelPrize: 20,
		iGlobalSeedVault: 30,
		iCERN: 15,
	},
	iArabia: {
		iProphetsMosque: 100,
		iSpiralMinaret: 100,
		iDomeOfTheRock: 100,
		iHouseOfWisdom: 100,
		iBurjKhalifa: 50,
		iAlamut: 20,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
		iAitBenhaddou: -30,
		iOuadaneKsar: -50,
	},
	iTibet : {
		iPotalaPalace: 40,
	},
	iMoors : {
		iMezquita: 100,
		iAlhambra: 50,
		iAitBenhaddou: 40,
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
		iProphetsMosque: -20,
		iGreatAdobeMosque: -30,
	},
	iJava : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 30,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iSpain : {
		iEscorial: 30,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iSagradaFamilia: 30,
		iCristoRedentor: 20,
		iWembley: 20,
		iIberianTradingCompanyBuilding: 20,
		iTorreDeBelem: 15,
		iNotreDame: 15,
		iMezquita: 15,

		iNotreDame: -20,
 		iOldSynagogue: -30,
	},
	iGeorgia : {
		iMonolithicChurch: 30,
		iNarekavank: 20,
		iHagiaSophia: 20,
		iAlamut: 10,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iOxfordUniversity: 30,
		iWembley: 30,
		iWestminsterPalace: 30,
		iTrafalgarSquare: 30,
		iBellRockLighthouse: 30,
		iCrystalPalace: 30,
		iChannelTunnel: 30,
		iBletchleyPark: 20,
		iAbbeyMills: 20,
		iMetropolitain: 20,
		iNationalGallery: 20,
		iKrakDesChevaliers: 20,
		iHarbourOpera: 20,
	},
	iYemen : {
		iAlhambra: -50,
		iOuadaneKsar: -40,
		iMezquita: -40,
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
		iGreatAdobeMosque: -30,
		iAitBenhaddou: -40,
	},
	iHolyRome : {
		iSaintThomasChurch: 30,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iBurma : {
		iShwedagonPaya: 50,
		iWatPreahPisnulok: 20,
		iEmeraldBuddha: 20,
	},
	iRus : {
		iSaintSophia: 40,
		iSaintBasilsCathedral: 20,
		iKremlin: 20,
		iNarekavank: -50,
	},
	iSamanids: {
		iItchanKhala: 60,
		iHouseOfWisdom: -30,
		iMezquita: -30,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
	},
	iMisr: {
		iAlAzhar: 50,
		iKrakDesChevaliers: 50,
		iDomeOfTheRock: 40,

		iAlamut: -20,
		iHouseOfWisdom: -20,
		iSpiralMinaret: -20,
		iTopkapiPalace: -80,
		iMezquita: -50,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
		iRoseGardenPalace: -30,
		iTombOfAskia: -60,
		iOuadaneKsar: -60,
	},
	iBuyids: {
		iAlamut: 60,
		iHouseOfWisdom: 40,
		iItchanKhala: 20,
			
		iAlAzhar: -10,
		iMezquita: -20,
		iOuadaneKsar: -30,
	},
	iHausa : {
		iOsunOsogbo: 50,
		iIyanuwo: 10,
		iKasubiTombs: -20,
		iRoyalRova: -30,
	},
	iBenin : {
		iIyanuwo: 50,
		iOsunOsogbo: 30,
		iKasubiTombs: -20,
		iRoyalRova: -30,
	},
	iBuganda : {
		iKasubiTombs: 80,
		iIyanuwo: -20,
		iOsunOsogbo: -20,
	},
	iPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
	},
	iMoors : {
		iAitBenhaddou: 40,
		iMezquita: 20,
		iAlhambra: 20,
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
		iProphetsMosque: -20,
		iGreatAdobeMosque: -30,
	},
	iPortugal : {
		# Could only occur if Portugal ends up Islamic though? - It's fine though as Oman finished it
		iStonetownFort: 60,
		
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iKulumbimbi: 30,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
		iSantaMariaDelFiore: -30,
	},
	iJerusalem : {
		iDomeOfTheRock: 100,
		iKrakDesChevaliers: 50,

		iEscorial: -40,
	},

	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iOman : {
		iStonetownFort: 50,

		iAlhambra: -30,
		iMezquita: -30,
		iUniversityOfSankore: -20,
		iSpiralMinaret: -20,
		iTopkapiPalace: -20,
		iBlueMosque: -20,
		iAitBenhaddou: -20,
		iGreatAdobeMosque: -10,
		iOuadaneKsar: -30,
	},

	iItaly : {
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
	},
	iMongols : {
		iSilverTreeFountain: 40,
		iItchanKhala: 30,
	},
	iRussia : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
		iTiananmenSquare: 20,
		iNarekavank: -30,
	},
	iOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iTunis : {
		iMezquita: 30,
		iAlhambra: 20,
		iAitBenhaddou: 20,
		iUniversityOfSankore: -40,
		iSpiralMinaret: -20,
		iTopkapiPalace: -30,
		iBlueMosque: -30,
		iProphetsMosque: -30,
		iUniversityOfSankore: -30,
		iGreatAdobeMosque: -30,
	},
	iTimurids : {
		iItchanKhala: 80,
		iGurEAmir: 40,
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,

		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
		iUniversityOfSankore: -50,
	},
	iGhorids: {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
		iOuadaneKsar: -50,
		iUniversityOfSankore: -60,
	},
	iThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iSweden : {
		iNobelPrize: 30,
		iGlobalSeedVault: 20,
	},
	iCongo: {
		iKulumbimbi: 100,
	},
	iIran: {
		iRoseGardenPalace: 40,
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iMadagascar : {
		iRoyalRova: 50,
		iIyanuwo: -20,
		iOsunOsogbo: -20,
		iKasubiTombs: -60,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
		iBourse: 40,
		iDeltaWorks: 40,
		iAtomium: 30,
		iBerlaymont: 30,
		iNationalGallery: 20,
		iWembley: 20,
		iCERN: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iManchuria : {
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iTiananmenSquare: 40,
		iPorcelainTower: 30,
		
		iBrandenburgGate: -30,
	},
	iGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iSaudis: {
		iBurjKhalifa: 30,
	},
	iAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
		iMetropolitain: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 50,
		iChapultepecCastle: 50,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iFloralisGenerica: 40,
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iBelgium: {
		iAtomium: 50,
		iBerlaymont: 50,
	},
	iAustralia : {
		iHarbourOpera: 50,
	},
	iCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	}
}