# -*- coding: utf-8 -*-
from aqt.qt import *
# open the dialog for the progress bar
def getProgressWidget():
	progressWidget = QWidget(None)
	layout = QVBoxLayout()
	progressWidget.setFixedSize(400, 35)
	progressWidget.setWindowModality(Qt.ApplicationModal)
	progressWidget.setWindowTitle("読み込み中…")
	bar = QProgressBar(progressWidget)
	bar.setFixedSize(380, 30)
	bar.move(1,1)
	per = QLabel(bar)
	per.setAlignment(Qt.AlignCenter)
	progressWidget.show()
	return progressWidget, bar;