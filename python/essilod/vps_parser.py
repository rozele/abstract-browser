#!/usr/bin/env python
# encoding: utf-8

from entity.virtualposter import VirtualPoster, serializer as posterSerializer
from entity.vps import VirtualPosterShowcase, serializer as showcaseSerializer
from entity.authors import Author
from entity.researchers import Researcher
from entity.people import Person
from entity.organizations import Organization
from static import get_keywords, get_sections
import cProfile
import csv
import argparse
import codecs
import re
import os

"""
Parses AGU .dat files for meeting sessions
Iterates over each line, extracting a Session instance for each
Uses SessionSummary subclass to extract data
"""

def parse_person(row, index, role):
    person = Person()
    person.name = "%s %s" % (row[index+1],row[index+2])
    person.email = row[index+4] if row[index+4] != '' else None
    person.identifier = "%s/person" % role.uri()
    return person

def parse_person2(row, index, role):
    person = Person()
    person.name = "%s %s" % (row[index+1],row[index+2])
    person.identifier = "%s/person" % role.uri()
    return person

def parse_organization(row, index):
    return Organization(trim_commas(", ".join(row[index:index+5]).replace(", ,", ",")))
    
def parse_organization2(row, index):
    return Organization(trim_commas(", ".join(row[index:index+6]).replace(", ,", ",")))

def trim_commas(s):
    i = len(s) - 1
    while (i > 0 and (s[i] == ' ' or s[i] == ',')):
        i -= 1
    return s[:i+1]

def parse_poster(row, id, vps):
    poster = VirtualPoster()
    poster.identifier=id
    poster.showcase=vps
    poster.title = row[1]
    poster.text=row[2]
    poster.division=row[3]
    
    firstAuthor = Author()
    firstAuthor.abstract = poster
    firstAuthor.index = 1
    firstAuthor.person = parse_person(row, 4, firstAuthor)
    firstAuthorOrganization = parse_organization(row, 9)
    firstAuthorOrganization.authorships.append(firstAuthor)
    firstAuthor.affiliations.append(firstAuthorOrganization)
    firstAuthor.corresponding = True
                
    researcher = Researcher()
    researcher.abstract = poster
    researcher.index = 1
    researcher.person = parse_person2(row, 14, researcher)
    researcherOrganization = parse_organization(row, 18)
    researcherOrganization.authorships.append(researcher)
    researcher.affiliations.append(researcherOrganization)
    
    poster.authors.append(firstAuthor)
    poster.researcher = researcher
    
    startIndex = 24
    maxAuthors = 8
    for i in range(2, maxAuthors + 1):
        if row[startIndex] != '':
            author = Author()
            author.abstract = poster
            author.index = i
            author.person = parse_person(row,startIndex,author)
            organization = parse_organization2(row,startIndex+5)
            organization.authorships.append(author)
            author.affiliations.append(organization)
            author.corresponding = False
            poster.authors.append(author)
        startIndex += 11
    
    poster.file = row[103] if row[103] != '' else None
    return poster 
    
def parse_vps(i,o,abbr,ext="ttl"):
    ofile = o + abbr + '.' + ext
    efile = o + abbr + ".err"
    vpss = {}
    with open(i,'rU') as csvfile:
        with open(efile,'w') as estream:
            with open(ofile,'w') as ostream:
                reader = csv.reader(csvfile)
                headers = reader.next()
                counter = 0
                for row in reader:
                    index = row[0]
                    counter = counter+1
                    vps = VirtualPosterShowcase(abbr,index)
                    if index in vpss:
                        vps = vpss[index]
                    else:
                        vpss[index] = vps           
                    poster = parse_poster(row,counter,vps)
                    if isinstance(poster,VirtualPoster):
                        ostream.write(posterSerializer.serialize(poster))
                    else:
                        estream.write(row)
                for index in vpss:
                    vps = vpss[index]
                    if (isinstance(vps,VirtualPosterShowcase)):
                        ostream.write(showcaseSerializer.serialize(vps))
                    else:
                        estream.write(vps)
                        
def get_args():
    parser = argparse.ArgumentParser(description='AGU Meeting File Parser')
    parser.add_argument(dest='input', nargs=1, help='specify input file')
    parser.add_argument(dest='output', nargs='?', help='specify output directory')
    parser.add_argument(dest='ext', nargs='?', default='ttl', help='set the extension (not yet working)')
    return parser.parse_args()

def main():
    args = get_args()
    
    file = args.input[0] if isinstance(args.input,list) else args.input
    basename = os.path.basename(file)
    abbr = basename[:-4]
    outdir = args.output if args.output else file[:-len(basename)]
    outdir = outdir[0] if isinstance(outdir,list) else outdir
    ext = args.ext[0] if isinstance(args.ext,list) else args.ext        
    parse_vps(file,outdir,abbr,ext)

main()
