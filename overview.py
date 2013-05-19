import time

catch = {}

type_map = {
	'500':'star_gate',
	'600':'station'
}

color_yellow = '(1.0, 1.0, 0.0)'

def GetType(itemID):
	hi = itemID[:3]
	if hi in type_map:
		return type_map[hi]
	return 'unknown'

def GetOvScroller():
	scroller = "ov_scroller"
	if scroller not in catch:
		eve.GetAttr('layer', 'main')
		eve.FindChild('main', 'overview')
		eve.FindChild('overview', '__maincontainer', '_')
		eve.FindChild('_', 'main', '_')
		eve.FindChild('_', 'overviewscroll2', scroller)
		catch[scroller] = scroller
	return scroller

def Refresh():
	scroller =sc = GetOvScroller()
	cont = GetOvEntryContainer()
	eve.GetParent(cont, 'clipper')
	for i in range(10):
		pos = int(eve.GetString(sc, '_position'))
		totalHeight = int(eve.GetString(sc, '_totalHeight'))
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
	if container not in catch:
		scroller = GetOvScroller()
		eve.FindChild(scroller, 'maincontainer', '_')
		eve.FindChild('_', '__clipper', '_')
		eve.FindChild('_', '__content', container)
		catch[container] = container;
	return container

def GetOvEntries():
	container = GetOvEntryContainer()
	entriess = 'ov_entries'
	eve.Children(container, entriess)
	return entriess

def GetEntryNode(entry):
	node = 'ov_entry_node'
	eve.GetAttr(entry, 'sr', '_')
	eve.GetAttr('_', 'node', node)
	return node

def GetEntryName(entry):
	node = GetEntryNode(entry)
	return eve.GetString(node, 'display_NAME')

def GetEntryTypeGroup(entry):
	node = GetEntryNode(entry)
	itemID = eve.GetString(node, 'itemID')
	return GetType(itemID)

def CheckSelected(entry):
	node = GetEntryNode(entry)
	return eve.GetBool(node, 'selected')

def GetWaypoint():
	waypoint = 'ov_waypoint'
	entries = GetOvEntries()
	l = eve.Len(entries)
	for i in range(l):
		eve.GetListItem(entries, i, waypoint)
		node = GetEntryNode(waypoint)
		color = eve.GetString(node, 'iconColor')
		if color == color_yellow:
			group = GetEntryTypeGroup(waypoint)
			if group == 'station' or group == 'star_gate':
				return waypoint
	return None

# active item view

def GetItemViewContainer():
	container = 'ov_item_view_btn_container'
	if container not in catch:
		eve.GetAttr('layer', 'main')
		eve.FindChild('main', 'selecteditemview')
		eve.GetAttr('selecteditemview', 'sr', '_')
		eve.GetAttr('_', 'actions', container)
		catch[container] = container
	return container

def GetItemViewBtns():
	container = GetItemViewContainer()
	btns = 'ov_item_view_btns'
	eve.Children(container, btns)
	return btns

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

# entries = GetOvEntries()
# l = eve.Len(entries)
# for i in range(l):
# 	eve.GetListItem(entries, i, 'entry')
# 	entry = 'entry'
# 	eve.Trace(GetEntryName(entry))
# 	node = GetEntryNode(entry)
# 	eve.Trace(eve.GetString(node, 'itemID'))
# 	eve.Trace(' ')
