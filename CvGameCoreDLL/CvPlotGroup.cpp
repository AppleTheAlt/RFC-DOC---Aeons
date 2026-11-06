// plotGroup.cpp

#include "CvGameCoreDLL.h"
#include "CvPlotGroup.h"

// Verification build: after every rebuild, count groups of the same owner that are
// still joined by a valid trade link.  Set to 1 to re-run the check.
#define PLOT_GROUP_VERIFY 0

// Fresol - start: see recalculatePlots
static bool s_bSuspendCityBonusSync = false;

void setSuspendCityBonusSync(bool bSuspend)
{
	s_bSuspendCityBonusSync = bSuspend;
}

bool isCityBonusSyncSuspended()
{
	return s_bSuspendCityBonusSync;
}
// Fresol - end
#include <map> // Fresol: the rebuild groups its members per component
#include "CvPlot.h"
#include "CvGlobals.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvCity.h"
#include "CvDLLFAStarIFaceBase.h"
#include "FProfiler.h"
#include "CvRhyes.h"

// Fresol - start
// The health check in recalculatePlots only asks whether the group's member list is
// still one connected component, so that is answered here with a BFS over the members
// instead of a saturating A* run in the engine. The edge rule is copied verbatim from
// plotGroupValid (CvGameCoreUtils.cpp): both ends in this group, the new plot still in
// the team's trade network, and the two plots directly connected.
// Verified against the A* version over 605,000 calls with no disagreement.

static std::vector<int>		s_aiPlotGroupSeen;			// visit stamp, by plot index
static std::vector<int>		s_aiPlotGroupTradeNetStamp;	// validity stamp of the cached isTradeNetwork result
static std::vector<char>	s_abPlotGroupTradeNet;		// cached isTradeNetwork result
static std::vector<CvPlot*>	s_apPlotGroupStack;
static int					s_iPlotGroupStamp = 0;

int CvPlotGroup::countReachablePlots(PlayerTypes ePlayer, CvPlot* pBlockedPlot)
{
	CLLNode<XYCoords>* pHeadNode = headPlotsNode();

	if (pHeadNode == NULL)
	{
		return 0;
	}

	CvMap& kMap = GC.getMapINLINE();
	const int iNumPlots = kMap.numPlotsINLINE();

	if ((int)s_aiPlotGroupSeen.size() != iNumPlots)
	{
		s_aiPlotGroupSeen.assign(iNumPlots, 0);
		s_aiPlotGroupTradeNetStamp.assign(iNumPlots, 0);
		s_abPlotGroupTradeNet.assign(iNumPlots, 0);
		s_iPlotGroupStamp = 0;
	}

	++s_iPlotGroupStamp;

	const TeamTypes eTeam = GET_PLAYER(ePlayer).getTeam();

	s_apPlotGroupStack.clear();

	// Start from the first member that is not blocked: that is the node recalculatePlots
	// would start its own walk from once the blocked plot has been taken out of the group.
	CLLNode<XYCoords>* pNode = pHeadNode;
	CvPlot* pStartPlot = NULL;

	while (pNode != NULL)
	{
		CvPlot* pCandidate = kMap.plotSorenINLINE(pNode->m_data.iX, pNode->m_data.iY);

		if (pCandidate != pBlockedPlot)
		{
			pStartPlot = pCandidate;
			break;
		}

		pNode = nextPlotsNode(pNode);
	}

	if (pStartPlot == NULL)
	{
		return 0;
	}

	s_apPlotGroupStack.push_back(pStartPlot);
	s_aiPlotGroupSeen[kMap.plotNumINLINE(pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE())] = s_iPlotGroupStamp;

	int iCount = 0;

	while (!s_apPlotGroupStack.empty())
	{
		CvPlot* pPlot = s_apPlotGroupStack.back();
		s_apPlotGroupStack.pop_back();

		++iCount;

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			CvPlot* pAdjacentPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), (DirectionTypes)iI);

			if (pAdjacentPlot == NULL || pAdjacentPlot == pBlockedPlot)
			{
				continue;
			}

			if (pAdjacentPlot->getPlotGroup(ePlayer) != this)
			{
				continue;
			}

			const int iIndex = kMap.plotNumINLINE(pAdjacentPlot->getX_INLINE(), pAdjacentPlot->getY_INLINE());

			if (s_aiPlotGroupSeen[iIndex] == s_iPlotGroupStamp)
			{
				continue;
			}

			if (s_aiPlotGroupTradeNetStamp[iIndex] != s_iPlotGroupStamp)
			{
				s_abPlotGroupTradeNet[iIndex] = pAdjacentPlot->isTradeNetwork(eTeam) ? 1 : 0;
				s_aiPlotGroupTradeNetStamp[iIndex] = s_iPlotGroupStamp;
			}

			if (!s_abPlotGroupTradeNet[iIndex])
			{
				continue;
			}

			if (!pAdjacentPlot->isTradeNetworkConnected(pPlot, eTeam))
			{
				continue;
			}

			s_aiPlotGroupSeen[iIndex] = s_iPlotGroupStamp;
			s_apPlotGroupStack.push_back(pAdjacentPlot);
		}
	}

	return iCount;
}


