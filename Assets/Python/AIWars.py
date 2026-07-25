from Core import *
from RFCUtils import *

from Events import handler
from Resurrection import getResurrectionTechs


### Constants ###

iMinIntervalEarly = 10
iMaxIntervalEarly = 20
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30

iRomeCarthageYear = -260
tRomeCarthageTL = (65, 45)
tRomeCarthageBR = (70, 49)

iRomeCarthageAgainYear = -180

iRomeGreeceYear = -150
tRomeGreeceTL = (73, 49)
tRomeGreeceBR = (78, 56)

iRomeMesopotamiaYear = -100
tRomeMesopotamiaTL = (82, 44)
tRomeMesopotamiaBR = (85, 50)

iRomeAnatoliaYear = -100
tRomeAnatoliaTL = (79, 51)
tRomeAnatoliaBR = (88, 55)

iRomeCreteYear = -80
tRomeCreteTL = (77, 48)
tRomeCreteBR = (78, 48)

iRomeCeltiaYear = -50
tRomeCeltiaTL = (56, 55)
tRomeCeltiaBR = (62, 59)

iRomeEgyptYear = 0
tRomeEgyptTL = (76, 40)
tRomeEgyptBR = (82, 45)

iRomeItalyYear = 0
tRomeItalyTL = (65, 53)
tRomeItalyBR = (70, 57)

# following setup: iPlayer, iPreferredTarget, TL, BR, iNumTargets, iStartYear, iTurnInterval
tConquestRomeCarthage = (0, iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 3, iRomeCarthageYear, 10)
tConquestRomeGreece = (1, iRome, iGreece, tRomeGreeceTL, tRomeGreeceBR, 2, iRomeGreeceYear, 10)
tConquestRomeAnatolia = (2, iRome, iGreece, tRomeAnatoliaTL, tRomeAnatoliaBR, 3, iRomeAnatoliaYear, 10)
tConquestRomeCrete = (14, iRome, iMinoa, tRomeCreteTL, tRomeCreteBR, 2, iRomeCreteYear, 10)
tConquestRomeCelts = (3, iRome, iCelts, tRomeCeltiaTL, tRomeCeltiaBR, 2, iRomeCeltiaYear, 10)
tConquestRomeEgypt = (4, iRome, iEgypt, tRomeEgyptTL, tRomeEgyptBR, 3, iRomeEgyptYear, 10)
tConquestRomeMesopotamia = (21, iRome, iJudah, tRomeMesopotamiaTL, tRomeMesopotamiaBR, 4, iRomeMesopotamiaYear, 20)
tConquestRomeCarthageAgain = (39, iRome, iCarthage, tRomeCarthageTL, tRomeCarthageBR, 3, iRomeCarthageAgainYear, 10)
tConquestRomeItaly = (40, iRome, iCelts, tRomeItalyTL, tRomeItalyBR, 3, iRomeItalyYear, 10)

iAlexanderYear = -340
tGreeceMesopotamiaTL = (81, 45)
tGreeceMesopotamiaBR = (90, 55)
tGreeceEgyptTL = (76, 40)
tGreeceEgyptBR = (82, 45)
tGreecePersiaTL = (91, 43)
tGreecePersiaBR = (97, 52)

tConquestGreeceMesopotamia = (6, iMacedon, iBabylonia, tGreeceMesopotamiaTL, tGreeceMesopotamiaBR, 6, iAlexanderYear, 20)
tConquestGreeceEgypt = (38, iMacedon, iEgypt, tGreeceEgyptTL, tGreeceEgyptBR, 4, iAlexanderYear, 20)
tConquestGreecePersia = (7, iMacedon, iPersia, tGreecePersiaTL, tGreecePersiaBR, 4, iAlexanderYear, 20)

iCholaSumatraYear = 1030
tCholaSumatraTL = (115, 26)
tCholaSumatraBR = (121, 31)

tConquestCholaSumatra = (8, iDravidia, iMalays, tCholaSumatraTL, tCholaSumatraBR, 1, iCholaSumatraYear, 10)

iSpainMoorsYear = 1180
tSpainMoorsTL = (55, 48)
tSpainMoorsBR = (60, 53)

tConquestSpainMoors = (9, iSpain, iMorocco, tSpainMoorsTL, tSpainMoorsBR, 3, iSpainMoorsYear, 5)

