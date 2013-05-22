import time
from util import *

catch = {}

def GetMenuLayer():
	layer = 'menu_layer'
	if layer not in catch:
		eve.GetAttr('layer', 'menu', layer)
		catch[layer] = layer
	return layer

def HasMenu():
	layer = GetMenuLayer()
	eve.Children(layer, '_')
	return eve.Len('_') > 0

def GetMenu():
	menu = 'menu_layer_dropdown_menu'
	layer = GetMenuLayer()
	eve.Children(layer, '_')
	eve.GetListItem('_', 0, menu)
	return menu

def Click(targetName):
	Log('Click menu item "' + targetName + '"', 1)

	while not HasMenu():
		time.sleep(0.5)

	menu = GetMenu()
	eve.FindChild(menu, '_entries', '_')
	eve.Children('_', 'entries')
	l = eve.Len('entries')
	for i in range(l):
		eve.GetListItem('entries', i, 'entry')
		if eve.GetString('entry', 'name') == 'entry':
			eve.FindChild('entry', 'EveLabelSmall', '_')
			name = eve.GetString('_', 'text')
			if name == targetName:
				eve.Click('_')
				Log('Menu item finded', -1)
				return True

	Log('Menu item not found', -1)
	return False


def ListCurrentMenu():
	menu = GetMenu()
	eve.FindChild(menu, '_entries', '_')
	eve.Children('_', 'entries')
	l = eve.Len('entries')
	for i in range(l):
		eve.GetListItem('entries', i, 'entry')
		if eve.GetString('entry', 'name') == 'entry':
			eve.FindChild('entry', 'EveLabelSmall', '_')
			name = eve.GetString('_', 'text')
			eve.Trace(name)

