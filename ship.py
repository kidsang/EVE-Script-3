import time
import shortcut as sc
from util import *

cache = {}

def GetShipUI():
	shipui = 'shipui'
	if shipui not in cache:
		eve.GetAttr('layer', 'shipui')
		cache[shipui] = shipui
	return shipui

def GetShipSr():
	shipsr = 'shipuisr'
	if shipsr not in cache:
		shipui = GetShipUI()
		eve.GetAttr(shipui, 'sr', shipsr)
		cache[shipsr] = shipsr
	return shipsr

def Ready():
	shipui = GetShipUI()
	return eve.GetBool(shipui, 'shipuiReady')

def Shield():
	shipui = GetShipUI()
	return eve.GetDouble(shipui, 'lastShield')

def Armor():
	shipui = GetShipUI()
	return eve.GetDouble(shipui, 'lastArmor')

def Structure():
	shipui = GetShipUI()
	return eve.GetDouble(shipui, 'lastStructure')

def Speed():
	shipui = GetShipUI()
	return eve.GetString(shipui, 'lastSpeed')

def Stop():
	sr = GetShipSr()
	eve.GetAttr(sr, 'stopButton', '_')
	eve.Click('_')

def Warping():
	sr = GetShipSr()
	eve.GetAttr(sr, 'speedStatus', '_')
	return eve.GetString('_', 'text') == '<center>(Warping)'

def GetSlot(s, i):
	slot = 'shipui_slot_' + str(s) + '_' + str(i)
	slotName = 'inFlight'
	if s == 0:
		slotName += 'LowSlot'
	elif s == 1:
		slotName += 'MediumSlot'
	else:
		slotName += 'HighSlot'
	slotName += str(i + 1)

	sr = GetShipSr()
	eve.GetAttr(sr, 'slotsContainer', '_')
	eve.FindChild('_', slotName, slot)
	return slot

def ClickSlot(slot):
	eve.Click(slot, 30, 40)

def SlotActivated(slot):
	eve.FindChild(slot, 'glow', '_')
	return eve.GetBool('_', 'display')

def SlotBusy(slot):
	eve.FindChild(slot, 'busy', '_')
	return eve.GetBool('_', 'display')

def TurnOnSlot(s, i):
	Log('Turn on slot ' + str(s) + ' ' + str(i), 1)
	slot = GetSlot(s, i)
	if not SlotActivated(slot):
		while SlotBusy(slot):
			time.sleep(0.2)
		ClickSlot(slot)
	Log('end', -1)

def TurnOffSlot(s, i):
	Log('Turn off slot ' + str(s) + ' ' + str(i), 1)
	slot = GetSlot(s, i)
	while SlotActivated(slot):
		ClickSlot(slot)
	Log('end', -1)

