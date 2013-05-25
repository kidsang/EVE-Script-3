from util import *
import re

cache = {}

StationInventoryReg = r"\('" + "InventoryStation" + r"'\,.*\)"
StationShipReg = r"\('" + "StationShips" + r"'\,.*\)"
SpaceInventoryReg = r"\('" + "InventorySpace" + r"'\,.*\)"
AgentWindowReg = r"agentinteraction.+"

def GetMain():
	main = 'ui_main_cont'
	if main not in cache:
		eve.GetAttr('layer', 'main', main)
		cache[main] = main
	return main

def Children():
	main = GetMain()
	eve.Children(main)

def HasForm(name):
	main = GetMain()
	eve.Children(main, '_')
	l = eve.Len('_')
	find = False
	for i in range(l):
		eve.GetListItem('_', i, 'form')
		if eve.GetString('form', 'name') == name:
			find = True
			break

	if find:
		find = CheckDisplay('form')
	return find

def GetForm(name, nick = None):
	main = GetMain()
	if not nick:
		nick = '_'
	eve.FindChild(main, name, nick)
	return nick

def HasFormReg(rexstr):
	rex = re.compile(rexstr)
	main = GetMain()
	eve.Children(main, '_')
	l = eve.Len('_')
	result = None
	for i in range(l):
		eve.GetListItem('_', i, 'form')
		result = rex.match(eve.GetString('form', 'name'))
		if result:
			break

	if result and CheckDisplay('form'):
		return result.group(0)
	return None

