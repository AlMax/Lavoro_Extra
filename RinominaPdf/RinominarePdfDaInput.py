import funzioni as functions
import frames as frame
import os
import traceback
import time

try:
    nomeProgramma = "Rinominatore PDF By ALMAX (GitHub)"
    functions.logOperazioni("")
    returnFrame = frame.RichiediFile(nomeProgramma)


    tipoFile = ".pdf"
    nomeExcel = returnFrame[0][0]
    directory = returnFrame[0][1]
    directory += "/"
    colonnaNomeOld = returnFrame[0][2]
    colonnaNomeNew = returnFrame[0][3]
    progress = returnFrame[1]

    fileExcel = functions.leggiExcel(nomeExcel, False)
    valori_old = functions.leggiExcel_colonna(fileExcel, colonnaNomeOld)
    valori_new = functions.leggiExcel_colonna(fileExcel, colonnaNomeNew)

    progress['maximum'] = len(valori_old)
    indice_prorgress = 0

    functions.logOperazioni("\n")
    indice_new = 0
    for fileAttuale in valori_old:
        functions.logOperazioni("\nCerco di rinominare il file " + fileAttuale + tipoFile +  " con " + valori_new[indice_new] + tipoFile)
        try:
            if fileAttuale.endswith(".pdf"):
                os.rename(directory + fileAttuale, directory + valori_new[indice_new] + tipoFile)
            else:
                os.rename(directory + fileAttuale + tipoFile, directory + valori_new[indice_new] + tipoFile)
            functions.logOperazioni("\nRinominazione avvenuta con successo!\n")
        except:
            functions.logOperazioni("\nErrore nel rinominare il file " + fileAttuale + tipoFile +  " che dovrebbe essere nella directory " + directory + "\nErrore: " + traceback.format_exc())
        indice_new += 1
        indice_prorgress += 1
        progress["value"] = indice_prorgress
        progress.update()
        time.sleep(5)
except:
    functions.logOperazioni("\nERRORE GENERALE: " + traceback.format_exc())

functions.Mbox(nomeProgramma, "Operazioni concluse, consultare il file Log.txt per i dettagli.")