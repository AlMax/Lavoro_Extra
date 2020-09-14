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

    fileLog = open("Log.txt", "a")
    if os.stat("Log.txt").st_size == 0:
        fileLog.write("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
    fileLog.write("\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

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
    try:
        #nomePDF = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file PDF senza l'estensione.\nEsempio: se il file si chiama 'test.pdf', basterà inserire 'test'")
        nomePDF = "cedolini"
        pdfFileObj = open(nomePDF+".pdf", 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        numPagine = pdfReader.numPages
    except Exception as errorePdf:
        f.Mbox(nomeProgramma,"Ci sono errori durante la lettura del PDF: " + nomePDF + ".pdf\nIl programma verrà interrotto.Si ricorda di inerire il nome correttamente.", 1)
        fileLog.write("Errore PDF: " + errorePdf + "\n")
        sys.exit()

    #Lettura Excel
    try:
        #nomeExcel = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")
        nomeExcel = "CF"
        excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
    except Exception as erroreExcel:
        f.Mbox(nomeProgramma,"Ci sono errori durante la lettura dell'excel: " + nomeExcel + ".xlsx\nIl programma cercherà comunque di dividere il singolo PDF.", 1)
        fileLog.write("Errore Excel: " + erroreExcel + "\n")

    #Creazione Cartelle
    fileLog.write(f.creaCartelle(cartelleSalvataggio))

    #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
    try:
        for indice,valore in excelReader[colonnaExcel].iteritems():
            pdf_name = excelReader[colonnaExcel][indice] #itero le singole celle

            if(pdf_name[-4:] != ".pdf"):
                pdf_name += ".pdf" #Mi assicuro che i nomi del file siano corretti

            pdf_da_trovare.append(pdf_name) #Aggiungo il nome del pdf alla lista dei pdf da trovare
    except Exception as erroreCellaExcel:
        fileLog.write("Errore lettura celle Excel: " + erroreCellaExcel + "\n")


    # Ciclo per analizzare ogni singola pagina e dividerla
    fileLog.write("\tInizializzazione estrapolazione pagine\n")
    for i in pbar(range(numPagine)):
        # Ottengo il testo della singola pagina
        pageObj = pdfReader.getPage(i)
        pageTxt = pageObj.extractText()

        #shlex si occupa di estratte ogni singola parola dell'excel in un array. psoix=False aiuta a non considerare alcuni caratteri speciali problematici
        try:
            txtExtract = shlex.split(pageTxt, posix=False)
        except Exception as errorShlex:
            fileLog.write("Errore di shlex: " + str(errorShlex) + " alla pagina " + str(i+1) + "\n")

        #Necessario mettere a NULL in modo da evitare del tutto rinominazioni scorrette
        parola = "NULL"
        codiceFiscale = "NULL"
        codiceFiscaleStampa = "NULL"
        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            if f.isCodiceFiscale(parola):
                print("\n\t" + parola)
                codiceFiscale = f.isCodiceFiscale(parola)[1]
                print("\n\t" + codiceFiscale + "\n\n")
                codiceFiscaleStampa = codiceFiscale + ".pdf"
                
                if (codiceFiscale in codiciFiscaliUtilizzati):
                    codiceFiscaleStampa = codiceFiscale + "-" + str(i) + ".pdf"
                    #print(str(codiciFiscaliUtilizzati.index(codiceFiscale)) + "   "+str(i+1)) #Questo print permette di dirti dove il CF è già comparso.
                break;

        codiciFiscaliUtilizzati.append(codiceFiscale)
        indici_codiciFiscaliUTilizzati.append(i)

        #Metto ogni file diviso nell'apposita cartella
        f.PDF_estraiPagine(pdfReader, i, cartelleSalvataggio[0], codiceFiscaleStampa)
        fileLog.write("\t\tAlla pagina " + (str(i+1)) + " ho trovato il codice fiscale " + codiceFiscaleStampa)

        #Copio i file da cercare tramite Excel in una cartella apposita
        codiceFiscale += ".pdf"
        if codiceFiscale in pdf_da_trovare:
            f.PDF_estraiPagine(pdfReader, i, cartelleSalvataggio[1], codiceFiscaleStampa)
            fileLog.write(" --> Era presente nell'Excel\n")
        else:
            fileLog.write(" --> NON era presente nell'Excel\n")
        #Stringa riepilogativa delle divisioni fatte
        divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscaleStampa + "\n"

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro."
    f.Mbox(nomeProgramma, numPagineOut + divisioniPagine, 1)

    fileLog.write("\tInizializzazione unione cedolini dello stesso Dipendente\n")
    fileLog.write("\t" + str(codiciFiscaliUtilizzati) + "\n")
    index_codiciFiscaliUtilizzati = 0
    for codiceFiscalePresente in codiciFiscaliUtilizzati:
        if codiciFiscaliUtilizzati.count(codiceFiscalePresente) > 1 and codiceFiscalePresente != "NULL":
            codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] = "NULL"
            index_codiciFiscaliUtilizzati += 1
            print(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]))
            f.PDF_unisci(codiceFiscalePresente,codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]), cartelleSalvataggio[0])
            fileLog.write("\t\tHo unito il PDF: " + codiceFiscalePresente + " con il PDF: " + codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)] + "-" + str(indici_codiciFiscaliUTilizzati[codiciFiscaliUtilizzati.index(codiceFiscalePresente)]) + "\n")
        #print(codiciFiscaliUtilizzati)

    fileLog.write("Operazioni concluse")
    fileLog.write("\t" + str(codiciFiscaliUtilizzati) + "\n")
    # Chiudo l'oggetto file
    pdfFileObj.close()

    fileLog.close()
except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    fileLog.write("Errore Generico: " + str(erroreBloccante))
    f.Mbox(nomeProgramma, messaggioErroreBloccante, 1)
