import hashlib

from serializer import TurtleMapping
from utils import config,urify_name

class Organization(object):
	
	def __init__(self,location,authorships=None,convenerships=None,identifier=None):
		self.location = location
		self.identifier = identifier
		self.authorships = [] if authorships == None else authorships
		self.convenerships = [] if convenerships == None else convenerships
		self.sha1 = self.hash()
		self._cached_uri = None

        def hash(self):
		sha1 = hashlib.sha1()
		sha1.update(self.location)
		return "urn:x-org:%s" % (sha1.hexdigest())

	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri

	def _uri(self):
		if len(self.authorships) > 0:
			return "%s/affiliation" % (self.authorships[0].uri())
		elif len(self.convenerships) > 0:
			return "%s/affiliation" % (self.convenerships[0].uri())
		elif self.identifier != None:
			return self.identifier
		
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://xmlns.com/foaf/0.1/Organization"]
	},
        "sha1" : {
		"type" : "resource",
		"predicate" : "http://abstractsearch.agu.org/ontology#organizationHash", 
	},
	"location" : {
		"type" : "literal",
		"predicate" : "http://purl.org/dc/terms/description",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string"
	}
}

serializer = TurtleMapping(mapping)
