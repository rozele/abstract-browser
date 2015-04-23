from SPARQLWrapper import SPARQLWrapper, JSON
from ..organizations import Organization
import types

class PersonLookup(object):

	def __init__(self):
		self._lookup = {}
	
	def add(self,person):
		if not person.uri() in self._lookup:
			self._lookup[person.uri()] = person

	def get(self,uri=None):
		if uri != None:
			return self._lookup[uri] if uri in self._lookup else None
		else:
			return self._lookup

class MeetingLookup(object):
	
	def __init__(self):
		self._lookup = {}
	
	def add(self,meeting):
		if not meeting.uri() in self._lookup:
			self._lookup[meeting.uri()] = meeting

	def get(self,uri=None):
		if uri != None:
			return self._lookup[uri] if uri in self._lookup else None
		else:
			return self._lookup
	
	
class OrganizationLookup(object):
	
	baseURI = "http://abstracts.agu.org/organizations/"
	
	def __init__(self):
		self._lookup = {}
		self._existing = {}
	
	def add(self,organization,existing=False):
		if existing and not organization.location in self._existing:
			self._existing[organization.location] = organization
		elif not organization.location in self._existing and not organization.location in self._lookup:
			organization.identifier = "%s%d" % (self.baseURI,len(self._lookup.keys()) + len(self._existing.keys()))
			self._lookup[organization.location] = organization
			
	def get(self,location=None):
		if location != None:
			org = self._existing[location] if location in self._existing else None
			org = self._lookup[location] if org == None and location in self._lookup else org
			return org
		else:
			return self._lookup

#Lookups for Cross-Dataset Identifiers
organizationLookup = OrganizationLookup()
meetingLookup = MeetingLookup()
personLookup = PersonLookup()

#SPARQL Result Handlers
def tally_organization(result):
	org = Organization(result["key"]["value"].encode("utf8"),result["id"]["value"].encode("utf8"))
#	org = Organization(result["key"]["value"],result["id"]["value"])
	organizationLookup.add(org,True)

#Query Utilities and Information
def init_lookup_from_sparql(template,tally,endpoint,graph=None,count=-1,limit=10000):
	fromclause = "FROM <%s> " % graph if graph != None else ""
	offset, first, results = 0, True, None
	while first or offset < count or len(results) == limit:
		first = False
		sparql = SPARQLWrapper(endpoint)
		sparql.setReturnFormat(JSON)
		paging = " LIMIT %d OFFSET %d" % (limit,offset) if count >= 0 else ""
		query = template.replace("{from}",fromclause).replace("{paging}",paging)
		sparql.setQuery(query)
		results = sparql.query().convert()
		for result in results["results"]["bindings"]:
			tally(result)
		offset += limit

def get_sparql_result_count(query,endpoint,graph=None):
	fromclause = "FROM <%s> " % graph if graph != None else ""
	sparqlCount = SPARQLWrapper(endpoint)
	query = query.replace("{from}",fromclause)
	sparqlCount.setQuery(query)
	sparqlCount.setReturnFormat(JSON)
	results = sparqlCount.query().convert()
	return int(results["results"]["bindings"][0]["count"]["value"])

def sparql_prefixes(prefixes):
	ret = ""
	for p in prefixes.keys():
		ret += "PREFIX %s: <%s> " % (p,prefixes[p])
	return ret
	
prefixes = {
	"foaf": "http://xmlns.com/foaf/0.1/",
	"dc": "http://purl.org/dc/terms/"
}

agu_queries = {	
	"organizations" : [
		sparql_prefixes(prefixes) + "SELECT count(DISTINCT ?id) as ?count {from} WHERE { ?id a foaf:Organization ; dc:description ?key . }",
		sparql_prefixes(prefixes) + "SELECT ?id ?key {from}WHERE { ?id a foaf:Organization ; dc:description ?key . }{paging}"
	]
}

#Initialize Lookups
def sparql_lookups():
	endpoint = "http://localhost:8890/sparql"
	graph = "http://abstracts.agu.org/graphs/1.0/organizations"
	orgscount = get_sparql_result_count(agu_queries["organizations"][0],endpoint,graph)
	init_lookup_from_sparql(agu_queries["organizations"][1],tally_organization,endpoint,graph,orgscount)