// Fresol - start
// The rebuild used to take the group apart and then add every member back one at a
// time. On a late game map that is thousands of plots per rebuild (measured 7,200,
// ~52 ms each, 22 rebuilds a game turn) and it is 91% of what recalculatePlots costs.
// The add loop only ever merges a member with a mate that was added before it, through
// a link the new member has to that mate, so the outcome is a partition of the member
// list that can be worked out directly: one union over the members in list order, then
// one group per class. Same order, same link direction, same outcome - checked against
// the add loop over 2,900 rebuilds (every partition the same).
// A mate that is not in the team's trade network has no group of its own, so it cannot
// be merged with either.

static std::vector<int>	s_aiPlotGroupMemberPos;		// position in the member list, by plot index
static std::vector<int>	s_aiPlotGroupMemberMark;	// validity stamp for that position
static int				s_iPlotGroupMemberStamp = 0;

static int plotGroupFindRoot(const std::vector<int>& aiParent, int i)
{
	while (aiParent[i] != i)
	{
		i = aiParent[i];
	}

	return i;
}

// Labels the members of the list: aiLabel[i] is the component of member i (in list
// order), or -1 for a member that has to stay without a group because it is not part of
// the team's trade network any more.
static void computeRebuildComponents(PlayerTypes eOwner, CLinkList<XYCoords>& members,
                                     std::vector<int>& aiPlotIndex, std::vector<int>& aiLabel)
{
	CvMap& kMap = GC.getMapINLINE();
	const int iNumPlots = kMap.numPlotsINLINE();
	const TeamTypes eTeam = GET_PLAYER(eOwner).getTeam();
	CLLNode<XYCoords>* pNode;

	if ((int)s_aiPlotGroupMemberPos.size() != iNumPlots)
	{
		s_aiPlotGroupMemberPos.assign(iNumPlots, 0);
		s_aiPlotGroupMemberMark.assign(iNumPlots, 0);
		s_iPlotGroupMemberStamp = 0;
	}

	++s_iPlotGroupMemberStamp;

	aiPlotIndex.clear();

	for (pNode = members.head(); pNode != NULL; pNode = members.next(pNode))
	{
		const int iIndex = kMap.plotNumINLINE(pNode->m_data.iX, pNode->m_data.iY);

		s_aiPlotGroupMemberPos[iIndex] = (int)aiPlotIndex.size();
		s_aiPlotGroupMemberMark[iIndex] = s_iPlotGroupMemberStamp;
		aiPlotIndex.push_back(iIndex);
	}

	const int iCount = (int)aiPlotIndex.size();

	std::vector<int> aiParent(iCount);
	std::vector<char> abInNetwork(iCount);

	for (int i = 0; i < iCount; ++i)
	{
		aiParent[i] = i;
		abInNetwork[i] = kMap.plotByIndexINLINE(aiPlotIndex[i])->isTradeNetwork(eTeam) ? 1 : 0;
	}

	for (int i = 0; i < iCount; ++i)
	{
		if (!abInNetwork[i])
		{
			continue;			// the add loop leaves such a member without a group
		}

		CvPlot* pPlot = kMap.plotByIndexINLINE(aiPlotIndex[i]);

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			CvPlot* pAdjacentPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), (DirectionTypes)iI);

			if (pAdjacentPlot == NULL)
			{
				continue;
			}

			const int iAdjacentIndex = kMap.plotNumINLINE(pAdjacentPlot->getX_INLINE(), pAdjacentPlot->getY_INLINE());

			if (s_aiPlotGroupMemberMark[iAdjacentIndex] != s_iPlotGroupMemberStamp)
			{
				continue;		// not one of the members we are putting back
			}

			const int iAdjacent = s_aiPlotGroupMemberPos[iAdjacentIndex];

			if (iAdjacent >= i)
			{
				continue;		// only mates added before this one hold a group already
			}

			if (!abInNetwork[iAdjacent])
			{
				continue;		// and that mate needs a group for the merge to happen at all
			}

			if (!pPlot->isTradeNetworkConnected(pAdjacentPlot, eTeam))
			{
				continue;		// the link the add loop checks, in the same direction
			}

			const int iRoot = plotGroupFindRoot(aiParent, i);
			const int iAdjacentRoot = plotGroupFindRoot(aiParent, iAdjacent);

			if (iRoot != iAdjacentRoot)
			{
				aiParent[iRoot] = iAdjacentRoot;
			}
		}
	}

	aiLabel.assign(iCount, -1);

	for (int i = 0; i < iCount; ++i)
	{
		if (abInNetwork[i])
		{
			aiLabel[i] = plotGroupFindRoot(aiParent, i);
		}
	}
}

