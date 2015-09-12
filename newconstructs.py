INPUT_FILE = "input_1_kwynn.html"

# Kwynn Buess 2015/09/11 for New Constructs - UNICODE FIXES - then whitespace (x2)

import codecs
import json
from html.parser import HTMLParser
from collections import OrderedDict

rawFileHTML = codecs.open (INPUT_FILE, 'r','cp1252').read()

class MyHTMLParser(HTMLParser):

	def __init__(self):

		super().__init__()
		
		self.wholeFileTextStr = ""
		self.divStr 	      = ""  # temporary for each div's text
		self.divStrStartIndex = 0
		self.inTable		  = False
		self.paragraphArray   = []
		
	def handle_starttag(self, tag, attrs):
		if tag == 'table' : self.inTable = True
		if tag == 'div'   : self.divStrStartIndex = len(self.wholeFileTextStr.encode('utf-8'))

	def handle_endtag(self, tag):
		if tag == 'td'    : self.wholeFileTextStr += ' '    
		if tag == 'tr'	  : self.wholeFileTextStr += "\n\n"
		if tag == 'table' : self.inTable = False
		if tag == 'div'   : 

			divStrLen    =  len(self.divStr.encode('utf-8'))
			if divStrLen == 0 : return
			
			if '$' in self.divStr : 
				self.paragraphArray.append(
						OrderedDict(
								[  
									('text' , self.divStr), 
									('start', self.divStrStartIndex), 
									('end', self.divStrStartIndex + divStrLen)  
								]
						)
					)
			
			self.wholeFileTextStr += "\n\n"
			self.divStr = ""

	def handle_data(self, rawText):
		self.wholeFileTextStr			  += rawText
		if not self.inTable : self.divStr += rawText

# END HTMLParser class ********

# ********** "MAIN" ***********
myHTMLparser = MyHTMLParser()
myHTMLparser.feed(rawFileHTML)
with open('document.txt'  , 'w') as f: f.write(myHTMLparser.wholeFileTextStr)
with open('paragraphs.txt', 'w') as f: f.write(json.dumps(myHTMLparser.paragraphArray, sort_keys=False, indent=4))
