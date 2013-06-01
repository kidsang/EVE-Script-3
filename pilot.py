import time
import overview as ov
import shortcut as sc
import info
import ship
import view
from util import *


def Autopilot():
	Log('Autopilot', 1)

	if view.CurrentView() != 'inflight':
		Log('Must run in view "inflight"')
		Log('', -1)
		return

	ov.SwitchTo('pilot')

	while True:
		if not info.HasWaypoint():
			Log('No waypoint finded')
			break

		waypoint = ov.GetWaypoint()
		while not waypoint:
			ov.ScrollDown()
			waypoint = ov.GetWaypoint()

		icon = ov.GetEntryIcon(waypoint)
		wptype = ov.GetTypeByIcon(icon)
		Log('Heading to ' + ov.GetEntryName(waypoint))

		while not CheckDisplay(waypoint):
			ov.ScrollTo(waypoint)

		ov.SelectEntry(waypoint)

		for i in range(3):
			eve.Press(sc.Activate)
			time.sleep(1)

		if wptype == 'station':
			while True:
				currentView = view.CurrentView()
				if currentView != 'hangar' and currentView != 'station':
					time.sleep(2)
				else:
					break
		else:
			lastSystem = info.CurrentSystem()
			while True:
				currentSystem = info.CurrentSystem()
				if lastSystem == currentSystem:
					time.sleep(2)
				else:
					break

		time.sleep(4)

	Log('end', -1)

