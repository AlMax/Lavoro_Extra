import ctypes
import os
import time
import datetime
import xlsxwriter
from lxml import etree
from io import StringIO
import traceback
import openpyxl
from string import ascii_uppercase
import win32com.client as win32

today = datetime.date.today().strftime("%d-%m-%Y")
now = datetime.datetime.now().strftime("%H.%M.%S")

def creaCartelle(nomi_cartelle):
    """Dato in input un array di stringe, creerà delle cartelle con le relative stringhe.
    Ritoenrà infine una stringa con gli esiti delle varie creazioni"""
    if isinstance(nomi_cartelle,list):
        for directory in nomi_cartelle:
            try:
                os.mkdir(directory)
                logOperazioni("Cartella " + directory + " creata.\n")
            except OSError as erroreCartella:
                logOperazioni("\tERRORE nel creare la cartella --> " + str(erroreCartella) + "\n")
    else:
        try:
            os.mkdir(nomi_cartelle)
            logOperazioni("Cartella " + nomi_cartelle + " creata.\n")
        except OSError:
            logOperazioni("\tERRORE nel creare la cartella " + nomi_cartelle + ", probabilmente esiste già.\n")

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    if log == "":
        if os.stat("Log.txt").st_size == 0:
            logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
        logOperazioni("\n\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")
    fileLog.write(log)
    fileLog.close()

def logExcel(colonne):
    nomeExcel = "Log.xlsx"
    workbook = xlsxwriter.Workbook(nomeExcel)
    worksheet = workbook.add_worksheet()

    for colonna in colonne:
        compilaColonnaExcel(worksheet, colonna, int(colonne.index(colonna)))

    workbook.close()
    riadattaColonneExcel(nomeExcel)
    logOperazioni("\n" + nomeExcel + " creato con successo!\n")

def riadattaColonneExcel(nomeExcel):
    try:
        currentDirectory = os.getcwd()
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(currentDirectory + '\\' + nomeExcel)
        ws = wb.Worksheets("Sheet1")
        ws.Columns.AutoFit()
        wb.Save()
        excel.Application.Quit()
        logOperazioni("\n\n" + nomeExcel + " ha le colonne riadattate correttamente.")
    except:
        logOperazioni("\n\n" + nomeExcel + " ha le colonne riadattate malissimo.")

def compilaColonnaExcel(worksheet, colonna, nColonna):
    row = 0
    for cella in colonna:
        worksheet.write(row, nColonna, cella)
        row += 1

def creaArrayConArray(array, contenutoArrayInterni):
    for contenuto in contenutoArrayInterni:
        array.append([])
        array[-1].append(contenuto)
    return array

def verifica_XML_XSD(filename_xml, filename_xsd):
    txt_conclusivo = ""

    # open and read schema file
    with open(filename_xsd, 'r') as schema_file:
        schema_to_check = schema_file.read()

    # open and read xml file
    with open(filename_xml, 'r') as xml_file:
        xml_to_check = xml_file.read()

    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    try:
        doc = etree.parse(StringIO(xml_to_check))
        txt_conclusivo += "Sintassi XML OK; \n"

    # check for file IO error
    except IOError as ioError:
        txt_conclusivo += "ERRORE File non valido: " + str(ioError) + "; \n"

    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        txt_conclusivo += "ERRORE Sinstassi XML: " + str(err) +"; \n"
        logOperazioni("\n\t\tERRORE Sinstassi XML: " + str(err.error_log))

    except Exception as errore:
        txt_conclusivo += "ERRORE Eccezione Sintassi XML: " + str(errore) + "; \n"
        logOperazioni("\n\t\tERRORE Eccezione Sintassi XML: " + str(errore))


    # validate against schema
    try:
        xmlschema.assertValid(doc)
        txt_conclusivo += "Schema XML Valido; \n"

    except etree.DocumentInvalid as err:
        txt_conclusivo += "ERRORE schema XML non valido: " + str(err) + "; \n"
        logOperazioni("\n\t\tERRORE schema XML non valido: " + str(err.error_log))

    except:
        txt_conclusivo += "ERRORE sconosciuto con lo schema: " + str(traceback.format_exc()) + "; \n"
        logOperazioni("\n\t\tERRORE sconosciuto con lo schema: " + str(traceback.format_exc()))

    xml_file = etree.parse(filename_xml)
    xml_validator = etree.XMLSchema(file=filename_xsd)

    is_valid = xml_validator.validate(xml_file)

    txt_conclusivo += "L'XML rispetta la struttura definita nell' XSD? " + str(is_valid)
    logOperazioni("\n\t\tL'XML rispetta la struttura definita nell' XSD? " + str(is_valid))

    if txt_conclusivo == "Sintassi XML OK; \nSchema XML Valido; \nL'XML rispetta la struttura definita nell' XSD? True":
        return "Convalidazione Corretta"
    return txt_conclusivo

def Mbox(title, text):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)