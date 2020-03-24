# -*- coding: utf-8 -*-
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki import notes
from .reading import MecabController

#　create a new item in the tool menu
def createMenuItem():
	menuItem = QAction("文を読み込む", mw)
	menuItem.triggered.connect(openSettings)
	mw.form.menuTools.addAction(menuItem)

# open the import doalog
def openSettings():
	settings = QDialog(mw)
	# file path
	filePathLabel = QLabel()
	filePathLabel.setText("ファイル名")
	filePathText = QLineEdit();
	filePathText.setFixedWidth(200)
	filePathText.setText("C:/Users/Arthur/AppData/Roaming/Anki2/addons21/sentenceImportTool/sentences_example.txt")#("E:\Jap\phrases\phrases.txt")("C:/Users/Arthur/AppData/Roaming/Anki2/addons21/sentenceImportTool/sentences_example.txt")
	searchButton = QPushButton("検索")
	searchButton.clicked.connect(lambda: filePathText.setText(getFileName()))
	# sentence deck
	sentenceDeckLabel = QLabel()
	sentenceDeckLabel.setText("文デッキ名")
	sentenceDeckText = QLineEdit();
	sentenceDeckText.setFixedWidth(200)
	sentenceDeckText.setText("漢字と文::文")#("漢字と文::文")("TestSentence")
	#　MCD deck
	mcdDeckLabel = QLabel()
	mcdDeckLabel.setText("ＭＣＤデッキ名")
	mcdDeckText = QLineEdit();
	mcdDeckText.setFixedWidth(200)
	mcdDeckText.setText("漢字と文::MCD")#("漢字と文::MCD")("TestMCD")
	# button
	importButton = QPushButton("読み込む")
	importButton.clicked.connect(lambda: checkDeck(filePathText.text().strip(), sentenceDeckText.text().strip(), mcdDeckText.text().strip(), settings))
	importButton.setFixedWidth(100)
	cancelButton = QPushButton("キャンセル")
	cancelButton.clicked.connect(lambda: settings.hide())
	cancelButton.setFixedWidth(100)
	# Layouts
	# file path layout
	filePathLayout = QHBoxLayout()
	filePathLayout.addStretch()
	filePathLayout.addWidget(filePathLabel)
	filePathLayout.addWidget(filePathText)
	filePathLayout.addWidget(searchButton)
	# sentence deck layout
	sentenceDeckLayout = QHBoxLayout()
	sentenceDeckLayout.addStretch()
	sentenceDeckLayout.addWidget(sentenceDeckLabel)
	sentenceDeckLayout.addWidget(sentenceDeckText)
	sentenceDeckLayout.addStretch()
	# mcd deck layout
	mcdDeckLayout = QHBoxLayout()
	mcdDeckLayout.addStretch()
	mcdDeckLayout.addWidget(mcdDeckLabel)
	mcdDeckLayout.addWidget(mcdDeckText)
	mcdDeckLayout.addStretch()
	#button layout
	buttonLayout = QHBoxLayout()
	buttonLayout.addStretch()
	buttonLayout.addWidget(importButton)
	buttonLayout.addWidget(cancelButton)
	buttonLayout.addStretch()
	#Main layout
	mainLayout = QVBoxLayout()
	mainLayout.addLayout(filePathLayout)
	mainLayout.addLayout(sentenceDeckLayout)
	mainLayout.addLayout(mcdDeckLayout)
	mainLayout.addLayout(buttonLayout)
	#Load settings view
	settings.setWindowTitle("文をファイルから読み込む")
	settings.setLayout(mainLayout)
	settings.show()

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

# return the filepath from the file dialog
def getFileName():
	fileData = QFileDialog.getOpenFileName(caption="ファイルを選択してください");
	return fileData[0]

# check if at least one deck was selected
def checkDeck(filePath, sentenceDeckName, mcdDeckName, settings):
	if not sentenceDeckName and not mcdDeckName:
		showInfo("デッキを選択してください")
	else:
		importFile(filePath, sentenceDeckName, mcdDeckName, settings)

# process to import the selected file if it exists
# first read the data from the file and then call the function for creating the notes
def importFile(filePath, sentenceDeckName, mcdDeckName, settings):
	try:
		file = open(filePath, mode='r', encoding='utf8')
		settings.hide()
		progressWidget, progressBar = getProgressWidget()
		data = readFile(file)
		file.close()
		# add to different decks
		progressBar.setMinimum(0)
		progressBar.setMaximum(len(data))
		
		# retrieving the decks ids
		sentenceDeckId = -1
		mcdDeckId = -1
		if sentenceDeckName:
			sentenceDeckId = mw.col.decks.id(sentenceDeckName)
		if mcdDeckName:
			mcdDeckId = mw.col.decks.id(mcdDeckName)
		
		# insert the data in the decks
		model = mw.col.models.byName("Japanese (recognition)")
		count = 0
		countCard = 0
		for card in data:
			count += 1
			progressBar.setValue(count)
			mw.app.processEvents()
			if sentenceDeckName:
				countCard += 1
				addToSentenceDeck(sentenceDeckId, model, card[0], card[1])
			if mcdDeckName:
				countCard += 1
				addToMCDDeck(mcdDeckId, model, card[0], card[1])
		mw.reset()
		progressWidget.hide()
		showInfo('デッキに対して' + str(countCard) + '枚のカードが読み込まれました')
	except OSError:
		showInfo("ファイルが見つかりません")

# read the content of a file and set the retrieves the associate data
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

# Add the collected data to the sentence deck
def addToSentenceDeck(deckId, model, sentence, definition):
	# create note
	addNote(deckId, model, sentence, definition, mecab.reading(sentence))

# Add the collected data to the MCD deck
def addToMCDDeck(deckId, model, sentence, definition):
	# split the definition between answer and def
	defSplit = definition.split(';')
	# create note
	addNote(deckId, model, sentence + '<br/>' + defSplit[1], defSplit[0], mecab.reading(sentence))

# Create a new note
def addNote(deckId, model, expression, meaning, reading):
	note = notes.Note(mw.col, model)
	note.model()['did'] = deckId
	note['Expression'] = expression
	note['Meaning'] = meaning
	note['Reading'] = reading
	mw.col.addNote(note)

# instanciate the controller that retrives the furigana reading from the sentence
mecab = MecabController()
createMenuItem()