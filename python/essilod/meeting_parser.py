#!/usr/bin/env python
# encoding: utf-8

from entity.sessions import HtmlSession, SessionParseError
from entity.sessions import serializer as sessionSerializer
from entity.sections import serializer as sectionSerializer
from entity.keywords import serializer as keywordSerializer
from entity.abstracts import HtmlAbstract, AbstractParseError, IgnoreAbstractError
from entity.abstracts import serializer as abstractSerializer
from entity.people import serializer as personSerializer
from entity.meetings import Meeting
from entity.meetings import serializer as meetingSerializer
from entity.organizations import serializer as organizationSerializer
from entity.serializer import TurtleMapping
from entity.matcher.lookup import personLookup, organizationLookup, sparql_lookups
from static import get_keywords, get_sections
import cProfile
import argparse
import codecs
import re
import os

"""
MeetingStream class parses AGU .txt files for meeting abstracts
Iterates over chunks of the document delimited by HTML comment lines
First attempts to process chunk as Abstract, then Session if failure
Uses HtmlAbstract and HtmlSession extensions to extract data
"""

class MeetingStream(object):
	
	def __init__(self,fstream,meeting,matcher=None):
		self.stream = fstream
		self.matcher = matcher
		self.meeting = meeting
		
	def _get_blocks(self):
		self.stream.readline()
		block = []
		regex = re.compile(r"<!-----*>")
		for line in self.stream:
			if regex.match(line) != None:
				yield block
				block = []
			else:
				block.append(line)
		if len(block) > 0:
			yield block
	
	def get_sessions(self):
		session = None
		abstracts = []
		for block in self._get_blocks():
			try:
				abstract = HtmlAbstract(block,session,None,True)
				abstract.session = session
				abstracts.append(abstract)
			except IgnoreAbstractError:
				continue
			except AbstractParseError:
				if session != None:
					session.abstracts = abstracts
					abstracts = []
					yield session
				try:
					session = HtmlSession(block,self.meeting,True)
				except SessionParseError:
					print "SessionParseError!"
					print block
					continue #this should not happen
		session.abstracts = abstracts
		yield session

def parse_meeting(i,o,abbr,ext="ttl"):
	ofile = o + abbr + '.' + ext
	mtg = Meeting(abbr)
	mstream = MeetingStream(open(i,"r"),mtg)
	ostream = codecs.open(ofile,"w","utf-8")
	ostream.write(unicode(meetingSerializer.serialize(mtg),errors="replace"))
	for session in mstream.get_sessions():
		ostream.write(unicode(sessionSerializer.serialize(session),errors="replace"))
		for abstract in session.abstracts:
			ostream.write(unicode(abstractSerializer.serialize(abstract),errors="replace"))
	ostream.close()

def get_args():
	parser = argparse.ArgumentParser(description='AGU Meeting File Parser')
	parser.add_argument(dest='input', nargs=1, help='specify input file or directory')
	parser.add_argument(dest='output', nargs='?', help='specify output file or directory')
	parser.add_argument(dest='ext', nargs='?', default='ttl', help='set the extension (not yet working)')
	parser.add_argument('--keywords', action='store_true', help='compute keyword static mappings')
	parser.add_argument('--sections', action='store_true', help='compute session static mappings')
	parser.add_argument('--sparqlMatching', action='store_true', help='match existing identifiers from triple store')
	return parser.parse_args()

def get_meeting_files(indir):	
	for f in os.listdir(indir):
		if f.endswith(".txt"):
			directory = indir + '/' if not indir.endswith('/') else indir
			yield directory + f

def main():
	args = get_args()
	
	indir = args.input[0] if isinstance(args.input,list) else args.input
	outdir = args.output if args.output else args.input
	outdir = outdir[0] if isinstance(outdir,list) else outdir
	outdir = outdir + '/' if not outdir.endswith('/') else outdir
	ext = args.ext[0] if isinstance(args.ext,list) else args.ext

	if args.sparqlMatching:
		sparql_lookups()
		
	files = get_meeting_files(indir)
	
	for f in files:
		abbr = f[len(indir):(len(ext) + 1)*-1]
		parse_meeting(f,outdir,abbr,ext)
		
	ostream = codecs.open(outdir + "people." + ext,"w","utf-8")
	for key in personLookup.get():
		ostream.write(unicode(personSerializer.serialize(personLookup.get(key)),errors="replace"))
	ostream.close()

	ostream = codecs.open(outdir + "organizations." + ext,"w","utf-8")
	for key in organizationLookup.get():			
		ostream.write(unicode(organizationSerializer.serialize(organizationLookup.get(key)),errors="replace"))
	ostream.close()

	if args.sections:
		ostream = codecs.open(outdir + "sections." + ext,"w","utf-8")
		for section in get_sections():
	  		ostream.write(unicode(sectionSerializer.serialize(section),errors="replace"))
		ostream.close()

	if args.keywords:
		ostream = codecs.open(outdir + "keywords." + ext,"w","utf-8")
		for keyword in get_keywords():
	  		ostream.write(unicode(keywordSerializer.serialize(keyword),errors="replace"))
		ostream.close()

if __name__ == '__main__':
	cProfile.run('main()')
