import maincont
import menu
from util import *

def GetDroneView():
	view = 'drone_view'
	maincont.GetForm('droneview', view)
	return view

def GetScroll():
	scroll = 'drone_scroll'
	view = GetDroneView()
	eve.FindChild(view, '__maincontainer', '_')
	eve.FindChild('_', 'main', '_')
	eve.FindChild('_', 'dronescroll', scroll)
	return scroll

def GetContent():
	content = 'drone_scroll_content'
	scroll = GetScroll()
	eve.FindChild(scroll, 'maincontainer', '_')
	eve.FindChild(scroll, '__clipper', '_')
	eve.FindChild(scroll, '__content', content)
	return content

def GetDronesInBay():
	entry = 'drones_in_bay'
	content = GetContent()
	eve.FindChild(content, 'droneOverviewDronesinbay', entry)
	return entry 

def GetDronesInSpace():
	entry = 'drones_in_space'
	content = GetContent()
	eve.FindChild(content, 'droneOverviewDronesinlocalspace', entry)
	return entry

def GetTitle(entry):
	eve.FindChild(entry, 'labelClipper', '_')
	eve.FindChild('_', 'EveLabelMedium', '_')
	return eve.GetString('_', 'text')

def ExtractTitleNumber(title):
	begin = title.rfind('(') + 1
	end = title.rfind(')')
	numstr = title[begin:end]
	return int(numstr)

def Launch():
	Log('Launch drones', 1)

	inbay = GetDronesInBay()
	if not CheckDisplay(inbay):
		view = GetDroneView()
		eve.Click(view, 100, 20)
		eve.Wheel(view, 9999, 100, 20)

	eve.RightClick(inbay, 100, 20)
	menu.WaitOpen()
	menu.Click('Launch Drones', False)

	Log('Launching...')
	while True:
		time.sleep(0.5)
		inspace = GetDronesInSpace()
		title = GetTitle(inspace)
		num = ExtractTitleNumber(title)
		if num == 5:
			break

	Log('end', -1)

def Return():
	Log('Drones return', 1)

	inspace = GetDronesInSpace()
	if not CheckDisplay(inspace):
		view = GetDroneView()
		eve.Click(view, 100, 20)
		eve.Wheel(view, -9999, 100, 20)

	eve.RightClick(inspace, 100, 20)
	menu.WaitOpen()
	menu.Click('Return to Drone Bay', False)

	Log('Returning...')
	while True:
		time.sleep(0.5)
		inspace = GetDronesInSpace()
		title = GetTitle(inspace)
		num = ExtractTitleNumber(title)
		if num == 0:
			break

	Log('end', -1)
