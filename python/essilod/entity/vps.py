from utils import config
from serializer import TurtleMapping

def nameLookup(abbr,index):
	return config["meeting_codes"][abbr] + " " + index if abbr in config["meeting_codes"] else None

def yearLookup(year):
	return year + 1900 if year > 95 else year + 2000
	
class VirtualPosterShowcase(object):
		
	def __init__(self,abbr,index):
		self.name = nameLookup(abbr[0:-2],index)
		self.index = index
		self.year = yearLookup(int(abbr[-2:]))
		self.code = abbr[0:-2].upper()
		self._cached_uri = None
	
	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		return "%svps/%d/%s" % (config["base"],self.year,self.index)

mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://abstractsearch.agu.org/ontology#VirtualPosterShowcase"]
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
