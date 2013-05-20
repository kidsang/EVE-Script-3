import time
import maincont
import shortcut as sc
import menu
from util import *

catch = {}

PrimerRex = r"\('.*',.*\)"

def GetLobby():
	while not maincont.HasForm('lobby'):
		time.sleep(1)
	lobby = 'station_lobby'
	maincont.GetForm('lobby', lobby)
	return lobby

def GetLobbySvcBtnCont():
	cont = 'station_lobby_svc_btn_cont'
	lobby = GetLobby()
	eve.GetAttr(lobby, 'sr', '_')
	eve.GetAttr('_', 'btnparent', cont)
	return cont

def GetLobbySvcBtn(name):
	btn = 'station_lobby_svc_btn_' + name
	cont = GetLobbySvcBtnCont()
	eve.FindChild(cont, name, btn)
	return btn

def Repair():
	Log('Repair', 1)

	btn = GetLobbySvcBtn('repairshop')
	eve.Click(btn)

	Log('Openning repair shop')
	while not maincont.HasForm('repairshop'):
		time.sleep(0.5)

	form = 'station_repairshop_wnd'
	maincont.GetForm('repairshop', form)
	repairItemBtn = 'station_repairshop_wnd_repair_item_btn'
	pickNewBtn = 'station_repairshop_wnd_pick_new_btn'
	repairAllBtn = 'station_repairshop_wnd_repair_all_btn'
	scroll = 'station_repairshop_wnd_scroll'
	eve.GetAttr(form, 'sr')
	eve.GetAttr('sr', 'selBtn', repairItemBtn)
	eve.GetAttr('sr', 'pickBtn', pickNewBtn)
	eve.GetAttr('sr', 'repairAllBtn', repairAllBtn)
	eve.GetAttr('sr', 'scroll', scroll)

	while int(eve.GetString(scroll, '_totalHeight')) == 0:
		time.sleep(1)

	Log('Select items')
	eve.Click(scroll, 40, 40)
	eve.Press('ctrl+a')

	eve.Click(repairItemBtn)
	while not CheckDisplay(pickNewBtn):
		time.sleep(0.5)

	if not CheckDisplay(repairAllBtn):
		Log('Nothing to repair')
	else:
		pass

	CloseWnd(form)

	Log('end', -1)

def OpenInventory():
	Log('Open inventory', 1)
	eve.Press(sc.Inventory)

	formname = None
	while not formname:
		formname = maincont.HasFormReg(r"\('" + "InventoryStation" + r"'\,.*\)")
		time.sleep(1)

	form = 'station_prime_inventory_wnd'
	maincont.GetForm(formname, form)
	eve.GetAttr(form, 'sr', '_')
	eve.GetAttr('_', 'loadingIndicator', '_')

	Log('Loading inventory items')
	while CheckDisplay('_'):
		time.sleep(1)

	Log('end', -1)
	return form

def FindItem(itemName):
	Log('Finding item "' + item + '" in inventory', 1)
	cont = 'station_inventory_wnd'
	maincont.GetForm('InventoryStation', cont)
	eve.FindChild(cont, 'scroll', '_')
	eve.FindChild('_', 'maincontainer', '_')
	eve.FindChild('_', '__clipper', '_')
	eve.FindChild('_', '__content', '_')
	eve.FindChild('_', 'entry_0', '_')

def _GetInventoryTreeCont(inventory):
	eve.FindChild(inventory, '__maincontainer', '_')
	eve.FindChild('_', 'main', '_')
	eve.FindChild('_', 'dividerCont', '_')
	eve.FindChild('_', 'mainCont', '_')
	eve.FindChild('_', 'tree', '_')
	eve.FindChild('_', 'clipCont', '_')
	eve.FindChild('_', 'mainCont', '_')
	return '_'


def GetInventoryTreeShipCargoUI(inventory):
	icon = 'station_inventory_tree_ship_cargo_icon'
	_GetInventoryTreeCont(inventory)
	eve.Children('_', '_')
	eve.GetListItem('_', 0, '_')
	eve.FindChild('_', 'icon', icon)
	return icon

def GetInventoryTreeItemHangarUI(inventory):
	icon = 'station_inventory_tree_item_hangar_icon'
	_GetInventoryTreeCont(inventory)
	eve.Children('_', '_')
	n = eve.Len('_') - 1
	eve.GetListItem('_', n, '_')
	eve.FindChild('_', 'icon', icon)
	return icon

