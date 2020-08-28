import ctypes
import PyPDF2
import shlex
import os
from progressbar import ProgressBar
from datetime import date

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

try:
    # Oggetto PDF
    pdfFileObj = open('cedolini.pdf', 'rb')

    # Readaer del PDF
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPagine = pdfReader.numPages
    divisioniPagine = ""
    codiciFiscaliUtilizzati = []
    today = date.today()
    directorySalvataggio = "Cedolini_Divisi " + today.strftime("(%d-%m-%Y)")
    pbar = ProgressBar()

    try:
        os.mkdir(directorySalvataggio)
    except OSError:
        errore =  "Errore nel creare la cartella, probabilmente esiste già.\nSi raccomanda di far partire un programma in una cartella vuota.\nIl programma cercherà comunque di generare i PDF ma potrebbero esserci delle anomalie e mancare dei PDF.\n\n"
    else:
        errore = "Tutto è andato a Buon fine.\n\n"

    # Ciclo per analizzare ogni singola pagina e dividerla
    for i in pbar(range(numPagine)):

        # Ottengo il testo della singola pagina
        pageObj = pdfReader.getPage(i)
        pageTxt = pageObj.extractText()
        txtExtract = shlex.split(pageTxt)

        # Estrapolo il codice fiscale in base alla sua composizione
        for parola in txtExtract:
            if len(parola) == 16:
                if ( (not parola[0:6].isnumeric()) and (parola[6:8].isnumeric()) and (not parola[8].isnumeric()) and (parola[9:11].isnumeric()) and (not parola[15].isnumeric()) ):
                    divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + parola + "\n"
                    codiceFiscale = parola
                    codiceFiscaleStampa = codiceFiscale

                    if (codiceFiscale in codiciFiscaliUtilizzati):
                        codiceFiscaleStampa = codiceFiscale + "-" + str(codiciFiscaliUtilizzati.count(codiceFiscale))

                    codiciFiscaliUtilizzati.append(codiceFiscale)
    # Stampo la stringa coi codici fiscali torvati
    #print(divisioniPagine)

        # Estrapolo il codice fiscale utilizzando la strina la posizione previdenziale=A95 e creo una stringa che riporti le operazioni fatte
    #    indexCF = txtExtract.index("A95") - 1
    #    codiceFiscale = txtExtract[indexCF]
    #    divisioniPagine += "Codice Fiscale della pagina " + str(i+1) + " --> " + codiceFiscale + "\n"

        # Divido la singola pagina dal PDF
        divisorePDF = PyPDF2.PdfFileWriter()
        divisorePDF.addPage(pdfReader.getPage(i))
        with open(directorySalvataggio + "/" + codiceFiscaleStampa + ".pdf", "wb") as pdfDiviso:
            divisorePDF.write(pdfDiviso)

    # Mostro una Form con le divisioni delle pagine fatte
    numPagineOut = errore + "Numero di pagine divise: " + str(numPagine) + "\n"
    divisioniPagine += "\n\nOperazione conclusa.\nGrazie mille e Buon lavoro"
    Mbox("Divisore PDF tramite Codice Fiscale By ALMAX (GitHub)",numPagineOut + divisioniPagine, 1)

    # Chiudo l'oggetto file
    pdfFileObj.close()
except Exception as erroreBloccante:
    messaggioErroreBloccante = "Il programma non riesce a partire a causa di un errore.\nSi ricorda che è obbligatorio rinominare il pdf da dividere in 'cedolini.pdf'\n\nIn caso non funzioni ancora, contattarmi alla mail ali.haider.maqsood@maw.it\n\nL'errore è:\n" + str(erroreBloccante)
    Mbox("Divisore PDF tramite Codice Fiscale By ALMAX (GitHub)", messaggioErroreBloccante, 1)
