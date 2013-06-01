import time
import menu
import maincont
import ship
import maincont
import shortcut as sc
from util import *

cache = {}

type_map = {
	'38_16_251':'star_gate',
	'38_16_252':'station',
	'38_16_28':'wreck'
}

revert_type_map = {}
for key in type_map.keys():
	revert_type_map[type_map[key]] = key

color_yellow = '(1.0, 1.0, 0.0)'

def GetTypeByIcon(iconPath):
	head = iconPath.rfind('/')
	tail = iconPath.rfind('.')
	key = iconPath[head+1:tail]
	if key in type_map:
		return type_map[key]
	return 'unknown'

def GetOvHeaderIcon():
	icon = 'overview_header_icon'
	if icon not in cache:
		eve.GetAttr('layer', 'main')
		eve.FindChild('main', 'overview')
		eve.FindChild('overview', '__maincontainer', '_')
		eve.FindChild('_', 'headerParent', '_')
		eve.FindChild('_', 'top', '_')
		eve.FindChild('_', 'captionParent', '_')
		eve.FindChild('_', 'overviewHeaderIcon', icon)
		cache[icon] = icon
	return icon

def GetOvScroller():
	scroller = "ov_scroller"
	if scroller not in cache:
		eve.GetAttr('layer', 'main')
		eve.FindChild('main', 'overview')
		eve.FindChild('overview', '__maincontainer', '_')
		eve.FindChild('_', 'main', '_')
		eve.FindChild('_', 'overviewscroll2', scroller)
		cache[scroller] = scroller
	return scroller

def Refresh():
	scroller = GetOvScroller()
	cont = GetOvEntryContainer()
	eve.GetParent(cont, 'clipper')
	for i in range(10):
		pos = int(eve.GetString(scroller, '_position'))
		totalHeight = int(eve.GetString(scroller, '_totalHeight'))
		contHeight = int(eve.GetString('clipper', 'displayHeight'))
		if pos + contHeight == totalHeight:
			break
		ScrollDown()

def Scroll(up):
	scroller = GetOvScroller()
	scrollerHeight = int(eve.GetString(scroller, '_displayHeight'))
	step = 19
	dz = scrollerHeight / step * 0.8
	if not up:
		dz *= -1
	eve.Wheel(scroller, dz)

def ScrollDown():
	Scroll(False)

def ScrollUp():
	Scroll(True)

def ScrollTo(entry):
	node = GetEntryNode(entry)
	idx = int(eve.GetString(node, 'idx'))
	dst = idx * 19
	scroller = GetOvScroller()
	src = int(eve.GetString(scroller, '_position'))
	dz = (src - dst) / 19 + 2
	eve.Wheel(scroller, dz)

def GetOvEntryContainer():
	container = "ov_entry_container"
	if container not in cache:
		scroller = GetOvScroller()
		eve.FindChild(scroller, 'maincontainer', '_')
		eve.FindChild('_', '__clipper', '_')
		eve.FindChild('_', '__content', container)
		cache[container] = container;
	return container

def GetOvEntries():
	container = GetOvEntryContainer()
	entries = 'ov_entries'
	eve.Children(container, entries)
	return entries

def GetEntryNode(entry):
	node = 'ov_entry_node'
	eve.GetAttr(entry, 'sr', '_')
	eve.GetAttr('_', 'node', node)
	return node

def GetEntryName(entry):
	node = GetEntryNode(entry)
	return eve.GetString(node, 'display_NAME')

def GetEntryIcon(entry):
	eve.FindChild(entry, 'iconContainer', '_')
	eve.FindChild('_', 'mainIcon', '_')
	return eve.GetString('_', 'texturePath')

def GetEntryDistance(entry):
	node = GetEntryNode(entry)
	return float(eve.GetString(node, 'rawDistance'))

def GetEntryColor(entry):
	node = GetEntryNode(entry)
	return eve.GetString(node, 'iconColor')

