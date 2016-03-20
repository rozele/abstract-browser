from utils import get_text_content, get_multiple_lines, get_html_content
from people import Person, serializer as personSerializer
from organizations import Organization, serializer as organizationSerializer
from matcher.lookup import personLookup, organizationLookup
from serializer import TurtleMapping
import re

class Researcher(object):
	
	def __init__(self,person=None,affiliations=None,corresponding="false",index=0,abstract=None):
		self.person = person
		self.name = None
		self.email = None
		self.affiliations = [] if affiliations == None else affiliations
		self.corresponding = corresponding
		self.index = index
		self.abstract = abstract
		self._cached_uri = None

	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri
	
	def _uri(self):
		return "%s/researcher%d" % (self.abstract.uri(),self.index)
        			
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://tw.rpi.edu/schema/Researcher"]
	},
	"affiliations" : {
		"type" : "object",
		"predicate" : "http://tw.rpi.edu/schema/withAffiliation",
		"recurse" : organizationSerializer
	},
	"person" : {
		"type" : "object",
		"predicate" : "http://tw.rpi.edu/schema/hasRole",
		"reverse" : True,
		"recurse" : personSerializer
	},
	"index" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#positiveInteger",
		"predicate" : "http://tw.rpi.edu/schema/index"
	}
}

serializer = TurtleMapping(mapping)
