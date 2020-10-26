import time
from zipfile import ZipFile
import xml.dom.minidom
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xml_structure as xmlManipulation
import frames as frame
import os
import funzioni as functions
import traceback

try:
    nomeProgramma = "Modificatore XML By ALMAX (GitHub)"
    ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
    namespace = "{http://servizi.lavoro.gov.it/unisomm}"
    returnFrame = frame.RichiediFile(nomeProgramma)
    campi = returnFrame[1]
    tutte_coordinate = returnFrame[2]
    progress = returnFrame[3]
    nome_zip = returnFrame[0]
    coordinate = []

    functions.logOperazioni("")
    logExcel0 = ["FILE"]
    logExcel1 = ["CAMPO DA MODIFICARE"]
    logExcel2 = ["VALORE DA MODIFICARE"]
    logExcel3 = ["VALORE MODIFICATO"]
    logExcel4 = ["ESITO"]

    with ZipFile(nome_zip, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        functions.logOperazioni("\nHo letto lo zip " + str(nome_zip) + ", trovando i seguenti file: " + str(listOfiles) + "\n")

        progress['maximum'] = len(listOfiles)*2
        indice_prorgress = 0

        for file in listOfiles:
            functions.logOperazioni("\n\tInizio a modificare il file " + str(file))
            tree = ET.parse(zipObj.open(file))
            root = tree.getroot()

            for xmlns_setting in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
                xmlns_setting.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
                xmlns_setting.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

            for campi_modifica in range(campi):
                i = campi_modifica
                coordinate.clear()

                try:
                    for coordinata in range(int(len(tutte_coordinate)/campi)-1):

                        coordinate.append(tutte_coordinate[i])
                        i += campi

                    functions.logOperazioni("\n\tFaccio partire il metodo per trovare il campo selezionato e modificarne il testo con: " + str(tutte_coordinate[i]))
                    coordinataXML = xmlManipulation.modificaCampo(root, namespace, coordinate, tutte_coordinate[i], logExcel2)

                    logExcel0.append(str(file))
                    logExcel1.append(str(coordinataXML))
                    logExcel3.append(str(tutte_coordinate[i]))
                    logExcel4.append("Positivo")
                except:
                    functions.logOperazioni("\n\tERRORE CICLO PER MODIFICARE I CAMPI: " + traceback.format_exc())
                    logExcel0.append(str(file))
                    logExcel1.append(str(coordinataXML))
                    logExcel3.append(str(tutte_coordinate[i]))
                    logExcel4.append("Negativo")

            indice_prorgress += 1
            progress["value"] = indice_prorgress
            progress.update()
            time.sleep(1)
            functions.logOperazioni("\n\tModifica dei campi per il file " + str(file) + " conclusa.\n")

    functions.logOperazioni("\nTento di rimuovere il vecchio zip e ricreare il nuovo.")
    os.remove(nome_zip)
    zipNuovo = ZipFile(nome_zip, 'w')
    for file in listOfiles:
        tree.write(str(file),encoding="utf-8", xml_declaration=True)
        zipNuovo.write(file)
        os.remove(file)

        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(1)
    functions.logExcel(logExcel0, logExcel1, logExcel2, logExcel3, logExcel4)
    functions.logOperazioni("\nOperazioni concluse con successo!")
except:
    functions.logOperazioni("\nERRORE GENERALE: " + traceback.format_exc())

functions.Mbox(nomeProgramma, "Operazioni concluse, consultare il file Log.txt per i dettagli.")