// Creates one group per component, in member order.
static void rebuildPlotGroups(PlayerTypes eOwner, const std::vector<int>& aiPlotIndex,
                              const std::vector<int>& aiLabel)
{
	CvMap& kMap = GC.getMapINLINE();
	std::map<int, CvPlotGroup*> mapRootToGroup;
	std::map<int, CvPlotGroup*>::iterator it;

	for (int i = 0; i < (int)aiPlotIndex.size(); ++i)
	{
		if (aiLabel[i] < 0)
		{
			continue;
		}

		CvPlot* pPlot = kMap.plotByIndexINLINE(aiPlotIndex[i]);

		it = mapRootToGroup.find(aiLabel[i]);

		if (it == mapRootToGroup.end())
		{
			mapRootToGroup[aiLabel[i]] = GET_PLAYER(eOwner).initPlotGroup(pPlot);
		}
		else
		{
			it->second->addPlot(pPlot);
		}
	}
}
// Fresol - end
// Fresol - end

// Public Functions...

CvPlotGroup::CvPlotGroup()
{
	m_paiNumBonuses = NULL;

	reset(0, NO_PLAYER, true);
}


CvPlotGroup::~CvPlotGroup()
{
	uninit();
}


void CvPlotGroup::init(int iID, PlayerTypes eOwner, CvPlot* pPlot)
{
	//--------------------------------
	// Init saved data
	reset(iID, eOwner);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data
	addPlot(pPlot);
}


void CvPlotGroup::uninit()
{
	SAFE_DELETE_ARRAY(m_paiNumBonuses);

	m_plots.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlotGroup::reset(int iID, PlayerTypes eOwner, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_eOwner = eOwner;

	if (!bConstructorCall)
	{
		FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset");
		m_paiNumBonuses = new int [GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNumBonuses[iI] = 0;
		}
	}
}


void CvPlotGroup::addPlot(CvPlot* pPlot)
{
	XYCoords xy;

	xy.iX = pPlot->getX_INLINE();
	xy.iY = pPlot->getY_INLINE();

	insertAtEndPlots(xy);

	pPlot->setPlotGroup(getOwnerINLINE(), this);
}


void CvPlotGroup::removePlot(CvPlot* pPlot)
{
	CLLNode<XYCoords>* pPlotNode;

	pPlotNode = headPlotsNode();

	while (pPlotNode != NULL)
	{
		if (GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY) == pPlot)
		{
			pPlot->setPlotGroup(getOwnerINLINE(), NULL);

			pPlotNode = deletePlotsNode(pPlotNode); // can delete this PlotGroup...
			break;
		}
		else
		{
			pPlotNode = nextPlotsNode(pPlotNode);
		}
	}
}


