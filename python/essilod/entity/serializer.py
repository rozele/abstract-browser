from utils import clean_literal, utf8_replace

class TurtleMapping(object):
	
	def __init__(self,mappings):
		self.mappings = mappings
	
	def serialize_attr(self,obj,attr):
		output = ""
		if hasattr(obj,attr) and getattr(obj,attr) != None:
			for mapping in self._do_mapping(attr,obj):
				output += "%s .\n" % mapping
		return output
		
	#serialize triples for Python object
	def serialize(self,obj):
		output = ""
		for key in self.mappings.keys():
			if hasattr(obj,key) and getattr(obj,key) != None:
				for mapping in self._do_mapping(key,obj):
					output += "%s .\n" % mapping
			for value in self._get_static_values(key):
				output += "%s .\n" % self._do_value_mapping(key,obj.uri(),value).next()
		return output
	
	#maps Python object attributes to triples
	def _do_mapping(self,key,subj):
		if isinstance(getattr(subj,key),list):
			for obj in getattr(subj,key):
				for mapping in self._do_value_mapping(key,subj.uri(),obj):
				 	yield mapping
		else:
			for mapping in self._do_value_mapping(key,subj.uri(),getattr(subj,key)):
			 	yield mapping
			
	#maps to a triple with a literal
	def _do_literal_value_mapping(self,key,subj,obj):
		for pred in self._get_predicates(key):
			if not isinstance(obj,str) and not isinstance(obj,unicode):
				result = "<%s> <%s> \"%s\"" % (subj,pred,clean_literal(str(obj),"turtle"))
			else:
				result = "<%s> <%s> \"%s\"" % (subj,pred,clean_literal(obj,"turtle"))
			if "lang" in self.mappings[key]:
				result = "%s@%s" % (result,self.mappings[key]["lang"])
			elif "datatype" in self.mappings[key]:
				result = "%s^^<%s>" % (result,self.mappings[key]["datatype"])
		 	yield result
	
	def _do_object_value_mapping(self,key,subj,obj):
		if obj != None:
			if "reverse" in self.mappings[key].keys() and self.mappings[key]["reverse"]:
				for pred in self._get_predicates(key):
					yield "<%s> <%s> <%s>" % (obj.uri(),pred,subj)
			else:
				for pred in self._get_predicates(key):
					yield "<%s> <%s> <%s>" % (subj,pred,obj.uri())
			recurse = self._do_recursive_mapping(key,obj)			
			if recurse != None:
			       	yield recurse[:-3]
				
	#checks if recursive mapping should be done and starts it
	def _do_recursive_mapping(self,key,obj):
		if "recurse" in self.mappings[key] and isinstance(self.mappings[key]["recurse"],TurtleMapping):
			return self.mappings[key]["recurse"].serialize(obj)
		else:
			return None
			
	#maps to a triple with URI object
	def _do_resource_value_mapping(self,key,subj,obj):
		for pred in self._get_predicates(key):
			yield "<%s> <%s> <%s>" % (subj,pred,obj)
	
	#maps a value directly into a triple
	def _do_value_mapping(self,key,subj,obj):
		if self.mappings[key]["type"] == "literal":
			return self._do_literal_value_mapping(key,subj,obj)
		elif self.mappings[key]["type"] == "object":
			return self._do_object_value_mapping(key,subj,obj)
		elif self.mappings[key]["type"] == "resource":
			if "reverse" in self.mappings[key].keys() and self.mappings[key]["reverse"]:
				return self._do_resource_value_mapping(key,obj,subj)
			else:
				return self._do_resource_value_mapping(key,subj,obj)
	
	#generator for predicates from either "predicates" or "predicate" in mapping
	def _get_predicates(self,key):
		if "predicates" in self.mappings[key].keys():
			for p in self.mappings[key]["predicates"]:
				yield p
		elif "predicate" in self.mappings[key].keys():
			yield self.mappings[key]["predicate"]
	
	#generator for all static "values" or "value" triples in mapping
	def _get_static_values(self,key):
		if "values" in self.mappings[key].keys():
			for v in self.mappings[key]["values"]:
				yield v
		elif "value" in self.mappings[key].keys():
			yield self.mappings[key]["value"]
