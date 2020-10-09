import frames as frame
import time

import zipfile

import xml.dom.minidom
from xml.dom import minidom

import xml.etree.ElementTree as ET

archive = zipfile.ZipFile('/Users/almax/Desktop/Varie/GitHub/MAW/Modifica_campi_xml/Payload.zip', 'r')
imgfile = archive.open('Payload.xml')

#https://stackabuse.com/reading-and-writing-xml-files-in-python/

tree = ET.parse(imgfile)
root = tree.getroot()

livelli = []

def perf_func(elem, func, level=0):
    func(elem,level)
    for child in list(elem):
        perf_func(child, func, level+1)

def print_level(elem,level):
    print('-'*level+elem.tag)
    try:
        livelli[level].append(elem.tag)
    except:
        livelli.append([])
        livelli[level].append(elem.tag)


perf_func(root, print_level)
print(livelli)
print(len(livelli))


print("\n\n\t\tnext")


tree.find('istanza/lavoratori/lavoratore/nome').text = "ciao"
a = tree.findall('istanza/lavoratori/lavoratore/cognome')

for b in a:
    b.text = "prova"

tree.write("test.xml")