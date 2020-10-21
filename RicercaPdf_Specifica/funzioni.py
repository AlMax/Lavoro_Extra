import ctypes
import os


def creaCartelle(nomi_cartelle):
    """Dato in input un array di stringe, creerà delle cartelle con le relative stringhe.
    Ritoenrà infine una stringa con gli esiti delle varie creazioni"""
    if isinstance(nomi_cartelle,list):
        for directory in nomi_cartelle:
            try:
                os.mkdir(directory)
                logOperazioni("\nCartella " + directory + " creata.")
            except OSError as erroreCartella:
                logOperazioni("\n\tERRORE nel creare la cartella --> " + str(erroreCartella))
    else:
        try:
            os.mkdir(nomi_cartelle)
            logOperazioni("\nCartella " + nomi_cartelle + " creata.")
        except OSError:
            logOperazioni("\n\tERRORE nel creare la cartella " + nomi_cartelle + ", probabilmente esiste già.")

def logOperazioni(log):
    """Scrittura dei log su apposito file"""
    fileLog = open("Log.txt", "a")
    fileLog.write(log)
    fileLog.close()


def Mbox(title, text):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)
