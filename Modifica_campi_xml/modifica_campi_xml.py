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
from xmldiff import main
from xmldiff import formatting
import re

try:
    functions.logOperazioni("")
    nomeProgramma = "Modificatore XML By ALMAX (GitHub)"
    ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
    namespace = "{http://servizi.lavoro.gov.it/unisomm}"
    returnFrame = frame.RichiediFile(nomeProgramma)
    campi = returnFrame[1]
    tutte_coordinate = returnFrame[2]
    progress = returnFrame[3]
    nome_zip = returnFrame[0]
    coordinate = []
    
    logExcel = []
    logExcel = functions.creaArrayConArray(logExcel, 
    ["FILE", 
    "CAMPO DA MODIFICARE", 
    "VALORE DA MODIFICARE", 
    "VALORE MODIFICATO", 
    "ESITO", 
    "DIFFERENZE"])

    zipObj = ZipFile(nome_zip, 'r')
    listOfiles = zipObj.namelist()
    functions.logOperazioni("\nHo letto lo zip " + str(nome_zip) + ";\nho trovando i seguenti file: " + str(listOfiles) + "\n")

    progress['maximum'] = len(listOfiles)*2
    indice_prorgress = 0
    indice_compare = 0

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
                coordinataXML = xmlManipulation.modificaCampo(root, namespace, coordinate, tutte_coordinate[i], logExcel[2])
                if coordinataXML == "CampoVuoto":
                    break

                logExcel[0].append(str(file))
                logExcel[1].append(str(coordinataXML[(coordinataXML.rfind("}"))+1:]))
                logExcel[3].append(str(tutte_coordinate[i]))
                logExcel[4].append("Positivo")
            except:
                functions.logOperazioni("\n\tERRORE CICLO PER MODIFICARE I CAMPI: " + traceback.format_exc())
                logExcel[0].append(str(file))
                logExcel[1].append(str(coordinataXML[38:]))
                logExcel[3].append(str(tutte_coordinate[i]))
                logExcel[4].append("Negativo")

        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(0.1)
        functions.logOperazioni("\n\tModifica dei campi per il file " + str(file) + " conclusa.\n")

        if file == listOfiles[0]:
            #os.remove(nome_zip)
            #functions.logOperazioni("\nTento di modificare lo Zip.\n")
            zipNuovo = ZipFile("copia.zip", 'w')


        functions.logOperazioni("\tRiscrittura del file: " + file)
    
        #controllo_xsd = functions.verifica_XML_XSD(file, "verifica.xsd")
        #for righe_excel in range(int(len(logExcel0)/len(listOfiles))):
        #    logExcel5.append(controllo_xsd)
        #tree = ET.parse(zipObj.open(file))
        tree.write(str(file), encoding="utf-8", xml_declaration=True)
        
        indice_compare += 1
        zipNuovo.write(file)
        os.remove(file)
        functions.logOperazioni("\n\tRiscrittura conclusa.\n")     

        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(0.1)

    zipObj.close()
    zipNuovo.close()

    zipOld = ZipFile(nome_zip, 'r')
    zipNew = ZipFile("copia.zip", 'r')

    for file in zipOld.namelist():
        differenze = main.diff_files(zipOld.open(file), zipNew.open(file))
        functions.logOperazioni("\nDifferenze nel file " + str(file) + " rispetto l'originale:")
        functions.logOperazioni("\n\t" + str(differenze))
        
        for righe_excel in range(int(len(logExcel[0])/len(listOfiles))):
            logExcel[5].append(str(differenze))

    zipOld.close()
    zipNew.close()

    os.remove(nome_zip)
    os.rename("copia.zip", nome_zip)

    functions.logExcel(logExcel)
    functions.logOperazioni("\n\nOperazioni concluse con successo!")
except:
    functions.logOperazioni("\n\nERRORE GENERALE: " + traceback.format_exc())

functions.Mbox(nomeProgramma, "Operazioni concluse,\nconsultare OBBLIGATORIAMENTE il file Log.xlsx\ned il file Log.txt per i dettagli.")