iTurksPersiaYear = 1050
tTurksPersiaTL = (91, 43)
tTurksPersiaBR = (98, 52)

iTurksAnatoliaYear = 1070
tTurksAnatoliaTL = (80, 51)
tTurksAnatoliaBR = (87, 55)

tConquestTurksPersia = (10, iTurks, iArabia, tTurksPersiaTL, tTurksPersiaBR, 4, iTurksPersiaYear, 5)
tConquestTurksAnatolia = (11, iTurks, iByzantium, tTurksAnatoliaTL, tTurksAnatoliaBR, 5, iTurksAnatoliaYear, 10)

iEnglandIrelandYear = 1200
tEnglandIrelandTL = (52, 64)
tEnglandIrelandBR = (54, 67)

tConquestEnglandIreland = (12, iEngland, iCelts, tEnglandIrelandTL, tEnglandIrelandBR, 2, iEnglandIrelandYear, 10)

iMongolsPersiaYear = 1220
tMongolsPersiaTL = (91, 43)
tMongolsPersiaBR = (98, 52)

tConquestMongolsPersia = (13, iMongols, iTurks, tMongolsPersiaTL, tMongolsPersiaBR, 7, iMongolsPersiaYear, 10)

iAssyriaMesopotamiaYear = -730
tAssyriaMesopotamiaTL = (82, 44)
tAssyriaMesopotamiaBR = (90, 50)

tConquestAssyriaMesopotamia = (15, iAssyria, iBabylonia, tAssyriaMesopotamiaTL, tAssyriaMesopotamiaBR, 4, iAssyriaMesopotamiaYear, 10)

iBabyloniaMesopotamiaYear = -630
tBabyloniaMesopotamiaTL = (82, 44)
tBabyloniaMesopotamiaBR = (90, 50)

tConquestBabyloniaMesopotamia = (16, iBabylonia, iAssyria, tBabyloniaMesopotamiaTL, tBabyloniaMesopotamiaBR, 4, iBabyloniaMesopotamiaYear, 10)

iPersiaMesopotamiaYear = -570
tPersiaMesopotamiaTL = (82, 44)
tPersiaMesopotamiaBR = (90, 50)

tConquestPersiaMesopotamia = (17, iPersia, iBabylonia, tPersiaMesopotamiaTL, tPersiaMesopotamiaBR, 6, iPersiaMesopotamiaYear, 10)

iPersiaEgyptYear = -530
tPersiaEgyptTL = (76, 40)
tPersiaEgyptBR = (82, 45)

tConquestPersiaEgypt = (18, iPersia, iEgypt, tPersiaEgyptTL, tPersiaEgyptBR, 2, iPersiaEgyptYear, 10)

iPersiaAnatoliaYear = -600
tPersiaAnatoliaTL = (79, 51)
tPersiaAnatoliaBR = (88, 55)

tConquestPersiaAnatolia = (19, iPersia, iHittites, tPersiaAnatoliaTL, tPersiaAnatoliaBR, 2, iPersiaAnatoliaYear, 10)

iPersiaGreeceYear = -450
tPersiaGreeceTL = (74, 53)
tPersiaGreeceBR = (78, 56)

tConquestPersiaGreece = (20, iPersia, iGreece, tPersiaGreeceTL, tPersiaGreeceBR, 1, iPersiaGreeceYear, 10)

iNubiaEgyptYear = -530
tNubiaEgyptTL = (76, 40)
tNubiaEgyptBR = (82, 45)

tConquestNubiaEgypt = (37, iNubia, iEgypt, tNubiaEgyptTL, tNubiaEgyptBR, 1, iNubiaEgyptYear, 10)


iVandalsRomeYear = 400
tVandalsRomeTL = (55, 45)
tVandalsRomeBR = (70, 48)

tConquestVandalsRome = (22, iVandals, iRome, tVandalsRomeTL, tVandalsRomeBR, 4, iVandalsRomeYear, 3)

iGermaniaEnglandYear = 400
tGermaniaEnglandTL = (51, 62)
tGermaniaEnglandBR = (59, 66)

tConquestGermaniaEngland = (41, iGermania, iRome, tGermaniaEnglandTL, tGermaniaEnglandBR, 4, iGermaniaEnglandYear, 2)

