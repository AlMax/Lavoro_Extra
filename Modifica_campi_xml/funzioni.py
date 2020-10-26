import ctypes
import os
import time
import datetime
import xlsxwriter

today = datetime.date.today().strftime("%d-%m-%Y")
now = datetime.datetime.now().strftime("%H.%M.%S")

def creaCartelle(nomi_cartelle):
    """Dato in input un array di stringe, creerà delle cartelle con le relative stringhe.
    Ritoenrà infine una stringa con gli esiti delle varie creazioni"""
    if isinstance(nomi_cartelle,list):
        for directory in nomi_cartelle:
            try:
                os.mkdir(directory)
                logOperazioni("Cartella " + directory + " creata.\n")
            except OSError as erroreCartella:
                logOperazioni("\tERRORE nel creare la cartella --> " + str(erroreCartella) + "\n")
    else:
        try:
            os.mkdir(nomi_cartelle)
            logOperazioni("Cartella " + nomi_cartelle + " creata.\n")
        except OSError:
            logOperazioni("\tERRORE nel creare la cartella " + nomi_cartelle + ", probabilmente esiste già.\n")

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    if log == "":
        if os.stat("Log.txt").st_size == 0:
            logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
        logOperazioni("\n\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")
    fileLog.write(log)
    fileLog.close()

def logExcel(colonna1, colonna2, colonna3, colonna4, colonna5):
    workbook = xlsxwriter.Workbook('Log.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0

    for cella1 in colonna1:
        worksheet.write(row, 0, cella1)
        row += 1

    row = 0

    for cella2 in colonna2:
        worksheet.write(row, 1, cella2)
        row += 1

    row = 0

    for cella3 in colonna3:
        worksheet.write(row, 2, cella3)
        row += 1

    row = 0

    for cella4 in colonna4:
        worksheet.write(row, 3, cella4)
        row += 1

    row = 0
    
    for cella5 in colonna5:
        worksheet.write(row, 4, cella5)
        row += 1

    workbook.close()

def Mbox(title, text):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)
