import os
import xml.etree.ElementTree as ET
import sys

songs = []

def scan(d):
    for path in os.walk(d):
        for filename in path[2]:
            songs.append(path[0]+'/'+filename)

def add_key(dst, name, data_type, value):
    new = ET.SubElement(dst, "key")
    new.text = name
    if data_type:
        new = ET.SubElement(dst, data_type)
        if value:
            new.text = str(value)

if __name__ == "__main__":
    """Generate a playlist from scratch, generally not used,
    but important.
    """
    xml = ET.Element('dict')
    add_key(xml, "Major Version", "integer", 1)
    add_key(xml, "Minor Version", "integer", 1)
    add_key(xml, "Date", "date", "2014-01-02T00:06:46Z")
    add_key(xml, "Application Version", "string", "11.1.3")
    add_key(xml, "Features", "integer", 5)
    add_key(xml, "Show Content Ratings", "true", None)
    add_key(xml, "Music Folder", "string", "file://localhost/G:/Music/")
    add_key(xml, "Library Persistent ID", "string", "?????")
    add_key(xml, "Tracks", None, None)
