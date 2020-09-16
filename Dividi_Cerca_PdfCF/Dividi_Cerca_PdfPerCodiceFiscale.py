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
import funzioni as f

try:

    nomeProgramma = "Dividi e Cerca PDF tramite Excel By ALMAX (GitHub)"

    today = date.today().strftime("%d-%m-%Y")
    now = datetime.datetime.now().strftime("%H.%M.%S")

    f.logOperazioni("")

    if os.stat("Log.txt").st_size == 0:
        f.logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
    f.logOperazioni("\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

    colonnaExcel = 'cercare'
    pdf_da_trovare = []
    divisioniPagine = ""
    codiciFiscaliUtilizzati = []
    indici_codiciFiscaliUTilizzati = []

    cartelleSalvataggio = []
    cartelleSalvataggio.append("Cedolini_Divisi_" + today + "_" + now)
    cartelleSalvataggio.append("Cedolini_Trovati_" + today + "_" + now)

    pbar = ProgressBar()
    ROOT = tk.Tk()
    ROOT.withdraw()


    #Lettura PDF
    #nomePDF = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file PDF senza l'estensione.\nEsempio: se il file si chiama 'test.pdf', basterà inserire 'test'")ni("\t\t\tErrore PDF: " + str(errorePdf) + "\n")
    oggettoPDF = f.leggiPDF("cedolini")
    pdfFileObj = oggettoPDF[0]
    lettorePDF = oggettoPDF[1]
    numPagine = oggettoPDF[2]

    #Lettura Excel
    #nomeExcel = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")
    excelReader = f.leggiExcel("CF")

    #Creazione Cartelle
    f.creaCartelle(cartelleSalvataggio)

    #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
    try:
        for indice,valore in excelReader[colonnaExcel].iteritems():
            pdf_name = excelReader[colonnaExcel][indice] #itero le singole celle

            if(pdf_name[-4:] != ".pdf"):
                pdf_name += ".pdf" #Mi assicuro che i nomi del file siano corretti

            pdf_da_trovare.append(pdf_name) #Aggiungo il nome del pdf alla lista dei pdf da trovare
    except Exception as erroreCellaExcel:
        f.logOperazioni("\tERRORE lettura celle Excel: " + str(erroreCellaExcel) + "\n")


    # Ciclo per analizzare ogni singola pagina e dividerla
    f.logOperazioni("\tInizializzazione estrapolazione pagine\n")
    for i in pbar(range(numPagine)):
        # Ottengo il testo della singola pagina
        pageObj = lettorePDF.getPage(i)
        pageTxt = pageObj.extractText()

        #shlex si occupa di estratte ogni singola parola dell'excel in un array. psoix=False aiuta a non considerare alcuni caratteri speciali problematici
        try:
            txtExtract = shlex.split(pageTxt, posix=False)
        except Exception as errorShlex:
            f.logOperazioni("\tERRORE di shlex: " + str(errorShlex) + " alla pagina " + str(i+1) + "\n")

        #Necessario mettere a NULL in modo da evitare del tutto rinominazioni scorrette
        parola = "NULL"
        codiceFiscale = "NULL"
        codiceFiscaleStampa = "NULL"
        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            #print(parola + str(f.isCodiceFiscale(parola)[0]))
            if f.isCodiceFiscale(parola)[0]:
                #print("\n\t" + parola)
                codiceFiscale = f.isCodiceFiscale(parola)[1]
                #print("\n\t" + codiceFiscale + "\n\n")
                codiceFiscaleStampa = codiceFiscale + ".pdf"

                if (codiceFiscale in codiciFiscaliUtilizzati):
                    codiceFiscaleStampa = codiceFiscale + "-" + str(i) + ".pdf"
                    #print(str(codiciFiscaliUtilizzati.index(codiceFiscale)) + "   "+str(i+1)) #Questo print permette di dirti dove il CF è già comparso.
                break;

        codiciFiscaliUtilizzati.append(codiceFiscale)
        indici_codiciFiscaliUTilizzati.append(i)

        #Metto ogni file diviso nell'apposita cartella
        f.PDF_estraiPagine(lettorePDF, i, cartelleSalvataggio[0], codiceFiscaleStampa)
        f.logOperazioni("\t\tAlla pagina " + (str(i+1)) + " ho trovato il codice fiscale " + codiceFiscaleStampa)

        #Copio i file da cercare tramite Excel in una cartella apposita
        codiceFiscale += ".pdf"
        if codiceFiscale in pdf_da_trovare:
            f.PDF_estraiPagine(lettorePDF, i, cartelleSalvataggio[1], codiceFiscaleStampa)
            f.logOperazioni(" --> Era presente nell'Excel\n")
        else:
            f.logOperazioni(" --> NON era presente nell'Excel\n")
        #Stringa riepilogativa delle divisioni fatte
        divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscaleStampa + "\n"

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro."
    f.Mbox(nomeProgramma, numPagineOut + divisioniPagine, 1)

    f.logOperazioni("\tInizializzazione unione cedolini dello stesso Dipendente\n")
    print("Procedo con l'unione dei cedolini che fanno riferimento allo stesso dipendente; attendere per favore.")
    #f.logOperazioni("\t" + str(codiciFiscaliUtilizzati) + "\n")
    index_codiciFiscaliUtilizzati = 0
    for codiceFiscalePresente in codiciFiscaliUtilizzati:
        if codiciFiscaliUtilizzati.count(codiceFiscalePresente) > 1 and codiceFiscalePresente != "NULL":
            codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] = "NULL"
            index_codiciFiscaliUtilizzati += 1
            #print(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]))
            f.PDF_unisci(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]), cartelleSalvataggio[0])
            f.logOperazioni("\t\tHo unito il PDF: " + codiceFiscalePresente + " con il PDF: " + codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]) + "\n")
        #print(codiciFiscaliUtilizzati)
    print("Operazioni concluse. Consultare il file Log.txt per i dettagli")
    f.logOperazioni("Operazioni concluse")
    #f.logOperazioni("\t" + str(codiciFiscaliUtilizzati) + "\n")
    # Chiudo l'oggetto file
    pdfFileObj.close()

except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    f.logOperazioni("\tERRORE Generico: " + str(erroreBloccante))
    f.Mbox(nomeProgramma, messaggioErroreBloccante, 1)