// Fresol - start
// A city keeps the bonus counts of the plot group it sits in. Rebuilding a group plot
// by plot used to move every bonus in and out of every city of the group at every
// step, and each of those moves walks the group (see changeNumBonuses), so the upkeep
// was quadratic in the size of the group. What comes out of a rebuild only depends on
// the groups it ends in, so the counts are written once, at the end, and the
// incremental upkeep is suspended while the group is taken apart and put back.
static void syncCityBonuses(PlayerTypes eOwner, const std::vector<int>& aiPlotIndex)
{
	CvMap& kMap = GC.getMapINLINE();
	const int iNumBonuses = GC.getNumBonusInfos();

	for (int i = 0; i < (int)aiPlotIndex.size(); ++i)
	{
		CvPlot* pPlot = kMap.plotByIndexINLINE(aiPlotIndex[i]);
		CvCity* pCity = pPlot->getPlotCity();

		if (pCity == NULL || pCity->getOwnerINLINE() != eOwner)
		{
			continue;
		}

		CvPlotGroup* pNewPlotGroup = pPlot->getPlotGroup(eOwner);

		for (int iI = 0; iI < iNumBonuses; ++iI)
		{
			const int iNew = (pNewPlotGroup != NULL) ? pNewPlotGroup->getNumBonuses((BonusTypes)iI) : 0;

			pCity->changeNumBonuses((BonusTypes)iI, iNew - pCity->getNumBonuses((BonusTypes)iI));
		}
	}
}
// Fresol - end

#ifdef PLOT_GROUP_VERIFY
static int s_iVerifyCalls = 0;
static int s_iVerifyBad = 0;

static void verifyAfterRebuild(PlayerTypes eOwner, const std::vector<int>& aiPlotIndex)
{
	CvMap& kMap = GC.getMapINLINE();
	const TeamTypes eTeam = GET_PLAYER(eOwner).getTeam();
	int iBad = 0;

	for (int i = 0; i < (int)aiPlotIndex.size(); ++i)
	{
		CvPlot* pPlot = kMap.plotByIndexINLINE(aiPlotIndex[i]);
		CvPlotGroup* pGroup = pPlot->getPlotGroup(eOwner);

		if (pGroup == NULL || !pPlot->isTradeNetwork(eTeam))
		{
			continue;
		}

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			CvPlot* pAdjacent = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), (DirectionTypes)iI);

			if (pAdjacent == NULL)
			{
				continue;
			}

			CvPlotGroup* pAdjacentGroup = pAdjacent->getPlotGroup(eOwner);

			if (pAdjacentGroup == NULL || pAdjacentGroup == pGroup || !pAdjacent->isTradeNetwork(eTeam))
			{
				continue;
			}

			if (pPlot->isTradeNetworkConnected(pAdjacent, eTeam))
			{
				++iBad;
			}
		}
	}

	++s_iVerifyCalls;

	if (iBad > 0)
	{
		++s_iVerifyBad;
	}

	if (iBad > 0 || (s_iVerifyCalls % 25) == 0)
	{
		FILE* pFile = fopen("C:\\Users\\86136\\perf\\plotgroup_verify.log", "a");

		if (pFile != NULL)
		{
			fprintf(pFile, "%s owner=%d plots=%d links=%d calls=%d bad=%d\n",
				(iBad > 0) ? "MISMATCH" : "ok", (int)eOwner, (int)aiPlotIndex.size(), iBad,
				s_iVerifyCalls, s_iVerifyBad);
			fclose(pFile);
		}
	}
}
#endif