iGothSpainYear = 390
tGothSpainTL = (55, 49)
tGothSpainBR = (62, 55)

iGothSpainYear = 390
tGothSpainTL = (55, 49)
tGothSpainBR = (62, 55)

tConquestGothSpain = (23, iGoths, iRome, tGothSpainTL, tGothSpainBR, 4, iGothSpainYear, 3)

iGothItalyYear = 450
tGothItalyTL = (65, 49)
tGothItalyBR = (70, 57)

tConquestGothItaly = (24, iGoths, iItaly, tGothItalyTL, tGothItalyBR, 4, iGothItalyYear, 3)

iHunsGothsYear = 420
tHunsGothsTL = (69, 57)
tHunsGothsBR = (77, 66)

tConquestHunsGoths = (25, iHuns, iGoths, tHunsGothsTL, tHunsGothsBR, 6, iHunsGothsYear, 10)

iHunsItalyYear = 420
tHunsItalyTL = (65, 53)
tHunsItalyBR = (70, 57)

tConquestHunsItaly = (26, iHuns, iItaly, tHunsItalyTL, tHunsItalyBR, 2, iHunsItalyYear, 10)

iHunsGaulYear = 420
tHunsGaulTL = (59, 55)
tHunsGaulBR = (64, 59)

tConquestHunsGaul = (27, iHuns, iItaly, tHunsGaulTL, tHunsGaulBR, 2, iHunsGaulYear, 10)

iCharlemagneYear = 750
tCharlemagneTL = (63, 52)
tCharlemagneBR = (69, 65)

tConquestCharlemagne = (28, iFrance, iGermania, tCharlemagneTL, tCharlemagneBR, 6, iCharlemagneYear, 10)

iUmmayadYear = 640
tUmmayadIberiaTL = (54, 48)
tUmmayadIberiaBR = (62, 55)

tConquestUmmayadIberia = (29, iArabia, iGoths, tUmmayadIberiaTL, tUmmayadIberiaBR, 2, iUmmayadYear, 10)

tUmmayadAfricaTL = (55, 45)
tUmmayadAfricaBR = (70, 48)

tConquestUmmayadAfrica = (30, iArabia, iVandals, tUmmayadAfricaTL, tUmmayadAfricaBR, 1, iUmmayadYear, 10)

iRomeNumidiaYear = -100
tRomeNumidiaTL = (60, 45)
tRomeNumidiaBR = (70, 49)

tConquestRomeNumidia = (31, iRome, iNumidia, tRomeNumidiaTL, tRomeNumidiaBR, 3, iRomeNumidiaYear, 10)

iOttomanTunisYear = 1570
tOttomanTunisTL = (63, 45)
tOttomanTunisBR = (69, 48)

tConquestOttomanTunis = (32, iOttomans, iTunis, tOttomanTunisTL, tOttomanTunisBR, 3, iOttomanTunisYear, 10)

iTimuridsPunjabYear = 1400
tTimuridsPunjabTL = (99, 46)
tTimuridsPunjabBR = (104, 51)

tConquestTimuridsPunjab = (33, iTimurids, iGhorids, tTimuridsPunjabTL, tTimuridsPunjabBR, 3, iTimuridsPunjabYear, 5)

iDelhiIndiaYear = 1210
tDelhiIndiaTL = (99, 40)
tDelhiIndiaBR = (110, 49)

tConquestDelhiIndia = (34, iGhorids, iIndia, tDelhiIndiaTL, tDelhiIndiaBR, 6, iDelhiIndiaYear, 5)

# Aeons - Slightly earlier because we want Timurids to move to India before collapsing
iMughalIndiaYear = 1490

tConquestMughalIndia = (35, iTimurids, iGhorids, tDelhiIndiaTL, tDelhiIndiaBR, 6, iMughalIndiaYear, 5)

# Originally Aeons - Was added to main version and adjusted accordingly
iOttomanEgyptYear = 1517
tOttomanEgyptTL = (76, 39)
tOttomanEgyptBR = (81, 45)

tConquestOttomanEgypt = (14, iOttomans, iMisr, tOttomanEgyptTL, tOttomanEgyptBR, 3, iOttomanEgyptYear, 5)

iEnglandCapeYear = 1765
tEnglandCapeTL = (72, 11)
tEnglandCapeBR = (76, 12)

