catch = {}

def GetViewSvc():
	view = 'view_svc'
	if view not in catch:
		eve.CallMemberMethod('sm', 'GetService', '"viewState"', view)
		catch[view] = view
	return view

def CurrentView():
	view = GetViewSvc()
	eve.CallMemberMethod(view, 'GetCurrentViewInfo', '', '_')
	return eve.GetString('_', 'name')
