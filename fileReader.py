# -*- coding: utf-8 -*-
# read file from filepath and setup the data
def readFile (filePath):
	try:
		file = open(filePath, mode='r', encoding='utf8')
	except OSError:
		raise
	else:
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