tConquestEnglandCape = (42, iEngland, iNetherlands, tEnglandCapeTL, tEnglandCapeBR, 2, iEnglandCapeYear, 5)

lConquests = [
	tConquestRomeCarthage, 
	tConquestRomeGreece, 
	tConquestRomeAnatolia, 
	tConquestRomeCelts, 
	tConquestRomeEgypt, 
	tConquestGreeceMesopotamia, 
	tConquestGreecePersia, 
	tConquestSpainMoors, 
	tConquestTurksPersia, 
	tConquestTurksAnatolia, 
	tConquestEnglandIreland,
	tConquestMongolsPersia,
	tConquestRomeCrete,
	tConquestAssyriaMesopotamia,
	tConquestBabyloniaMesopotamia,
	tConquestPersiaMesopotamia,
	tConquestPersiaEgypt,
	tConquestPersiaAnatolia,
	tConquestPersiaGreece,
	tConquestRomeMesopotamia,
	tConquestVandalsRome,
	tConquestGothSpain,
	tConquestGothItaly,
	tConquestHunsGoths,
	tConquestHunsItaly,
	tConquestHunsGaul,
	tConquestCharlemagne,
	tConquestUmmayadIberia,
	tConquestUmmayadAfrica,
	tConquestOttomanTunis,
	tConquestTimuridsPunjab,
	tConquestDelhiIndia,
	tConquestMughalIndia,
	tConquestOttomanEgypt,
	tConquestNubiaEgypt,
	tConquestGreeceEgypt, 
	tConquestRomeCarthageAgain,
	tConquestRomeItaly,
	tConquestGermaniaEngland,
	tConquestEnglandCape,
]


@handler("GameStart")
def setup():
	iTurn = year(-2000) # Aeons - Start aggression earlier - was 1200BC
	if scenario() == i600AD:  #late start condition
		iTurn = year(700)
	elif scenario() == i1500AD: # Aeons - Move from 1540 to 1520 so Ottomans can attack sooner for example
		iTurn = year(1520)
	elif scenario() == i1700AD:
		iTurn = year(1720)
	elif scenario() == i1100AD:
		iTurn = year(1120)
	data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly-iMinIntervalEarly)


@handler("BeginGameTurn")
def restorePeaceMinors(iGameTurn):
	if iGameTurn > turns(50):
		iMinor = players.independent().periodic(20)
		if iMinor:
			restorePeaceHuman(iMinor, False)
			
		iMinor = players.independent().periodic(60)
		if iMinor:
			restorePeaceAI(iMinor, False)


@handler("BeginGameTurn")
def startMinorWars(iGameTurn):
	if iGameTurn > turns(50):	
		iMinor = players.independent().periodic(13)
		if iMinor:
			minorWars(iMinor)


@handler("BeginGameTurn")
def checkConquests():
	for tConquest in lConquests:
		checkConquest(tConquest)
		
		
@handler("BeginGameTurn")
def checkWarPlans(iGameTurn):		
	if iGameTurn == data.iNextTurnAIWar:
		planWars(iGameTurn)


@handler("BeginGameTurn")
def checkTargetMinors():
	targetMinors()


@handler("BeginGameTurn")
def increaseAggressionLevels():
	for iLoopPlayer in players.major():
		data.players[iLoopPlayer].iAggressionLevel = dAggressionLevel[iLoopPlayer] + rand(2)


@handler("techAcquired")	
def forgetMemory(iTech, iTeam, iPlayer):
	if year() <= year(1700):
		return

	if iTech in [iPsychology, iTelevision]:
		pPlayer = player(iPlayer)
		for iLoopPlayer in players.major().without(iPlayer):
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR, -1)
			
			if pPlayer.AI_getMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND) > 0:
				pPlayer.AI_changeMemoryCount(iLoopPlayer, MemoryTypes.MEMORY_DECLARED_WAR_ON_FRIEND, -1)


@handler("changeWar")
def resetAggressionLevel(bWar, iTeam, iOtherTeam):
	if bWar and not is_minor(iTeam) and not is_minor(iOtherTeam):
		data.players[iTeam].iAggressionLevel = 0
		data.players[iOtherTeam].iAggressionLevel = 0

		
