import time
from zipfile import ZipFile
import xml.dom.minidom
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xml_structure as xmlManipulation
import frames as frame
import os

ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
namespace = "{http://servizi.lavoro.gov.it/unisomm}"
returnFrame = frame.RichiediFile("Programmino Laura")
campi = returnFrame[1]
tutte_coordinate = returnFrame[2]
nome_zip = returnFrame[0]
coordinate = []

with ZipFile(nome_zip, 'r') as zipObj:
    listOfiles = zipObj.namelist()
    for file in listOfiles:
        tree = ET.parse(zipObj.open(file))
        root = tree.getroot()

        for xmlns_setting in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
            xmlns_setting.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
            xmlns_setting.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

        for campi_modifica in range(campi):
            i = campi_modifica
            coordinate.clear()
            for coordinata in range(int(len(tutte_coordinate)/campi)-1):

                coordinate.append(tutte_coordinate[i])
                i += campi

            xmlManipulation.modificaCampo(root, namespace, coordinate, tutte_coordinate[i])

os.remove(nome_zip)
zipNuovo = ZipFile(nome_zip, 'w')
for file in listOfiles:
    tree.write(str(file),encoding="utf-8", xml_declaration=True)
    zipNuovo.write(file)
    os.remove(file)


