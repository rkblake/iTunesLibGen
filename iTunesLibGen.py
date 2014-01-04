import sys
import os
import xml.etree.ElementTree as ET
from mutagen.mp3 import MP3

i = 0

def add_key(dst, name, data_type, value):
    new = ET.SubElement(dst, "key")
    new.text = name+'\n\t\t'
    if data_type:
        new = ET.SubElement(dst, data_type)
        if value:
            new.text = str(value)

def add_song(dst, path):
    add_key(dst, i, None, None)
    fdict = ET.SubElement(dst, 'dict')
    audio = MP3(path)
    add_key(fdict, "Track ID", "integer", i)
    add_key(fdict, "Name", "string", audio["TIT2"])
    add_key(fdict, "Artist", "string", audio["TPE1"])
    add_key(fdict, "Album Artist", "string", audio["TPE2"])
    add_key(fdict, "Composer", "string", audio["TCOM"])
    add_key(fdict, "Album", "string", audio["TALB"])
    add_key(fdict, "Genre", "string", audio["TCON"])
    add_key(fdict, "Kind", "string", audio["TFLT"])
    add_key(fdict, "Size", "integer", get_filesize(path))
    add_key(fdict, "Total Time", "integer", audio["TLEN"])
    add_key(fdict, "Disc Number", "integer", split_trackdisc(audio["TPOS"]), True))
    add_key(fdict, "Disc Count", "integer", split_trackdisc(audio["TPOS"]), False))
    add_key(fdict, "Track Number", "integer", split_trackdisc(audio["TRCK"], True))
    add_key(fdict, "Track Count", "integer", split_trackdisc(audio["TRCK"], False))
    add_key(fdict, "Year", "integer", audio["TDRC"])
    add_key(fdict, "Date Modified", "date", None)           #TODO: this
    add_key(fdict, "Date Added", "date", None)              #TODO: this
    add_key(fdict, "Bit Rate", "integer", None)             #TODO: this
    add_key(fdict, "Sample Rate", "integer", None)          #TODO: this
    add_key(fdict, "Comments", "string", audio["COMM"])
    add_key(fdict, "Artwork Count", "integer", None)        #TODO: this
    add_key(fdict, "Persistent ID", "string", None)         #TODO: this
    add_key(fdict, "Track Type", "string", "File")
    add_key(fdict, "Location", "string", format_path(path))
    add_key(fdict, "File Folder Count", "integer", 4)
    add_key(fdict, "Library Folder Count", "integer", 1)
    i += 2

def format_path(path):
    if sys.platform == 'win32':
        str = 'file://localhost/' + str
        str = str.replace('\\','/')
    else:
        str = 'file://localhost' + str
    str = str.replace(' ','%20')
    return str
                          
def split_trackdisc(frame, first):
    index = str.find('/')
    if first:
        return str[:index]
    else:
        return str[-index:]

def get_filesize(path):
    if sys.platform == 'win32':
        return os.path.getsize(path.replace("\\","\\\\")
    else:
        return os.path.getsize(path)

path = sys.argv[1]
library = open('iTunes Music Library.xml', 'w')
library.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')

plist = ET.Element('plist')
plist.attrib = {'version': '1.0'}
plist.text = '\n'
mdict = ET.SubElement(plist, 'dict')
mdict.text = '\n\t'
add_key(mdict, "Major Version", "integer", 1)
add_key(mdict, "Minor Version", "integer", 1)
add_key(mdict, "Date", "date", "1994-12-18T00:00:00Z")                  #TODO: function for date in format: <YYYY-MM-DD>T<HH:MM:SS>Z
add_key(mdict, "Application Version", "string", "11.1.3")               #TODO: function for itunes version
add_key(mdict, "Features", "integer", 5)
add_key(mdict, "Show Content Ratings", "true", None)
add_key(mdict, "Music Folder", "path", format_path(path))
add_key(mdict, "Library Persistent ID", "string", "0123456789abcdef")   #TODO: this?
add_key(mdict, "Tracks", None, None)
sdict = ET.SubElement(mdict, 'dict')
sdict.text = '\n\t\t'



library.write(ET.tostring(plist))
library.close()
