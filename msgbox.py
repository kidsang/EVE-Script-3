
from util import *

cache = {}

def GetModalLayer():
	modal = 'modal_layer'
	if modal not in cache:
		eve.GetAttr('layer', 'modal', modal)
		cache[modal] = modal
	return modal

def HasMsgBox():
	layer = GetModalLayer()
	return HasChild(layer, 'l_modal_modal')

def GetMsgBox():
	box = 'modal_msg_box'
	layer = GetModalLayer()
	eve.FindChild(layer, 'l_modal_modal', '_')
	eve.FindChild('_', 'modal', box)
	return box

def GetTitle(box):
	eve.FindChild(box, '__maincontainer', '_')
	eve.FindChild('_', 'topParent', '_')
	eve.FindChild('_', 'EveCaptionLarge', '_')
	return eve.GetString('_', 'text')

def GetBtns(box):
	btns = 'modal_msg_box_btns'
	eve.FindChild(box, '__maincontainer', '_')
	eve.FindChild(box, 'bottom', '_')
	eve.FindChild(box, 'btnsmainparent', '_')
	eve.FindChild(box, 'btns', btns)
	return btns

def Confirm(box):
	btns = GetBtns(box)
	eve.FindChild(btns, 'Yes_Btn', '_')
	eve.Click('_')

def Close(box):
	CloseWnd(box)