def IsWreck(entry):
	return GetTypeByIcon(GetEntryIcon(entry)) == 'wreck'

def CheckSelected(entry):
	node = GetEntryNode(entry)
	return eve.GetBool(node, 'selected')

def CheckTargeted(entry):
	return eve.GetBool(entry, 'targetedByMeIndicator')

def CheckTargeting(entry):
	return eve.GetBool(entry, 'targetingIndicator')

def CheckHostile(entry):
	return eve.GetBool(entry, 'hostileIndicator')

def CheckActiveTarget(entry):
	return eve.GetBool(entry, 'myActiveTargetIndicator')

def CheckAttackingMe(entry):
	return eve.GetBool(entry, 'attackingMeIndicator')

def SelectEntry(entry):
	eve.Click(entry)
	while not CheckSelected(entry):
		eve.Click(entry, 15, 15)

def GetWaypoint():
	waypoint = 'ov_waypoint'
	entries = GetOvEntries()
	l = eve.Len(entries)
	for i in range(l):
		eve.GetListItem(entries, i, waypoint)
		node = GetEntryNode(waypoint)
		color = eve.GetString(node, 'iconColor')
		if color == color_yellow:
			icon = GetEntryIcon(waypoint)
			group = GetTypeByIcon(icon)
			if group == 'station' or group == 'star_gate':
				return waypoint
	return None

def GetOvEntryByIcon(iconName):
	Log('Finding entry "' + iconName + '" in overview', 1)

	entry = 'ov_entry'
	current = 0
	scroller = GetOvScroller()
	cont = GetOvEntryContainer()
	eve.GetParent(cont, 'clipper')
	totalHeight = int(eve.GetString(scroller, '_totalHeight'))
	contHeight = int(eve.GetString('clipper', 'displayHeight'))
	eve.Click(scroller, 60, 60)

	while True:
		entries = GetOvEntries()
		l = eve.Len(entries)
		Log('Finding in row ' + str(current) + ' to ' + str(l))
		for i in range(current, l):
			eve.GetListItem(entries, i, entry)
			icon = GetEntryIcon(entry)
			group = GetTypeByIcon(icon)
			if group == iconName:
				ScrollTo(entry)
				Log('Entry finded: ' + iconName, -1)
				return entry

		current = l / 2
		pos = int(eve.GetString(scroller, '_position'))
		if pos + contHeight < totalHeight:
			ScrollDown()
		else:
			Log('Entry not found', -1)
			return None


def GetOvEntryByName(targetName, fullyMatch = False):
	Log('Finding entry "' + targetName + '" in overview', 1)

	entry = 'ov_entry'
	current = 0
	scroller = GetOvScroller()
	cont = GetOvEntryContainer()
	eve.GetParent(cont, 'clipper')
	totalHeight = int(eve.GetString(scroller, '_totalHeight'))
	contHeight = int(eve.GetString('clipper', 'displayHeight'))
	eve.Click(scroller, 60, 60)

	while True:
		entries = GetOvEntries()
		l = eve.Len(entries)
		Log('Finding in row ' + str(current) + ' to ' + str(l))
		for i in range(current, l):
			eve.GetListItem(entries, i, entry)
			name = GetEntryName(entry)
			matched = False
			if fullyMatch and name == targetName:
				matched = True
			if not fullyMatch and name.find(targetName) != -1:
				matched = True
			if matched:
				ScrollTo(entry)
				Log('Entry finded: ' + name, -1)
				return entry

		current = l / 2
		pos = int(eve.GetString(scroller, '_position'))
		if pos + contHeight < totalHeight:
			ScrollDown()
		else:
			Log('Entry not found', -1)
			return None

# active item view

def GetItemViewContainer():
	container = 'ov_item_view_btn_container'
	main = maincont.GetMain()
	eve.FindChild(main, 'selecteditemview')
	eve.GetAttr('selecteditemview', 'sr', '_')
	eve.GetAttr('_', 'actions', container)
	return container

