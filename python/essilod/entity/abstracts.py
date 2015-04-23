from sessions import Session
from authors import HtmlAuthor
from authors import serializer as authorSerializer
from keywords import TextKeyword
from serializer import TurtleMapping
from utils import get_text_content, get_multiple_lines, fix_abstract_links
import re

class Abstract(object):
	
	def __init__(self,title=None,aid=None,authors=None,text=None,session=None,keywords=None,raw=None):
		self.title = title
		self.identifier = aid
		self.authors = [] if authors == None else authors
		self.authorCount = 0
		self.text = text
		self.session = session
		self.keywords = [] if keywords == None else keywords
		self.raw = raw
		self._cached_uri = None

	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		return "%s/%s" % (self.session.meeting.uri(),self.identifier)

class HtmlAbstract(Abstract):
	
	tags = ["HR:","AN:","TI:","AU:","EM:","AF:","AB:","DE:","SC:","JN:","MN:"]
	authorTags = ["EM:","AF:"]
	identifierRegex = re.compile("[A-Z]{1,3}\d{1,3}[A-Z]?\-\d{1,4}")
	htmlRegex = re.compile(r'<.*?>')

	def __init__(self,content,session,meeting,split=False):
		super(HtmlAbstract,self).__init__()
		self.content = content.split("\n") if not split else content
		self.raw = self.htmlRegex.sub('', ' '.join(content))
		self.session = session
		self.meeting = meeting
		self._parse()
	
	def _parse(self):
		idx = 0
		while idx < len(self.content):
			idx = self._parse_next(idx)
		if not self._validate():
			raise AbstractParseError()
		
	def _parse_next(self,idx):
		start = self.content[idx].strip()[0:3]
		if not start in self.tags:
			return idx+1
		elif start == "HR:":
			return self._parse_hour(idx)
		elif start == "AN:":
			return self._parse_identifier(idx)
		elif start == "TI:":
			return self._parse_title(idx)
		elif start == "AU:":
			return self._parse_author(idx)
		elif start == "AB:":
			return self._parse_text(idx)
		elif start == "DE:":
			return self._parse_keywords(idx)
		else:
			return idx+1
		
	def _parse_author(self,idx):
		idx, content = get_multiple_lines([tag for tag in self.tags if not tag in self.authorTags],idx,self.content)
		self.authorCount += 1
		author = HtmlAuthor(content,self)
		author.index = self.authorCount
		self.authors.append(author)
		return idx+1

	def _parse_hour(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.time = get_text_content("span",content)
		return idx+1

	def _parse_identifier(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		matches = self.identifierRegex.search(get_text_content("span",content))
		if matches == None:
			raise IgnoreAbstractError()
		else:
			self.identifier = matches.group(0)
			return idx+1
		
	def _parse_keywords(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.keywords.append(TextKeyword(get_text_content("span",content)))
		return idx+1			

	def _parse_text(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = get_text_content("span","<newline>".join(content.split("\n")))
		content = fix_abstract_links(content)
		if content == None:
			print self.content
		self.text = "\n".join(content.split("<newline>")).strip()
		return idx+1

	def _parse_title(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.title = get_text_content("span",content)
		return idx+1
	
	def _validate(self):
		self.session = self.session if self.session != None else Session(self.identifier.split('-')[0],None,None,None,None,None,self.meeting) if self.identifier != None else None
		return self.title != None and self.identifier != None and len(self.authors) > 0 and self.text != None and self.session != None

class IgnoreAbstractError(Exception):
	
	def __init__(self,msg=None):
		self.msg = msg

class AbstractParseError(Exception):
	
	def __init__(self,msg=None):
		self.msg = msg
		
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://abstractsearch.agu.org/ontology#Abstract"]
	},
	"raw" : {
		"type" : "literal",
		"predicate" : "http://abstractsearch.agu.org/ontology#raw",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"lang" : "en"
	},
	"title" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/title",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"lang" : "en"
	},
	"identifier" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/identifier"
	},
	"authors" : {
		"type" : "object",
		"predicate" : "http://tw.rpi.edu/schema/hasAgentWithRole",
		"recurse" : authorSerializer
	},
	"text" : {
		"type" : "literal",
		"predicate" : "http://swrc.ontoware.org/ontology#abstract",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"lang" : "en"
	},
	"session" : {
		"type" : "object",
		"predicate" : "http://data.semanticweb.org/ns/swc/ontology#relatedToEvent"
	},
	"keywords" : {
		"type" : "object",
		"predicate" : "http://data.semanticweb.org/ns/swc/ontology#hasTopic"
	}
}

serializer = TurtleMapping(mapping)
