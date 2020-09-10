import ctypes
import PyPDF2
import shlex
import os
from progressbar import ProgressBar
from datetime import date
import sys
import pandas as pd

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

try:
    # Oggetto PDF
    pdfFileObj = open('cedolini.pdf', 'rb')

    # Readaer del PDF
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPagine = pdfReader.numPages
    divisioniPagine = ""
    today = date.today()
    directorySalvataggio = "Cedolini_Divisi " + today.strftime("(%d-%m-%Y)")
    pbar = ProgressBar()
    colonnaExcel = 'cercare'
    pdf_da_trovare = []
    nomeExcel = "CF"

    try:
        #Leggo l'excel
        excelReader = pd.read_excel('%s.xlsx' %nomeExcel)
    except Exception as erroreLettura:
        Mbox("Cerca PDF tramite Excel By ALMAX (GitHub)","Non esiste alcun excel denominato " + nomeExcel + ".xlsx\nIl programma verrà chiuso.", 1)
        print(erroreLettura)
        sys.exit();

    try:
        os.mkdir(directorySalvataggio)
    except OSError:
        errore =  "Errore nel creare la cartella, probabilmente esiste già.\nSi raccomanda di far partire un programma in una cartella vuota.\nIl programma cercherà comunque di generare i PDF ma potrebbero esserci delle anomalie e mancare dei PDF.\n\n"
    else:
        errore = "Tutto è andato a Buon fine.\n\n"


    for indice,valore in excelReader[colonnaExcel].iteritems():
    #In questo loop analizziamo ogni singolo elemento della colonna dell'excel; l'oggetto excelReader è una Serie
        try:
            pdf_name = excelReader[colonnaExcel][indice]
            if(pdf_name[-4:] != ".pdf"):
                pdf_name += ".pdf"

            pdf_da_trovare.append(pdf_name)
        except Exception as erroreBloccante:
            print(erroreBloccante)
            #erroreBloccante contiene il log dell'errore

    print(pdf_da_trovare)
    # Ciclo per analizzare ogni singola pagina e dividerla
    for i in pbar(range(numPagine)):

        # Ottengo il testo della singola pagina
        pageObj = pdfReader.getPage(i)
        pageTxt = pageObj.extractText()

        try:
            txtExtract = shlex.split(pageTxt, posix=False)
        except Exception as errorShlex:
            print(str(errorShlex) + str(i+1))


        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            if len(parola) == 16:
                if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
                    codiceFiscale = parola
                    codiceFiscaleStampa = codiceFiscale + ".pdf"

        # Estrapolo il codice fiscale utilizzando la strina la posizione previdenziale=A95 e creo una stringa che riporti le operazioni fatte
    #    indexCF = txtExtract.index("A95") - 1
    #    codiceFiscale = txtExtract[indexCF]
    #    divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscale + "\n"

        # Divido la singola pagina dal PDF
        if codiceFiscaleStampa in pdf_da_trovare:
            divisorePDF = PyPDF2.PdfFileWriter()
            divisorePDF.addPage(pdfReader.getPage(i))
            with open(directorySalvataggio + "/" + codiceFiscaleStampa, "wb") as pdfDiviso:
                divisorePDF.write(pdfDiviso)
            divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscaleStampa + "\n"

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = errore + "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro"
    Mbox("Divisore PDF tramite Codice Fiscale By ALMAX (GitHub)",numPagineOut + divisioniPagine, 1)

    # Chiudo l'oggetto file
    pdfFileObj.close()
except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\nSi ricorda che è obbligatorio rinominare il pdf da dividere in 'cedolini.pdf'\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    Mbox("Divisore PDF tramite Codice Fiscale By ALMAX (GitHub)", messaggioErroreBloccante, 1)
