from people import Person, serializer as personSerializer
from organizations import Organization, serializer as organizationSerializer
from matcher.lookup import personLookup, organizationLookup
from serializer import TurtleMapping

class Convener(object):
	
	def __init__(self,person=None,index=0,affiliations=None,session=None):
		self.person = person
		self.name = None
		self.email = None
		self.affiliations = [] if affiliations == None else affiliations
		self.index = index
		self.session = session
		self._cached_uri = None

	def uri(self):
		if self._cached_uri == None:
			self._cached_uri = self._uri()
		return self._cached_uri
	
	def _uri(self):
		return "%s/convener%d" % (self.session.uri(),self.index)
		
class HtmlConvener(Convener):
	
	def __init__(self,content,session):
		super(HtmlConvener,self).__init__()
		self.session = session
		convenerInfo = [s.strip() for s in content.split(",")]
		self.name = convenerInfo[0]
		organization = Organization(", ".join(convenerInfo[1:]))
		organization.convenerships.append(self)
		self.affiliations = [organization]
		self.person = Person(self.name)
		self.person.convenerships.append(self)
	
	def _conflate_organization(self,location):
		existingOrganization = organizationLookup.get(location)
		if existingOrganization != None:
			self.affiliations = [existingOrganization]
		else:
			organization = Organization(location)
			organizationLookup.add(organization)
			self.affiliations = [organization]
	
	def _conflate_person(self):
		self.person = Person(self.name)
		self.person.convenerships.append(self)
		existingPerson = personLookup.get(self.person.uri())
		if existingPerson == None:
			personLookup.add(self.person)
		else:
			self.person = existingPerson
			self.person.convenerships.append(self)
			
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://abstractsearch.agu.org/ontology#ConvenerRole"]
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
		"recurse": personSerializer
	},
	"index" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#positiveInteger",
		"predicate" : "http://tw.rpi.edu/schema/index"
	}
}

serializer = TurtleMapping(mapping)
