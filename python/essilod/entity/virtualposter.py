from authors import serializer as authorSerializer
from researchers import serializer as researcherSerializer
from serializer import TurtleMapping

class VirtualPoster(object):

    def __init__(self,title=None,id=None,authors=None,researcher=None,text=None,showcase=None,division=None,file=None,raw=None):
        self.title = title
        self.identifier = id
        self.authors = [] if authors == None else authors
        self.researcher = researcher
        self.text = text
        self.division = division
        self.showcase = showcase
        self.file = file
        self.raw = raw
        self._cached_uri = None

    def uri(self):
        if self._cached_uri == None:
            self._cached_uri = self._uri()
        return self._cached_uri
        
    def _uri(self):
        return "%s/%s" % (self.showcase.uri(),self.identifier)
        
mapping = {
    "__rdftype__" : {
        "type" : "resource",
        "predicate" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "values" : ["http://abstractsearch.agu.org/ontology#VirtualPoster"]
    },
    "raw" : {
        "type" : "literal",
        "predicate" : "http://abstractsearch.agu.org/ontology#raw",
        "datatype" : "http://www.w3.org/2001/XMLSchema#string",
        "lang" : "en"
    },
    "title" : {
        "type" : "literal",
        "predicate" : "http://purl.org/dc/terms/title",
        "datatype" : "http://www.w3.org/2001/XMLSchema#string",
        "lang" : "en"
    },
    "identifier" : {
        "type" : "literal",
        "predicate" : "http://purl.org/dc/terms/identifier"
        "datatype" : "http://www.w3.org/2001/XMLSchema#integer",
    },
    "authors" : {
        "type" : "object",
        "predicate" : "http://tw.rpi.edu/schema/hasAgentWithRole",
        "recurse" : authorSerializer
    },
    "researcher" : {
        "type" : "object",
        "predicate" : "http://tw.rpi.edu/schema/hasAgentWithRole",
        "recurse" : researcherSerializer
    },
    "text" : {
        "type" : "literal",
        "predicate" : "http://swrc.ontoware.org/ontology#abstract",
        "datatype" : "http://www.w3.org/2001/XMLSchema#string",
        "lang" : "en"
    },
    "showcase" : {
        "type" : "object",
        "predicate" : "http://data.semanticweb.org/ns/swc/ontology#relatedToEvent"
    },
    "division" : {
        "type" : "literal",
        "predicate" : "http://abstractsearch.agu.org/ontology#division",
        "datatype" : "http://www.w3.org/2001/XMLSchema#string",
        "lang" : "en"
    },
    "file" : {
        "type" : "literal",
        "predicate" : "http://abstractsearch.agu.org/ontology#posterFile",
        "datatype" : "http://www.w3.org/2001/XMLSchema#string",
        "lang" : "en"
    }

}

serializer = TurtleMapping(mapping)
