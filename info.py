import time
import re
from util import *

cache = {}

LocationHeaderRex = re.compile(r'<url.*?>(.*?)</url>')

def GetInfoContainer():
	info = 'info_panel_main_cont'
	if info not in cache:
		eve.GetAttr('layer', 'sidepanels', '_')
		eve.FindChild('_', 'sidePanel', '_')
		eve.FindChild('_', 'InfoPanelContainer', '_')
		eve.FindChild('_', 'mainCont', info)
		cache[info] = info
	return info

def GetSystemCaptionUI():
	name = 'info_panel_system_caption_ui'
	cont = GetInfoContainer()
	eve.FindChild(cont, 'InfoPanelLocationInfo', '_')
	eve.FindChild('_', 'topCont', '_')
	eve.FindChild('_', 'headerCont', '_')
	eve.FindChild('_', 'header', name)
	return name

def CurrentSystem():
	ui = GetSystemCaptionUI()
	raw = eve.GetString(ui, 'text')
	result = LocationHeaderRex.match(raw)
	return result.group(1)

def GetRoutePanel():
	name = 'info_panel_route_info'
	cont = GetInfoContainer()
	eve.FindChild(cont, 'InfoPanelRoute', name)
	return name

def GetNoDestinationLabel():
	name = 'info_panel_no_destination_label'
	panel = GetRoutePanel()
	eve.FindChild(panel, 'mainCont', '_')
	eve.FindChild('_', 'noDestinationLabel', name)
	return name

def HasWaypoint():
	panel = GetRoutePanel()
	while not CheckDisplay(panel):
		time.sleep(0.5)
	name = GetNoDestinationLabel()
	return not CheckDisplay(name)

def GetAgentMissionsPanel():
	name = 'info_panel_agent_mission_panel'
	cont = GetInfoContainer()
	eve.FindChild(cont, 'InfoPanelMissions', name)
	return name

def OpenUtilMenu():
	Log('Open util menu', 1)
	panel = GetAgentMissionsPanel()
	eve.FindChild(panel, 'mainCont', '_')
	eve.FindChild('_', 'UtilMenu', '_')
	eve.FindChild('_', 'EveLabelMedium', '_')
	eve.Click('_')
	Log('end', -1)

def ClickUtilMenu(itemName):
	Log('Click util menu item "' + itemName + '"')
	eve.GetAttr('layer', 'utilmenu', '_')
	eve.FindChild('_', 'ExpandedUtilMenu', '_')
	eve.Children('_', 'children')
	l = eve.Len('children')
	for i in range(l):
		eve.GetListItem('children', i, '_')
		if eve.GetString('_', 'name') == 'UtilMenuIconEntry':
			eve.FindChild('_', 'EveLabelMedium', '_')
			if eve.GetString('_', 'text') == itemName:
				eve.Click('_')
				return True
	return False

def OpenUtilMenuAddClick(itemName):
	OpenUtilMenu()
	ClickUtilMenu(itemName)

def Dock():
	OpenUtilMenuAddClick('Dock')

def SetDestination():
	OpenUtilMenuAddClick('Set Destination')

def WarpToLocation():
	OpenUtilMenuAddClick('Warp to Location')

# WarpToLocation()
