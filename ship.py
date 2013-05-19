import shortcut as sc

catch = {}

def GetShipUI():
	shipui = 'shipui'
	if shipui not in catch:
		eve.GetAttr('layer', 'shipui')
		catch[shipui] = shipui
	return shipui

def GetShipSr():
	shipsr = 'shipuisr'
	if shipsr not in catch:
		shipui = GetShipUI()
		eve.GetAttr(shipui, 'sr', shipsr)
		catch[shipsr] = shipsr
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