def checkConquest(tConquest, tPrereqConquest = (), iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iID, iCiv, iPreferredTargetCiv, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest


	# Aeons - Bring this stuff up closer to the top, to increase loading time.
	iStartTurn = year(iYear) + turns(data.iSeed % 10 - 5)
	if turn() < iStartTurn - turns(5):
		return
	if turn() > iStartTurn + iIntervalTurns:
		return

	iSelectedCiv = iCiv

	# Removed this - It was kind of stupid

	# Aeons - Dynamic conquerors if Rome isn't strong enough. 
	#if iSelectedCiv == iRome and not player(iRome).isHuman():
	#	# Selects the strongest civ possible with Mediterranean adjcent capital
	#	# This will probably be Carthage or Greece, if the human player is strongest, no conquerors
	#	validPlayers = players.major().existing().where(lambda p: plots.capital(p) in plots.region(rMediterraneanSea).expand(1) and not civ(p) == iMacedon and not civ(p) == iPreferredTargetCiv)
	#	if validPlayers == None:
	#		return
	#	iSelectedCiv = civ(validPlayers.maximum(lambda p: player(p).getNumMilitaryUnits()))

	# Aeons - return for conquests like Carthage vs Carthage
	#if iSelectedCiv == iPreferredTargetCiv:
	#	return
	
	iPlayer = slot(iSelectedCiv)
	if iPlayer < 0:
		return
		
	iPreferredTarget = slot(iPreferredTargetCiv)

	if player(iPlayer).isHuman():
		return
		
	if not player(iPlayer).isExisting() and iSelectedCiv != iTurks: 
		return
	
	if team(iPlayer).isAVassal():
		return
	
	if data.lConquest[iID]:
		return
		
	if iPreferredTarget >= 0 and player(iPreferredTarget).isExisting() and team(iPreferredTarget).isVassal(iPlayer):
		return
	
	if tPrereqConquest and not isConquered(tPrereqConquest):
		return
	
	if iSelectedCiv == iSpain and (iPreferredTarget < 0 or player(iPreferredTarget).isHuman()):
		return
	
	if turn() == iStartTurn - turns(5):
		warnConquest(iPlayer, iSelectedCiv, iPreferredTargetCiv, tTL, tBR)
	
	if turn() < player(iSelectedCiv).getLastBirthTurn() + turns(3): 
		return
	
	if not (iStartTurn <= turn() <= iStartTurn + iIntervalTurns):
		return
	
	spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan)
	data.lConquest[iID] = True


def warnConquest(iPlayer, iCiv, iPreferredTargetCiv, tTL, tBR):
	text = text_if_exists("TXT_KEY_MESSAGE_CONQUERORS_%s_%s" % (infos.civ(iCiv).getIdentifier(), infos.civ(iPreferredTargetCiv).getIdentifier()), adjective(iPlayer), otherwise="TXT_KEY_MESSAGE_CONQUERORS_GENERIC")
	conquerorCities = cities.owner(iPlayer)
	
	for iTarget, targetCities in cities.rectangle(tTL, tBR).notowner(iPlayer).grouped(CyCity.getOwner):
		message(iTarget, str(text), color=iRed, location=targetCities.closest_all(conquerorCities), button=infos.civ(iCiv).getButton())


def isConquered(tConquest):
	iID, iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns = tConquest

	iNumMinorCities = 0
	for city in cities.start(tTL).end(tBR):
		if city.getOwner() in players.minor(): iNumMinorCities += 1
		elif city.getOwner() != iPlayer: return False
		
	if 2 * iNumMinorCities > len(lAreaCities): return False
	
	return True


def conquerorWar(iPlayer, iTarget, iWarPlan):
	# reset at war counters because this is essentially a renewed war, will avoid cheap peace out of the conquerors
	if team(iPlayer).isAtWar(team(iTarget).getID()):
		team(iPlayer).AI_setAtWarCounter(team(iTarget).getID(), 0)
		team(iTarget).AI_setAtWarCounter(team(iPlayer).getID(), 0)
		
		team(iPlayer).AI_setWarPlan(team(iTarget).getID(), iWarPlan)
		
	# otherwise declare war
	else:
		declareWar(iPlayer, iTarget, iWarPlan)


