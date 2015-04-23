import re
from meetings import Meeting
from sections import Section
from conveners import HtmlConvener
from conveners import serializer as convenerSerializer
from serializer import TurtleMapping
from utils import get_text_content, get_multiple_lines, clean_conveners
	
class Session(object):
	
	identifierRegex = "([A-Z]{1,3})\d{1,3}[A-Z]?"
	
	def __init__(self,sid=None,name=None,loc=None,day=None,time=None,section=None,
				 meeting=None,conveners=None,cosponsors=None,stype=None,abstracts=[]):
		self.name = name
		self.identifier = sid
		self.location = loc
		self.time = time
		self.day = day
		self.meeting = meeting
		self.conveners = [] if conveners == None else conveners
		self.cosponsors = [] if cosponsors == None else cosponsors
		self.abstracts = [] if abstracts == None else abstracts
		self.type = stype
		self.section = section
		self._cached_uri = None
		
	def add_abstract(self,abstract):
		self.abstracts.append(abstract)
	
	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		return "%s/%s" % (self.meeting.uri(),self.identifier)

class SummarySession(Session):
	
	def __init__(self,content,meeting):
		super(SummarySession,self).__init__()
		self.meeting = meeting
		self.content = content
		self._parse()
	
	def _parse(self):
		content = self.content.split(':')
		self.section = Section(content[0])
		self.identifier = content[0] + content[1] + content[2]
		self.location = content[5]
		self.time = content[4]
		self._parse_name(content[6])
			
	def _parse_name(self,content):
		parts = re.split("<br\s?\/>",content)
		self.name = parts[0].strip()
		m = re.search("\(\s*joint\s+with\s+([A-Z]+(,\s?[A-Z]+))\)",self.name,flags=re.IGNORECASE)
		if m:
			self._parse_cosponsors(m.group(1))
	
	def _parse_cosponsors(self,content):
		for section in content.split(','):
			self.cosponsors.append(Section(section.strip()))
		
class HtmlSession(Session):
	
	tags = ["SS:","LO:","DA:","HR:","SN:","PR:","JN:","MN:"]
	
	def __init__(self,content,meeting,split=False):
		super(HtmlSession,self).__init__()
		self.meeting = meeting
		self.content = content.split("\n") if not split else content
		self._parse()
	
	def _parse(self):
		idx = 0
		while idx < len(self.content):
			idx = self._parse_next(idx)
		if not self._validate():
			raise SessionParseError("val")
		
	def _parse_next(self,idx):
		start = self.content[idx].strip()[0:3]
		if not start in self.tags:
			return idx+1
		elif start == "SS:":
			return self._parse_identifier(idx)
		elif start == "LO:":
			return self._parse_location(idx)
		elif start == "DA:":
			return self._parse_day(idx)
		elif start == "HR:":
			return self._parse_hour(idx)
		elif start == "SN:":
			return self._parse_name(idx)
		elif start == "PR:":
			return self._parse_conveners(idx)
		elif start == "JN:":
			return self._parse_journal(idx)
		else:
			return idx+1
	
	def catch(self):
		return
		
	def _parse_conveners(self,idx):
		#if self.identifier == "IN13A":
		#	self.catch()
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		content = clean_conveners(content)
		self.conveners = [HtmlConvener(s.strip(),self) for s in get_text_content("span",content).split(";")]
		count = 1
		for convener in self.conveners:
			convener.index = count
			count += 1
		return idx+1
		
	def _parse_day(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.day = get_text_content("span",content)
		return idx+1
	
	def _parse_hour(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.hour = get_text_content("span",content)
		return idx+1
		
	def _parse_identifier(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		matches = re.search(self.identifierRegex,content)
		if matches == None:
			print content
			raise SessionParseError("id")
		else:
			self.identifier = matches.group(0)
			self.section = Section(matches.group(1),None,"OS" in self.meeting.code)
			return idx+1
	
	def _parse_journal(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.journal = get_text_content("span",content)
		return idx+1	

	def _parse_location(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.location = get_text_content("span",content)
		return idx+1
	
	def _parse_name(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.name = get_text_content("span",content)
		
		return idx+1
	
	def _validate(self):
		return self.identifier != None and self.name != None and self.meeting != None and self.section != None
		
class SessionParseError(Exception):

	def __init__(self,msg=None):
		self.msg = msg
		
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://data.semanticweb.org/ns/swc/ontology#SessionEvent"]
	},
	"name" : {
		"type" : "literal",
		"predicate" : "http://swrc.ontoware.org/ontology#eventTitle",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"lang" : "en"
	},
	"identifier" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/identifier"
	},
	"conveners" : {
		"type" : "object",
		"predicate" : "http://tw.rpi.edu/schema/hasAgentWithRole",
		"recurse" : convenerSerializer
	},
	"meeting" : {
		"type" : "object",
		"predicate" : "http://data.semanticweb.org/ns/swc/ontology#isSubEventOf"
	},
	"section" : {
		"type" : "object",
		"predicate" : "http://abstractsearch.agu.org/ontology#section"
	},
	"cosponsors" : {
		"type" : "object",
		"predicate" : "http://abstractsearch.agu.org/ontology#cosponsor"
	}
}

serializer = TurtleMapping(mapping)
