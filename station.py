import time
import maincont
import shortcut as sc
import view
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
		formname = maincont.HasFormReg(maincont.StationInventoryReg)
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

def GetInventory():
	form = 'station_prime_inventory_wnd'
	maincont.GetForm(formname, form)
	return form

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

def ListInventoryItems(inventory):
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

def LoadOrUnloadItem(itemName, load, invOpened = False):
	if load:
		Log('Load item "' + itemName + '"', 1)
	else:
		Log('Unload item "' + itemName + '"', 1)

	if invOpened:
		inventory = GetInventory()
	else:
		inventory = OpenInventory()

	shipIcon = GetInventoryTreeShipCargoUI(inventory)
	hangarIcon = GetInventoryTreeItemHangarUI(inventory)

	if load:
		eve.Click(hangarIcon)
	else:
		eve.Click(shipIcon)

	item = FindItemIn(GetInventoryBody(), itemName)

	if load:
		eve.DragDrop(item, shipIcon, 30, 30)
	else:
		eve.DragDrop(item, hangarIcon, 30, 30)

	if load:
		eve.Click(shipIcon)
	else:
		eve.Click(hangarIcon)

	while not FindItemIn(GetInventoryBody(), itemName):
		time.sleep(1)

	maincont.CloseWnd(inventory)

	Log('end', -1)

def LoadItem(itemName, invOpened = False):
	LoadOrUnloadItem(itemName, True, invOpened)

def UnloadItem(itemName, invOpened = False):
	LoadOrUnloadItem(itemName, False, invOpened)

def StackItemsInHangar(invOpened = False):
	Log('Stack items in hangar', 1)

	if invOpened:
		inventory = GetInventory()
	else:
		inventory = OpenInventory()

	hangarIcon = GetInventoryTreeItemHangarUI(inventory)
	eve.Click(hangarIcon)

	cont = GetInventoryBody()
	eve.RightClick(cont, 40, 40)
	menu.Click('Stack All')

	maincont.CloseWnd(inventory)

	Log('end', -1)

def OpenFitting():
	Log('Open fitting window')
	eve.Press(sc.Fitting)

	form = 'station_fitting_wnd'
	while not maincont.HasForm('fitting'):
		time.sleep(1)
	maincont.GetForm('fitting', form)
	Log('end', -1)
	return form

def GetSlot(fitting, i, j):
	slot = 'station_fitting_slot'
	slotName = 'slot_' + str(i) + '_' + str(j)
	eve.GetAttr(fitting, 'sr', '_')
	eve.GetAttr('_', 'fitting', '_')
	eve.FindChild('_', 'slotParent', '_')
	eve.FindChild('_', slotName, slot)
	return slot

def UnfitSlots(slotIDs):
	Log('Unfitting slots:' + str(slotIDs), 1)

	fitting = OpenFitting()

	for slotID in slotIDs:
		slot = GetSlot(fitting, slotID[0], slotID[1])
		eve.RightClick(slot, 20, 30)
		menu.Click('Unfit')

	maincont.CloseWnd(fitting)
	Log('end', -1)

def FitEquips(equipNames, invOpened = False):
	Log('Fitting equipments:' + str(equipNames), 1)

	if invOpened:
		inventory = GetInventory()
	else:
		inventory = OpenInventory()

	for equipName in equipNames:
		equip = FindItemIn(GetInventoryBody(), equipName)
		eve.RightClick(equip, 30, 30)
		menu.Click('Fit to Active Ship')

	maincont.CloseWnd(inventory)
	Log('end', -1)

def OpenShipHangar():
	Log('Open ship hangar', 1)
	eve.Press(sc.ShipHangar)

	formname = None
	while not formname:
		formname = maincont.HasFormReg(maincont.StationShipReg)
		time.sleep(1)

	form = 'station_prime_ship_hangar_wnd'
	maincont.GetForm(formname, form)
	eve.GetAttr(form, 'sr', '_')
	eve.GetAttr('_', 'loadingIndicator', '_')

	Log('Loading ships')
	while CheckDisplay('_'):
		time.sleep(1)

	Log('end', -1)
	return form

def GetShipHangarBody():
	cont = 'station_ship_hangar_wnd'
	maincont.GetForm('StationShips', cont)
	return cont

def ActivateShip(shipName):
	Log('Activating ship "' + shipName + '"', 1)
	shipHangar = OpenShipHangar()
	ship = FindItemIn(GetShipHangarBody(), shipName)
	eve.RightClick(ship, 30, 30)
	menu.Click('Make Active')
	maincont.CloseWnd(shipHangar)
	Log('end', -1)

def GetUndockBtnCont():
	cont = 'station_undock_btn_cont'
	if cont not in catch:
		eve.GetAttr('layer', 'sidepanels', '_')
		eve.FindChild('_', 'Neocom', '_')
		eve.FindChild('_', 'mainCont', '_')
		eve.FindChild('_', 'fixedButtonCont', cont)
		catch[cont] = cont
	return cont

def Undock():
	Log('Undocking', 1)

	cont = GetUndockBtnCont()
	eve.FindChild(cont, 'undock', '_')
	eve.Click('_')

	Log('Entering space')
	while not view.CurrentView() == 'inflight':
		time.sleep(1)

	time.sleep(4)

	Log('end', -1)
