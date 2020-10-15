import time
from zipfile import ZipFile
import xml.dom.minidom
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xml_structure as xmlManipulation
import frames as frame


ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
namespace = "{http://servizi.lavoro.gov.it/unisomm}"
returnFrame = frame.RichiediFile("Programmino Laura")


with ZipFile('/Users/Ali Haider Maqsood/Documents/GitHub/MAW/Modifica_campi_xml/compressa.zip', 'r') as zipObj:
    listOfiles = zipObj.namelist()
    for file in listOfiles:
        tree = ET.parse(zipObj.open(file))
        root = tree.getroot()

        for xmlns_setting in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
            xmlns_setting.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
            xmlns_setting.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

        for campi_modifica in range(returnFrame[1]):
            coordinate = returnFrame[2]
            xmlManipulation.modificaCampo(root, namespace, coordinate)


        tree.write("newitems" + str(file),encoding="utf-8", xml_declaration=True)


