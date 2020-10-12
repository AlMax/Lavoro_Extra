import frames as frame
import time

import zipfile

import xml.dom.minidom
from xml.dom import minidom

import xml.etree.ElementTree as ET
ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
#archive = zipfile.ZipFile('/Users/Ali Haider Maqsood/Documents/GitHub/MAW/Modifica_campi_xml/UNISOMM_20201007_110200.zip', 'r')
#imgfile = archive.open('UNISOM_07102020_958250_544088_A.xml')

#https://stackabuse.com/reading-and-writing-xml-files-in-python/

tree = ET.parse("uni.xml")
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




tree = ET.parse('uni.xml')
root = tree.getroot()

# modifying an attribute
for uni in root.iter('{http://servizi.lavoro.gov.it/unisomm}UniSomm'):
    uni.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    uni.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

# changing a field text
for elem in root.findall('{http://servizi.lavoro.gov.it/unisomm}Lavoratore'):
    for ele in elem.findall('{http://servizi.lavoro.gov.it/unisomm}AnagraficaCompleta'):
        e1 = ele.find("{http://servizi.lavoro.gov.it/unisomm}nome")
        e1.text = 'new text'

# modifying an attribute
for elem in root.iter('{http://servizi.lavoro.gov.it/unisomm}AgenziaSomministrazione/{http://servizi.lavoro.gov.it/unisomm}DatoreAnagraficaCompleta/{http://servizi.lavoro.gov.it/unisomm}nome'):
    elem.set('name', 'newitem')

# adding an attribute
for elem in root.iter('{http://servizi.lavoro.gov.it/unisomm}AgenziaSomministrazione/{http://servizi.lavoro.gov.it/unisomm}DatoreAnagraficaCompleta/{http://servizi.lavoro.gov.it/unisomm}nome'):
    elem.set('name2', 'newitem2')

tree.write('newitems.xml')
