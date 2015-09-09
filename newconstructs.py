INPUT_FILE = "input_1_kwynn.html"

# Kwynn Buess 2015/09/08 for New Constructs - see README

import codecs
import json
from html.parser import HTMLParser
from collections import OrderedDict

rawFileHTML = codecs.open (INPUT_FILE, 'r','cp1252').read() # if not codecs, you'll get Kwynn-utf8-error-2308

class MyHTMLParser(HTMLParser):

	def __init__(self):

		super().__init__()  # if skip this, you'll get Kwynn-rawdata-error-2049
		
		self.wholeFileTextStr = ""
		self.divStr 	      = ""  # temporary for each div's text
		self.divStrStartIndex = 0
		self.inTable   		  = False
		self.paragraphArray   = []
		
	def handle_starttag(self, tag, attrs):
		if tag == 'table' : self.inTable = True
		if tag == 'div'   :	self.divStrStartIndex = len(self.wholeFileTextStr)

	def handle_endtag(self, tag):
		if tag == 'td'    : self.wholeFileTextStr += ' '    
		if tag == 'tr'	  : self.wholeFileTextStr += "\n\n"
		if tag == 'table' : self.inTable = False
		if tag == 'div'   : 

			divStrLen = len(self.divStr)
			if divStrLen == 0 : return
			
			if '$' in self.divStr : 
				self.paragraphArray.append(
										OrderedDict(
												[('text' , self.divStr),('start', self.divStrStartIndex),('end'  , self.divStrStartIndex + divStrLen)]
										)
									)
			
			self.wholeFileTextStr += "\n\n"
			self.divStr = ""

	def handle_data(self, rawText):    # data as in "leaf," raw text, no HTML left, aka inner text or leaf innerHTML
		self.wholeFileTextStr 			  += rawText
		if not self.inTable : self.divStr += rawText

# END HTMLParser class ********

# ********** "MAIN" ***********
myHTMLparser = MyHTMLParser()
myHTMLparser.feed(rawFileHTML)
with open('document.txt'  , 'w') as f: f.write(myHTMLparser.wholeFileTextStr)
with open('paragraphs.txt', 'w') as f: f.write(json.dumps(myHTMLparser.paragraphArray, sort_keys=False, indent=4))
