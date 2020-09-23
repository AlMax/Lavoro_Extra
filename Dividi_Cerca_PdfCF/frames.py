from tkinter import *
from tkinter.ttk import *
import sys
import os
from tkinter.filedialog import askopenfilename

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
        valori_lettura.append(field_txt.get())
        if len(valori_lettura) != 3:
            ripristina(all_buttons, all_texts, valori_lettura)
            return
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"
        root.quit()

    try:
        buttons = []
        texts = []
        valori_lettura = []

        txt_pdf = "Selezione il file PDF"
        txt_xls = "Selezione il file EXCEL"
        txt_label = "Selezionare il PDF da leggere\n\n\nSelezionare l'Excel da leggere\n\n\nInserire il nome della cella dell'Excel"
        texts.extend([txt_pdf, txt_xls, txt_label])

        root = Tk()
        root.title(nome_programma)
        root.geometry('380x180')
        root.resizable(0, 0)

        valore = StringVar()

        label = Label(root, text= txt_label).pack(side= LEFT,anchor = NW, pady = 12, padx = 15)

        btn_pdf = Button(root, text = txt_pdf, command = lambda:caricaFile(btn_pdf, [(txt_pdf, "*.pdf")], valori_lettura))
        btn_xls = Button(root, text = txt_xls, command = lambda:caricaFile(btn_xls, [(txt_xls, "*.xls"), (txt_xls, "*.xlsx")], valori_lettura))
        field_txt = Entry(root, textvariable=valore, width = 15)
        buttons.extend([btn_pdf, btn_xls])

        btn_modifica = Button(root, text ='RIPRISTINA', command = lambda:ripristina(buttons, texts, valori_lettura))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([field_txt, btn_modifica, btn_conferma],buttons, texts, valori_lettura))

        btn_pdf.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        btn_xls.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        field_txt.pack(anchor = NW, pady = 10, padx = 10)
        btn_modifica.place(relx=0.3, rely=0.83, anchor=CENTER)
        btn_conferma.place(relx=0.7, rely=0.83, anchor=CENTER)
    

        root.mainloop()
        return valori_lettura
    except Exception as erroreFrame:
        return (str(erroreFrame))