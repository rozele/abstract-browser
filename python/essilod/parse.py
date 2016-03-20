#!/usr/bin/env python
# encoding: utf-8

from entity.sessions import HtmlSession, SessionParseError, serializer as sessionSerializer
from entity.sections import serializer as sectionSerializer
from entity.keywords import serializer as keywordSerializer
from entity.abstracts import HtmlAbstract, AbstractParseError, IgnoreAbstractError, serializer as abstractSerializer
from entity.meetings import Meeting, serializer as meetingSerializer
from static import get_keywords, get_sections
import cProfile
import argparse
import codecs
import re
import os

"""
Parses AGU .dat files for meeting sessions
Iterates over each line, extracting a Session instance for each
Uses SessionSummary subclass to extract data
"""

class BlockStream(object):
	
	def __init__(self,fstream,mtg):
		self.stream = fstream
		self.meeting = mtg

	def _get_blocks(self):
		self.stream.readline()
		block = []
		regex = re.compile(r"<!-----*>")
		for line in self.stream:
			if regex.match(line) != None and len(block) > 0:
				yield block
				block = []
			elif line.strip() != "":
				block.append(line)
		if len(block) > 0:
			yield block

	def enumerate(self):
		for block in self._get_blocks():
			try:
				yield HtmlSession(block,self.meeting,True)
			except SessionParseError:
				try:
					yield HtmlAbstract(block,None,self.meeting,True)
				except IgnoreAbstractError:
					yield block

def parse_meeting(i,o,abbr,ext="ttl"):
	ofile = o + abbr + '.' + ext
	efile = o + abbr + ".err"
	ostream = codecs.open(ofile,"w","utf8")
	estream = None
	mtg = Meeting(abbr)
	bstream = BlockStream(open(i,"r"), mtg)
	ostream.write(unicode(meetingSerializer.serialize(mtg), errors="ignore"))
	for item in bstream.enumerate():
		if isinstance(item,HtmlSession):
			ostream.write(unicode(sessionSerializer.serialize(item), errors="ignore"))
		elif isinstance(item,HtmlAbstract):
			ostream.write(unicode(abstractSerializer.serialize(item), errors="ignore"))
		elif isinstance(item,list):
			estream = estream if estream != None else codecs.open(efile, "w", "utf16")
			estream.write(unicode(' '.join(item), errors="ignore"))
	ostream.close()
	if estream != None:
		estream.close()

def get_meeting_files(indir):	
	for f in os.listdir(indir):
		if f.endswith(".txt"):
			yield os.path.join(indir, f)

def get_args():
	parser = argparse.ArgumentParser(description='AGU Meeting File Parser')
	parser.add_argument(dest='input', nargs=1, help='specify input directory')
	parser.add_argument(dest='output', nargs='?', help='specify output directory')
	parser.add_argument(dest='ext', nargs='?', default='ttl', help='set the extension (not yet working)')
	parser.add_argument('--keywords', action='store_true', help='compute keyword static mappings')
	parser.add_argument('--sections', action='store_true', help='compute session static mappings')
	return parser.parse_args()

def main():
	args = get_args()
	
	indir = args.input[0] if isinstance(args.input,list) else args.input
	outdir = args.output if args.output else args.input
	outdir = outdir[0] if isinstance(outdir,list) else outdir
	outdir = outdir + '/' if not outdir.endswith('/') else outdir
	ext = args.ext[0] if isinstance(args.ext,list) else args.ext
		
	files = get_meeting_files(indir)
	
	for f in files:
		abbr = f[len(indir):(len(ext) + 1)*-1]
		parse_meeting(f,outdir,abbr,ext)

	if args.sections:
		ostream = codecs.open(outdir + "sections." + ext,"w","utf-8")
		for section in get_sections():
	  		ostream.write(unicode(sectionSerializer.serialize(section),errors="ignore"))
		ostream.close()

	if args.keywords:
		ostream = codecs.open(outdir + "keywords." + ext,"w","utf-8")
		for keyword in get_keywords():
	  		ostream.write(unicode(keywordSerializer.serialize(keyword),errors="ignore"))
		ostream.close()

main()
