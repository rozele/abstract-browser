#!/usr/bin/env python

from subprocess import call
import argparse
import re
import os

parser = argparse.ArgumentParser(description='AGU Meeting RDF Loader')
parser.add_argument(dest='dir', nargs=1, help='specify input file or directory')
parser.add_argument(dest='version', nargs='?', default='2.0', help='set the version number for the graphs')
parser.add_argument(dest='base', nargs='?', default='http://abstractsearch.agu.org/graphs', help='set the base URI for graphs created')
parser.add_argument(dest='script', nargs='?', default='../utils/virtuoso/vload', help='set the script used to load RDF')
parser.add_argument(dest='ext', nargs='?', default='ttl', help='set the extension (not yet working)')
args = parser.parse_args()

indir = args.dir[0] if isinstance(args.dir,list) else args.dir
version = args.version[0] if isinstance(args.version,list) else args.version
base = args.base[0] if isinstance(args.base,list) else args.base
base = "%s/%s/" % (base,version)
script = args.script[0] if isinstance(args.script,list) else args.script
ext = args.ext[0] if isinstance(args.ext,list) else args.ext

files = {}
for f in os.listdir(indir):
    if f.endswith("." + ext):
        files[f] = indir + f

for f in files:
	title = re.match("^([a-z]{2})(\d{2})."+ext+"$",f)
	graph = None
	if title:
		year = int(title.group(2)) + 2000 if int(title.group(2)) < 95 else int(title.group(2)) + 1900
		graph = "%s/%s/%s/%s" % (args.base,version,year,title.group(1).upper())
	else:
		graph = "%s%s" % (base,f[:-4])
	ex = "%s %s %s %s" % (script,ext,files[f],graph)
	print ex
	os.system(ex)
