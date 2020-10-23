from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import sys
import os
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import funzioni as functions
import traceback

def RichiediFile(nome_programma):

    def caricaFile(button, fileType, valori_lettura):
        if fileType == "dir":
            file = askdirectory()
        else:
            file = askopenfilename(filetypes = fileType)

        if file != "":
            valori_lettura.append(file)
            button['text'] = os.path.basename(file)
            button['state'] = "disabled"
        else:
            button['text'] = "Errore! Riprovare"

    def ripristina(all_buttons, all_texts, valori_lettura):
        indice = 0
        for button in all_buttons:
            button['text'] = all_texts[indice]
            button['state'] = "enabled"
            indice += 1
        valori_lettura.clear()

    def conferma(bottoni_da_disabilitare, all_buttons, all_texts, valori_lettura):
        valori_lettura.append(field_txt_old.get())
        valori_lettura.append(field_txt_new.get())
        if len(valori_lettura) < 4:
            ripristina(all_buttons, all_texts, valori_lettura)
            functions.Mbox(nome_programma, "Attenzione! Compilare i 4 campi per poter continuare")
            return
        ripristina(all_buttons, all_texts, [])
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"
        root.quit()

    try:
        buttons = []
        texts = []
        valori_lettura = []

        txt_xls = "Seleziona il file EXCEL"
        txt_label = "Selezionare l'Excel da leggere\n\n\nInserire il nome della colonna con i nomi attuali dei file\n\n\nInserire il nome della colonna che contiene i nuovi nomi dei file\n\n\nSelezionare la cartella con i file\n\n\nBarre del progresso delle elaborazioni.\nAttendere il riempimento."
        txt_dir = "Seleziona la cartella"
        texts.extend([txt_xls, txt_dir])

        root = Tk()
        root.title(nome_programma)
        root.geometry('510x275')
        root.resizable(0, 0)

        valore = StringVar()
        valore1 = StringVar()

        label = Label(root, text= txt_label).pack(side= LEFT,anchor = NW, pady = 12, padx = 15)

        btn_xls = Button(root, text = txt_xls, command = lambda:caricaFile(btn_xls, [(txt_xls, "*.xls"), (txt_xls, "*.xlsx")], valori_lettura))
        field_txt_old = Entry(root, textvariable=valore, width = 30)
        valore.set("old")
        field_txt_new = Entry(root, textvariable=valore1, width = 30)
        valore1.set("new")
        btn_dir = Button(root, text = txt_dir, command = lambda:caricaFile(btn_dir, "dir", valori_lettura))
        buttons.extend([btn_xls, btn_dir])
        progressBarSys = ttk.Progressbar(root, orient="horizontal", length=286,mode="determinate")
        
        btn_modifica = Button(root, text ='RIPRISTINA', command = lambda:ripristina(buttons, texts, valori_lettura))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([field_txt_old, field_txt_new, btn_modifica, btn_conferma, btn_xls, btn_dir],buttons, texts, valori_lettura))

        btn_xls.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        field_txt_old.pack(anchor = NW, pady = 13, padx = 10)
        field_txt_new.pack(anchor = NW, pady = 10, padx = 10)
        btn_dir.pack(side = TOP, anchor = NW, pady = 11, padx = 10)
        progressBarSys.pack(anchor = NW, pady = 15, padx = 10)

        btn_modifica.place(relx=0.3, rely=0.91, anchor=CENTER)
        btn_conferma.place(relx=0.7, rely=0.91, anchor=CENTER)


        root.mainloop()
        return valori_lettura, progressBarSys
    except:
        functions.logOperazioni("\nErrore nel Frame: " + traceback.format_exc())

#print(RichiediFile("Test"))