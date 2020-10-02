from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import sys
import os
from tkinter.filedialog import askopenfilename
import funzioni as functions

def RichiediFile(nome_programma):

    def caricaFile(button, fileType, valori_lettura):
        file = askopenfilename(filetypes = fileType)
        if file != "":
            valori_lettura.append(file)
            button['text'] = os.path.basename(file)
            button['state'] = "disabled"
            return valori_lettura
        button['text'] = "Errore! Riprovare"

    def ripristina(all_buttons, all_texts, valori_lettura):
        indice = 0
        for button in all_buttons:
            button['text'] = all_texts[indice]
            button['state'] = "enabled"
            indice += 1
        valori_lettura.clear()

    def conferma(bottoni_da_disabilitare, all_buttons, all_texts, valori_lettura):
        valori_lettura.append(field_txt_istanze.get())
        valori_lettura.append(field_txt_lavoratori.get())
        if len(valori_lettura) != 3:
            ripristina(all_buttons, all_texts, valori_lettura)
            return
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"
        functions.logOperazioni("Confermato")
        root.quit()

    try:
        buttons = []
        texts = []
        valori_lettura = []

        #txt_pdf = "Selezione il file PDF"
        txt_xls = "Selezione il file EXCEL"
        txt_label = "Selezionare l'Excel da leggere\n\n\nInserire il nome del foglio con i dati delle Istanze\n\n\nInserire il nome del foglio con i dati dei Lavoratori\n\n\nBarra del progresso.\nOgni completamento significa il completamento \ndi un'istanza Cliente con relativi Lavoratori."
        texts.extend([txt_xls, txt_label])

        root = Tk()
        root.title(nome_programma)
        root.geometry('450x270')
        root.resizable(0, 0)

        valore = StringVar()
        valore1 = StringVar()

        label = Label(root, text= txt_label).pack(side= LEFT,anchor = NW, pady = 12, padx = 15)

        #btn_pdf = Button(root, text = txt_pdf, command = lambda:caricaFile(btn_pdf, [(txt_pdf, "*.pdf")], valori_lettura))
        btn_xls = Button(root, text = txt_xls, command = lambda:caricaFile(btn_xls, [(txt_xls, "*.xls"), (txt_xls, "*.xlsx")], valori_lettura))
        field_txt_istanze = Entry(root, textvariable=valore, width = 30)
        valore.set("DATI ISTANZE")
        field_txt_lavoratori = Entry(root, textvariable=valore1, width = 30)
        valore1.set("DATI LAVORATORI")
        buttons.extend([btn_xls])
        progressBar = ttk.Progressbar(root, orient="horizontal", length=286,mode="determinate")

        btn_modifica = Button(root, text ='RIPRISTINA', command = lambda:ripristina(buttons, texts, valori_lettura))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([field_txt_istanze, field_txt_lavoratori, btn_modifica, btn_conferma],buttons, texts, valori_lettura))

        #btn_pdf.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        btn_xls.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        field_txt_istanze.pack(anchor = NW, pady = 10, padx = 10)
        field_txt_lavoratori .pack(anchor = NW, pady = 10, padx = 10)
        progressBar.pack(anchor = NW, pady = 34, padx = 10)

        btn_modifica.place(relx=0.3, rely=0.85, anchor=CENTER)
        btn_conferma.place(relx=0.7, rely=0.85, anchor=CENTER)


        root.mainloop()
        return valori_lettura, progressBar
    except Exception as erroreFrame:
        functions.logOperazioni(str(erroreFrame))
