import time
import re
import station
import msgbox
import maincont
from util import *

MissionNameReg = r'<span id=subheader>(.+?)</span>'

def GetAgent(agentName):
	agent = 'mission_agent'
	lobby = station.GetLobby()
	eve.GetAttr(lobby, 'sr', '_')
	eve.GetAttr('_', 'scroll', '_')
	eve.FindChild('_', 'maincontainer', '_')
	eve.FindChild('_', '__clipper', '_')
	eve.FindChild('_', '__content', '_')
	eve.FindChild('_', agentName, agent)
	return agent

def StartConversation(agentName):
	Log('Start conversation with ' + agentName, 1)
	agent = GetAgent(agentName)
	eve.FindChild(agent, 'removeButton', '_')
	eve.Click('_')

	wnd = 'mission_agent_wnd'
	wndName = None
	Log('Wait until window opened')
	while not wndName:
		time.sleep(1)
		wndName = maincont.HasFormReg(maincont.AgentWindowReg)

	Log('Loading content')
	maincont.GetForm(wndName, wnd)
	eve.GetAttr(wnd, 'sr', '_')
	eve.GetAttr('_', 'main', '_')
	l = 0
	while l == 0:
		eve.Children('_', 'children')
		l = eve.Len('children')
		time.sleep(0.5)

	if not HasChild('_', 'rightPane'):
		ExpandMissionDetails(wnd)

	time.sleep(1)

	Log('end', -1)
	return wnd

def ExpandMissionDetails(wnd):
	Log('Expand mission details', 1)

	btns = GetButtons(wnd)
	if HasChild(btns, 'Request Mission_Btn'):
		eve.FindChild(btns, 'Request Mission_Btn', '_')
	else:
		eve.FindChild(btns, 'View Mission_Btn', '_')
	eve.Click('_')

	Log('Expanding...')
	eve.GetAttr(wnd, 'sr', '_')
	eve.GetAttr('_', 'main', '_')
	while not HasChild('_', 'rightPane'):
		time.sleep(1)

	Log('end', -1)

def GetButtons(wnd):
	btns = 'mission_agent_wnd_btns'
	eve.GetAttr(wnd, 'buttonGroup', '_')
	eve.FindChild('_', 'btns', btns)
	return btns

def GetMissionName(wnd):
	eve.GetAttr('_', 'htmlCache', '_')
	eve.GetDictItem('_', 'briefingBrowser', '_')
	html = eve.ToStr('_')
	reg = re.compile(MissionNameReg)
	result = reg.search(html)
	return result.group(1)

def QuitMission(wnd):
	Log('Quit mission', 1)

	btns = GetButtons(wnd)
	eve.FindChild(btns, 'Quit Mission_Btn', '_')
	eve.Click('_')

	Log('Wait for msg box show up')
	while not msgbox.HasMsgBox():
		time.sleep(1)

	box = msgbox.GetMsgBox()
	msgbox.Confirm(box)

	Log('end', -1)

def DoSthAndClose(wnd, sth):
	btns = GetButtons(wnd)
	eve.FindChild(btns, sth + '_Btn', '_')
	eve.Click('_')
	CloseWnd(wnd)

def CompleteMission(wnd):
	Log('Complete mission', 1)
	DoSthAndClose(wnd, 'Complete Mission')
	Log('end', -1)

def AcceptMission(wnd):
	Log('Accept mission', 1)
	DoSthAndClose(wnd, 'Accept')
	Log('end', -1)

# wnd = StartConversation('Aura')
# AcceptMission(wnd)
# CompleteMission(wnd)

# wndName = maincont.HasFormReg(maincont.AgentWindowReg)
# maincont.GetForm(wndName, '_')
