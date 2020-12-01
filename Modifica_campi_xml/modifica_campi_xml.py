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
import difflib
from xmldiff import formatting
import re
from os import walk

try:
    functions.logOperazioni("")
    nomeProgramma = "Modificatore XML By ALMAX (GitHub)"
    ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
    namespace = "{http://servizi.lavoro.gov.it/unisomm}"
    returnFrame = frame.RichiediFile(nomeProgramma)
    campi = returnFrame[1]
    tutte_coordinate = returnFrame[2]
    progress = returnFrame[3]
    nome_directory = returnFrame[0]
    elencoZip = []
    elencoZip.clear
    coordinate = []
    listaDifferenze = []
    
    logExcel = []
    logExcel = functions.creaArrayConArray(logExcel, 
    ["FILE", 
    "CAMPO DA MODIFICARE", 
    "VALORE DA MODIFICARE", 
    "VALORE MODIFICATO", 
    "ESITO", 
    "DIFFERENZE"])

    for (dirpath, dirnames, filenames) in walk(nome_directory):
        print(filenames)
    
    for singoloFile in filenames:
        if(singoloFile.endswith('.zip')):
            elencoZip.append(singoloFile)
    #print(elencoZip)

    indice_prorgress = 0
    for nome_file_zip in elencoZip:
        logExcel[0].clear()
        logExcel[1].clear()
        logExcel[3].clear()
        logExcel[4].clear()
        logExcel[5].clear()

        nome_zip = nome_directory + "/" + nome_file_zip
        zipObj = ZipFile(nome_zip, 'r')
        listOfiles = zipObj.namelist()
        functions.logOperazioni("\nHo letto lo zip " + str(nome_zip) + ";\nho trovando i seguenti file: " + str(listOfiles) + "\n")

        progress['maximum'] = (len(listOfiles)*3*len(elencoZip)) + 2
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
                zipNuovo = ZipFile("copia.zip", 'w')


            functions.logOperazioni("\tRiscrittura del file: " + file)
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
            treeOld = ET.parse(zipOld.open(file)).getroot()
            treeNew = ET.parse(zipNew.open(file)).getroot()
            oldS = ET.tostring(treeOld, encoding='utf8', method='xml')
            newS = ET.tostring(treeNew, encoding='utf8', method='xml')
            splitOld = oldS.decode().split("\n")
            splitNew = newS.decode().split("\n")
            differenze = difflib.ndiff(splitOld, splitNew)
            functions.logOperazioni("\nDifferenze nel file " + str(file) + " rispetto l'originale:")

            listaDifferenze.clear()
            for riga in differenze:
                if riga.startswith("- ") or riga.startswith("+ "):
                    listaDifferenze.append(riga)
            functions.logOperazioni("\n\t" + str(list(listaDifferenze)) + "\n")
            
            for righe_excel in range(int(len(logExcel[0])/len(listOfiles))):
                logExcel[5].append(str(list(listaDifferenze)))

            indice_prorgress += 1
            progress["value"] = indice_prorgress
            progress.update()
            time.sleep(0.1)

        zipOld.close()
        zipNew.close()

        os.remove(nome_zip)
        os.rename("copia.zip", nome_zip)

        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(0.1)

        #functions.logExcel(logExcel)
        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(0.1)
    functions.logOperazioni("\n\nOperazioni concluse con successo!")
except:
    functions.logOperazioni("\n\nERRORE GENERALE: " + traceback.format_exc())

functions.Mbox(nomeProgramma, "Operazioni concluse,\nconsultare OBBLIGATORIAMENTE il file Log.xlsx\ned il file Log.txt per i dettagli.")