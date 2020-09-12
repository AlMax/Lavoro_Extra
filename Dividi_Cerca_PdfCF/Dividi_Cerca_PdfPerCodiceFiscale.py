import ctypes
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

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

try:

    nomeProgramma = "Dividi e Cerca PDF tramite Excel By ALMAX (GitHub)"

    today = date.today().strftime("%d-%m-%Y")
    now = datetime.datetime.now().strftime("%H:%M:%S")

    fileLog = open("Log.txt", "a")
    if os.stat("Log.txt").st_size == 0:
        fileLog.write("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
    fileLog.write("\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

    colonnaExcel = 'cercare'
    pdf_da_trovare = []
    divisioniPagine = ""
    codiciFiscaliUtilizzati = []

    directoryDivisi = "Cedolini_Divisi " + today
    directoryCercati = "Cedolini_Trovati " + today

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
        Mbox(nomeProgramma,"Ci sono errori durante la lettura del PDF: " + nomePDF + ".pdf\nIl programma verrà interrotto.Si ricorda di inerire il nome correttamente.", 1)
        fileLog.write("Errore PDF: " + errorePdf + "\n")
        sys.exit()

    #Lettura Excel
    try:
        #nomeExcel = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")
        nomeExcel = "CF"
        excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
    except Exception as erroreExcel:
        Mbox(nomeProgramma,"Ci sono errori durante la lettura dell'excel: " + nomeExcel + ".xlsx\nIl programma cercherà comunque di dividere il singolo PDF.", 1)
        fileLog.write("Errore Excel: " + erroreExcel + "\n")

    #Creazione Cartelle
    try:
        os.mkdir(directoryDivisi)
        os.mkdir(directoryCercati)
        erroreDirectory = "Tutto è andato a Buon fine.\n\n"
    except OSError:
        erroreDirectory =  "Errore nel creare la cartella, probabilmente esiste già.\nSi raccomanda di far partire un programma in una cartella vuota.\nIl programma cercherà comunque di generare i PDF ma potrebbero esserci delle anomalie e mancare dei PDF.\n\n"


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
    fileLog.write("\tInizializzazione esrapolazione pagine\n")
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
        unito = False
        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            if len(parola) == 16:
                if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
                    codiceFiscale = parola
                    codiceFiscaleStampa = codiceFiscale + ".pdf"

                if (codiceFiscale in codiciFiscaliUtilizzati):
                    #print(codiciFiscaliUtilizzati)
                    #unisciPdf = PyPDF2.PdfFileWriter()
                    #unisciPdf.addPage(pdfReader.getPage(codiciFiscaliUtilizzati.index(codiceFiscale)+1))
                    #codiciFiscaliUtilizzati[codiciFiscaliUtilizzati.index(codiceFiscale)] = "UNITO A " + codiceFiscale
                    #print(codiciFiscaliUtilizzati)
                    #print(codiceFiscale + "\n\n")
                    #codiceFiscaleStampa = codiceFiscale + "-" + str(i) + ".pdf"
                    #print(str(codiciFiscaliUtilizzati.index(codiceFiscale)) + "   "+str(i+1)) #Questo print permette di dirti dove il CF è già comparso.
                    oggettoPDF = open(directoryDivisi + "/" + codiceFiscale + ".pdf", 'rb')
                    lettorePDF = PyPDF2.PdfFileReader(oggettoPDF)
                    cercatorePDF = PyPDF2.PdfFileWriter()
                    paginePDF = pdfReader.numPages
                    for j in range(paginePDF):
                        cercatorePDF.addPage(lettorePDF.getPage(0))
                    cercatorePDF.addPage(pdfReader.getPage(i))

                    with open(directoryDivisi + "/" + codiceFiscale + ".pdf", "wb") as pdfUnito:
                        cercatorePDF.write(pdfUnito)
                    unito = True;
                    

        if not unito:
            # Divido la singola pagina dal PDF
            divisorePDF = PyPDF2.PdfFileWriter()
            divisorePDF.addPage(pdfReader.getPage(i))

            #Metto ogni file diviso nell'apposita cartella
            with open(directoryDivisi + "/" + codiceFiscaleStampa, "wb") as pdfDiviso:
                divisorePDF.write(pdfDiviso)
                fileLog.write("\t\tAlla pagina " + (str(i+1)) + " ho trovato il codice fiscale " + codiceFiscaleStampa)
                codiciFiscaliUtilizzati.append(codiceFiscale)

            #Copio i file da cercare tramite Excel in una cartella apposita
            codiceFiscale += ".pdf"
            if codiceFiscale in pdf_da_trovare:
                with open(directoryCercati + "/" + codiceFiscaleStampa, "wb") as pdfDiviso:
                    divisorePDF.write(pdfDiviso)
                    fileLog.write(" --> Era presente nell'Excel\n")
            else:
                fileLog.write(" --> NON era presente nell'Excel\n")

            #Stringa riepilogativa delle divisioni fatte
            divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscaleStampa + "\n"

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = erroreDirectory + "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro."
    Mbox(nomeProgramma, numPagineOut + divisioniPagine, 1)

    fileLog.write("Operazioni concluse")
    # Chiudo l'oggetto file
    pdfFileObj.close()
    fileLog.close()
except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    fileLog.write("Errore Generico: " + str(erroreBloccante))
    Mbox(nomeProgramma, messaggioErroreBloccante, 1)
