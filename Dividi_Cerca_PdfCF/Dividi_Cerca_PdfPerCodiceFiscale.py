import PyPDF2
import shlex
import os
from progressbar import ProgressBar
from datetime import date
import datetime
import sys
import pandas as pd
from tkinter import simpledialog
import tkinter as tk
import funzioni as functions
import frames as frame

try:

    nomeProgramma = "Gestione PDF By ALMAX (GitHub)"

    today = date.today().strftime("%d-%m-%Y")
    now = datetime.datetime.now().strftime("%H.%M.%S")

    functions.logOperazioni("")

    if os.stat("Log.txt").st_size == 0:
        functions.logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
    functions.logOperazioni("\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

    pdf_da_trovare = []
    codiciFiscaliUtilizzati = []
    indici_codiciFiscaliUTilizzati = []
    logPagina = []
    logPagina.append("Pagina del PDF")
    logCF = []
    logCF.append("Codice Fiscale")
    logFound = []
    logFound.append("Trovato")

    cartelleSalvataggio = []
    cartelleSalvataggio.append("Cedolini_Divisi_" + today + "_" + now)
    cartelleSalvataggio.append("Cedolini_Trovati_" + today + "_" + now)

    pbar = ProgressBar()
    ROOT = tk.Tk()
    ROOT.withdraw()

    nomi_file = frame.RichiediFile(nomeProgramma)
    nomePDF = [nome for nome in nomi_file if ".pdf" in nome][0]
    nomeExcel = [nome for nome in nomi_file if ".xls" in nome][0]

    #Lettura PDF
    oggettoPDF = functions.leggiPDF(nomePDF)
    pdfFileObj = oggettoPDF[0]
    lettorePDF = oggettoPDF[1]
    numPagine = oggettoPDF[2]

    #Lettura Excel
    colonnaExcel = nomi_file[2]
    functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel), colonnaExcel, pdf_da_trovare)

    #Creazione Cartelle
    functions.creaCartelle(cartelleSalvataggio)

    # Ciclo per analizzare ogni singola pagina e dividerla
    functions.logOperazioni("\tInizializzazione estrapolazione pagine\n")
    for i in pbar(range(numPagine)):
        # Ottengo il testo della singola pagina
        pageObj = lettorePDF.getPage(i)
        pageTxt = pageObj.extractText()

        #shlex si occupa di estratte ogni singola parola dell'excel in un array. psoix=False aiuta a non considerare alcuni caratteri speciali problematici
        try:
            txtExtract = shlex.split(pageTxt, posix=False)
        except Exception as errorShlex:
            functions.logOperazioni("\tERRORE di shlex: " + str(errorShlex) + " alla pagina " + str(i+1) + "\n")

        #Necessario mettere a NULL in modo da evitare del tutto rinominazioni scorrette
        parola = "NULL"
        codiceFiscale = "NULL"
        codiceFiscaleStampa = "NULL"
        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            #print(parola + str(functions.isCodiceFiscale(parola)[0]))
            if functions.isCodiceFiscale(parola)[0]:
                #print("\n\t" + parola)
                codiceFiscale = functions.isCodiceFiscale(parola)[1]
                #print("\n\t" + codiceFiscale + "\n\n")
                codiceFiscaleStampa = codiceFiscale + ".pdf"

                if (codiceFiscale in codiciFiscaliUtilizzati):
                    codiceFiscaleStampa = codiceFiscale + "-" + str(i) + ".pdf"
                    #print(str(codiciFiscaliUtilizzati.index(codiceFiscale)) + "   "+str(i+1)) #Questo print permette di dirti dove il CF è già comparso.
                break;

        codiciFiscaliUtilizzati.append(codiceFiscale)
        indici_codiciFiscaliUTilizzati.append(i)

        #Metto ogni file diviso nell'apposita cartella
        functions.PDF_estraiPagine(lettorePDF, i, cartelleSalvataggio[0], codiceFiscaleStampa)
        logPagina.append("Pagina " + (str(i+1)))
        logCF.append(codiceFiscale)

        #Copio i file da cercare tramite Excel in una cartella apposita
        #codiceFiscale += ".pdf"
        if codiceFiscale in pdf_da_trovare:
            functions.PDF_estraiPagine(lettorePDF, i, cartelleSalvataggio[1], codiceFiscaleStampa)
            logFound.append("Era presente nell'Excel")
        else:
            logFound.append("NON era presente nell'Excel")

    functions.logOperazioni("\tInizializzazione unione cedolini dello stesso Dipendente\n")
    print("Procedo con l'unione dei cedolini che fanno riferimento allo stesso dipendente; attendere per favore.")
    #functions.logOperazioni("\t" + str(codiciFiscaliUtilizzati) + "\n")
    index_codiciFiscaliUtilizzati = 0
    for codiceFiscalePresente in codiciFiscaliUtilizzati:
        if codiciFiscaliUtilizzati.count(codiceFiscalePresente) > 1 and codiceFiscalePresente != "NULL":
            codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] = "NULL"
            index_codiciFiscaliUtilizzati += 1
            #print(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]))
            functions.PDF_unisci(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]), cartelleSalvataggio[0])
            #functions.PDF_unisci(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]), cartelleSalvataggio[1])
            functions.logOperazioni("\t\tHo unito il PDF: " + codiceFiscalePresente + " con il PDF: " + codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]) + "\n")
        #print(codiciFiscaliUtilizzati)
    print("Operazioni concluse.")
    functions.Mbox(nomeProgramma, "Operazioni concluse. Consultare il file Log.txt per i dettagli", 1)
    functions.logOperazioni("Operazioni concluse.")
    #functions.logOperazioni("\t" + str(codiciFiscaliUtilizzati) + "\n")
    # Chiudo l'oggetto file
    pdfFileObj.close()
    functions.logExcel(logPagina, logCF, logFound)

except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    functions.logOperazioni("\tERRORE Generico: " + str(erroreBloccante))
    functions.Mbox(nomeProgramma, messaggioErroreBloccante, 1)
