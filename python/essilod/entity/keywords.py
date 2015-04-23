from utils import config
from serializer import TurtleMapping
import re

class Keyword(object):
	
	def __init__(self,identifier,name=None,related=None,parent=None):
		self.identifier = identifier
		self.name = name
		self.related = related
		self.parent = parent
		self._cached_uri = None
	
	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		if not self.identifier:
			return None
		else:
			return "%skeywords/%s" % (config["base"],self.identifier) 
		
class TextKeyword(Keyword):
	
	def __init__(self,text):
		self._cached_uri = None
		self.identifier = None
		match = re.match("^\[?(\d{4})\]?(.*?)(\((\d{4}(,\s*\d{4})*)\))?$",text)
		if match:
			self.identifier = match.group(1)
			self.name = match.group(2).strip()
			self.related = [Keyword(i.strip()) for i in match.group(4).split(",")] if match.group(4) != None else None
			self.parent = Keyword(self.identifier[0:2] + "00") if self.identifier[2:4] != "00" else None

mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://swrc.ontoware.org/ontology#ResearchTopic"]
	},
	"name" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/subject",
		"lang" : "en"
	},
	"identifier" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/identifier",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
	},
	"related" : {
		"type" : "object",
		"predicate" : "http://www.w3.org/2004/02/skos/core#related"
	},
	"parent" : {
		"type" : "object",
		"predicate" : "http://www.w3.org/2004/02/skos/core#broadMatch"
	}
}

serializer = TurtleMapping(mapping)
