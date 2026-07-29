from Definitions import *
from Locations import *


lHappinessResources = [iResource for iResource in infos.bonuses() if infos.bonus(iResource).getHappiness() > 0]
lResources = [iResource for iResource in infos.bonuses()]

# second Phoenician goal: reveal 50% of the African coast by 1 AD
lAfricanCoastRegions = [rRegion for rRegion in lAfrica if rRegion != rMadagascar] 

# first Norse goal: control a European core in 1050 AD
lNorseTargets = [plots.core(iCiv) for iCiv in dCivGroups[iCivGroupEurope] if iCiv not in (iCelts, iNorse) and dBirth[iCiv] <= 1050] + [plots.core(iCelts, iPeriod=iPeriodInsularCelts)]

# first Portuguese goal
lIndianTradeRegions = [rArabia, rSindh, rRajputana, rDeccan, rDravida, rHornOfAfrica, rSwahiliCoast, rCape, rKalahari, rCongo, rGuinea, rSahel, rSahara, rMaghreb]

# second Portuguese goal: acquire 12 colonial resources by 1650 AD
lColonialResources = [iBanana, iSpices, iSugar, iCoffee, iTea, iTobacco, iCocoa]

# Third Ghana goal
lWestAfricaRegions = [rSahel, rGuinea]

# third Aztec goal: control a European core by 1750 AD
lAztecTargets = [plots.core(iCiv) for iCiv in dCivGroups[iCivGroupEurope]]

# third Thai goal: allow no foreign powers in South Asia in 1900 AD
lSouthAsianCivs = [iHarappa, iIndia, iDravidia, iVietnam, iMalays, iJava, iKhmer, iBurma, iTimurids, iThailand, iGhorids]

# Ethiopia and Kanem-Bornu
lAfricanCivs = [iCiv for iCiv in dCivGroups[iCivGroupAfrica]]
lAfricanCivs.extend(iCiv for iCiv in dCivGroups[iCivGroupNorthAfrica])

# first Russian goal: control three Orthodox Cathedrals and three Orthodox wonders by 1550 AD
lOrthodoxWonders = [iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding) and iOrthodoxy in [infos.building(iBuilding).getPrereqReligion(), infos.building(iBuilding).getOrPrereqReligion()]]

# State religion wonders
lCatholicWonders = [iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding) and iCatholicism in [infos.building(iBuilding).getPrereqReligion(), infos.building(iBuilding).getOrPrereqReligion()]]

lZoroastrianWonders = [iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding) and iZoroastrianism in [infos.building(iBuilding).getPrereqReligion(), infos.building(iBuilding).getOrPrereqReligion()]]

lIslamicWonders = [iBuilding for iBuilding in infos.buildings() if isWonder(iBuilding) and iIslam in [infos.building(iBuilding).getPrereqReligion(), infos.building(iBuilding).getOrPrereqReligion()]]

# first Saudi goal: allow only Arab civilizations in the Arab World
lArabCivs = [iArabia, iMoors, iMisr, iSaudis, iMorocco, iOman, iYemen]

# city names
AMSTERDAM = "TXT_KEY_VICTORY_NAME_AMSTERDAM"
ANGKOR = "TXT_KEY_VICTORY_NAME_ANGKOR"
AYUTTHAYA = "TXT_KEY_VICTORY_NAME_AYUTTHAYA"
BABYLON = "TXT_KEY_VICTORY_NAME_BABYLON"
BAGHDAD = "TXT_KEY_VICTORY_NAME_BAGHDAD"
BERLIN = "TXT_KEY_VICTORY_NAME_BERLIN"
BRUSSELS = "TXT_KEY_VICTORY_NAME_BRUSSELS"
BUENOS_AIRES = "TXT_KEY_VICTORY_NAME_BUENOS_AIRES"
CARTHAGE = "TXT_KEY_VICTORY_NAME_CARTHAGE"
CAIRO = "TXT_KEY_VICTORY_NAME_CAIRO"
CONSTANTINOPLE = "TXT_KEY_VICTORY_NAME_CONSTANTINOPLE"
CORDOBA = "TXT_KEY_VICTORY_NAME_CORDOBA"
LHASA = "TXT_KEY_VICTORY_NAME_LHASA"
MEXICO_CITY = "TXT_KEY_VICTORY_NAME_MEXICO_CITY"
MOSCOW = "TXT_KEY_VICTORY_NAME_MOSCOW"
MUBENDE = "TXT_KEY_VICTORY_NAME_MUBENDE"
PARIS = "TXT_KEY_VICTORY_NAME_PARIS"
SUSA = "TXT_KEY_VICTORY_NAME_SUSA"
PERSEPOLIS = "TXT_KEY_VICTORY_NAME_PERSEPOLIS"
TENOCHTITLAN = "TXT_KEY_VICTORY_NAME_TENOCHTITLAN"
TOLLAN = "TXT_KEY_VICTORY_NAME_TOLLAN"
VIENNA = "TXT_KEY_VICTORY_NAME_VIENNA"
SELEUCIA = "TXT_KEY_VICTORY_NAME_SELEUCIA"
TOLEDO = "TXT_KEY_VICTORY_NAME_TOLEDO"
ROME = "TXT_KEY_VICTORY_NAME_ROME"
ARTASHAT = "TXT_KEY_VICTORY_NAME_ARTASHAT"
JERUSALEM = "TXT_KEY_VICTORY_NAME_JERUSALEM"
LISBON = "TXT_KEY_VICTORY_NAME_LISBON"
VENICE = "TXT_KEY_VICTORY_NAME_VENICE"
BEIJING = "TXT_KEY_VICTORY_NAME_BEIJING"
MOGADISHU = "TXT_KEY_VICTORY_NAME_MOGADISHU"
MWIMBELE = "TXT_KEY_VICTORY_NAME_MWIMBELE"

# city descriptors
ANOTHER_CAPITAL = "TXT_KEY_VICTORY_NAME_ANOTHER_CAPITAL"
CAPITAL = "TXT_KEY_VICTORY_NAME_CAPITAL"
DIFFERENT_CAPITAL = "TXT_KEY_VICTORY_NAME_DIFFERENT_CAPITAL"
ITS_CITY = "TXT_KEY_VICTORY_NAME_ITS_CITY"
MALAYAN_CITY = "TXT_KEY_VICTORY_NAME_MALAYAN_CITY"
BENIN_CITY = "TXT_KEY_VICTORY_NAME_BENIN_CITY"
MOZAMBIQUE = "TXT_KEY_VICTORY_NAME_MOZAMBIQUE"
CAPE_TOWN = "TXT_KEY_VICTORY_NAME_CAPE_TOWN"
PRETORIA = "TXT_KEY_VICTORY_NAME_PRETORIA"

