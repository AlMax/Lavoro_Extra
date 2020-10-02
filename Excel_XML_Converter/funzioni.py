import ctypes
import os
import sys
import pandas as pd

def leggiExcel(nomeExcel, foglio):
    #Lettura Excel
    try:
        excelReader = pd.read_excel(nomeExcel, sheet_name = foglio)
        logOperazioni("Ho letto l'excel: " + nomeExcel + "\n")
        return excelReader
    except Exception as erroreExcel:
        logOperazioni("\tERRORE EXCEL: " + str(erroreExcel) + "\n")

def leggiExcel_colonna(excelReader, nome_colonnaExcel, elementi_colonna):
    #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
    try:
        logOperazioni("\tDall'excel, tento di leggere la colonna '" + nome_colonnaExcel + "'\n")
        for indice,valore in excelReader[nome_colonnaExcel].iteritems():
            contenuto_cella = str(excelReader[nome_colonnaExcel][indice]) #itero le singole celle
            elementi_colonna.append(contenuto_cella) #Aggiungo il nome del pdf alla lista dei pdf da trovare
            logOperazioni("\t\tAlla cella " + str(indice+1) + " ho letto il valore --> " + contenuto_cella + "\n")
    except Exception as erroreCellaExcel:
        logOperazioni("\tERRORE lettura celle Excel: " + str(erroreCellaExcel) + "\n")

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    fileLog.write(log)
    fileLog.close()

def Mbox(title, text, style):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)