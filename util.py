import time

util_scope = {
	'indent':0
}

def Log(what, *arg):
	indent = util_scope['indent']
	eve.Trace((' ' * indent) + what)
	if len(arg) > 0:
		if arg[0] > 0:
			indent += 4
		else:
			indent -= 4
		util_scope['indent'] = indent

def LogToFile(what):
	f = open('kid.log', 'a')
	f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	f.write('\t\t' + what + '\n')

def CheckDisplay(entry):
	return eve.GetBool(entry, 'display')

def HasChild(cont, name):
	eve.Children(cont, '__cs')
	l = eve.Len('__cs')
	for i in range(l):
		eve.GetListItem('__cs', i, '__c')
		if eve.GetString('__c', 'name') == name:
			return True
	return False

def CloseWnd(wnd):
	eve.Click(wnd)
	eve.FindChild(wnd, '__maincontainer', '_')
	while not HasChild('_', 'headerButtons'):
		time.sleep(0.5)
	eve.FindChild('_', 'headerButtons', '_')
	eve.FindChild('_', 'close', '_')
	while not CheckDisplay('_'):
		time.sleep(0.5)
	eve.Click('_', 16, 16)

