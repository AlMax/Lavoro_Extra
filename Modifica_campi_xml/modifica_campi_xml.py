import frames as frame
import time

import zipfile

import xml.dom.minidom
from xml.dom import minidom

import xml.etree.ElementTree as ET

archive = zipfile.ZipFile('/Users/almax/Desktop/Varie/GitHub/MAW/Excel_XML_Converter/Payload.zip', 'r')
imgfile = archive.open('Payload.xml')

#https://stackabuse.com/reading-and-writing-xml-files-in-python/

tree = ET.parse(imgfile)
root = tree.getroot()

# changing a field text
for elem in root.iter('denominazioneAPL'):
    elem.text = 'new text'

# modifying an attribute
for elem in root.iter('denominazioneAPL'):
    print(elem.get('name'))
    elem.set('name', 'newitem')

# adding an attribute
for elem in root.iter('denominazioneAPL'):
    elem.set('name2', 'newitem2')

tree.write('/Users/almax/Desktop/Varie/GitHub/MAW/Excel_XML_Converter/newitems.xml')