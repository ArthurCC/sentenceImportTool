# -*- coding: utf-8 -*-
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki import notes
from .reading import MecabController

def createMenuItem():
	menuItem = QAction("文を読み込む", mw)
	menuItem.triggered.connect(openSettings)
	mw.form.menuTools.addAction(menuItem)

def openSettings():
	settings = QDialog(mw)
	# file path
	filePathLabel = QLabel()
	filePathLabel.setText("ファイル名")
	filePathText = QLineEdit();
	filePathText.setFixedWidth(200)
	filePathText.setText("E:\Jap\phrases\phrases.txt")
	searchButton = QPushButton("検索")
	searchButton.clicked.connect(lambda: filePathText.setText(getFileName()))
	# button
	importButton = QPushButton("読み込む")
	importButton.clicked.connect(lambda: importFile(filePathText.text(), settings))
	importButton.setFixedWidth(100)
	cancelButton = QPushButton("キャンセル")
	cancelButton.clicked.connect(lambda: settings.hide())
	cancelButton.setFixedWidth(100)
	# Layouts
	#file path layout
	filePathLayout = QHBoxLayout()
	filePathLayout.addStretch()
	filePathLayout.addWidget(filePathLabel)
	filePathLayout.addWidget(filePathText)
	filePathLayout.addWidget(searchButton)
	#button layout
	buttonLayout = QHBoxLayout()
	buttonLayout.addStretch()
	buttonLayout.addWidget(importButton)
	buttonLayout.addWidget(cancelButton)
	buttonLayout.addStretch()
	#Main layout
	mainLayout = QVBoxLayout()
	mainLayout.addLayout(filePathLayout)
	mainLayout.addLayout(buttonLayout)
	#Load settings view
	settings.setWindowTitle("文をファイルから読み込む")
	settings.setLayout(mainLayout)
	settings.show()

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

def getFileName():
	fileData = QFileDialog.getOpenFileName(caption="ファイルを選択してください");
	return fileData[0]

def importFile(filePath, settings):
	settings.hide()
	progressWidget, progressBar = getProgressWidget()
	try:
		file = open(filePath, mode='r', encoding='utf8')
		data = readFile(file)
		file.close()
		# add to different decks
		progressBar.setMinimum(0)
		progressBar.setMaximum(len(data))
		deckTestId = mw.col.decks.id('漢字と文::文')
		deckTestMCDId = mw.col.decks.id('漢字と文::MCD')
		model = mw.col.models.byName("Japanese (recognition)")
		count = 0
		for card in data:
			count += 1
			progressBar.setValue(count)
			mw.app.processEvents()
			addToSentenceDeck(deckTestId, model, card[0], card[1])
			addToMCDDeck(deckTestMCDId, model, card[0], card[1])
		mw.reset()
		progressWidget.hide()
		showInfo('デッキに対して' + str(len(data)) + '枚のカードが読み込まれました')
	except OSError:
		showInfo("ファイルが見つかりません")

def readFile(file):
	isSentenceLine = True
	data = []
	sentence = ''
	definition = ''
	for line in file:
		line = line.strip()
		# If line empty we add the preceding sentence and definition
		if not line:
			data.append([sentence, definition])
			sentence = ''
			definition = ''
			isSentenceLine = True
		# Otherwise we set up the sentence or definition
		else:
			if isSentenceLine:
				sentence = line
				isSentenceLine = False
			else:
				definition += line + '<br/>'
	data.append([sentence, definition])
	return data

def addToSentenceDeck(deckId, model, sentence, definition):
	# create note
	addNote(deckId, model, sentence, definition, mecab.reading(sentence))

def addToMCDDeck(deckId, model, sentence, definition):
	# split the definition between answer and def
	defSplit = definition.split(';')
	# create note
	addNote(deckId, model, sentence + '<br/>' + defSplit[1], defSplit[0], mecab.reading(sentence))
	
def addNote(deckId, model, expression, meaning, reading):
	note = notes.Note(mw.col, model)
	note.model()['did'] = deckId
	note['Expression'] = expression
	note['Meaning'] = meaning
	note['Reading'] = reading
	mw.col.addNote(note)
	
mecab = MecabController()
createMenuItem()