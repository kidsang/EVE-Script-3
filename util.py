
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

def CheckDisplay(entry):
	return eve.GetBool(entry, 'display')


