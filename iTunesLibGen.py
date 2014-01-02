import sys
#import random
import xml.etree.ElementTree as ET

def add_key(dst, name, data_type, value):
    new = ET.SubElement(dst, "key")
    new.text = name+'\n\t\t'
    if data_type:
        new = ET.SubElement(dst, data_type)
        if value:
            new.text = str(value)

#path = sys.argv[1]
library = open('iTunes Music Library.xml', 'w')
library.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')

plist = ET.Element('plist')
plist.attrib = {'version': '1.0'}
plist.text = '\n'
mdict = ET.SubElement(plist, 'dict')
mdict.text = '\n\t'
add_key(mdict, "Major Version", "integer", 1)
add_key(mdict, "Minor Version", "integer", 1)
add_key(mdict, "Date", "date", "1994-12-18T00:00:00Z")      #TODO: function for date in format: <YYYY-MM-DD>T<HH:MM:SS>Z
add_key(mdict, "Application Version", "string", "11.1.3")   #TODO: function for itunes version
add_key(mdict, "Features", "integer", 5)
add_key(mdict, "Show Content Ratings", "true", None)
add_key(mdict, "Music Folder", "path", "file://localhost/Users/randallblake/Music/iTunes/iTunes%20Media/")  #TODO: use path from script parameter
add_key(mdict, "Library Persistent ID", "string", "0123456789abcdef")   #TODO: this?
add_key(mdict, "Tracks", None, None)

tree = ET.ElementTree(plist)
ET.dump(tree)
#print ET.tostring(tree)
library.write(ET.tostring(plist))
library.close()