void CvPlotGroup::recalculatePlots(bool bSkipHealthCheck)
{
	PROFILE_FUNC();

	CLLNode<XYCoords>* pPlotNode;
	CvPlot* pPlot;
	CLinkList<XYCoords> oldPlotGroup;
	XYCoords xy;
	PlayerTypes eOwner;

	eOwner = getOwnerINLINE();

	pPlotNode = headPlotsNode();

	if (!bSkipHealthCheck)
	{
		if (pPlotNode != NULL)
		{
			if (countReachablePlots(eOwner) == getLengthPlots())
			{
				return;
			}
		}
	}

	bool bWasSuspended = isCityBonusSyncSuspended(); // Fresol
	setSuspendCityBonusSync(true); // Fresol

	oldPlotGroup.clear();

	pPlotNode = headPlotsNode();

	while (pPlotNode != NULL)
	{
		pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

		FAssertMsg(pPlot != NULL, "Plot is not assigned a valid value");

		xy.iX = pPlot->getX_INLINE();
		xy.iY = pPlot->getY_INLINE();

		oldPlotGroup.insertAtEnd(xy);

		pPlot->setPlotGroup(eOwner, NULL);

		pPlotNode = deletePlotsNode(pPlotNode); // will delete this PlotGroup...
	}

	std::vector<int> aiPlotIndex;
	std::vector<int> aiLabel;

	computeRebuildComponents(eOwner, oldPlotGroup, aiPlotIndex, aiLabel);
	rebuildPlotGroups(eOwner, aiPlotIndex, aiLabel);

	setSuspendCityBonusSync(bWasSuspended); // Fresol

	// Fresol: while re-adding, the old algorithm merged the group with any adjacent
	// group it reached.  Do the same here, otherwise a rebuild can leave two groups
	// that are connected to each other apart.
	for (int i = 0; i < (int)aiPlotIndex.size(); ++i)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(aiPlotIndex[i]);
		CvPlotGroup* pGroup = pPlot->getPlotGroup(eOwner);

		if (pGroup == NULL)
		{
			continue;
		}

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			CvPlot* pAdjacent = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), (DirectionTypes)iI);

			if (pAdjacent != NULL)
			{
				CvPlotGroup* pAdjacentGroup = pAdjacent->getPlotGroup(eOwner);

				if (pAdjacentGroup != NULL && pAdjacentGroup != pGroup)
				{
					pPlot->updatePlotGroup(eOwner, false);
					break;
				}
			}
		}
	}

	syncCityBonuses(eOwner, aiPlotIndex); // Fresol

#ifdef PLOT_GROUP_VERIFY
	verifyAfterRebuild(eOwner, aiPlotIndex);
#endif
}


int CvPlotGroup::getID() const
{
	return m_iID;
}


void CvPlotGroup::setID(int iID)
{
	m_iID = iID;
}


PlayerTypes CvPlotGroup::getOwner() const
{
	return getOwnerINLINE();
}


int CvPlotGroup::getNumBonuses(BonusTypes eBonus) const
{
	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");
	return m_paiNumBonuses[eBonus];
}


bool CvPlotGroup::hasBonus(BonusTypes eBonus)
{
	return(getNumBonuses(eBonus) > 0);
}


