from utils import config
from serializer import TurtleMapping

def nameLookup(abbr):
	return config["meeting_codes"][abbr] if abbr in config["meeting_codes"] else None

def yearLookup(abbr):
	year = int(abbr[2:])
	return year + 1900 if year > 95 else year + 2000
	
class Meeting(object):
		
	def __init__(self,abbr):
		self.name = nameLookup(abbr[0:2])
		self.year = yearLookup(abbr)
		self.code = abbr[0:2].upper()
		self._cached_uri = None
	
	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		return "%smeetings/%d/%s" % (config["base"],self.year,self.code)

mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://swrc.ontoware.org/ontology#Meeting"]
	},
	"name" : {
		"type" : "literal",
		"predicate" : "http://swrc.ontoware.org/ontology#eventTitle",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"lang" : "en"
	},
	"year" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#gYear",
		"predicates" : [
			"http://swrc.ontoware.org/ontology#year"
		]	
	},
	"code" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"predicates" : [
			"http://abstractsearch.agu.org/ontology#meetingCode"
		]
	}
}

serializer = TurtleMapping(mapping)
