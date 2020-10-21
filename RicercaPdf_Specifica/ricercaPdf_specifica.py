from os import walk
import os
import re
import shutil
import funzioni as function
import time
import datetime
import frames as frame
import traceback

nomeProgramma = "SpacchettatorePDF By ALMAX (GitHub)"
nomi_file = []
cartella = ""

today = datetime.date.today().strftime("%d-%m-%Y")
now = datetime.datetime.now().strftime("%H.%M.%S")

returnFrame = frame.RichiediFile(nomeProgramma)
progress = returnFrame[1]

function.logOperazioni("")

if os.stat("Log.txt").st_size == 0:
    function.logOperazioni("Scorrere in basso per avere i log piu' recenti.\nI Log vengono registrati ogni volta che viene lanciato il programma.")
function.logOperazioni("\n\n\nI seguenti Log fanno riferimento al giorno " + today + " alle ore " + now + "\n")

try:
    for file in os.listdir(returnFrame[0]):
        if file.endswith(".pdf"):
            nomi_file.append(file)
except:
    function.logOperazioni("\nErrore nel cercare i PDF nella cartella " + str(returnFrame[0]) + "\nErrore: " + traceback.format_exc())

try:
    progress['maximum'] = len(nomi_file)
    indice_prorgress = 0

    for filename in nomi_file:
        try:
            function.logOperazioni("\nTento di spostare il file " + filename)
            posizioni = [search.start() for search in re.finditer('_', filename)]
            cartella = ""

            for i in range(len(filename)):
                if i > posizioni[1] and i < posizioni[2]:
                    cartella += filename[i]
            if os.path.isdir('./'+cartella): 
                shutil.move(filename, cartella)
            else:
                function.creaCartelle(cartella)
                shutil.move(filename, cartella)
            function.logOperazioni("\n\tIl file " + filename + " è stato spostato.\n")
        except:
            function.logOperazioni("\nErrore nello spostamento del file " + filename + "\nErrore: " + traceback.format_exc())

        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        
except:
    function.logOperazioni("\nCi sono state delle anomalie durante le varie elaborazioni.\nErrore: " + traceback.format_exc())

function.Mbox(nomeProgramma, "Elaborazioni concluse, consultare il file Log.txt per i dettagli.")
