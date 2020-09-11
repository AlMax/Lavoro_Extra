import ctypes
import PyPDF2
import shlex
import os
from progressbar import ProgressBar
from datetime import date
import sys
import pandas as pd
from tkinter import simpledialog
import tkinter as tk

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

try:

    ROOT = tk.Tk()
    ROOT.withdraw()

    # Oggetto PDF
    nomePDF = simpledialog.askstring(title="Dividi e Cerca PDF tramite Excel",
                                      prompt="Inserire il nome del file PDF senza l'estensione.\nEsempio: se il file si chiama 'test.pdf', basterà inserire 'test'")
    pdfFileObj = open(nomePDF+".pdf", 'rb')

    # Readaer del PDF
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPagine = pdfReader.numPages
    divisioniPagine = ""
    today = date.today()
    directoryDivisi = "Cedolini_Divisi " + today.strftime("(%d-%m-%Y)")
    directoryCercati = "Cedolini_Trovati " + today.strftime("(%d-%m-%Y)")
    pbar = ProgressBar()
    colonnaExcel = 'cercare'
    pdf_da_trovare = []
    nomeExcel = simpledialog.askstring(title="Dividi e Cerca PDF tramite Excel",
                                      prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")

    try:
        #Leggo l'excel
        excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
    except Exception as erroreLettura:
        Mbox("Dividi e Cerca PDF tramite Excel By ALMAX (GitHub)","Non esiste alcun excel denominato " + nomeExcel + ".xlsx\nIl programma cercherà comunque di dividere il singolo PDF.", 1)
        print(erroreLettura)


    try:
        os.mkdir(directoryDivisi)
        os.mkdir(directoryCercati)
    except OSError:
        errore =  "Errore nel creare la cartella, probabilmente esiste già.\nSi raccomanda di far partire un programma in una cartella vuota.\nIl programma cercherà comunque di generare i PDF ma potrebbero esserci delle anomalie e mancare dei PDF.\n\n"
    else:
        errore = "Tutto è andato a Buon fine.\n\n"

    try:
        for indice,valore in excelReader[colonnaExcel].iteritems():
        #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
            try:
                pdf_name = excelReader[colonnaExcel][indice]
                if(pdf_name[-4:] != ".pdf"):
                    pdf_name += ".pdf"

                pdf_da_trovare.append(pdf_name)
            except Exception as erroreBloccante:
                print(erroreBloccante)
                #erroreBloccante contiene il log dell'errore
    except Exception:
        print("no")

    # Ciclo per analizzare ogni singola pagina e dividerla
    for i in pbar(range(numPagine)):

        # Ottengo il testo della singola pagina
        pageObj = pdfReader.getPage(i)
        pageTxt = pageObj.extractText()

        try:
            txtExtract = shlex.split(pageTxt, posix=False)
        except Exception as errorShlex:
            print("Errore di shlex: " + str(errorShlex) + " alla pagina " + str(i+1))

        parola = "errore"
        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            if len(parola) == 16:
                if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
                    codiceFiscale = parola
                    codiceFiscaleStampa = codiceFiscale + ".pdf"

        # Divido la singola pagina dal PDF
        divisorePDF = PyPDF2.PdfFileWriter()
        divisorePDF.addPage(pdfReader.getPage(i))
        if codiceFiscaleStampa in pdf_da_trovare:
            with open(directoryCercati + "/" + codiceFiscaleStampa, "wb") as pdfDiviso:
                divisorePDF.write(pdfDiviso)
        with open(directoryDivisi + "/" + codiceFiscaleStampa, "wb") as pdfDiviso:
            divisorePDF.write(pdfDiviso)
        divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscaleStampa + "\n"

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = errore + "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro"
    Mbox("Dividi e Cerca PDF tramite Codice Fiscale By ALMAX (GitHub)",numPagineOut + divisioniPagine, 1)

    # Chiudo l'oggetto file
    pdfFileObj.close()
except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    Mbox("Dividi e Cerca PDF tramite Codice Fiscale By ALMAX (GitHub)", messaggioErroreBloccante, 1)
