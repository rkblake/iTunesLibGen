import sys
#import random
import xml.etree.ElementTree as ET
from mutagen.mp3 import MP3

int = 0

def add_key(dst, name, data_type, value):
    new = ET.SubElement(dst, "key")
    new.text = name+'\n\t\t'
    if data_type:
        new = ET.SubElement(dst, data_type)
        if value:
            new.text = str(value)

def add_song(dst, path):
    add_key(dst, int, None, None)
    fdict = ET.SubElement(dst, 'dict')
    file = MP3(path)
    add_key(fdict, "Track ID", "integer", int)
    add_key(fdict, "Name", "string", file["TIT2"])
    add_key(fdict, "Artist", "string", file["TPE1"])
    add_key(fdict, "Album Artist", "string", file["TPE2"])
    add_key(fdict, "Composer", "string", file["TCOM"])
    add_key(fdict, "Album", "string", file["TALB"])
    add_key(fdict, "Genre", "string", file["TCON"])
    add_key(fdict, "Kind", "string", file["TFLT"])
    add_key(fdict, "Size", "integer", None)                 #TODO: this
    add_key(fdict, "Total Time", "integer", file["TLEN"])
    add_key(fdict, "Disc Number", "integer", file["TPOS"])
    add_key(fdict, "Disc Count", "integer", file["TPOS"])
    add_key(fdict, "Track Number", "integer", file["TRCK"])
    add_key(fdict, "Track Count", "integer", file["TRCK"])
    add_key(fdict, "Year", "integer", file["TDRC"])
    add_key(fdict, "Date Modified", "date", None)           #TODO: this
    add_key(fdict, "Date Added", "date", None)              #TODO: this
    add_key(fdict, "Bit Rate", "integer", None)             #TODO: this
    add_key(fdict, "Sample Rate", "integer", None)          #TODO: this
    add_key(fdcit, "Comments", "string", file["COMM"])
    add_key(fdict, "Artwork Count", "integer", None)        #TODO: this
    add_key(fdict, "Persistent ID", "string", None)         #TODO: this
    add_key(fdict, "Track Type", "string", "File")
    add_key(fdict, "Location", "string", None)              #TODO: this!!!
    add_key(fdict, "File Folder Count", "integer", -1)
    add_key(fdict, "Library Folder Count", "integer", -1)
    int += 2

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
sdict = ET.SubElement(mdict, 'dict')
sdict.text = '\n\t\t'



library.write(ET.tostring(plist))
library.close()