from entity.sessions import SummarySession
from entity.sessions import serializer as sessionSerializer
from entity.meetings import Meeting
import argparse
import codecs
import re
import os

"""
Parses AGU .dat files for meeting sessions
Iterates over each line, extracting a Session instance for each
Uses SessionSummary subclass to extract data
"""

class SessionInfoStream(object):
	
	def __init__(self,fstream,mtg):
		self.stream = fstream
		self.meeting = mtg
		
	def _get_lines(self):
		for line in self.stream:
			yield line
	
	def get_sessions(self):
		for line in self._get_lines():
			yield SummarySession(line,self.meeting)

def parse_sessions(i,o,abbr,ext="ttl"):
	mtg = Meeting(abbr)
	sstream = SessionInfoStream(open(i,"r"),mtg)
	ostream = codecs.open(o,"w","utf-8")
	for session in sstream.get_sessions():
		ostream.write(unicode(sessionSerializer.serialize_attr(session,"cosponsors"), errors="replace"))
	ostream.close()

parser = argparse.ArgumentParser(description='AGU Meeting File Parser')
parser.add_argument(dest='input', nargs=1, default='../data/agu/meetings/', help='specify input file')
parser.add_argument(dest='output', nargs=1, default='../data/agu/newrdf/', help='specify output file')
parser.add_argument(dest='ext', nargs='?', default='ttl', help='set the extension (not yet working)')
args = parser.parse_args()

outfile = args.output[0] if isinstance(args.output,list) else args.output
infile = args.input[0] if isinstance(args.input,list) else args.input
ext = args.ext[0] if isinstance(args.ext,list) else args.ext
abbr = infile[len(infile) - (len(ext) + 5):(len(ext) + 1)*-1]
parse_sessions(infile,outfile,abbr,ext)