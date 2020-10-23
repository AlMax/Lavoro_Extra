import ctypes
import os
import sys
import pandas as pd
import time
import datetime
import traceback

today = datetime.date.today().strftime("%d-%m-%Y")
now = datetime.datetime.now().strftime("%H.%M.%S")

def leggiExcel(nomeExcel, foglio):
    #Lettura Excel
    try:
        if foglio:
            excelReader = pd.read_excel(nomeExcel, sheet_name = foglio)
        else:
            excelReader = pd.read_excel(nomeExcel)
        logOperazioni("\nHo letto l'excel: " + nomeExcel)
        return excelReader
    except:
        logOperazioni("\n\tERRORE lettura Excel: " + traceback.format_exc())

def leggiExcel_colonna(excelReader, nome_colonnaExcel):
    #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
    elementi_colonna = []
    try:
        #logOperazioni("\tDall'excel, tento di leggere la colonna '" + nome_colonnaExcel + "'\n")
        for indice,valore in excelReader[nome_colonnaExcel].iteritems():
            contenuto_cella = str(excelReader[nome_colonnaExcel][indice]) #itero le singole celle
            elementi_colonna.append(contenuto_cella) #Aggiungo il nome del pdf alla lista dei pdf da trovare
            #logOperazioni("\t\tAlla cella " + str(indice+1) + " ho letto il valore --> " + contenuto_cella + "\n") 
        logOperazioni("\nColonna " + nome_colonnaExcel + " letta con successo!")
        return elementi_colonna
    except:
        logOperazioni("\n\tERRORE nella lettura della colonna Excel: " + traceback.format_exc())

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    if log == "":
        if os.stat("Log.txt").st_size == 0:
            logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
        logOperazioni("\n\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")
    fileLog.write(log)
    fileLog.close()

def Mbox(title, text):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)