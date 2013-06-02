from util import *
import overview as ov

class ScanTask():

	def __init__(self, types, sortByDistance = False):
		'''
		types: list, types you want to scan, see overview.type_map
		sortByDistance: sort the result or not
		'''
		self._types = types
		self._sortByDistance = sortByDistance

	def run():
		Log('Scan task started', 1)

		entry = 'ov_entry'
		entries = ov.GetOvEntries()
		result = []

		l = eve.Len(entries)
		for i in range(l):
			eve.GetListItem(entries, i, entry)
			icon = ov.GetEntryIcon(entry)
			t = ov.GetTypeByIcon(icon)
			if t in self._types:
				dis = ov.GetEntryDistance(entry)
				result.append([dis, {
					'type':t,
					'name':ov.GetEntryName(entry),
					'distance':dis,
					'locked':ov.CheckTargeted(entry)
					}])

		if self._sortByDistance:
			result.sort()

		Log('end', -1)
		return result
