import sys
import os
import random
import re
import xml.etree.ElementTree as ET
from mutagen.mp3 import MP3
from datetime import datetime
from math import trunc

def add_key(dst, name, data_type, value):
    new = ET.SubElement(dst, "key")
    new.text = str(name)+'\n\t\t'
    if data_type:
        new = ET.SubElement(dst, data_type)
        if value:
            new.text = str(value)

def add_song(dst, path , track_id):
    add_key(dst, track_id, None, None)
    fdict = ET.SubElement(dst, 'dict')
    audio = MP3(path)
    add_key(fdict, "Track ID", "integer", track_id)
    try:
        add_key(fdict, "Name", "string", audio["TIT2"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Artist", "string", audio["TPE1"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Album Artist", "string", audio["TPE2"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Composer", "string", audio["TCOM"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Album", "string", audio["TALB"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Genre", "string", audio["TCON"])
    except KeyError:
        pass
    add_key(fdict, "Kind", "string", "MPEG audio file")
    add_key(fdict, "Size", "integer", get_filesize(path))
    add_key(fdict, "Total Time", "integer", trunc(audio.info.length * 1000))
    try:
        add_key(fdict, "Disc Number", "integer", split_trackdisc(audio["TPOS"], True))
    except KeyError:
        pass
    try:
        add_key(fdict, "Disc Count", "integer", split_trackdisc(audio["TPOS"], False))
    except KeyError:
        pass
    add_key(fdict, "Track Number", "integer", split_trackdisc(audio["TRCK"], True))
    add_key(fdict, "Track Count", "integer", split_trackdisc(audio["TRCK"], False))
    add_key(fdict, "Year", "integer", audio["TDRC"])
    add_key(fdict, "Date Modified", "date", get_date())
    add_key(fdict, "Date Added", "date", get_date())
    add_key(fdict, "Bit Rate", "integer", audio.info.bitrate / 1000)
    add_key(fdict, "Sample Rate", "integer", audio.info.sample_rate)
    try:
        add_key(fdict, "Comments", "string", audio["COMM"])
    except KeyError:
        pass
    add_key(fdict, "Artwork Count", "integer", None)        #TODO: this
    try:
        add_key(fdict, "Sort Album", "string", audio["TSOA"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Sort Album Artist", "string", audio["TSO2"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Sort Artist", "string", audio["TSOP"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Sort Composer", "string", audio["TSOC"])
    except KeyError:
        pass
    try:
        add_key(fdict, "Sort Name", "string", audio["TSOT"])
    except KeyError:
        pass
    add_key(fdict, "Persistent ID", "string", gen_id())
    add_key(fdict, "Track Type", "string", "File")
    add_key(fdict, "Location", "string", format_path(path))
    add_key(fdict, "File Folder Count", "integer", 4)       #TODO: this
    add_key(fdict, "Library Folder Count", "integer", 1)    #TODO: this

def format_path(path):
    formatted_path = ''
    if sys.platform == 'win32':
        formatted_path = 'file://localhost/' + formatted_path
        formatted_path = formatted_path.replace('\\','/')
    else:
        formatted_path = 'file://localhost' + formatted_path
    formatted_path = formatted_path.replace(' ','%20')
    return formatted_path

def split_trackdisc(frame, first):
    index = str(frame).find('/')
    if first:
        return frame[:index]
    else:
        return frame[-index:]

def get_filesize(path):
    if sys.platform == 'win32':
        return os.path.getsize(path.replace("\\","\\\\"))
    else:
        return os.path.getsize(path)

def get_date():
    return datetime(datetime.now().year,
                     datetime.now().month,
                     datetime.now().day,
                     datetime.now().hour,
                     datetime.now().minute,
                     datetime.now().second).isoformat()+"Z"

def gen_id():
    return ''.join([random.choice('123456789ABCDEF') for i in xrange(16)])

if __name__ == "__main__":
    track_id = 0
    path = sys.argv[1]
    library = open('iTunes Music Library.xml', 'w')
    library.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                  '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" '
                  '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')

    plist = ET.Element('plist')
    plist.attrib = {'version': '1.0'}
    plist.text = '\n'
    mdict = ET.SubElement(plist, 'dict')
    mdict.text = '\n\t'
    add_key(mdict, "Major Version", "integer", 1)
    add_key(mdict, "Minor Version", "integer", 1)
    add_key(mdict, "Date", "date", get_date())
    add_key(mdict, "Application Version", "string", "11.1.3")
    add_key(mdict, "Features", "integer", 5)
    add_key(mdict, "Show Content Ratings", "true", None)
    add_key(mdict, "Music Folder", "path", format_path(path))
    add_key(mdict, "Library Persistent ID", "string", gen_id())
    add_key(mdict, "Tracks", None, None)
    sdict = ET.SubElement(mdict, 'dict')
    sdict.text = '\n\t\t'
    for folder in os.walk(path):
        for filename in folder[2]:
            if re.search('.mp3', filename, re.IGNORECASE):
                print(folder[0]+filename)
                add_song(sdict, folder[0]+filename, track_id)
                track_id += 2

    library.write(ET.tostring(plist))
    library.close()