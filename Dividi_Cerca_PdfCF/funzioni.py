import PyPDF2
import ctypes
import os

def isCodiceFiscale(parola):
    """Data in input una stringa, viene analizzata la composizione della stringa per determinare se è un codice fiscale o meno.
    Ritorna True in caso sia un codice fiscale, False altrimenti. """
    if len(parola) == 16:
        if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
            return True
    return False


def PDF_estraiPagine(pdf_vecchio, indici_pagine, directorySalvataggio, nomeFile):
    """La funzione usa la libreria PyPDF2 e si occupa di strarre le singole pagine da un dato PDF.
    pdf_vecchio è il reader, generalmente dichiarato come pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    indici_pagine è la posizione delle pagine specifiche da estrarre; può essere un singolo indice o più di uno; in case fossero tanti, è strettamente necessario sia un array
    directorySalvataggio è il nome della cartella in cui salvare il/i file_estratto
    nomeFile è il nome che verrà assegnato al PDF contenente le pagine divise."""

    file_da_scrivere = PyPDF2.PdfFileWriter()

    if isinstance(indici_pagine,list):
        for i in indici_pagine:
            file_da_scrivere.addPage(pdf_vecchio.getPage(i))
    else:
        file_da_scrivere.addPage(pdf_vecchio.getPage(indici_pagine))

    #Metto ogni file diviso nell'apposita cartella
    with open(directorySalvataggio + "/" + nomeFile, "wb") as file_estratto:
        file_da_scrivere.write(file_estratto)

def PDF_unisci(nome_pdf1, nome_pdf2, directorySalvataggio):
    #Lettura PDF
    try:
        #nomePDF = simpledialog.askstring(title=nomeProgramma, prompt="Inserire il nome del file PDF senza l'estensione.\nEsempio: se il file si chiama 'test.pdf', basterà inserire 'test'")
        pdfFileObj_1 = open(directorySalvataggio + "/" + nome_pdf1+".pdf", 'rb')
        pdfReader_1 = PyPDF2.PdfFileReader(pdfFileObj_1)
        pdfFileObj_2 = open(directorySalvataggio + "/" + nome_pdf2+".pdf", 'rb')
        pdfReader_2 = PyPDF2.PdfFileReader(pdfFileObj_2)

        numPagine1 = pdfReader_1.numPages
        numPagine2 = pdfReader_2.numPages

        pdf_unito = PyPDF2.PdfFileWriter()
        for i in range(numPagine1):
            pdf_unito.addPage(pdfReader_1.getPage(i))
        for i in range(numPagine2):
            pdf_unito.addPage(pdfReader_2.getPage(i))

        with open(directorySalvataggio + "/pdfUnito.pdf", "wb") as file_da_scrivere:
            pdf_unito.write(file_da_scrivere)

        pdfFileObj_1.close()
        pdfFileObj_2.close()
        os.remove(directorySalvataggio + "/" + nome_pdf1+".pdf")
        os.remove(directorySalvataggio + "/" + nome_pdf2+".pdf")
        os.rename(directorySalvataggio + "/pdfUnito.pdf", directorySalvataggio + "/" + nome_pdf1+".pdf")

    except Exception as errorePdf:
        f.Mbox(nomeProgramma,"Ci sono errori durante la lettura del PDF: " + nome_pdf1 + ".pdf\nIl programma verrà interrotto.Si ricorda di inerire il nome correttamente.", 1)
        fileLog.write("Errore PDF: " + errorePdf + "\n")
        sys.exit()

def creaCartelle(nomi_cartelle):
    """Dato in input un array di stringe, creerà delle cartelle con le relative stringhe.
    Ritoenrà infine una stringa con gli esiti delle varie creazioni"""
    esito_creazione = ""
    if isinstance(nomi_cartelle,list):
        for directory in nomi_cartelle:
            try:
                os.mkdir(directory)
                esito_creazione += "Cartella " + directory + " creata.\n"
            except OSError:
                esito_creazione +=  "Errore nel creare la cartella " + directory + ", probabilmente esiste già.\n"
    else:
        try:
            os.mkdir(nomi_cartelle)
            esito_creazione += "Cartella " + nomi_cartelle + " creata.\n"
        except OSError:
            esito_creazione +=  "Errore nel creare la cartella " + nomi_cartelle + ", probabilmente esiste già.\n"
    return esito_creazione


def Mbox(title, text, style):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
