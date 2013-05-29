import sys
import time
from task import *
from util import *
import shortcut as sc
import overview as ov
import maincont

class LootTask(Task):

	def __init__(self, trace = False, tractorBeamSlots = None, afterburnerSlot = None):
		'''
		trace: approach wreck before loot
		tractorBeamSlots: list of tuple, tractor beam slot positions
		afterburnerSlot: tuple, afterburner slot position

		'''
		self._trace = trace
		self._tractorBeamSlots = tractorBeamSlots
		self._afterburnerSlot = afterburnerSlot

	def run(self):
		Log('Loot task started.', 1)

		entry = 'ov_entry'
		entries = ov.GetOvEntries()

		minDistance = sys.maxint 
		minIndex = -1
		# lockedIndex = -1
		l = eve.Len(entries)
		for i in range(l):
			eve.GetListItem(entries, i, entry)
			if ov.IsWreck(entry):
				dis = ov.GetEntryDistance(entry)
				if dis < minDistance:
					minDistance = dis
					minIndex = i

		if minIndex != -1:
			eve.GetListItem(entries, minIndex, entry)
			ov.ScrollTo(entry)
			ov.SelectEntry(entry)

			if minDistance < 2000:
				Log('Looting ' + ov.GetEntryName(entry))
				eve.Click(ov.OpenCargoBtn())
				invName = None

				Log('Openning cargo')
				while not invName:
					time.sleep(0.5)
					invName = maincont.HasFormReg(maincont.SpaceInventoryReg)

				inv = ov.GetInventory(invName)
				ov.LootAll(inv)
				CloseWnd(inv)

			elif self._trace:
				if self._afterburnerSlot:
					pass
				Log('Approaching ' + ov.GetEntryName(entry))
				eve.Press(sc.Approach)
		else:
			Log('No wreck found')

		Log('end', -1)


# task = LootTask(trace = True)
# task.run()