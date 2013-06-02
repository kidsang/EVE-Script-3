import time
import station
import ship
import info
import pilot
import mission
import overview
import maincont
from util import *

import TheRogueSlaveTrader1

battles = {
	'The Rogue Slave Trader (1 of 2)':TheRogueSlaveTrader1
}

agent = 'Eratsaka Ogyonin' # lv4

equipmap = {
	'em':'Armor EM Hardener II',
	'ex':'Armor Explosive Hardener II',
	't':'Armor Thermic Hardener II',
	'k':'Armor Kinetic Hardener II',
}
unfits = [(2, 2), (2, 3)]
defense = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]

def loop():
	Log('Mission Bot Begin.')
	LogToFile('Mission Bot Begin.')
	while True:
		if not run():
			return

def run():

	missionWnd = mission.StartConversation(agent)

	missionName = mission.GetMissionName(missionWnd)

	missionType = None
	if missionName in battles:
		missionType = 'b'
	else:
		Log('Error: can not find mission bot ' + missionName)
		return False

	Log(missionName + ' begin')
	LogToFile(missionName + ' begin')

	mission.AcceptMission(missionWnd)

	info.SetDestination()

	if missionType == 'b':
		runBattle(missionName)

	Log(missionName + ' end')
	LogToFile(missionName + ' end')

	return True

def runBattle(missionName):

	bot = battles[missionName]

	if getattr(bot, 'fits', None):
		station.UnfitSlots(unfits)
		fits = bot.fits
		equips = [equipmap[key] for key in fits]
		station.FitEquips(equips)

	station.Undock()

	pilot.Autopilot()

	# problem
	ship.EnableDefense(defense)

	info.WarpToLocation()

	# bot.run()
	pass

# main = maincont.GetMain()
# eve.Click(main, 500, 500)
# # wnd = mission.StartConversation(agent)
# # mission.QuitMission(wnd)
# runBattle('The Rogue Slave Trader (1 of 2)')

Log('finished')
