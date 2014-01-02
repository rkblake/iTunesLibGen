import sys
#import random
import xml.etree.ElementTree as ET

#path = sys.argv[1]
library = open('iTunes Music Library.xml', 'w')
library.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')

plist = ET.Element('plist')
plist.attrib = {'version': '1.0'}
plist.text = '\n'

print ET.tostring(plist)

library.close()
tree = ET.ElementTree(plist)
tree.write("iTunes Music Library.xml")