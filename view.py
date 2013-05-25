cache = {}

def GetViewSvc():
	view = 'view_svc'
	if view not in cache:
		eve.CallMemberMethod('sm', 'GetService', '"viewState"', view)
		cache[view] = view
	return view

def CurrentView():
	view = GetViewSvc()
	eve.CallMemberMethod(view, 'GetCurrentViewInfo', '', '_')
	return eve.GetString('_', 'name')
