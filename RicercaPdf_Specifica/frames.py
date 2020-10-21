from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import sys
import os
from tkinter.filedialog import askdirectory
import funzioni as functions

def RichiediFile(nome_programma):

    def caricaFile(button, valori_lettura):
        file = askdirectory()
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

    def conferma(bottoni_da_disabilitare, all_buttons):

        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"

        for button in all_buttons:
            button['state'] = "disabled"
        
        root.quit()

    try:
        buttons = []
        texts = []
        valori_lettura = []

        txt_dir = "Seleziona la directory"
        txt_label = "Selezionare la cartella con i PDF\n\n\nAvanzamento Elaborazioni"

        texts.extend([txt_dir])

        root = Tk()
        root.title(nome_programma)
        root.geometry('380x135')
        root.resizable(0, 0)

        label = Label(root, text= txt_label).pack(side= LEFT,anchor = NW, pady = 12, padx = 15)

        btn_dir = Button(root, text = txt_dir, command = lambda:caricaFile(btn_dir, valori_lettura))

        buttons.extend([btn_dir])
        progressBarSys = ttk.Progressbar(root, orient="horizontal", length=150,mode="determinate")
        
        btn_modifica = Button(root, text ='RIPRISTINA', command = lambda:ripristina(buttons, texts, valori_lettura))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([btn_modifica, btn_conferma],buttons))

        btn_dir.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        progressBarSys.pack(anchor = NW, pady = 11, padx = 10)

        btn_modifica.place(relx=0.3, rely=0.83, anchor=CENTER)
        btn_conferma.place(relx=0.7, rely=0.83, anchor=CENTER)


        root.mainloop()
        return valori_lettura[0], progressBarSys
    except Exception as erroreFrame:
        functions.logOperazioni(str(erroreFrame))

#print(RichiediFile("Test"))