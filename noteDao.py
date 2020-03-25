# -*- coding: utf-8 -*-
from anki import notes

# class that handles adding new notes to the anki model
class NoteDao:
	def __init__(self, mw):
		self.mw = mw
		# instanciate the controller that retrives the furigana reading from the sentence

	# Create a new note
	def addNote(self, deckId, model, expression, meaning, reading):
		note = notes.Note(self.mw.col, model)
		note.model()['did'] = deckId
		note['Expression'] = expression
		note['Meaning'] = meaning
		note['Reading'] = reading
		self.mw.col.addNote(note)