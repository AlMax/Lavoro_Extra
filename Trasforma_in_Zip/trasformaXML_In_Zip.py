import os
import datetime
import traceback
import ctypes
from zipfile import ZipFile

def Mbox(title, text):
    """Messaggi Pop-up"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)

try:
    today = datetime.date.today().strftime("%d-%m-%Y")
    now = datetime.datetime.now().strftime("%H.%M.%S")


    files = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.dirname(os.path.realpath(__file__))):
        files.extend(filenames)
        break

    print("Ho trovato i seguenti XML: ")
    with ZipFile('Zippamento(' + today + '_' + now +').zip', 'w') as zipObj:
        for nome in filenames:

            if(nome.endswith('.xml')):
                print(nome)
                nomeZip = nome[:-4]+'.zip'
                zipObj2 = ZipFile(nomeZip, 'w')
                zipObj2.write(nome)
                zipObj2.close()

                zipObj.write(nomeZip)
                os.remove(nomeZip)

    zipObj.close()
    esito = "Operazioni concluse con successo!"
except:
    esito = str(traceback.format_exc())

Mbox("Zippatore XML By ALMAX (GitHub)", "Esito del raggruppamento in Zip degli XML nella cartella:\n" + esito)