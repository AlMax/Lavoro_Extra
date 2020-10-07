import ctypes
import os


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
    fileLog.write(log)
    fileLog.close()


def Mbox(title, text, style):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
