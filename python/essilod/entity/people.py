from utils import config,urify_name
from serializer import TurtleMapping
from BeautifulSoup import BeautifulSoup
import re

class Person(object):
	
	def __init__(self,name=None,email=None,authorships=None,convenerships=None,identifier=None):
		self.email = re.match("[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",email) if email != None else None
		self.email = self.email.group(0) if self.email != None else None
		self.name = name
		self.authorships = [] if authorships == None else authorships
		self.convenerships = [] if convenerships == None else convenerships
		self.identifier = identifier
		self._cached_uri = None

	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri
	
	def _uri(self):
		if self.email != None:
			return "%speople/%s" % (config["base"],self.email.lower())
		elif len(self.authorships) > 0:
			return "%speople/%s%s_%s_author%s" % (
				config["base"],
				self.authorships[0].abstract.session.meeting.code,
				str(self.authorships[0].abstract.session.meeting.year)[2:4],
				self.authorships[0].abstract.identifier,
				self.authorships[0].index
			)
		elif len(self.convenerships) > 0:
			return "%speople/%s%s_%s_convener%s" % (
				config["base"],
				self.convenerships[0].session.meeting.code,
				str(self.convenerships[0].session.meeting.year)[2:4],
				self.convenerships[0].session.identifier,
				self.convenerships[0].index
			)
		elif self.identifier != None:
			return self.identifier
			
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://xmlns.com/foaf/0.1/Person"]
	},
	"name" : {
		"type" : "literal",
		"predicate" : "http://xmlns.com/foaf/0.1/name",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string"
	},
	"email" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#string",
		"predicate" : "http://xmlns.com/foaf/0.1/mbox"
	},
}

serializer = TurtleMapping(mapping)
