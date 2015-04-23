from utils import get_text_content, get_multiple_lines, get_html_content
from people import Person, serializer as personSerializer
from organizations import Organization, serializer as organizationSerializer
from matcher.lookup import personLookup, organizationLookup
from serializer import TurtleMapping
import re

class Author(object):
	
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
		return "%s/author%d" % (self.abstract.uri(),self.index)
	
class HtmlAuthor(Author):
	
	tags = ["AU:","EM:","AF:"]	
	
	def __init__(self,content,abstract,split=False):
		super(HtmlAuthor,self).__init__()
		self.abstract = abstract
		self.content = content.split("\n") if not split else content
		self._parse()
		
	def _parse(self):
		idx = 0
		while idx < len(self.content):
			idx = self._parse_next(idx)
		if not self._validate():
			raise AuthorParseError
		else:
			self._conflate_person()
	
	def _conflate_organization(self):
		if len(self.affiliations) > 0:
			existingOrganization = organizationLookup.get(self.affiliations[0].location)
			if existingOrganization != None:
				self.affiliations = [existingOrganization]
			else:
				organizationLookup.add(self.affiliations[0])
	
	def _conflate_person(self):
		self.person = Person(self.name,self.email)
		self.person.authorships.append(self)
	
	def _parse_next(self,idx):
		start = self.content[idx].strip()[0:3]
		if not start in self.tags:
			return idx+1
		elif start == "AU:":
			return self._parse_name(idx)
		elif start == "EM:":
			return self._parse_email(idx)
		elif start == "AF:":
			return self._parse_affiliation(idx)
		else:
			return idx+1
	
	def _parse_affiliation(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		content = get_html_content("span","af",content,True).strip()
		organization = Organization(content)
		organization.authorships.append(self)
		self.affiliations.append(organization)
		return idx+1
	
	def _parse_email(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.email = get_text_content("span",content)
		return idx+1
		
	def _parse_name(self,idx):
		idx, content = get_multiple_lines(self.tags,idx,self.content)
		content = " ".join(content.split("\n"))
		self.name = get_text_content("span",content)
		regex = "\*\s*(.*)"
		self.corresponding = re.match(regex,self.name)
		self.name = self.name if not self.corresponding else self.corresponding.group(1)
		self.corresponding = "true" if self.corresponding != None else "false"
		return idx+1
	
	def _validate(self):
		return self.name != None
		
mapping = {
	"__rdftype__" : {
		"type" : "resource",
		"predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
		"values" : ["http://tw.rpi.edu/schema/Author"]
	},
	"corresponding" : {
		"type" : "literal",
		"datatype" : "http://www.w3.org/2001/XMLSchema#boolean",
		"predicate" : "http://abstractsearch.agu.org/ontology#isCorrespondingAuthor",

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