# area names
AFRICA = "TXT_KEY_VICTORY_NAME_AFRICA"
AFRICAN_COAST = "TXT_KEY_VICTORY_NAME_AFRICAN_COAST"
ANDALUSIA = "TXT_KEY_VICTORY_NAME_ANDALUSIA"
ANDES = "TXT_KEY_VICTORY_NAME_ANDES"
ATLANTIC_COAST = "TXT_KEY_VICTORY_NAME_ATLANTIC_COAST"
AMERICAS = "TXT_KEY_VICTORY_NAME_AMERICAS"
ANATOLIA = "TXT_KEY_VICTORY_NAME_ANATOLIA"
ASIA = "TXT_KEY_VICTORY_NAME_ASIA"
BACTRIA = "TXT_KEY_VICTORY_NAME_BACTRIA"
BALKANS = "TXT_KEY_VICTORY_NAME_BALKANS"
BRAZIL = "TXT_KEY_VICTORY_NAME_BRAZIL"
BRITAIN = "TXT_KEY_VICTORY_NAME_BRITAIN"
CARIBBEAN = "TXT_KEY_VICTORY_NAME_CARIBBEAN"
CAUCASUS = "TXT_KEY_VICTORY_NAME_CAUCASUS"
CENTRAL_ASIA = "TXT_KEY_VICTORY_NAME_CENTRAL_ASIA"
CHINA = "TXT_KEY_VICTORY_NAME_CHINA"
CHINA_AND_MANCHURIA = "TXT_KEY_VICTORY_NAME_CHINA_AND_MANCHURIA"
DECCAN = "TXT_KEY_VICTORY_NAME_DECCAN"
DZUNGARIA = "TXT_KEY_VICTORY_NAME_DZUNGARIA"
EASTER_ISLAND = "TXT_KEY_VICTORY_NAME_EASTER_ISLAND"
EASTERN_EUROPE = "TXT_KEY_VICTORY_NAME_EASTERN_EUROPE"
EGYPT = "TXT_KEY_VICTORY_NAME_EGYPT"
EGYPT_COASTAL = "TXT_KEY_VICTORY_NAME_EGYPT_COASTAL"
EUROPE = "TXT_KEY_VICTORY_NAME_EUROPE"
EUROPE_OR_NORTH_AMERICA = "TXT_KEY_VICTORY_NAME_EUROPE_OR_NORTH_AMERICA"
GAUL = "TXT_KEY_VICTORY_NAME_GAUL"
GRAN_COLOMBIA = "TXT_KEY_VICTORY_NAME_GRAN_COLOMBIA"
GUAYANAS = "TXT_KEY_VICTORY_NAME_GUAYANAS"
HAWAII = "TXT_KEY_VICTORY_NAME_HAWAII"
IBERIA = "TXT_KEY_VICTORY_NAME_IBERIA"
INDIA = "TXT_KEY_VICTORY_NAME_INDIA"
THE_MIDDLE_EAST = "TXT_KEY_VICTORY_NAME_THE_MIDDLE_EAST"
INDUSVALLEY = "TXT_KEY_VICTORY_NAME_INDUSVALLEY"
INDOCHINA = "TXT_KEY_VICTORY_NAME_INDOCHINA"
INDONESIA = "TXT_KEY_VICTORY_NAME_INDONESIA"
ITALY = "TXT_KEY_VICTORY_NAME_ITALY"
KOREA = "TXT_KEY_VICTORY_NAME_KOREA"
LEVANT = "TXT_KEY_VICTORY_NAME_LEVANT"
MAGHREB = "TXT_KEY_VICTORY_NAME_MAGHREB"
MANCHURIA = "TXT_KEY_VICTORY_NAME_MANCHURIA"
MARQUESAS = "TXT_KEY_VICTORY_NAME_MARQUESAS"
MEDITERRANEAN = "TXT_KEY_VICTORY_NAME_MEDITERRANEAN"
MESOPOTAMIA = "TXT_KEY_VICTORY_NAME_MESOPOTAMIA"
NEAR_EAST = "TXT_KEY_VICTORY_NAME_NEAR_EAST"
NEW_ZEALAND = "TXT_KEY_VICTORY_NAME_NEW_ZEALAND"
NORTH_AFRICA = "TXT_KEY_VICTORY_NAME_NORTH_AFRICA"
NORTH_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_AMERICA"
NORTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_NORTH_CENTRAL_AMERICA"
NUBIA = "TXT_KEY_VICTORY_NAME_NUBIA"
OCEANIA = "TXT_KEY_VICTORY_NAME_OCEANIA"
PACIFIC_COAST = "TXT_KEY_VICTORY_NAME_PACIFIC_COAST"
PANNONIA = "TXT_KEY_VICTORY_NAME_PANNONIA"
PERSIA = "TXT_KEY_VICTORY_NAME_PERSIA"
PERU = "TXT_KEY_VICTORY_NAME_PERU"
PHILIPPINES = "TXT_KEY_VICTORY_NAME_PHILIPPINES"
PONTIC_STEPPE = "TXT_KEY_VICTORY_NAME_PONTIC_STEPPE"
PUNJAB = "TXT_KEY_VICTORY_NAME_PUNJAB"
RUSSIA = "TXT_KEY_VICTORY_NAME_RUSSIA"
SCANDINAVIA = "TXT_KEY_VICTORY_NAME_SCANDINAVIA"
SIBERIA = "TXT_KEY_VICTORY_NAME_SIBERIA"
SIBERIAN_COAST = "TXT_KEY_VICTORY_NAME_SIBERIAN_COAST"
SOUTH_AFRICA = "TXT_KEY_VICTORY_NAME_SOUTH_AFRICA"
SOUTH_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_AMERICA"
SOUTH_ASIA = "TXT_KEY_VICTORY_NAME_SOUTH_ASIA"
SOUTH_CENTRAL_AMERICA = "TXT_KEY_VICTORY_NAME_SOUTH_CENTRAL_AMERICA"
SRIVIJAYA = "TXT_KEY_VICTORY_NAME_SRIVIJAYA"
SUDAN = "TXT_KEY_VICTORY_NAME_SUDAN"
SYRIA = "TXT_KEY_VICTORY_NAME_SYRIA"
TRANSOXIANA = "TXT_KEY_VICTORY_NAME_TRANSOXIANA"
WEST_AFRICA = "TXT_KEY_VICTORY_NAME_WEST_AFRICA"
GREECE_AND_ANATOLIA = "TXT_KEY_VICTORY_NAME_GREECE_ANATOLIA"
CITIES_SURROUNDING_MOUNTAINS = "TXT_KEY_VICTORY_NAME_CITIES_SURROUNDING_MOUNTAINS"

# area descriptors
ARAB_WORLD = "TXT_KEY_VICTORY_NAME_ARAB_WORLD"
ANDEAN_COAST = "TXT_KEY_VICTORY_NAME_ANDEAN_COAST"
BALTIC_SEA_REGION = "TXT_KEY_VICTORY_NAME_BALTIC_SEA_REGION"
RED_SEA_REGION = "TXT_KEY_VICTORY_NAME_RED_SEA_REGION"
PERSIAN_GULF = "TXT_KEY_VICTORY_NAME_PERSIAN_GULF"
CANADIAN_TERRITORY = "TXT_KEY_VICTORY_NAME_CANADIAN_TERRITORY"
CITIES_IN_CANADA = "TXT_KEY_VICTORY_NAME_CITIES_IN_CANADA"
CITY_IN_CHINA = "TXT_KEY_VICTORY_NAME_CITY_IN_CHINA"
CITY_IN_PERSIA = "TXT_KEY_VICTORY_NAME_CITY_IN_PERSIA"
COLONIAL = "TXT_KEY_VICTORY_NAME_COLONIAL"
INDIAN_TRADE_ROUTE = "TXT_KEY_VICTORY_NAME_INDIAN_TRADE_ROUTE"
MEDITERRANEAN_PORT = "TXT_KEY_VICTORY_NAME_MEDITERRANEAN_PORT"
NILE = "TXT_KEY_VICTORY_NAME_NILE"
WORLD_COASTLINES = "TXT_KEY_VICTORY_NAME_WORLD_COASTLINES"
THE_WORLD = "TXT_KEY_VICTORY_NAME_THE_WORLD"
WEST_AFRICA = "TXT_KEY_VICTORY_NAME_WEST_AFRICA"
SOUTHERN_AFRICA = "TXT_KEY_VICTORY_NAME_SOUTHERN_AFRICA"
AFRICAN_LAKES = "TXT_KEY_VICTORY_NAME_AFRICAN_LAKES"
BANTU_REGIONS = "TXT_KEY_VICTORY_NAME_BANTU_REGIONS"
EAST_AFRICA = "TXT_KEY_VICTORY_NAME_EAST_AFRICA"
MALAYA = "TXT_KEY_VICTORY_NAME_MALAYA"
BORNEO = "TXT_KEY_VICTORY_NAME_BORNEO"

# building descriptors
SHRINES = "TXT_KEY_VICTORY_NAME_SHRINES"
TEMPLES = "TXT_KEY_VICTORY_NAME_TEMPLES"
CHRISTIAN_CATHEDRALS = "TXT_KEY_VICTORY_NAME_CHRISTIAN_CATHEDRALS"
STATE_RELIGION_CATHEDRAL = "TXT_KEY_VICTORY_NAME_STATE_RELIGION_CATHEDRAL"
ORTHODOX_WONDERS = "TXT_KEY_VICTORY_NAME_ORTHODOX_WONDERS"
ORTHODOX_WONDER = "TXT_KEY_VICTORY_NAME_ORTHODOX_WONDER"
CATHOLIC_WONDER = "TXT_KEY_VICTORY_NAME_CATHOLIC_WONDER"
ZOROASTRIAN_WONDER = "TXT_KEY_VICTORY_NAME_ZOROASTRIAN_WONDER"
ISLAMIC_WONDER = "TXT_KEY_VICTORY_NAME_ISLAMIC_WONDER"
ISLAMIC_CATHEDRAL = "TXT_KEY_VICTORY_NAME_ISLAMIC_CATHEDRAL"
ISLAMIC_CATHEDRALS = "TXT_KEY_VICTORY_NAME_ISLAMIC_CATHEDRALS"
CATHEDRALS = "TXT_KEY_VICTORY_NAME_CATHEDRALS"

# resource descriptors
UNIQUE_RESOURCES = "TXT_KEY_VICTORY_NAME_UNIQUE_RESOURCES"
DIFFERENT_HAPPINESS_RESOURCES = "TXT_KEY_VICTORY_NAME_DIFFERENT_HAPPINESS_RESOURCES"
HAPPINESS_RESOURCES = "TXT_KEY_VICTORY_NAME_HAPPINESS_RESOURCES"
TRADING_COMPANY_RESOURCES = "TXT_KEY_VICTORY_NAME_TRADING_COMPANY_RESOURCES"

