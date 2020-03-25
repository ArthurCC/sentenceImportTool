# -*- coding: utf-8 -*-
# import the main window object (mw) from aqt
from aqt import mw
from .settingsDialog import SettingsDialog
from aqt.qt import *

#　create a new item in the tool menu
def createMenuItem():
	menuItem = QAction("文を読み込む", mw)
	settings = SettingsDialog(mw)
	menuItem.triggered.connect(lambda: settings.openSettings())
	mw.form.menuTools.addAction(menuItem)

createMenuItem()