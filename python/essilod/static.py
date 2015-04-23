from entity.utils import config
from entity.keywords import TextKeyword
from entity.sections import Section
import urllib
import os
import re

def get_keywords():
	url = "http://localhost/resources/AGU_index_terms.txt"
	stream = urllib.urlopen(url)
	for line in stream:
		line = line.strip()
		if re.match("^\d{4}",line):
			yield TextKeyword(line)

def get_sections():
	for code in config["section_codes"]:
		yield Section(code,config["section_codes"][code])
	for code in config["os_section_codes"]:
		yield Section(code,config["os_section_codes"][code],True)