# unit descriptors
MOUNTED = "TXT_KEY_VICTORY_NAME_MOUNTED"

# routes descriptors
LAND_BASED_TRADE = "TXT_KEY_VICTORY_NAME_LAND_BASED_TRADE"

# civilization descriptors
AFRICAN = "TXT_KEY_VICTORY_NAME_AFRICAN"
NORTH_AFRICAN = "TXT_KEY_VICTORY_NAME_NORTH_AFRICAN"
AFRICAN_CIVS = "TXT_KEY_VICTORY_NAME_AFRICAN_CIVS"
ALL_EUROPEAN = "TXT_KEY_VICTORY_NAME_ALL_EUROPEAN"
ARAB = "TXT_KEY_VICTORY_NAME_ARAB"
CHRISTIAN = "TXT_KEY_VICTORY_NAME_CHRISTIAN"
EUROPEAN = "TXT_KEY_VICTORY_NAME_EUROPEAN"
OLD_WORLD_CIVILIZATION = "TXT_KEY_VICTORY_NAME_OLD_WORLD_CIVILIZATION"
LOCAL = "TXT_KEY_VICTORY_NAME_LOCAL"
OTHER_TURKIC = "TXT_KEY_VICTORY_NAME_OTHER_TURKIC"
OTHER_TURKISH_MONGOL_OR_PERSIAN = "TXT_KEY_VICTORY_NAME_OTHER_TURKISH_MONGOL_OR_PERSIAN"

# separators
OR = "TXT_KEY_OR"

# goal descriptors
FIRST_NORSE_GOAL = "TXT_KEY_VICTORY_GOAL_NORSE_1"
THIRD_AZTEC_GOAL = "TXT_KEY_VICTORY_GOAL_AZTECS_3"

ISLAMIC = "TXT_KEY_VICTORY_NAME_ISLAMIC"




