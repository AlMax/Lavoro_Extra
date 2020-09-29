from xml.dom import minidom
from lxml import etree
import os
import funzioni as functions
import re
from lxml import etree
from io import StringIO
import sys
import frames as frame
from datetime import date
import datetime
from tkinter import *
from tkinter import ttk
import time


try: 
    today = date.today().strftime("%d-%m-%Y")
    now = datetime.datetime.now().strftime("%H.%M.%S")

    functions.logOperazioni("")

    if os.stat("Log.txt").st_size == 0:
        functions.logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
    functions.logOperazioni("\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

    documento = minidom.Document()
    xml = documento.createElement('tis')
    documento.appendChild(xml)

    attributi_istanza = []
    attributi_istanza.extend(["identificativoPratica", "denominazioneAPL", "ragioneSocialeUtilizzatore", "partitaIvaUtilizzatore", "matricolaInpsUtilizzatore", "codiceAtecoUtilizzatore", "sedeUnitaProduttiva", "mensilitaAggiuntive", "settoreRiferimento", "autocertificazioneSettimane", "note"])

    dati_tutti_lavoratori = []
    dati_tutti_lavoratori.extend(["annoRiferimento", "meseRiferimento", "codiceFiscale", "cognome", "nome", "tipologiaContratto", "sgraviAliquotaContributivaPrevidenziale", "retribuzioneMensileLorda", "retribuzioneTisRiconosciuta", "contribuzioneTisRiconosciuta", "quotaRateiMensilitaAggiuntive", "quotaRateiRolPermessiFerie", "totaleOreTisRiconosciute", "lavoratoreAlleDipendenze25Marzo"])

    tutti_lavoratori = [[]]
    tutti_clienti = [[]]
    array = []
    lista = []
    identificativi_lavoratori = []

    nomeProgramma = "Convertitore XML By ALMAX (GitHub)"
    frameReturn = frame.RichiediFile(nomeProgramma)

    nomi_file = frameReturn[0]
    nomeExcel = [nome for nome in nomi_file if ".xls" in nome][0]

    progressBar = frameReturn[1]


    functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, nomi_file[2]), "identificativoPratica", identificativi_lavoratori)


    indice = 0
    for dato_lavoratori in dati_tutti_lavoratori:
        colonnaExcel = dato_lavoratori
        functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, nomi_file[2]), colonnaExcel, array)
        if indice == 0:
            tutti_lavoratori[0] = array.copy()
        else:
            lista = array.copy()
            tutti_lavoratori.append(lista)
        array.clear()
        indice += 1

    progressBar['maximum'] = len(tutti_lavoratori[2])

    indice = 0
    for attributo in attributi_istanza:
        colonnaExcel = attributo
        functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, nomi_file[1]), colonnaExcel, array)
        if indice == 0:
            tutti_clienti[0] = array.copy()
        else:
            lista = array.copy()
            tutti_clienti.append(lista)
        array.clear()
        indice += 1

    indice_dato_cliente = 0
    for cliente in range(len(tutti_clienti[0])):
        indice_array_cliente = 0

        functions.logOperazioni("Inizio estrapolazione del cliente " + str(tutti_clienti[indice_array_cliente]) + "\n")
        padre = documento.createElement('istanza')
        xml.appendChild(padre)
    
        for attributo in attributi_istanza:
            figlio = documento.createElement(attributo)
            dato_cliente = tutti_clienti[indice_array_cliente]
            if dato_cliente[indice_dato_cliente] == 'nan':
                figlio.appendChild(documento.createTextNode(""))
            else:
                figlio.appendChild(documento.createTextNode(dato_cliente[indice_dato_cliente]))
            padre.appendChild(figlio)
            indice_array_cliente += 1
        

        figlio = documento.createElement('lavoratori')
        padre.appendChild(figlio)

        indice_dato_lavoratore = 0
        
        for lavoratore in range(len(tutti_lavoratori[2])):

            progressBar["value"] = indice_dato_lavoratore
            time.sleep(0.05)
            progressBar.update()

            functions.logOperazioni("Estrapolato " + str(indice_dato_lavoratore+1) + " lavoratore su " + str(len(tutti_lavoratori[2])) + " lavoratori.\n")
            identificativoPratica = tutti_clienti[0]
            if identificativi_lavoratori[lavoratore] == identificativoPratica[indice_dato_cliente]:
                nipote = documento.createElement('lavoratore')
                figlio.appendChild(nipote)

            indice_array_lavoratore = 0
            for dati_lavoratore in dati_tutti_lavoratori:
                
                if identificativi_lavoratori[lavoratore] == identificativoPratica[indice_dato_cliente]:
                    pro_nipote = documento.createElement(dati_lavoratore)
                    dato_lavoratore = tutti_lavoratori[indice_array_lavoratore]
                    pro_nipote.appendChild(documento.createTextNode(dato_lavoratore[indice_dato_lavoratore]))
                    nipote.appendChild(pro_nipote)
                
                indice_array_lavoratore += 1
            indice_dato_lavoratore += 1
        
        functions.logOperazioni("Concludo estrpolazione del cliente " + str(indice_dato_cliente+1) + "\n")
    
        indice_dato_cliente += 1



    xml_str = documento.toprettyxml(indent="\t")


    save_path_file = "test.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


    filename_xml = "test.xml"
    filename_xsd = "validation.xsd"

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
        print('XML well formed, syntax ok.')

    # check for file IO error
    except IOError:
        print('Invalid File')

    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        print('XML Syntax Error, see error_syntax.log')
        with open('error_syntax.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except Exception as errore:
        print(errore)
        quit()


    # validate against schema
    try:
        xmlschema.assertValid(doc)
        print('XML valid, schema validation ok.')

    except etree.DocumentInvalid as err:
        print('Schema validation error, see error_schema.log')
        with open('error_schema.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except:
        print('Unknown error, exiting.')
        quit()





    xml_file = etree.parse("test.xml")
    xml_validator = etree.XMLSchema(file="validation.xsd")

    is_valid = xml_validator.validate(xml_file)

    print("L'XML rispetta la struttura definita nell' XSD? " + str(is_valid))


    tree = etree.parse("test.xml")
    string = etree.tostring(tree.getroot(), pretty_print = False, xml_declaration = True, standalone = True, encoding = "UTF-8")
    with open("test.xml", "wb") as f:
        f.write(string)

    
   
except Exception as erroreGenerale:
    print(str(erroreGenerale)) 