def ListItemViewBtns():
	container = GetItemViewContainer()
	eve.Children(container)

def GetItemViewBtn(name):
	btn = 'ov_item_view_btn'
	name = 'selectedItem' + name
	container = GetItemViewContainer()
	eve.FindChild(container, name, btn)
	return btn

def AlignToBtn():
	return GetItemViewBtn('AlignTo')

def WarpToBtn():
	return GetItemViewBtn('WarpTo')

def JumpBtn():
	return GetItemViewBtn('Jump')

def OrbitBtn():
	return GetItemViewBtn('Orbit')

def KeepAtRangeBtn():
	return GetItemViewBtn('KeepAtRange')

def LockTargetBtn():
	return GetItemViewBtn('LockTarget')

def UnLockTargetBtn():
	return GetItemViewBtn('UnLockTarget')

def DockBtn():
	return GetItemViewBtn('Dock')

def OpenCargoBtn():
	return GetItemViewBtn('OpenCargo')

def GetInventory(invName):
	inv = 'overview_inventory_space_prime'
	maincont.GetForm(invName, inv)
	return inv

def LootAll(inventory):
	eve.FindChild(inventory, '__maincontainer', '_')
	eve.FindChild('_', 'main', '_')
	eve.FindChild('_', 'rightCont', '_')
	eve.FindChild('_', 'bottomRightcont', '_')
	eve.FindChild('_', 'specialActionsCont', '_')
	eve.Children('_', 'children')
	while eve.Len('children') == 0:
		time.sleep(0.5)
	eve.FindChild('_', 'invLootAllBtn', '_')
	eve.Click('_')

# 

def SwitchTo(ovname):
	Log('Switch to overview setting "' + ovname + '"', 1)
	icon = GetOvHeaderIcon()
	eve.Click(icon, 16, 16)
	while not menu.HasMenu():
		time.sleep(0.5)
	menu.Click('Load ' + ovname)
	Log('end', -1)

def ActivateAccelerationGate(gateName = None):
	Log('Travel throught acceleration gate', 1)

	if not gateName:
		gateName = 'Acceleration Gate'

	entry = GetOvEntryByName(gateName)

	SelectEntry(entry)

	Log('Approaching acceleration gate')
	while not ship.Warping():
		eve.Press(sc.Activate)
		time.sleep(1)

	Log('Warping')
	while ship.Warping():
		time.sleep(0.5)

	Log('end', -1)

def PickTarget(targetName = None, fullyMatch = False):

	if not targetName:
		targetName = 'Cargo'

	Log('Picking ' + targetName, 1)

	entry = GetOvEntryByName(targetName, fullyMatch)
	SelectEntry(entry)

	btn = OpenCargoBtn()
	invName = None
	Log('Approaching target')
	while not invName:
		eve.Click(btn)
		invName = maincont.HasFormReg(maincont.SpaceInventoryReg)
		time.sleep(0.5)

	inv = GetInventory(invName)
	LootAll(inv)
	CloseWnd(inv)

	Log('end', -1)

def LockTarget(targetName, ensureTargeted = False, fullyMatch = True):
	Log('Lock target "' + targetName + '"', 1)

	entry = GetOvEntryByName(targetName)
	SelectEntry(entry)

	eve.Press(sc.Lock)
	if not CheckTargeted(entry):
		while not CheckTargeting(entry):
			eve.Press(sc.Lock)
			time.sleep(0.5)

	while ensureTargeted and not CheckTargeted(entry):
		time.sleep(0.5)

	Log('end', -1)

# entries = GetOvEntries()
# l = eve.Len(entries)
# for i in range(l):
# 	eve.GetListItem(entries, i, 'entry')
# 	entry = 'entry'
# 	eve.Trace(GetEntryName(entry))
# 	icon = GetEntryIcon(entry)
# 	eve.Trace(GetTypeByIcon(iconPath))
# 	eve.Trace(' ')
