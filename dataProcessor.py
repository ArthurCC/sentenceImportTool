# -*- coding: utf-8 -*-
# import the "show info" tool from utils.py
from aqt.utils import showInfo
from .noteDao import NoteDao
from .fileReader import readFile
from .progressWidget import getProgressWidget
from aqt.utils import showInfo
from .reading import MecabController

# Process the data from the file
class DataProcessor:
	def __init__(self, mw):
		self.mw = mw
		self.noteDao = NoteDao(mw)
		self.mecab = MecabController()
	
	# process to import the selected file if it exists
	# first read the data from the file and then call the function for creating the notes
	def importFile(self, filePath, sentenceDeckName, mcdDeckName, settings):
		progressWidget, progressBar = getProgressWidget()
		try:
			data = readFile(filePath)
		except:
			progressWidget.hide()
			showInfo("ファイルが見つかりません")
		else:
			settings.hide()
			# add to different decks
			progressBar.setMinimum(0)
			progressBar.setMaximum(len(data))
			
			# retrieving the decks ids
			sentenceDeckId = -1
			mcdDeckId = -1
			if sentenceDeckName:
				sentenceDeckId = self.mw.col.decks.id(sentenceDeckName)
			if mcdDeckName:
				mcdDeckId = self.mw.col.decks.id(mcdDeckName)
			
			# insert the data in the decks
			model = self.mw.col.models.byName("Japanese (recognition)")
			count = 0
			countCard = 0
			for card in data:
				count += 1
				progressBar.setValue(count)
				self.mw.app.processEvents()
				if sentenceDeckName:
					countCard += 1
					self.noteDao.addNote(sentenceDeckId, model, card[0], card[1], self.mecab.reading(card[0]))
				if mcdDeckName:
					countCard += 1
					# split the definition between answer and def
					defSplit = card[1].split(';')
					# the expression becomes the sentence + definition without the word
					# the meaning becomes the word to learn
					sentence = card[0] + '<br/>' + defSplit[1]
					self.noteDao.addNote(mcdDeckId, model, sentence, defSplit[0], self.mecab.reading(card[0]))
			self.mw.reset()
			progressWidget.hide()
			showInfo('デッキに対して' + str(countCard) + '枚のカードが読み込まれました')