dGoals = {

	iSouthAfrica: (
		All(
			PoweredCitiesCount(5),
			BuildingCount(iAgriculturalFactory, 5),
			by=1910,
		),
		UnitCount(iICBM, 6, by=1980),
		AreaPercent(plots.regions(*lAfrica).named(AFRICA), 80, subject=ALLIES),
	),

	iBoers: (
		TradeMissionCount(start(iNetherlands).named(AMSTERDAM), 4, by=1860),
		All(
			RouteConnection([iRouteRailroad], city(tCape).named(CAPE_TOWN), plots.regions(rSwahiliCoast).named(EAST_AFRICA)),
			CityBuilding(city(tCape).named(CAPE_TOWN), iRailwayStation),
			CityBuilding(city(tPretoria).named(PRETORIA), iRailwayStation),
			by=1900,
		),
		All(
			AveragePopulation(15),
			AreaPopulationPercent(plots.regions(rCape).named(SOUTH_AFRICA), 4),
			by=1930,
		),
	),

	iZulu: (
		All(
			Discover(iGeneralship, by=1800),
			UnitLevelCount(6, 3, by=1880),
			LargerArmyThanPopulationTurns(100, by=1950),
		),
		UnitCount(iArtillery, 2, by=1900),
		BuildingCount((iFactory, 10), (iSewer, 8), (iUniversity, 8), (iLevee, 5), (iPark, 5), by=1980),
	),

	iKatanga: (
		BuildingCount(iChokweSculpture, 1, by=1700),
		CultureCover(plots.region(rCongo), by=1900),
		CityPopulation(start(iKatanga).named(MWIMBELE), 15, by=1940),
	),

	iMadagascar: (
		AllContacted(by=1700),
		All(
			SettledCityCount(plots.regions(*lOceania).named(OCEANIA), 3),
			Control(
				plots.rectangle(tBorneo).named(BORNEO),
			    plots.rectangle(tMalaya).named(MALAYA),
				subject=VASSALS,
			),
			by=1850,
		),
		ControlledResourceCount(different(happiness_resources()).named(DIFFERENT_HAPPINESS_RESOURCES), 10, by=1900),
	),

	iFunj: (
		All(
			BuildingCount((iIslamicCathedral, 1)),
			AreaNoReligion(plots.regions(rNubia, rSahel, rEthiopia, rSwahiliCoast, rMadagascar, rZambezi).named(EAST_AFRICA), iOrthodoxy),
			by=1750,
		),
		RiverPopulationCount(60, by=1900),
		All(
			TechsTraded(10),
			BestTechPlayers(3, subject=ISLAMIC_RELIGIONS),	
			by=1960,
		),
	),
	iAdal: (
		 BuildingCount(wonders(), 4, by=1550),
		 All(
			ResourceCount(different(resources()).named(UNIQUE_RESOURCES), 15),
			TradeRouteCount(15),
			by=1600,
		 ),
		 All(
			FirstDiscover(iSociology),
		 	FirstDefensivePact(),
		 ),
	),
	iBuganda: (
		All(
			BestPopulationCityTurns(city(tMubende).named(MUBENDE), 3),
			FoundedCultureAmount(2000),
			by=1500,
		),
		All(
			PlotCount(plots.regions(rChad, rTana, rTurkana, rNyanza, rMwitanzege, rRweru, rTanganyika, rBangweulu, rRukwa, rMalawi, rMaiNdombe).named(AFRICAN_LAKES), 15),
			RazeCount(2),
			SlaveTradeGold(800),
			by=1820,
		),
		All(
			PopulationCityCount(5, 5, by=1850),
			BuildingCount(religious_buildings(cathedral).named(CATHEDRALS), 4, by=1930),
		),
	),
	iZimbabwe: (
		BuildingCount(iZimbabweBuilding, 1, by=1450),
		PopulationCount(30, by=1750),
		RaidGold(600, by=1770),
	),
	iSomalia: (
		All(
			FirstDiscoverCivs(civs(*lAfricanCivs).named(AFRICAN_CIVS), iExploration),
		),
		All(
			TradeMissionRegion(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 3),
			DiplomaticMissionRegion(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 1),
			TradeMissionRegion(plots.regions(rNorthChina, rSouthChina).named(CHINA), 3),
			DiplomaticMissionRegion(plots.regions(rNorthChina, rSouthChina).named(CHINA), 1),
			by=1600
		),
		All(
			TerrainCount(iCoast, 50),
			SpecialistCount(great_people(), 6),
			by=1800
		),
	),

	iAshanti: (
		All(
			CityCultureLevel(capital().named(CAPITAL), iCultureLevelRefined, by=1800),
			CityCultureLevel(capital().named(CAPITAL), iCultureLevelInfluential, by=1900),
			CityCultureLevel(capital().named(CAPITAL), iCultureLevelLegendary, by=2026),	
		),
		ResourceCount(sum(lHappinessResources).named(HAPPINESS_RESOURCES), 10, by=1900),
		All(
			CompleteEra(iIndustrial),
			LifeExpectancyTurns(60, 100),
			by=1980
		),
	),

	iBenin: (
		All(
			CityBuildingCount(start(iBenin).named(BENIN_CITY), anyBuildings(), 15, by=1400),
			Wonder(iIyanuwo, by=1500),
		),
		All(
			CommerceRegion(plots.region(rGuinea), 3500),
			TradeMissionCount(city(tLisbon).named(LISBON), 1),
			by=1650
	
		),
		All(
			Wonder(iOsunOsogbo),
			BuildingCount(iPaganTemple, 6),
			DefeatedUndiscoveredUnits(10),
			by=1700
		),
																																																													
	),

	iHausa: (
			PopulationCityCount(6, 7, by=1650),
			All(
				AreaNoStateReligion(plots.regions(*lWestAfricaRegions).named(WEST_AFRICA), sum(iOrthodoxy, iCatholicism, iProtestantism).named(CHRISTIAN)),
				VassalCount(2, civs=civs(*lAfricanCivs).named(AFRICA), iStateReligion=iIslam),
				at=1850,
			),
			All(
				Wonder(iHollywood),
				CorporationCount(iOilIndustry, 3),
				TeamRank(5),
				by=1960,
			),
	),

	iKanemBornu: (
			All(
				AcquiredCities(2),
				TerrainCount(iDesert, 15),
				by=1000,
			),
			All(
				TradeGold(5000),
				AllAttitude(AttitudeTypes.ATTITUDE_FRIENDLY, civs=group(iCivGroupNorthAfrica).named(NORTH_AFRICAN)),
				at=1500,
			),
			FirstDiscoverCivs(civs(*lAfricanCivs).named(AFRICAN_CIVS), iFirearms),
	),

	iSonghai: (
		All(
			Wonder(iTombOfAskia),
			UnitLevelCount(4, 5),
			by=1500,
		),
		All(
			Wonder(iGreatAdobeMosque),
			ResourceCount(different(happiness_resources()).named(DIFFERENT_HAPPINESS_RESOURCES), 5),
			by=1580,
		),
		All(
			Wonder(iUniversityOfSankore),
			CitySpecialistCount(wonder(iUniversityOfSankore).named(ITS_CITY), great_people(), 2),
			by=1620,
		),
	),


	iGhana: (
		All(
			ContactCount(3, by=400),
			TradeRouteCount(3, by=650),
		),
		All(
			SlaveTradeGold(500),
			UnitCount(iLancer, 10),
			by=1200,
		),
		All(
			TradeRouteCommerce(3000),
			AreaPercent(plots.regions(*lWestAfricaRegions).named(WEST_AFRICA), 50),
			by=1400,
		),
	),


	iJerusalem: (
		All(
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 10, iStateReligion=sum(iOrthodoxy, iCatholicism, iProtestantism).named(CHRISTIAN)),
			CompleteEra(iMedieval),
			by=1500,
		),
		All(
			CityCulture(city(tJerusalem).named(JERUSALEM), 5000),
			CultureAmountRegion(plots.region(rEgypt), 5000),
			by=1500,
		),
		All(
			AreaNoStateReligion(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), iIslam),
			AreaNoStateReligion(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), iShia),
			by=1600,
		),
	),


	iGeorgia: (
		StateReligionSurpassCount(iOrthodoxy, 2, at=1220),
		GoldenAgeTurns(20, by=1450),
		PopulationCountRegion((plots.all().where(lambda pl: pl.isPeak())).expand(1).named(CITIES_SURROUNDING_MOUNTAINS), 20, at=1490),
	),


	iGokturks: (
		DifferentCities(
			CityCultureLevel(capital().named(CAPITAL), iCultureLevelDeveloping, by=700),
			CityCultureLevel(capital().named(DIFFERENT_CAPITAL), iCultureLevelRefined, by=900),
			CityCultureLevel(capital().named(ANOTHER_CAPITAL), iCultureLevelInfluential, by=1100),
		),
		All(
			PillageCount(20),
			RouteConnection(NamedList(iRouteRoad).named(LAND_BASED_TRADE), plots.regions(rNorthChina, rSouthChina).named(CITY_IN_CHINA), plots.regions(rPersia, rKhorasan).named(CITY_IN_PERSIA)),
			by=900,
		),
		All(
			UnitCount(iLancer, 5),
			BestArmy(by=1100),
		),
	),

	iTunis: (
		CitySpecialistCount(capital().named(CAPITAL), iSpecialistSlave, 10, by=1400),
		AreaPercent(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 15, by=1500),
		PopulationCityCount(15, 3, by=1600),
	),

	iKhazars: (
		All(
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 1, civs=group(iCivGroupEurope).named(EUROPE)),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 1, civs=civs(iChina).named(CHINA)),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 1, civs=group(iCivGroupMiddleEast).named(THE_MIDDLE_EAST)),
			by=970,
		),
		TradeRouteCount(12, by=970),
 		BuildingCount(iJewishCathedral, 1, by=1350),
	),

	iOman: (
		CultureCover(plots.region(rPersianGulf).named(PERSIAN_GULF), by=1400),
		ConqueredCities(3, civs=group(iCivGroupEurope).named(EUROPEAN), outside=plots.regions(*lEurope).named(EUROPE), by=1750),
		TradeRouteCount(35, by=1750),
	),

	iYemen: (
		All(
			AveragePopulation(12),
			CityCount(plots.all().adjacent_region(rRedSea).land().named(RED_SEA_REGION), 2),
			at=1250,
		),
		CultureAmountRegion(plots.region(rArabia), 5000, by=1500),
		All(
			ResourceCount(iCoffee, 4),
			ResourceCount(iIncense, 4),
			ResourceCount(iSpices, 2),
			by=1600,
		),
	),

	iSamanids: (
		All(
			GoldenAges(1),
			GreatGenerals(2),
			by=1050,
		),
		CultureCityCount(500, 5, by=1200),
		ControlTurns(plots.regions(rPersia, rKhorasan).named(PERSIA), 30, by=1300),
	),


	iBuyids: (
		All(
			BestPopulationCity(city(tBabylon).named(BAGHDAD)),
			BestCultureCity(city(tBabylon).named(BAGHDAD)),
			at=1200,
		),
		BuildingCount(religious_buildings(shrine).named(SHRINES), 5, by=1200),
		FirstEnterEraX(iIndustrial),
	),


	iMisr: (
		All(
			CityBuilding(city(tCairo).named(CAIRO), iPalace, iAlAzhar),
			ReligionSpreadCount(iShia, 10),
			by=1150,
		),
		All(
			AreaPopulationCount(plots.rectangle(tNile).without(lNileExceptions).named(NILE), 40),
			TradeRouteCommerce(3000),
			BuildingCount(religious_buildings(shrine).named(SHRINES), 3),
			by=1250
		),
		All(
			ReligionSpreadPercent(iIslam, 20),
			UnitCount(iHandCannon, 10),
			TradeGold(10000),
			at=1550,
		),
	),


	iArmenia: (
			All(
				BuildingCount(
					(sum(*lZoroastrianWonders).named(ZOROASTRIAN_WONDER), 1),
					(iZoroastrianCathedral, 1),
					by=250,
				),
				BuildingCount(
					(sum(*lOrthodoxWonders).named(ORTHODOX_WONDERS), 3),
					(iOrthodoxCathedral, 1), 
					by=1200,
				),
			),
			CityDifferentGreatPeopleCount(start(iArmenia).named(ARTASHAT), 5, by=600),
			All(
				CityBuildingCount(start(iArmenia).named(ARTASHAT), anyBuildings(), 20, by=600),
				CityCultureLevel(start(iArmenia).named(ARTASHAT), iCultureLevelLegendary, at=1650),
			),
	),


	iParthia: (
			Control(
			plots.region(rLevant).named(LEVANT),
			plots.region(rMesopotamia),
			plots.region(rPersia),
			at=200,
			),
			EraFirstDiscover((iMedieval, 8)),
			Control(
			plots.region(rArabia),
			plots.region(rAnatolia),
			plots.region(rEgypt),
			plots.regions(rTransoxiana, rKhorasan).named(BACTRIA),
			by=600,
			),
	),

	iScythia: (
			DefeatedUnits(civs(iPersia), 15, by=-350),
			LandPercent(3, by=-350),
			CultureCover(plots.all().region(rPonticSteppe).land().named(PONTIC_STEPPE), by=-300),
	),

	iNumidia: (
			All(
				CityCount(plots.region(rIberia), 1),
				CityCount(plots.region(rItaly), 1),
				CityCount(plots.region(rMaghreb).named(AFRICA), 4),
			at=200,
			),
			AveragePopulation(8, at=200),
			TradeMissionCount(city(tRome).named(ROME), 2, by=300),
	),

	iHuns: (
			CityCount(
			(plots.region(rItaly), 2),
			(plots.region(rFrance).named(GAUL), 2),
			by=450,
			),
			RazeCount(3, by=500),
			GoldAmount(3000, by=500),
	),
	
	iGoths: (
			FirstDiscover(iFeudalism),
			All(
				Control(plots.region(rItaly), by=500),
				RaidGold(1000, by=600),
		  	 ),
			All(
				Control(plots.region(rIberia), by=500),
				CultureAmountRegion(plots.region(rIberia), 3000, by=1000),
		  	 ),
	),


	iVandals: (
			PillageCount(20, by=500),
			Control(plots.region(rMaghreb).named(MAGHREB), by=500),
			CityPopulation(city(tCarthage).named(CARTHAGE), 15, by=750),
	),


	iGermania: (
			 DefeatedUnits(civs(iRome), 10, by=150),
			 CityCount(plots.region(rBritain), 2, by=500),
			 BuildingCount(
			 	(sum(*lCatholicWonders).named(CATHOLIC_WONDER), 1), 
				by=1100
			),
	),
	iMycenae: (
			All(
				CityCount(plots.regions(rGreece, rAnatolia).named(GREECE_AND_ANATOLIA), 4),
				NoCityLost(),
				by=-800,
		  	 ),
			 BuildingCount(wonders(), 4, by=-700),
			 CitySpecialistCount(capital().named(CAPITAL), great_people(), 4, by=-700),
	),
	iSparta: (
			 All(
			 CityCount(plots.regions(rGreece, rAnatolia).named(GREECE_AND_ANATOLIA), 4),
			 CityCount(plots.region(rItaly), 1),
			 at=-400,
			 ),
			 UnitLevelCount(5, 10, by=-300),
			 BuildingCount((iBarracks, 5), (iArena, 5), (iPaganTemple, 5), by=-300),
	),
	iMacedon: (
			Control(
			plots.region(rAnatolia),
			plots.region(rLevant).named(LEVANT),
			plots.region(rMesopotamia),
			plots.region(rPersia),
			plots.region(rEgypt),
			at=-300,
			),
			All(
				Control(
					plots.regions(rTransoxiana, rKhorasan).named(BACTRIA),
					plots.regions(rHinduKush, rPunjab, rSindh).named(INDUSVALLEY),
				),
				CitySpecialistCount(city(tBabylon).named(SELEUCIA), great_people(), 5),
				by=-250,	
			),
			Wonders(iGreatLibrary, iGreatLighthouse, by=-200),	
	),


	iElam: (
		ContactCount(4, by=-1825),
		All(
			TradeRouteCommerce(150, by=-1000),
			TradeRouteCommerce(400, by=-800),
		),
		RazeCount(2, by=-800),
	),


	iSumeria: (
		CompleteEra(iAncient, by=-600),
		All(
		CityCount(plots.region(rMesopotamia).named(MESOPOTAMIA), 3, at=-2100),
		CityCount(plots.region(rMesopotamia).named(MESOPOTAMIA), 3, at=-1000),
		CityCount(plots.region(rMesopotamia).named(MESOPOTAMIA), 3, at=-320),
		),
		All(
			AveragePopulation(3, at=-2100),
			AveragePopulation(5, at=-1000),
			AveragePopulation(10, at=-320),
		),
	),

	iEgypt: (
		All(
			Wonders(iGreatSphinx, iPyramids),
			CultureAmount(500),
			by=-1200,
		),
		Control(
			plots.region(rNubia).named(NUBIA),
			plots.region(rLevant).named(LEVANT),
			at=-600,
		),
		All(
			Wonders(iGreatLibrary, iGreatLighthouse),
			CultureAmount(5000),
			by=-300,
		),
	),
	iBabylonia: (
		EraFirstDiscover((iClassical, 8)),
		CityBuildingCount(city(tBabylon).named(BABYLON), wonders(), 3, by=-600),
		All(
			CityPopulation(city(tBabylon).named(BABYLON), 12),
			CityCultureLevel(city(tBabylon).named(BABYLON), iCultureLevelRefined),
			by=-600,
		),
	),
	iHarappa: (
		TradeConnection(by=-1800),
		BuildingCount((iReservoir, 3), (iGranary, 2), (iWeaver, 2), by=-1500),
		PopulationCount(45, by=-800),
	),

	iMinoa: (
		All(
			PopulationInAreaPercent(plots.regions(*lEuropeProper).named(EUROPE), 60, at=-1300),
			PopulationInAreaPercent(plots.regions(*lEuropeProper).named(EUROPE), 60, at=-540),
		),
		OpenBorderCount(5, by=-1000),
		AreaPercent(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 20, by=-550),
	),


	iAssyria: (
		All(
			Control(
			plots.region(rMesopotamia).named(MESOPOTAMIA),
			),
			UnitLevelCount(3, 3),
			by=-1000,
		),
		Control(
			plots.region(rMesopotamia).named(MESOPOTAMIA),
			plots.region(rLevant).named(LEVANT),
			plots.region(rEgypt).named(EGYPT),
			by=-650,
		),
		CitySpecialistCount(capital().named(CAPITAL), great_people(), 3, by=-630),
	),
	iChina: (
		BuildingCount((iConfucianCathedral, 4), (iTaoistCathedral, 4), by=900),
		FirstDiscover(iCompass, iPaper, iGunpowder, iPrinting),
		GoldenAges(4, by=1800),
	),
	iHittites: (
		ResourceCount(sum(iCopper, iIron), 4, by=-900),
		Production(1200, by=-800),
		FirstTribute(),
	),
	iNubia: (
		All(
			GoldAmount(400),
			CultureAmount(300),
			ResourceCount(sum(lHappinessResources).named(HAPPINESS_RESOURCES), 5),
			by=-900,
		),
		HappyCityPopulation(40, by=-500),
		All(
			TradeNetworkReligionCityCount(iOrthodoxy, 12, by=500),
			TradeNetworkReligionCityCount(iOrthodoxy, 24, by=1000),
		),
	),
	iGreece: (
		Wonders(iParthenon, iColossus, iTempleOfArtemis, by=-400),
		ControlledResourceCount(
			(improvement_resources(iFishingBoats, iHarvestBoats), 6),
			by=-400
		),
		CompleteEra(iClassical, by=200),
	),
	iIndia: (
		BuildingCount((iHinduShrine, 1), (iBuddhistShrine, 1), at=-250),
		BuildingCount(religious_buildings(temple).named(TEMPLES), 30, by=600),
		PopulationPercent(20, at=1200),
	),
	iPhoenicia: (
		All(
			ControlledResourceCount(iDye, 5),
			TradeRouteCount(15),
			RevealedPercent(plots.all().sea().adjacent_regions(*lAfricanCoastRegions).named(AFRICAN_COAST), 25),
			by=-300
		),
		All(
			CityBuilding(city(tCarthage).named(CARTHAGE), iPalace, iGreatCothon, by=-400),
			Control(
				plots.rectangle(tPhoenicianItaly).without(lPhoenicianItalyExceptions).named(ITALY),
				plots.region(rIberia),
				at=-150
			),
		),
		All(
		CultureAmountRegion(plots.region(rLevant).named(LEVANT), 300, by=-600),
		CultureAmountRegion(plots.region(rMaghreb).named(AFRICA), 1500, by=-300),
		CultureAmountRegion(plots.rectangle(tPhoenicianItaly).without(lPhoenicianItalyExceptions).named(ITALY), 3000, by=1),
		),
	),

	iJudah: (
		All(
			BuildingCount(iJewishShrine, 1, at=-500),
			BuildingCount(iOrthodoxShrine, 1, at=350),
		),
		BuildingCount((iJewishCathedral, 1), by=200),
		FoundedCultureAmount(10000, by=400),
		
	),

	iPolynesia: (
		Settle(
			plots.rectangle(tHawaii).named(HAWAII),
			(plots.rectangle(tNewZealandEast) + plots.rectangle(tNewZealandWest)).named(NEW_ZEALAND),
			plots.rectangle(tMarquesas).named(MARQUESAS),
			plots.rectangle(tEasterIsland).named(EASTER_ISLAND),
			required=2,
			by=600,
		),
		Settle(
			plots.rectangle(tHawaii).named(HAWAII),
			(plots.rectangle(tNewZealandEast) + plots.rectangle(tNewZealandWest)).named(NEW_ZEALAND),
			plots.rectangle(tMarquesas).named(MARQUESAS),
			plots.rectangle(tEasterIsland).named(EASTER_ISLAND),
			by=800,
		),
		Wonder(iMoaiStatues, by=1000),
	),
	iPersia: (
		RouteConnection([iRouteRoad], city(tPersepolis).named(PERSEPOLIS), plots.region(rAnatolia), by=-500),
		BuildingCount(wonders(), 12, by=-300),
		PopulationPercent(25, at=-300),
	),
	iCelts: (
		ConqueredCities(2, bControl=False, by=-400),
		All(
			CityCount(plots.region(rFrance).named(GAUL), 3),
			Settle(
				plots.region(rIreland),
				plots.region(rBritain),
				plots.region(rIberia),
				plots.region(rCentralEurope).named(PANNONIA),
			),
			by=-400,
		),
		Control(
			plots.region(rGreece),
			at=-275,
		),
	),
	iRome: (
		BuildingCount((iBarracks, 8), (iAqueduct, 6), (iArena, 5), (iForum, 4), by=-50),
		CityCount(
			(plots.region(rIberia), 2),
			(plots.region(rFrance).named(GAUL), 3),
			(plots.region(rBritain), 1),
			(plots.region(rMaghreb).named(AFRICA), 3),
			(plots.regions(rGreece, rAnatolia).named(ANATOLIA), 4),
			(plots.region(rEgypt).named(EGYPT), 3),
			(plots.region(rLevant).named(LEVANT), 2),
			at=100,
		),
		All(
			FirstDiscover(iArchitecture, iPolitics, iScholarship, iMachinery, iCivilService),
			TeamRank(1, at=476),
		),
	),
	iMaya: (
		All(
			Discover(iCalendar, by=-250),
			Discover(iArithmetics, by=-150),
		),
		Wonder(iTempleOfKukulkan, by=400),
		ContactBeforeRevealed(civs(*lBioOldWorld).named(OLD_WORLD_CIVILIZATION), plots.regions(*lAmerica).named(AMERICAS)),
	),
	iDravidia: (
		All(
			CultureAmount(10000, at=600),
			GoldAmount(7500, at=600),
			TradeGold(10000, by=1200),
		),
		Control(
			plots.regions(rDravida, rDeccan, rRajputana).named(DECCAN),
			plots.region(rBengal),
			plots.rectangle(tSrivijaya).named(SRIVIJAYA),
			plots.birth(iBurma),
			subject=VASSALS,
			at=1000,
		),
		PopulationCity(25, by=1500),
	),
	iEthiopia: (
		All(
			Discover(iMedicine),
			ResourceCount(iIncense, 5),
			by=300,
		),
		All(
			StateReligion(iOrthodoxy, mode=STATELESS),
			SpecialistCount(iSpecialistGreatProphet, 5),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8, iStateReligion=sum(iOrthodoxy, iCatholicism).named(CHRISTIAN)),
			by=1200,
		),
		All(
			LiberatedCities(plots.regions(*lAfrica).named(AFRICA), group(iCivGroupAfrica).named(AFRICAN), 12),
			AllAttitude(AttitudeTypes.ATTITUDE_PLEASED, civs=civs(*lAfricanCivs).named(AFRICAN)),
			at=1930,
		),
	),
	iToltecs: (
		All(
			CityPopulation(city(tTenochtitlan).named(TOLLAN), 12),
			CityCulture(city(tTenochtitlan).named(TOLLAN), 400),
			by=200,
		),
		GoldenAges(1, by=550),
		All(
			PopulationCount(50),
			CultureAmount(5000),
			by=1000,
		),
	),
	iKushans: (
		Constructed(
			(iPaganTemple, 3),
			(iBuddhistTemple, 6),
			(iHinduTemple, 3),
			by=250,
		),
		All(
			CorporationCount(iSilkRoute, 8),
			ReligionSpreadCount(iBuddhism, 12),
			by=450,
		),
		All(
			GoldAmount(6000),
			CultureAmount(6000),
			by=600,
		),
	),
	iKorea: (
		BuildingCount((iBuddhistCathedral, 1), (iConfucianCathedral, 1), by=800),
		FirstDiscover(iEducation, iPrinting, iFirearms, iStatecraft),
		SunkShips(20, by=1700),
	),
	iKhmer: (
		All(
			CultureAmount(3000, by=600),
			CultureAmount(20000, by=1400),
		),
		All(
			BuildingCount((iHinduMonastery, 5), (iBuddhistMonastery, 5)),
			Wonder(iWatPreahPisnulok),
			at=1150,
		),
		All(
			AveragePopulation(12, at=1000),
			AveragePopulation(15, by=1400),
			BestPopulationCity(city(tAngkor).named(ANGKOR), at=1400),
		),
	),
	iMali: (
		All(
			Wonder(iUniversityOfSankore, by=1400),
			TechsTraded(8, by=1500),
		),
		TradeMissionCount(holy_city(), 1, by=1450),
		GoldAmount(10000, by=1650),
	),
	iByzantium: (
		All(
			AverageCultureAmount(300),
			GoldAmount(6000),
			TradeRouteCount(40),
			by=1000
		),
		All(
			BestPopulationCity(city(tConstantinople).named(CONSTANTINOPLE)),
			BestCultureCity(city(tConstantinople).named(CONSTANTINOPLE)),
			at=1200,
		),
		Control(
			plots.region(rGreece),
			plots.region(rBalkans).named(BALKANS),
			plots.region(rAnatolia),
			plots.region(rCaucasus).named(CAUCASUS),
			plots.region(rLevant).named(LEVANT),
			plots.region(rEgypt),
			plots.region(rMaghreb).named(AFRICA),
			plots.rectangle(tAndalusia).named(ANDALUSIA),
			plots.region(rItaly),
			at=1450,
		),
	),
	iFrance: (
		CityCultureLevel(start(iFrance).named(PARIS), iCultureLevelLegendary, at=1700),
		All(
			AreaPercent(plots.regions(*lEuropeProper).named(EUROPE), 40, subject=VASSALS),
			AreaPercent(plots.regions(*[iRegion for iRegion in lNorthAmerica if iRegion != rAmericanArctic]).named(NORTH_AMERICA), 40, subject=VASSALS),
			at=1800,
		),
		CityBuilding(start(iFrance).named(PARIS), iNotreDame, iVersailles, iLouvre, iEiffelTower, iMetropolitain, by=1900),
	),
	iMalays: (
		All(
			TradeRouteCommerce(1600, by=850),
			TradeRouteCommerce(8000, by=1200),
		),
		ResourceCount(different(happiness_resources()).named(DIFFERENT_HAPPINESS_RESOURCES), 12, by=1300),
		CityBuilding(area_city(tMalaya).named(MALAYAN_CITY), iHinduCathedral, iBuddhistCathedral, iIslamicCathedral, by=1450),
	),
	iJapan: (
		FoundedCultureAmount(30000, by=1600),
		Control(
			plots.region(rKorea),
			plots.regions(rManchuria, rAmur).named(MANCHURIA),
			plots.regions(rNorthChina, rSouthChina).named(CHINA),
			plots.region(rIndochina),
			plots.region(rIndonesia),
			plots.region(rPhilippines).named(PHILIPPINES),
			subject=VASSALS,
			at=1940,
		),
		EraFirstDiscover((iGlobal, 8), (iDigital, 8)),
	),
	iNorse: (
		Control(required=2, at=1000, desc_key=FIRST_NORSE_GOAL, *lNorseTargets),
		FirstSettle(plots.regions(*lAmerica).named(AMERICAS), allowed=dCivGroups[iCivGroupAmerica], by=1000),
		RaidGold(3000, by=1250),
	),
	iTurks: (
		Control(
				plots.regions(rLevant, rMesopotamia).named(MESOPOTAMIA),
				plots.region(rTransoxiana),
				plots.regions(rPersia, rKhorasan).named(PERSIA),
				plots.region(rAnatolia),
				by=1150,
			),
		Constructed(
			(iNationalCollege, 1),
			(iAcademy, 2),
			by=1250,
		),
		All(
			AllowNone(
				civs(iOttomans, iTimurids, iGokturks, iGhorids).named(OTHER_TURKIC),
				plots.all().named(THE_WORLD),
			),
			PopulationPercent(15),
			by=1450,
		),
	),
	iMorocco: (
 		All(
 			Control(plots.region(rMaghreb).named(MAGHREB)),
 			ConqueredCities(3, inside=plots.region(rIberia).named(IBERIA)),
 			ConqueredCities(2, inside=plots.rectangle(tWestAfrica).named(WEST_AFRICA)),
 			by=1350,
 		),
		All(
			Wonder(iAitBenhaddou, by=1300),	
			BuildingCount(wonders(), 5, by=1500),
		),
		All(
 			DefeatedUnits(civs(iSpain, iPortugal, iFrance), 30, by=1900),
 			ReligionSpreadPercent(iIslam, 30, by=1900),
		),
 	),
	iArabia: (
		Control(
				plots.region(rArabia),
				plots.region(rEgypt).named(EGYPT),
				plots.regions(rLevant, rMesopotamia).named(MESOPOTAMIA),
				plots.region(rMaghreb).named(MAGHREB),
				plots.regions(rPersia, rKhorasan).named(PERSIA),
				plots.rectangle(tAndalusia).named(ANDALUSIA),
				at=700,
			),
		CompleteEra(iMedieval, by=1350),
		All(
			ControlTurns(plots.region(rArabia), 150),
			ControlTurns(plots.region(rEgypt).named(EGYPT), 150),
			ControlTurns(plots.regions(rLevant, rMesopotamia).named(MESOPOTAMIA), 150),
			ControlTurns(plots.region(rMaghreb).named(MAGHREB), 100),
			ControlTurns(plots.regions(rPersia, rKhorasan).named(PERSIA), 100),
			ControlTurns(plots.region(rIberia).named(IBERIA), 50),
			by=1800,
		),	
	),
	iTibet: (
		AcquiredCities(8, by=1000),
		ReligionSpreadPopulationCount(iBuddhism, 60, by=1400),
		CitySpecialistCount(start(iTibet).named(LHASA), iSpecialistGreatProphet, 8, by=1700),
	),
	iMoors: (
		All(
 			CityCount(plots.region(rMaghreb).named(MAGHREB), 3),
 			Control(
 				plots.region(rIberia).named(IBERIA),
 				subject=VASSALS,
 				by=909,
 			),
		),
		All(
			Wonders(iMezquita, iAlhambra),
			CitySpecialistCount(start(iMoors).named(CORDOBA), sum(iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatEngineer), 6),
			by=1350,
		),
		All(
			FirstSettle(plots.regions(*lAmerica).named(AMERICAS), allowed=dCivGroups[iCivGroupAmerica]),
			RevealedPercent(plots.all().sea().where(lambda p: p.getTerrainType() in [iCoast, iArcticCoast]).named(WORLD_COASTLINES), 55),
			PiracyGold(1500),
			by=1550,
		),
	),
	iJava: (
		Wonders(iPrambanan, iBorobudur, by=1100),
		HappyCityPopulation(75, by=1350),
		BuildingCount(iIslamicCathedral, 3, by=1500),
	),
	iSpain: (
		FirstSettle(plots.regions(*lAmerica).named(AMERICAS), allowed=dCivGroups[iCivGroupAmerica]),
		ControlledResourceCount(sum(iSilver, iGold), 15, subject=VASSALS, by=1650),
		All(
			ReligionSpreadPercent(iCatholicism, 30),
			AreaNoStateReligion(plots.regions(*lEuropeProper).named(EUROPE), iProtestantism),
			at=1650,
		),
	),
	iEngland: (
		All(
			CityCount(
				(plots.regions(*lNorthAmerica).named(NORTH_AMERICA), 8),
				(plots.regions(*(lSouthAmerica + lCentralAmerica)).named(SOUTH_CENTRAL_AMERICA), 4),
				(plots.regions(*lAfrica).named(AFRICA), 5),
			),
			UnitCombatLevelCount(UnitCombatTypes.UNITCOMBAT_NAVAL, 3, 25),
			by=1770,
		),
		All(
			CityCount(
				(plots.regions(*lAsia).named(ASIA), 12),
				(plots.regions(*lAfrica).named(AFRICA), 10),
			),
			SettledCityCount(plots.regions(*lOceania).named(OCEANIA), 6),
			RouteConnection([iRouteRailroad], plots.regions(rEgypt, rMaghreb).coastal().named(NORTH_AFRICA), plots.regions(rCape).named(SOUTH_AFRICA)),
			by=1880,
		),
		All(
			BuildingCount((iFactory, 20), (iAgriculturalFactory, 15), by=1850),
			ResourceCount(iFertilizer, 5, by=1850),
			EraFirstDiscover((iRenaissance, 8), (iIndustrial, 8)),
		)
	),
	iHolyRome: (
		All(
			BuildingCount(iCatholicShrine, 1, at=1000),
			BuildingCount(iOrthodoxShrine, 1, at=1200),
			BuildingCount(iProtestantShrine, 1, at=1500),
		),
		VassalCount(3, civs=group(iCivGroupEurope).named(EUROPE), iStateReligion=iCatholicism, by=1650),
		All(
			CitySpecialistCount(city(tVienna).named(VIENNA), sum(iSpecialistGreatArtist, iSpecialistGreatStatesman), 10),
			AttitudeCount(AttitudeTypes.ATTITUDE_PLEASED, 8, civs=group(iCivGroupEurope).named(EUROPE), bIndependent=True),
			at=1806,
		),
	),
	iBurma: (
		GoldAmount(3000, by=1150),
		GoldenAges(3, by=1600),
		All(
			Control(plots.region(rIndochina), at=1580),
			Control(plots.region(rIndochina), at=1760),
		),
	),
	iRus: (
		ReligionPopulationCount(iOrthodoxy, 40, by=1200),
		DefeatedUnits(civs(iBarbarian, iMongols), 25, by=1280),
		All(
			ImprovementCount((iCamp, 8), (iQuarry, 3)),
			TradeRouteCount(25),
			by=1400,
		),
	),
	iVietnam: (
		GreatPeople(iGreatGeneral, 2, by=1450),
		All(
			BuildingCount(iConfucianCathedral, 1),
			BuildingCount(iSchool, 4),
			BuildingCount(iConfucianMonastery, 4),
			by=1600,
		),
		CultureLevelCityCount(iCultureLevelInfluential, 3, by=1650),
	),
	iSwahili: (
		All(
			ImportCount(sum(lHappinessResources).named(HAPPINESS_RESOURCES), 100, by=1250),
			TradeRouteCount(25, by=1500),
		),
		RevealedPercent(plots.all().sea().where(lambda p: p.getTerrainType() in [iCoast, iArcticCoast]).named(WORLD_COASTLINES), 35, by=1400),
		Control(
 			plots.region(rCape),
			plots.birth(iOman),
 			plots.region(rEthiopia),
			plots.region(rHornOfAfrica),
			plots.region(rMadagascar),
			plots.region(rGreatLakes),
			required=3,
 			by=1500,
 		),
	),
	iPoland: (
		PopulationCityCount(12, 3, by=1400),
		FirstDiscover(iCivilLiberties),
		BuildingCount(sum(iOrthodoxCathedral, iCatholicCathedral, iProtestantCathedral).named(CHRISTIAN_CATHEDRALS), 5, by=1600),
	),
	iPortugal: (
		WaterAreaPercent(plots.regions(*lIndianTradeRegions).expand(1).regions(rAtlanticOcean, rIndianOcean, rArabianSea).named(INDIAN_TRADE_ROUTE), 35, by=1550),
		All(
			AreaBlockadeGold(plots.regions(*lAsia).named(ASIA), 500),
			AreaReligionSpreadCount(plots.regions(*lAsia).named(ASIA), iCatholicism, 8),
			by=1650,
		),
		All(
			ResourceCount(sum(lColonialResources).named(TRADING_COMPANY_RESOURCES), 16),
			TradeRouteCommerce(10000),
			by=1700,
		),
	),
	iInca: (
		All(
			BuildingCount(iTambo, 7),
			Route(plots.region(rAndes).coastal().passable().without(lAndeanRoadExceptions).named(ANDEAN_COAST), [iRouteRoad]),
			by=1550,
		),
		GoldAmount(2500, by=1550),
		PopulationInAreaPercent(plots.regions(*lSouthAmerica).named(SOUTH_AMERICA), 90, at=1775),
	),
	iItaly: (
		Wonders(iSanMarcoBasilica, iSistineChapel, iSantaMariaDelFiore, by=1500),
		CultureLevelCityCount(iCultureLevelInfluential, 4, by=1600),
		AreaPercent(plots.all().adjacent_region(rMediterraneanSea).named(MEDITERRANEAN), 65, by=1930),
	),
	iMongols: (
		Control(plots.regions(rNorthChina, rSouthChina).named(CHINA), at=1350),
		All(
			SackCount(20),
			LandPercent(16),
			by=1450,
		),
		All(
			LandTradeRouteCount(100),
			GreatPeople(iGreatStatesman, 4),
			by=1500,
		),
	),
	iAztecs: (
		BestPopulationCity(start(iAztecs).named(TENOCHTITLAN), at=1520),
		SacrificeGoldenAges(16, by=1650),
		Control(required=1, by=1750, desc_key=THIRD_AZTEC_GOAL, *lAztecTargets)
	),
	iGhorids: (
		All(
			BuildingCount(iIslamicCathedral, 3),
			SpecialistCount(iSpecialistSlave, 12),
			by=1200,
		),	
		All(
			AreaNoReligion(plots.regions(*lIndia).named(INDIA), iHinduism),	
			AreaNoReligion(plots.regions(*lIndia).named(INDIA), iBuddhism),
        	by=1400,
		),
		AllowNone(
			civs(iTurks, iTimurids, iMongols, iParthia, iPersia, iBuyids, iSamanids).named(OTHER_TURKISH_MONGOL_OR_PERSIAN),
			plots.regions(*lIndia).named(INDIA),
			at=1500,
		),	
	),
	iTimurids: (
		All(
			LandPercent(5),
			PopulationPercent(10),
			by=1500
		),
		Wonders(iRedFort, iShalimarGardens, iTajMahal, by=1660),
		CultureAmount(50000, by=1750),
	),
	iThailand: (
		OpenBorderCount(10, at=1650),
		BestPopulationCity(start(iThailand).named(AYUTTHAYA), at=1700),
		AllowOnly(plots.regions(rDravida, rDeccan, rBengal, rIndochina, rIndonesia).named(SOUTH_ASIA), civs(*lSouthAsianCivs).named(LOCAL), at=1900),
	),
	iSweden: (
		StateReligionCount(group(iCivGroupEurope).named(EUROPEAN), iProtestantism, 6, by=1650),
		CultureCover(plots.all().adjacent_region(rBalticSea).land().named(BALTIC_SEA_REGION), by=1700),
		HappiestTurns(50, by=1980),
	),
	iTatars: (
		All(
			Control(plots.regions(rRuthenia, rRussia, rVolga, rEuropeanArctic).named(RUSSIA), subject=VASSALS),
			DespoilmentGold(400),
			by=1500,
		),
		All(
			Control(
				plots.regions(rUrals, rSiberia).named(SIBERIA),
				plots.regions(rCentralAsianSteppe, rTransoxiana).named(CENTRAL_ASIA),
			),
			UnitCombatLevelCount(sum(UnitCombatTypes.UNITCOMBAT_LIGHT_CAVALRY, UnitCombatTypes.UNITCOMBAT_HEAVY_CAVALRY).named(MOUNTED), 4, 20),
			by=1550,
		),
		All(
			TributeGold(500),
			DespoilmentGold(2500),
			by=1780,
		),
	),
	iRussia: (
		All(
			BuildingCount(iOrthodoxCathedral, 2, by=1500),
			BuildingCount(sum(lOrthodoxWonders).named(ORTHODOX_WONDERS), 3, by=1600),
		),
		All(
			SettledCities(12, area=plots.regions(rUrals, rSiberia, rCentralAsianSteppe, rAmur).named(SIBERIA), by=1700),
			RouteConnection([iRouteRailroad], plots.capitals(iRussia).named(MOSCOW), plots.regions(rSiberia, rAmur).adjacent_regions(rSeaOfJapan, rSeaOfOkhotsk, rBeringSea).named(SIBERIAN_COAST), by=1920),
		),
		All(
			Communist(),
			AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5, bCommunist=True),
			UnitCount((iICBM, 30), (iSatellite, 30)),
			by=1970,
		),
	),
	iOttomans: (
		CityBuildingCount(capital().named(CAPITAL), wonders(), 4, at=1550),
		All(
			Control(
				plots.region(rAnatolia),
				plots.region(rCaucasus).named(CAUCASUS),
				plots.region(rPonticSteppe).named(PONTIC_STEPPE),
				plots.region(rLevant).named(LEVANT),
				plots.region(rMesopotamia),
				plots.region(rArabia),
				plots.region(rEgypt),
				plots.region(rMaghreb).named(MAGHREB),
				plots.region(rGreece),
				plots.region(rBalkans).named(BALKANS),
			),
			CityCount(plots.region(rCentralEurope), 2),
			by=1700,
		),
		SpecialistCount(sum(iSpecialistGreatGeneral, iSpecialistGreatArtist, iSpecialistGreatStatesman), 12, by=1800),
	),
	iCongo: (
		ReligiousVotePercent(20, by=1750),
		SlaveTradeGold(1200, by=1500),
		EnterEraBefore(iIndustrial, iGlobal),
	),
	iIran: (
		OpenBorderCount(10, civs=group(iCivGroupEurope).named(EUROPEAN), by=1650),
		Control(
			plots.region(rMesopotamia).named(MESOPOTAMIA),
			plots.region(rTransoxiana).named(TRANSOXIANA),
			plots.region(rPunjab).named(PUNJAB),
			at=1750,
		),
		CultureCity(20000, at=1800),
	),
	iNetherlands: (
		CitySpecialistCount(start(iNetherlands).named(AMSTERDAM), iSpecialistGreatMerchant, 4, at=1745),
		ConqueredCities(4, civs=group(iCivGroupEurope).named(EUROPEAN), outside=plots.regions(*lEurope).named(EUROPE), by=1745),
		ResourceCount(iSpices, 10, by=1775),
	),
	iManchuria: (
		Control(
			plots.region(rMongolia),
			plots.rectangle(tDzungaria).without(lDzungariaExceptions).named(DZUNGARIA),
			plots.region(rTibet),
			plots.birth(iBurma),
			plots.birth(iVietnam),
			plots.region(rKorea),
			subject=VASSALS,
			by=1750,
		),
		All(
			GoldAmount(25000),
			CultureAmount(50000),
			AreaPopulationPercent(plots.regions(rSouthChina, rNorthChina, rManchuria).named(CHINA_AND_MANCHURIA), 12),
			by=1850,
		),
		BestTechPlayer(at=1900),
	),
	iGermany: (
		CitySpecialistCount(start(iGermany).named(BERLIN), great_people(), 9, at=1900),
		Control(
			plots.region(rItaly),
			plots.region(rCentralEurope),
			plots.region(rFrance),
			plots.region(rBritain),
			plots.rectangle(tScandinavia).without(lScandinaviaExceptions).named(SCANDINAVIA),
			plots.regions(rPoland, rBaltics, rRuthenia, rRussia).named(EASTERN_EUROPE),
			at=1940,
		),
		EraFirstDiscover((iIndustrial, 8), (iGlobal, 8)),
	),
	iSaudis: (
		AllowOnly(plots.regions(rMaghreb, rEgypt, rNubia, rLevant, rMesopotamia, rArabia).named(ARAB_WORLD), civs(*lArabCivs).named(ARAB), at=1920),
		GreatPeople(iGreatProphet, 7, by=1930),
		All(
			ResourceCount(iOil, 12, subject=ALLIES),
			CorporationCount(iOilIndustry, 4),
			GoldAmount(25000),
			by=1970,
		),
	),
	iAmerica: (
		ControlledResourceCount(
			(improvement_resources(iFarm, iPasture), 20),
			(improvement_resources(iPlantation, iOrchard), 15),
			(improvement_resources(iMine, iQuarry), 35),
			subject=VASSALS,
			by=1880,
		),
		Wonders(iStatueOfLiberty, iBrooklynBridge, iEmpireStateBuilding, iGoldenGateBridge, iPentagon, iUnitedNations, by=1950),
		All(
			CommercePercent(75, subject=ALLIES),
			PowerPercent(75, subject=ALLIES),
			by=1990,
		),
	),
	iArgentina: (
		GoldenAges(2, by=1930),
		CityCultureLevel(start(iArgentina).named(BUENOS_AIRES), iCultureLevelLegendary, by=1960),
		GoldenAges(6, by=2000),
	),
	iMexico: (
		BuildingCount(state_religion_building(cathedral).named(STATE_RELIGION_CATHEDRAL), 3, by=1880),
		GreatPeople(iGreatGeneral, 3, by=1940),
		BestPopulationCity(start(iMexico).named(MEXICO_CITY), at=1960),
	),
	iColombia: (
		Control(
			plots.region(rNewGranada).named(GRAN_COLOMBIA),
			plots.region(rCentralAmerica),
			plots.region(rAndes).named(ANDES),
			at=1870,
		),
		Control(
			plots.regions(*lSouthAmerica).named(SOUTH_AMERICA),
			subject=ALLIES,
			at=1920,
		),
		ResourceTradeGold(3000, by=1950),
	),
	iBrazil: (
		ImprovementCount((iSlavePlantation, 12), (iPasture, 4), at=1880),
		Wonders(iWembley, iCristoRedentor, iItaipuDam),
		All(
			ImprovementCount(iForestPreserve, 30),
			FreeSpecialistCity(12),
			by=1950,
		),
	),
	iBelgium: (
		GreatPeople(iGreatEngineer, 4, by=1920),
		All(
			ControlledResourceCount((iBanana, 4), (iIvory, 3), (iGems, 3), by=1900),
			ControlledResourceCount(iRubber, 3, by=1920),
			ControlledResourceCount(iUranium, 1, by=1950),
		),
		AreaPercent(plots.regions(rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rBaltics, rScandinavia).named(EUROPE), 65, subject=ALLIES, by=1960),
	),
	iAustralia: (
		ControlledResourceCount(improvement_resources(iMine), 18, by=1900),
		All(
			GreatPeople(iGreatGeneral, 3),
			AreaUnitGiftedCount(plots.regions(*(lEurope + lNorthAmerica)).named(EUROPE_OR_NORTH_AMERICA), 30),
			by=1940,
		),
		All(
			EraFirstDiscover(iGlobal, 5),
			ImprovementCount((iForestPreserve, 12), (iMarinePreserve, 8)),
			by=2000,
		),
	),
	iCanada: (
		All(
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.regions(rMaritimes, rQuebec).adjacent_region(rAtlanticOcean).named(ATLANTIC_COAST)),
			RouteConnection([iRouteRailroad], capital().named(CAPITAL), plots.regions(rCascadia, rAmericanArctic).adjacent_region(rPacificOcean).named(PACIFIC_COAST)),
			by=1920,
		),
		All(
			Control((plots.regions(rMaritimes, rQuebec, rOntario) + plots.regions(rGreatPlains, rCascadia).where(lambda p: p.getY() >= iCanadaSouthernBorder) + plots.region(rAmericanArctic).where(lambda p: iCanadaWesternBorder <= p.getX() <= iCanadaEasternBorder)).named(CITIES_IN_CANADA)),
 			AreaPercent((plots.regions(rMaritimes, rQuebec, rOntario) + plots.regions(rGreatPlains, rCascadia).where(lambda p: p.getY() >= iCanadaSouthernBorder) + plots.region(rAmericanArctic).where(lambda p: iCanadaWesternBorder <= p.getX() <= iCanadaEasternBorder)).named(CANADIAN_TERRITORY), 50),
			NoCityConquered(),
			by=1950,
		),
		BrokeredPeace(12, by=2000),
	),
}


for iCiv, goals in dGoals.items():
	for index, goal in enumerate(goals):
		title_key = "TXT_KEY_VICTORY_TITLE_%s%s" % (infos.civ(iCiv).getIdentifier(), index+1)
		goal.options["title_key"] = title_key


def descriptions(iCiv):
	for goal in dGoals[iCiv]:
		print goal.description()