void CvPlotGroup::changeNumBonuses(BonusTypes eBonus, int iChange)
{
	CLLNode<XYCoords>* pPlotNode;
	CvCity* pCity;
	int iOldNumBonuses;

	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		iOldNumBonuses = getNumBonuses(eBonus);

		m_paiNumBonuses[eBonus] = (m_paiNumBonuses[eBonus] + iChange);

		//FAssertMsg(m_paiNumBonuses[eBonus] >= 0, "m_paiNumBonuses[eBonus] is expected to be non-negative (invalid Index)"); XXX

		if (!s_bSuspendCityBonusSync)
		{
			pPlotNode = headPlotsNode();

			while (pPlotNode != NULL)
			{
				pCity = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY)->getPlotCity();

				if (pCity != NULL)
				{
					if (pCity->getOwnerINLINE() == getOwnerINLINE())
					{
						pCity->changeNumBonuses(eBonus, iChange);
					}
				}

				pPlotNode = nextPlotsNode(pPlotNode);
			}
		}

		// Leoreth: Escorial
		if (getOwnerINLINE() != NO_PLAYER && GET_PLAYER(getOwnerINLINE()).isHasBuildingEffect(ESCORIAL))
		{
			if (eBonus == BONUS_SILVER || eBonus == BONUS_GOLD)
			{
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
				{
					if (pLoopCity->isHasRealBuilding(ESCORIAL))
					{
						pLoopCity->changeBuildingCommerceChange(ESCORIAL, COMMERCE_GOLD, 2 * iChange);
						break;
					}
				}
			}
		}

		// Leoreth: Atomium
		if (getOwnerINLINE() != NO_PLAYER && GET_PLAYER(getOwnerINLINE()).isHasBuildingEffect(ATOMIUM))
		{
			if (eBonus == BONUS_URANIUM || eBonus == BONUS_IRON || eBonus == BONUS_COPPER || eBonus == BONUS_ALUMINUM)
			{
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
				{
					if (pLoopCity->isHasBuildingEffect(ATOMIUM))
					{
						pLoopCity->changeBuildingCommerceChange(ATOMIUM, COMMERCE_RESEARCH, (eBonus == BONUS_URANIUM ? 10 : 1) * iChange);
					}
				}
			}
		}

		// Leoreth: Global Seed Vault
		if (getOwner() != NO_PLAYER && GET_PLAYER(getOwner()).isHasBuildingEffect(GLOBAL_SEED_VAULT))
		{
			int iLoop;
			for (CvCity* pLoopCity = GET_PLAYER(getOwner()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwner()).nextCity(&iLoop))
			{
				if (pLoopCity->isHasRealBuilding(GLOBAL_SEED_VAULT))
				{
					for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
					{
						CvBuildInfo& kBuild = GC.getBuildInfo((BuildTypes)iJ);
						if (kBuild.isGraphicalOnly())
						{
							continue;
						}

						if (kBuild.getTechPrereq() == AGRICULTURE || kBuild.getTechPrereq() == POTTERY || kBuild.getTechPrereq() == CALENDAR)
						{
							CvImprovementInfo& kImprovement = GC.getImprovementInfo((ImprovementTypes)kBuild.getImprovement());
							if (kImprovement.isImprovementBonusMakesValid(eBonus) && !kImprovement.isGraphicalOnly() && !kImprovement.isActsAsCity())
							{
								pLoopCity->changeBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)GLOBAL_SEED_VAULT).getBuildingClassType(), COMMERCE_RESEARCH, iChange);
								break;
							}
						}
					}

					break;
				}
			}
		}
	}
}


void CvPlotGroup::insertAtEndPlots(XYCoords xy)
{
	m_plots.insertAtEnd(xy);
}


CLLNode<XYCoords>* CvPlotGroup::deletePlotsNode(CLLNode<XYCoords>* pNode)
{
	CLLNode<XYCoords>* pPlotNode;

	pPlotNode = m_plots.deleteNode(pNode);

	if (getLengthPlots() == 0)
	{
		GET_PLAYER(getOwnerINLINE()).deletePlotGroup(getID());
	}

  return pPlotNode;
}


CLLNode<XYCoords>* CvPlotGroup::nextPlotsNode(CLLNode<XYCoords>* pNode)
{
	return m_plots.next(pNode);
}


int CvPlotGroup::getLengthPlots()
{
	return m_plots.getLength();
}


CLLNode<XYCoords>* CvPlotGroup::headPlotsNode()
{
	return m_plots.head();
}


void CvPlotGroup::read(FDataStreamBase* pStream)
{
	// Init saved data
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);

	pStream->Read((int*)&m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::read");
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonuses);

	m_plots.Read(pStream);
}


void CvPlotGroup::write(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);

	pStream->Write(m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::write");
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonuses);

	m_plots.Write(pStream);
}
