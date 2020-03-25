# -*- coding: utf-8 -*-~
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from .dataProcessor import DataProcessor

# class settings dialog that handles the dialog settings to import the file, and define the decks in which we will create sentence notes
class SettingsDialog:
	def __init__(self, mw):
		self.mw = mw
		self.processor = DataProcessor(mw)
	
	# open the import dialog
	def openSettings(self):
		settings = QDialog(self.mw)
		# file path
		filePathLabel = QLabel()
		filePathLabel.setText("ファイル名")
		filePathText = QLineEdit();
		filePathText.setFixedWidth(200)
		filePathText.setText("C:/Users/Arthur/AppData/Roaming/Anki2/addons21/sentenceImportTool/sentences_example.txt")#("E:\Jap\phrases\phrases.txt")("C:/Users/Arthur/AppData/Roaming/Anki2/addons21/sentenceImportTool/sentences_example.txt")
		searchButton = QPushButton("検索")
		searchButton.clicked.connect(lambda: filePathText.setText(self.getFileName()))
		# sentence deck
		sentenceDeckLabel = QLabel()
		sentenceDeckLabel.setText("文デッキ名")
		sentenceDeckText = QLineEdit();
		sentenceDeckText.setFixedWidth(200)
		sentenceDeckText.setText("TestSentence")#("漢字と文::文")("TestSentence")
		#　MCD deck
		mcdDeckLabel = QLabel()
		mcdDeckLabel.setText("ＭＣＤデッキ名")
		mcdDeckText = QLineEdit();
		mcdDeckText.setFixedWidth(200)
		mcdDeckText.setText("TestMCD")#("漢字と文::MCD")("TestMCD")
		# button
		importButton = QPushButton("読み込む")
		importButton.clicked.connect(lambda: self.checkDeck(filePathText.text().strip(), sentenceDeckText.text().strip(), mcdDeckText.text().strip(), settings))
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

	@staticmethod
	# return the filepath from the file dialog
	def getFileName():
		fileData = QFileDialog.getOpenFileName(caption="ファイルを選択してください");
		return fileData[0]

	# check if at least one deck was selected, if so we process to the file reading
	def checkDeck(self, filePath, sentenceDeckName, mcdDeckName, settings):
		if not sentenceDeckName and not mcdDeckName:
			showInfo("デッキを選択してください")
		else:
			self.processor.importFile(filePath, sentenceDeckName, mcdDeckName, settings)