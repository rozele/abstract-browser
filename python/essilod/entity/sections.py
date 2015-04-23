from utils import config
from serializer import TurtleMapping

class Section(object):
	
	def __init__(self,identifier,name=None,os=False):
		self.identifier = identifier
		self.name = name
		self.os = os
		self._cached_uri = None
		
	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		if self.os:
			return "%ssections/OS/%s" % (config["base"],self.identifier)
		else: 
			return "%ssections/%s" % (config["base"],self.identifier)

mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://abstractsearch.agu.org/ontology#Section"]
	},
	"name" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/title",
		"lang" : "en"
	},
	"identifier" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/identifier",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
	}
}

serializer = TurtleMapping(mapping)