def spawnCrusaders(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):
	iCiv = civ(iPlayer)
	
	if not player(iPlayer).isExisting():
		for iTech in getResurrectionTechs(iPlayer):
			team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
			
	targetPlots = plots.rectangle(tTL, tBR)
			
	targetCities = cities.rectangle(tTL, tBR).notowner(iPlayer).where(lambda city: not team(city).isVassal(iPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iPlayer))))
	owners = set(city.getOwner() for city in targetCities)
	
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isExisting():
		conquerorWar(iPlayer, iPreferredTarget, iWarPlan)
			
	for iOwner in owners:
		conquerorWar(iPlayer, iOwner, iWarPlan)
		message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iPlayer))
		
	for city in targetCities:
		iExtra = 0
		if active() not in [iPlayer, city.getOwner()]: 
			iExtra += 1
			
		if not player(iPlayer).isHuman():
			if iCiv == iMongols:
				iExtra += 1
		
		tPlot = findNearestLandPlot(city, iPlayer)
		
		dConquestUnits = {
			iCitySiege: 1 + min(1, iExtra),
			iDefend: 1,
		}
		units = makeUnits(iPlayer, iCrusader, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
		units += createRoleUnits(iPlayer, tPlot, dConquestUnits.items())
		units.promotion(iVolunteer)


	
def spawnConquerors(iPlayer, iPreferredTarget, tTL, tBR, iNumTargets, iYear, iIntervalTurns, iWarPlan = WarPlanTypes.WARPLAN_TOTAL):

	iSelectedPlayer = iPlayer

	iCiv = civ(iSelectedPlayer)
	
	if not player(iSelectedPlayer).isExisting():
		for iTech in getResurrectionTechs(iSelectedPlayer):
			team(iSelectedPlayer).setHasTech(iTech, True, iSelectedPlayer, False, False)
			
	targetPlots = plots.rectangle(tTL, tBR)
			
	targetCities = cities.rectangle(tTL, tBR).notowner(iSelectedPlayer).where(lambda city: not team(city).isVassal(iSelectedPlayer)).lowest(iNumTargets, lambda city: (city.getOwner() == iPreferredTarget, distance(city, capital(iSelectedPlayer))))
	owners = set(city.getOwner() for city in targetCities)
	
	if iPreferredTarget >= 0 and iPreferredTarget not in owners and player(iPreferredTarget).isExisting():
		conquerorWar(iSelectedPlayer, iPreferredTarget, iWarPlan)
			
	for iOwner in owners:
		conquerorWar(iSelectedPlayer, iOwner, iWarPlan)
		message(iOwner, 'TXT_KEY_UP_CONQUESTS_TARGET', name(iSelectedPlayer))
		
	for city in targetCities:
		iExtra = 0
		if active() not in [iSelectedPlayer, city.getOwner()]: 
			iExtra += 1
			
		if not player(iSelectedPlayer).isHuman():
			if iCiv == iMongols:
				iExtra += 1
		
		tPlot = findNearestLandPlot(city, iSelectedPlayer)
		
		dConquestUnits = {
			iCityAttack: 2 + iExtra + max(0, iExtra-2),
			iCitySiege: 1 + min(1, iExtra),
			iDefend: 1,
		}
		units = createRoleUnits(iSelectedPlayer, tPlot, dConquestUnits.items())
		

		if iCiv == iHuns:
			units += makeUnits(iSelectedPlayer, iHeavyHorseArcher, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)

		# Aeons - Give Rome some extras
		elif iCiv == iRome:
			units += makeUnits(iSelectedPlayer, iBallista, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iLegion, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		elif iCiv == iVandals:
			units += makeUnits(iSelectedPlayer, iCatapult, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iHeavySwordsman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		elif iCiv == iGoths:
			units += makeUnits(iSelectedPlayer, iKontosCavalry, tPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iCatapult, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)

		elif iCiv == iGermania:
			units += makeUnits(iSelectedPlayer, iGermanicWarrior, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iCatapult, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		elif iCiv == iFrance:
			units += makeUnits(iSelectedPlayer, iArmouredHorseman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iTrebuchet, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		elif iCiv == iSpain:
			units += makeUnits(iSelectedPlayer, iCrusader, tPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
		
		elif iCiv == iGhorids:
			units += makeUnits(iSelectedPlayer, iMujahideenSpearman, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)
			units += makeUnits(iSelectedPlayer, iMujahid, tPlot, 1, UnitAITypes.UNITAI_ATTACK_CITY)

		if iCiv in [iEngland]:
			units += createRoleUnit(iSelectedPlayer, tPlot, iShockCity, iExtra)
			if year() >= year(1700): # Aeons - Cape War
				units += createRoleUnit(iPlayer, tPlot, iCityAttack, 2)
				units += createRoleUnit(iPlayer, tPlot, iCitySiege, 2)
			
		if iCiv in [iTurks, iTimurids]:
			units += createRoleUnit(iSelectedPlayer, tPlot, iShockCity, 2+iExtra)

		if iCiv == iOttomans:
			units += createRoleUnit(iPlayer, tPlot, iShockCity, 1+iExtra)
			units += createRoleUnit(iPlayer, tPlot, iCitySiege, 1+iExtra)
			units += createRoleUnit(iPlayer, tPlot, iCityAttack, 2+iExtra)

		units.promotion(iVolunteer)


def declareWar(iPlayer, iTarget, iWarPlan):
	if team(iPlayer).isVassal(iTarget):
		team(iPlayer).setVassal(iTarget, False, False)
		
	team(iPlayer).declareWar(iTarget, True, iWarPlan)


def planWars(iGameTurn):
	# skip if there is a world war
	if iGameTurn > year(1500):
		iCivsAtWar = 0
		for iLoopPlayer in players.major():
			if team(iLoopPlayer).getAtWarCount(True) > 0:
				iCivsAtWar += 1
		if 100 * iCivsAtWar / game.countCivPlayersAlive() > 50:
			data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)
			return

	iAttackingPlayer = determineAttackingPlayer()
	iTargetPlayer = determineTargetPlayer(iAttackingPlayer)
	
	if iAttackingPlayer is None:
		return

	data.players[iAttackingPlayer].iAggressionLevel = 0
	
	if iTargetPlayer == -1:
		return
		
	if team(iAttackingPlayer).canDeclareWar(iTargetPlayer):
		team(iAttackingPlayer).AI_setWarPlan(iTargetPlayer, WarPlanTypes.WARPLAN_PREPARING_LIMITED)
	
	data.iNextTurnAIWar = iGameTurn + getNextInterval(iGameTurn)


def targetMinors():
	for iPlayer in players.major().ai().existing().periodic_iter(10):
		if players.major().existing().any(lambda p: team(iPlayer).isAtWar(player(p).getTeam())):
			continue
	
		if players.major().existing().any(lambda p: team(iPlayer).AI_getWarPlan(player(p).getTeam()) != WarPlanTypes.NO_WARPLAN):
			continue
		
		for city in cities.all().where(is_minor).revealed(iPlayer):
			if team(iPlayer).isAtWar(city.getTeam()):
				continue
		
			if plot(city).getPlayerSettlerValue(iPlayer) >= 5 or plot(city).getPlayerWarValue(iPlayer) >= 2:
				declareWar(iPlayer, city.getOwner(), WarPlanTypes.WARPLAN_LIMITED)
				break


def determineAttackingPlayer():
	return players.major().existing().where(isNotPlanning).where(possibleTargets).maximum(lambda p: data.players[p].iAggressionLevel)


def possibleTargets(iPlayer):
	return players.major().existing().without(iPlayer).where(lambda p: team(iPlayer).canDeclareWar(player(p).getTeam()))


def isNotPlanning(iPlayer):
	return players.major().existing().without(iPlayer).all(lambda p: team(iPlayer).AI_getWarPlan(player(p).getTeam()) == -1)


def determineTargetPlayer(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	lPotentialTargets = []
	dTargetValues = defaultdict({}, 0)

	# determine potential targets
	for iLoopPlayer in possibleTargets(iPlayer):
		pLoopPlayer = player(iLoopPlayer)
		tLoopPlayer = team(iLoopPlayer)
		
		if iLoopPlayer == iPlayer: continue
		
		# requires live civ and past contact
		if not pLoopPlayer.isExisting(): continue
		if not tPlayer.isHasMet(iLoopPlayer): continue
		
		# no masters or vassals
		if tPlayer.isVassal(iLoopPlayer): continue
		if tLoopPlayer.isVassal(iPlayer): continue
		
		# not already at war
		if tPlayer.isAtWar(iLoopPlayer): continue
		
		# birth protected
		if pLoopPlayer.isBirthProtected(): continue
		
		lPotentialTargets.append(iLoopPlayer)
		
	if not lPotentialTargets: 
		return -1
		
	# iterate the map for all potential targets
	for plot in plots.all():
		iOwner = plot.getOwner()
		if iOwner in lPotentialTargets:
			dTargetValues[iOwner] += plot.getPlayerWarValue(iPlayer)
				
	# hard to attack with lost contact
	for iLoopPlayer in lPotentialTargets:
		if not pPlayer.canContact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 8
		
	# normalization
	iMaxValue = max(dTargetValues.values())
	if iMaxValue == 0: 
		return -1
	
	for iLoopPlayer in lPotentialTargets:
		dTargetValues[iLoopPlayer] *= 500
		dTargetValues[iLoopPlayer] /= iMaxValue
		
	for iLoopPlayer in lPotentialTargets:
		iLoopCiv = civ(iLoopPlayer)
	
		# randomization
		if dTargetValues[iLoopPlayer] <= iThreshold:
			dTargetValues[iLoopPlayer] += rand(100)
		else:
			dTargetValues[iLoopPlayer] += rand(300)
		
		# balanced by attitude
		iAttitude = pPlayer.AI_getAttitude(iLoopPlayer) - 2
		if iAttitude > 0:
			dTargetValues[iLoopPlayer] /= 2 * iAttitude
			
		# exploit plague
		if data.players[iLoopPlayer].iPlagueCountdown > 0 or data.players[iLoopPlayer].iPlagueCountdown < -10:
			if turn() > player(iLoopPlayer).getLastBirthTurn() + turns(20):
				dTargetValues[iLoopPlayer] *= 3
				dTargetValues[iLoopPlayer] /= 2
	
		# determine master
		iMaster = master(iLoopPlayer)
				
		# master attitudes
		if iMaster >= 0:
			iAttitude = player(iMaster).AI_getAttitude(iLoopPlayer)
			if iAttitude > 0:
				dTargetValues[iLoopPlayer] /= 2 * iAttitude
		
		# peace counter
		if not tPlayer.isAtWar(iLoopPlayer):
			iCounter = min(7, max(1, tPlayer.AI_getAtPeaceCounter(iLoopPlayer)))
			if iCounter <= 7:
				dTargetValues[iLoopPlayer] *= 20 + 10 * iCounter
				dTargetValues[iLoopPlayer] /= 100
				
		# defensive pact
		if tPlayer.isDefensivePact(iLoopPlayer):
			dTargetValues[iLoopPlayer] /= 4
			
		# consider power
		iOurPower = tPlayer.getPower(True)
		iTheirPower = team(iLoopPlayer).getPower(True)
		if iOurPower > 2 * iTheirPower:
			dTargetValues[iLoopPlayer] *= 2
		elif 2 * iOurPower < iTheirPower:
			dTargetValues[iLoopPlayer] /= 2
			
		# spare smallish civs
		if iLoopCiv in [iNetherlands, iPortugal, iItaly]:
			dTargetValues[iLoopPlayer] *= 4
			dTargetValues[iLoopPlayer] /= 5
			
		# no suicide
		if iCiv == iNetherlands:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				dTargetValues[iLoopPlayer] /= 2
		elif iCiv == iPortugal:
			if iLoopCiv == iSpain:
				dTargetValues[iLoopPlayer] /= 2
		elif iCiv == iItaly:
			if iLoopCiv in [iFrance, iHolyRome, iGermany]:
				dTargetValues[iLoopPlayer] /= 2

		# Spain prefers Moors in Iberia
		if (iCiv == iSpain and iLoopCiv != iMoors) or (iCiv == iFrance and iLoopCiv == iSpain):
			if cities.regions(rIberia).owner(iMoors):
				dTargetValues[iLoopPlayer] /= 4
				
	return dict_max(dTargetValues)
				

def getNextInterval(iGameTurn):
	if iGameTurn > year(1600):
		iMinInterval = iMinIntervalLate
		iMaxInterval = iMaxIntervalLate
	else:
		iMinInterval = iMinIntervalEarly
		iMaxInterval = iMaxIntervalEarly
		
	iMinInterval = turns(iMinInterval)
	iMaxInterval = turns(iMaxInterval)
	
	return rand(iMinInterval, iMaxInterval)