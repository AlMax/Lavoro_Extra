import os
import ctypes
import PyPDF2
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import tkinter as tk
from tkinter import simpledialog
import sys
from datetime import date

today = date.today()
successi = "I seguenti file sono stati trovati con successo:\n"
errori = "I seguenti file non sono stati trovati:\n"
directorySalvataggio = "Pdf_Trovati " + today.strftime("(%d-%m-%Y)")
colonnaExcel = 'cercare'

ROOT = tk.Tk()
ROOT.withdraw()
nomeExcel = simpledialog.askstring(title="Cerca PDF tramite Excel",
                                  prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


try:
    os.mkdir(directorySalvataggio)
except OSError:
    errore =  "Errore nel creare la cartella, probabilmente esiste già.\nIl programma cercherà comunque di cercare i PDF.\n\n"
else:
    errore = "Tutto è andato a Buon fine.\n\n"


try:
    #Leggo l'excel
    excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
except Exception as erroreLettura:
    Mbox("Cerca PDF tramite Excel By ALMAX (GitHub)","Non esiste alcun excel denominato " + nomeExcel + ".xlsx\nIl programma verrà chiuso.", 1)
    sys.exit();

print("Adesso inizio ad eseguire le elaborazioni, di seguito eventuali errori.\n")

for indice,valore in excelReader[colonnaExcel].iteritems():

#In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
    try:
        pdf_name = excelReader[colonnaExcel][indice]
        if(pdf_name[-4:] != ".pdf"):
            pdf_name += ".pdf"

        #Codice per trovare e ricopiare il pdf da cercare in uno nuovo da salvare nella cartella
        pdfFileObj = open(pdf_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pdfFinder = PyPDF2.PdfFileWriter()
        numPagine = pdfReader.numPages
        for i in range(numPagine):
            pdfFinder.addPage(pdfReader.getPage(i))

        with open(directorySalvataggio + "/" + pdf_name, "wb") as pdfTrovato:
            pdfFinder.write(pdfTrovato)

        successi += pdf_name + "\n"
    except Exception as erroreBloccante:
        errori += pdf_name + "\n"
        print(erroreBloccante)
        #erroreBloccante contiene il log dell'errore

Mbox("Cerca PDF tramite Excel By ALMAX (GitHub)","I FILE SONO STATI COPIATI NELLA CARTELLA: " + directorySalvataggio + "\n\n" + successi + "\n" + errori, 1)
