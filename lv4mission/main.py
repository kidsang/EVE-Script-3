import time
import station
import msgbox
import ship
import info
import pilot
import mission
import maincont
from util import *

battles = {
	
}

agent = 'Eratsaka Ogyonin' # lv4

defense = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]

def loop():
	Log('Mission Bot Begin.')
	LogToFile('Mission Bot Begin.')
	while True:
		if not run():
			return

def run():
	pass

def runBattle(missionName):
	bot = battles[missionName]
	pass

# main = maincont.GetMain()
# eve.Click(main, 500, 500)
# wnd = mission.StartConversation(agent)
# mission.QuitMission(wnd)

box = msgbox.GetMsgBox()
msgbox.Close(box)
# Log(msgbox.GetTitle(box))
# msgbox.Confirm(box)
Log('finished')
