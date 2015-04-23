import re
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape

def get_text_content(tag,content):
	m = re.search(r"<"+tag+".*?>\s*(.*?)\s*(<br/?>)?</?"+tag+">",content)
	m = re.search(r"<"+tag+".*?>\s*(.*?)\s*(<br/?>)?",content) if not m else m
	return m.group(1) if m != None else None

def fix_abstract_links(content):
	try:
		content = re.sub("src=\"/", "src=\"http://www.agu.org/", content)
		content = re.sub("href=\"/", "src=\"http://www.agu.org/", content)
		return content
	except TypeError:
		print content
		return content

def utf8_replace(pattern, replace):
	s = pattern % replace
	s = s.decode('utf-8','replace')
	return s
	
def get_multiple_lines(prefixes,idx,lines):		
	content = ""
	while idx+1 < len(lines) and not lines[idx+1].strip()[0:3] in prefixes:
		content += "\n" + lines[idx].strip()
		idx += 1
	content += "\n" + lines[idx].strip()
	return idx, content
	
def get_html_content(tag,clazz,content,textonly=False):
	soup = BeautifulSoup(content)
	result = ''
	for el in soup.findAll(tag, { 'class' : clazz }):
		result += ''.join([unicode(c) for c in el])
	if textonly:
		result = ''.join(BeautifulSoup(result).findAll(text=True))
	return result.encode("utf8")

def urify_name(name):
	name = re.sub("\\\\","",name)
	return re.sub("\s","_",name)

def clean_conveners(content):
	return unescape(content)

def clean_non_printables(content):
	ret = ""
	for c in content:
		ret += c if ord(c) >= 32 else " "
	return ret
	
def clean_literal(content,t):
	if t == "turtle":
		for r in turtle_chars:
			content = content.replace(r[0],r[1])
		new_content = ""
		for c in content:
			new_content += c if c >= chr(32) else ' '
		content = new_content
	#content = filter(lambda x: ord(x) >= 32, content)
	#content = clean_non_printables(content)
	return content
	
turtle_chars = [
	["\\","\\\\"],
	["\"","\\\""],
	["\n","\\n"]
]	
	
config = {
	"base" : "http://abstractsearch.agu.org/",
	"meeting_codes" : {
		"fm" : "Fall Meeting",
		"ja" : "Joint Assembly",
		"os" : "Ocean Sciences Meeting",
		"wp" : "Western Pacific Geophysics Meeting",
		"sm" : "Joint Assembly",
	},
	"section_codes" : {
		"U" : "Union",
		"A" : "Atmospheric Sciences",
		"AE" : "Atmospheric and Space Electricity",
		"B" : "Biogeosciences",
		"C" : "Cryosphere",
		"CG" : "Canadian Geophysical Union",
		"EP" : "Earth and Planetary Surface Processes",
		"IN" : "Earth and Space Science Informatics",
		"ED" : "Education and Human Resources",
		"G" : "Geodesy",
		"GA" : "Geological Association of Canada",
		"GC" : "Global Environmental Change",
		"GP" : "Geomagnetism and Paleomagnetism",
		"GS" : "Geochemical Society",
		"H" : "Hydrology",
		"IA" : "International Association of Hydrogeologists - Canadian National Chapter",
		"M" : "Mineralogical Society of America",
		"MA" : "Mineralogical Association of Canada",
		"MR" : "Mineral and Rock Physics",
		"NH" : "Natural Hazards",
		"NG" : "Nonlinear Geophysics",
		"NS" : "Near Surface Geophysics",
		"OS" : "Ocean Sciences",
		"PP" : "Paleoceanography and Paleoclimatology",
		"P" : "Planetary Sciences",
		"PA" : "Public Affairs",
		"S" : "Seismology",
		"SA" : "SPA-Aeronomy",
		"SH" : "SPA-Solar and Heliospheric Physics",
		"SI" : "Societal Impacts and Policy Sciences",
		"SM" : "SPA-Magnetospheric Physics",
		"SP" : "Solar Physics Division - AAS",
		"DI" : "Study of Earth's Deep Interior",
		"T" : "Tectonophysics",
		"V" : "Volcanology, Geochemistry, Petrology"
	},
	"os_section_codes" : {
		"BO" : "Biological Oceanography",
		"CO" : "Chemical Oceanography",
		"ED" : "Education and Outreach",
		"GO" : "Geological Oceanography",
		"IT" : "Interdisciplinary",
		"MP" : "Marine Policy",
		"MT" : "Marine Technology",
		"PA" : "Paleoceanography",
		"PO" : "Physical Oceanography"
	}
}
