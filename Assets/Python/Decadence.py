# Aeons
from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
from StoredData import data # edead
from Consts import *
from RFCUtils import *
from operator import itemgetter
from Events import handler
from Modifiers import *
from Civics import *

from Locations import *
from Core import *

def changeDecadence(iPlayer, iAmount):
    iDecadenceBefore = data.players[iPlayer].iDecadence
    data.players[iPlayer].iDecadence += iAmount

    if(data.players[iPlayer].iDecadence < 0):
        data.players[iPlayer].iDecadence = 0

    # Cap at 30 Decadence
    if(data.players[iPlayer].iDecadence > 30):
        data.players[iPlayer].iDecadence = 30

    iRealAmount =  data.players[iPlayer].iDecadence - iDecadenceBefore

    if(iRealAmount == 0):
        return

    # Worsen modifiers by 10 per decadence - Ignore first 3 rises
    iEffectiveBefore = max(3, iDecadenceBefore)
    iEffectiveAfter = max(3, data.players[iPlayer].iDecadence)
    iModifierAdjustment = iEffectiveAfter - iEffectiveBefore
    if iModifierAdjustment != 0:
        for iModifier in (iModifierResearchCost, iModifierCitiesMaintenance, iModifierBuildingCost, iModifierUnitCost, iModifierWonderCost, iModifierCivicUpkeep):
            changeModifier(iPlayer, iModifier, 10*iModifierAdjustment)

# Building a Wonder raises decadence
@handler("buildingBuilt")
def raiseDecadenceFromWonder(city, iBuilding):
	if infos.building(iBuilding).isTeamShare():
		changeDecadence(city.getOwner(), 1)

# Being first to discover tech - 50% chance of decadence increase
@handler("techAcquired")
def raiseDecadenceFromFirstTech(iTech, iTeam, iPlayer):
    if scenarioStart() or game.getGameTurn() <= year(dBirth[civ(iPlayer)]):
		return
    if game.countKnownTechNumTeams(iTech) == 1:
        if rand(2) == 1:
            changeDecadence(iPlayer, 1)

# 1/20 chance of decadence loss per turn
@handler("EndPlayerTurn")
def lowerDecadenceTick(iGameTurn, iPlayer):
    if(rand(turns(20)) == 1):
        changeDecadence(iPlayer, -1)
        civic = civics(iPlayer)
        
        # Monasticism doubles decadence decrease tick
        if civic.iReligion == iMonasticism:
             changeDecadence(iPlayer, -1)


# Statesmen can purge corruption to lower decadence by 3
def statesmanLowerDecadence(iPlayer):
    changeDecadence(iPlayer, -3)

# With sufficient decadence, revolters will spawn in borders
#@handler("BeginGameTurn")
#def decadenceRevolters():
#    for iPlayer in players.major().existing():
#        if data.players[iPlayer].iDecadence >= 5: # Decadence must be at least 5 for a chance of revolters
#                for city in cities.owner(player(iPlayer)):
#                    if(rand(turns(150)) <= data.players[iPlayer].iDecadence/2): 
#                        iEra = player(iPlayer).getCurrentEra()
#                        spawnPlot = plots.surrounding(city).without(city).land().passable().no_enemies(iBarbarian).random()
#                        if iEra == iAncient: # 3 Warriors
#                            created_unit = makeUnit(iBarbarian, iWarrior, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iWarrior, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iWarrior, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                        elif iEra == iClassical: # 3 Levymen
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                        elif iEra == iMedieval: # 3 Levymen, 1 Maceman
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iMaceman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                        elif iEra == iRenaissance: # 3 Levyman, 1 Arquebus, 1 Bombard
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iLevyman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_PEASANT_REVOLTER")
#                            created_unit = makeUnit(iBarbarian, iArquebusier, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iBombard, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                        elif iEra == iIndustrial: # 3 Musket, 1 Artillery
#                            created_unit = makeUnit(iBarbarian, iMusketeer, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iMusketeer, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iMusketeer, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iArtillery, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                        elif iEra == iGlobal: # 3 Rifles, 1 Artillery
#                            created_unit = makeUnit(iBarbarian, iRifleman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iRifleman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iRifleman, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iArtillery, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                        elif iEra == iDigital: # 3 Infantry, 1 Mobile Artillery, 1 tank
#                            created_unit = makeUnit(iBarbarian, iInfantry, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iInfantry, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iInfantry, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iMobileArtillery, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")
#                            created_unit = makeUnit(iBarbarian, iTank, spawnPlot, UnitAITypes.UNITAI_ATTACK)
#                            set_unit_adjective(created_unit, "TXT_KEY_ADJECTIVE_REBEL")                          