def GetInventoryBody():
	cont = 'station_inventory_wnd'
	maincont.GetForm('InventoryStation', cont)
	return cont

def ListInventoryItems():
	inventory = GetInventoryBody()
	eve.FindChild(inventory, 'scroll', '_')
	eve.FindChild('_', 'maincontainer', '_')
	eve.FindChild('_', '__clipper', '_')
	eve.FindChild('_', '__content', '_')
	eve.Children('_', 'rows')
	for i in range(eve.Len('rows')):
		eve.GetListItem('rows', i, 'rowItem')
		rowName = eve.GetString('rowItem', 'name')
		if rowName.find('entry_') != 0:
			continue
		# eve.Str('rowItem')
		eve.Children('rowItem', 'invItems')
		for j in range(eve.Len('invItems')):
			eve.GetListItem('invItems', j, 'invItem')
			itemName = eve.GetString('invItem', 'name')
			eve.Trace(itemName)
	# eve.FindChild('_', 'entry_0', '_')

def FindItemIn(cont, targetName):
	Log('Finding item "' + targetName + '"', 1)
	eve.FindChild(cont, 'scroll')
	eve.FindChild('scroll', 'maincontainer', '_')
	eve.FindChild('_', '__clipper', 'clipper')
	eve.FindChild('clipper', '__content', '_')

	totalHeight = int(eve.GetString('scroll', '_totalHeight'))
	clipperHeight = int(eve.GetString('clipper', 'displayHeight'))

	def ScrollDown():
		dz = clipperHeight / 92 * 6
		eve.Click('scroll')
		eve.Wheel('scroll', -dz)

	def ScrollTo(line):
		eve.Click('scroll')
		eve.Wheel('scroll', 99999)
		eve.Wheel('scroll', -(line * 6 - line / 3))

	def _Find():
		curRow = 0
		while True:
			eve.Children('_', 'rows')
			numRows = eve.Len('rows')
			Log('Finding in row ' + str(curRow) + ' to ' + str(numRows))
			for i in range(curRow, numRows):
				eve.GetListItem('rows', i, 'rowItem')
				rowName = eve.GetString('rowItem', 'name')
				if rowName.find('entry_') == 0:
					eve.Children('rowItem', 'invItems')
					for j in range(eve.Len('invItems')):
						eve.GetListItem('invItems', j, 'invItem')
						itemName = eve.GetString('invItem', 'name')
						if itemName == targetName:
							return 'invItem', curRow
					curRow += 1
			position = int(eve.GetString('scroll', '_position'))
			if position + clipperHeight < totalHeight:
				ScrollDown()
			else:
				return None

	result = _Find()
	if result:
		ScrollTo(result[1])
		Log('Item finded', -1)
		return result[0]
	else:
		Log('Item not found', -1)
		return None

def LoadOrUnloadItem(itemName, load):
	if load:
		Log('Load item "' + itemName + '"', 1)
	else:
		Log('Unload item "' + itemName + '"', 1)

	inventory = OpenInventory()
	shipIcon = GetInventoryTreeShipCargoUI(inventory)
	hangarIcon = GetInventoryTreeItemHangarUI(inventory)

	if load:
		eve.Click(hangarIcon)
	else:
		eve.Click(shipIcon)

	item = FindItemIn(GetInventoryBody(), itemName)


	if load:
		eve.DragDrop(item, shipIcon)
	else:
		eve.DragDrop(item, hangarIcon)


	if load:
		eve.Click(shipIcon)
	else:
		eve.Click(hangarIcon)

	while not FindItemIn(GetInventoryBody(), itemName):
		time.sleep(1)

	maincont.CloseWnd(inventory)

	Log('end', -1)

def LoadItem(itemName):
	LoadOrUnloadItem(itemName, True)

def UnloadItem(itemName):
	LoadOrUnloadItem(itemName, False)

def StackItemsInHangar():
	Log('Stack items in hangar', 1)

	inventory = OpenInventory()
	hangarIcon = GetInventoryTreeItemHangarUI(inventory)
	eve.Click(hangarIcon)

	cont = GetInventoryBody()
	eve.RightClick(cont, 40, 40)
	menu.Click('Stack All')

	maincont.CloseWnd(inventory)

	Log('end', -1)
	
