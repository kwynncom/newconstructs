INPUT_FILE = "input_1_kwynn.html"

# Kwynn Buess 2015/09/19 11:12pm EDT for New Constructs - less "len()" calls

import codecs, json
from html.parser import HTMLParser ; from collections import OrderedDict


rawFileHTML = codecs.open (INPUT_FILE, 'r','cp1252').read()


class docClass :
	def __init__(self):
		self.wholeStr  = '' ; self.wholeLen  = 0
		self.divStr    = '' ; self.divLen    = 0
		self.hasDollar = False
		
	def cat(self, strIN, isDiv = False):
		tempLen          = len(strIN.encode('utf-8'))
		self.wholeStr   += strIN ; self.wholeLen   += tempLen
		if isDiv : 	   
			self.divStr += strIN ; self.divLen     += tempLen
			if not self.hasDollar and '$' in strIN : self.hasDollar = True 

	def resetDiv(self): self.divStr = '' ; self.divLen = 0 ; self.hasDollar = False
		
	def getWholeStr(self):  return self.wholeStr ; 
	def getWholeLen(self):  return self.wholeLen
	def getDivStr(self):    return self.divStr
	def getDivLen(self):    return self.divLen	
	def getHasDollar(self): return self.hasDollar

class MyHTMLParser(HTMLParser):

	def __init__(self):
		super().__init__()
		self.divStrStartIndex = 0
		self.inTable          = False
		self.paragraphArray   = []
		self.docO             = docClass()
		
	def handle_starttag(self, tag, attrs):
		if tag == 'table' : self.inTable = True
		if tag == 'div'   : self.divStrStartIndex = self.docO.getWholeLen()

	def handle_endtag(self, tag):
		if tag == 'table' : self.inTable = False
		if tag == 'td'    : self.docO.cat(' ')    
		if tag == 'tr'	  : self.docO.cat("\n\n")
		if tag == 'div'   : 
			if (self.docO.getDivLen() == 0) : return
			if self.docO.getHasDollar() : self.newPara()
			self.docO.cat("\n\n")
			self.docO.resetDiv()

	def handle_data(self, rawText):	self.docO.cat(rawText, not self.inTable)

	def newPara(self):
		self.paragraphArray.append(
			OrderedDict(
					[  
						('text' , self.docO.getDivStr()), 
						('start', self.divStrStartIndex), 
						('end'  , self.divStrStartIndex + self.docO.getDivLen() - 1)
					]
			)
		)
# END HTMLParser class ********

# ********** "MAIN" ***********
myHTMLparser = MyHTMLParser() ; myHTMLparser.feed(rawFileHTML)
with open('document.txt'  , 'w') as f: f.write(myHTMLparser.docO.getWholeStr())
with open('paragraphs.txt', 'w') as f: f.write(json.dumps(myHTMLparser.paragraphArray, sort_keys=False, indent=4))
