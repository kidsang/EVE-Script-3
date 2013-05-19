import time
import re
from util import *

catch = {}

LocationHeaderRex = re.compile(r'<url.*?>(.*?)</url>')

def GetInfoContainer():
	info = 'info_panel_main_cont'
	if info not in catch:
		eve.GetAttr('layer', 'sidepanels', '_')
		eve.FindChild('_', 'sidePanel', '_')
		eve.FindChild('_', 'InfoPanelContainer', '_')
		eve.FindChild('_', 'mainCont', info)
		catch[info] = info
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
	if name not in catch:
		cont = GetInfoContainer()
		eve.FindChild(cont, 'InfoPanelRoute', name)
		catch[name] = name
	return name

def GetNoDestinationLabel():
	name = 'info_panel_no_destination_label'
	cont = GetInfoContainer()
	eve.FindChild(cont, 'InfoPanelRoute', '_')
	eve.FindChild('_', 'mainCont', '_')
	eve.FindChild('_', 'noDestinationLabel', name)
	return name

def HasWaypoint():
	panel = GetRoutePanel()
	while not CheckDisplay(panel):
		time.sleep(0.5)
	name = GetNoDestinationLabel()
	return not CheckDisplay(name)
