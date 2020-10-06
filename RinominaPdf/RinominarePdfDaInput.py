import os
import ctypes
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import tkinter as tk
from tkinter import simpledialog
import sys

ROOT = tk.Tk()
ROOT.withdraw()
nomeExcel = simpledialog.askstring(title="Rinominatore PDF tramite Excel",
                                  prompt="Inserire il nome del file xlsx senza l'estensione.\nEsempio: se il file si chiama 'test.xlsx', basterà inserire 'test'")

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    fileLog.write(log)
    fileLog.close()

successi = "I seguenti file sono stati rinominati con successo:\n"
errori = "I seguenti file non sono stati trovati:\n"
old_name = ""

try:
    #Leggo l'excel
    excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
except Exception as erroreLettura:
    Mbox("Rinominatore PDF tramite Excel By ALMAX (GitHub)","Non esiste alcun excel denominato " + nomeExcel + ".xlsx\nIl programma verrà chiuso.", 1)
    sys.exit();

#print("Adesso inizio ad eseguire le elaborazioni, di seguito eventuali errori.\n")
for indice,valore in excelReader['old'].iteritems():
#In questo loop analizziamo ogni singolo elemento della colonna 'old' dell'excel; l'oggetto excelReader è una Serie
    try:
        old_name = str(excelReader['old'][indice]) + ".pdf"
        new_name = str(excelReader['new'][indice]) + ".pdf"
        os.rename(old_name, new_name)
        successi += old_name + "-->" + new_name + "\n"
    except Exception as erroreBloccante:
        errori += old_name + "\n"
        #erroreBloccante contiene il log dell'errore

logOperazioni(successi + "\n" + errori)
Mbox("Rinominatore PDF tramite Excel By ALMAX (GitHub)","Consultare il file Log.txt", 1)