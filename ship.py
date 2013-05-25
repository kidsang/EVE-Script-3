import shortcut as sc

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

