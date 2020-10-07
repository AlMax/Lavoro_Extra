from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
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

    def ripristina():
        root.destroy()
        RichiediFile(nome_programma)

    def conferma(bottoni_da_disabilitare, all_buttons, all_texts, valori_lettura, campi_extra, campi_extra2, campi_extra3):
        for campo in campi_extra:
            valori_lettura.append(campo.get())
            campo['state'] = "disabled"

        for campo2 in campi_extra2:
            valori_lettura.append(campo2.get())
            campo2['state'] = "disabled"

        for campo3 in campi_extra3:
            valori_lettura.append(campo3.get())
            campo3['state'] = "disabled"
            
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"

        for button in all_buttons:
            button['state'] = "disabled"

        root.quit()

    def aggiungiCampo(root, campi_extra, campi_extra2,campi_extra3, label, frame):
        if len(campi_extra) >= 10:
            print("Ve ne servono davvero così tanti?")
        else:
            top = Frame(root)
            top.pack(side=TOP)
            frame.append(top)
            campi_extra.append(Combobox(root, values = ["ciao", "buongiorno", "arrivederci"],state='readonly'))
            campi_extra[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra2.append(Combobox(root, values = ["ci vediamo", "buonasera", "addio"],state='readonly'))
            campi_extra2[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra3.append(Combobox(root, values = ["arigatou", "bon", "urco"],state='readonly'))
            campi_extra3[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            label.config(text = label['text'] + "\n\n\nciaoyeyhs5tesy5" + str(len(campi_extra)))

    try:
        buttons = []
        texts = []
        valori_lettura = []
        nomi_file = []
        campi_extra = []
        campi_extra2 = []
        campi_extra3 = []
        valori = []
        frame = []
        
        
        txt_pdf = "Selezione il file PDF"
        txt_xls = "Selezione il file EXCEL"
        txt_label = "Selezionare il PDF da leggere\n\n\nSelezionare l'Excel da leggere\n\n\nBarra del Progresso\n\n\nAggiungi"
        texts.extend([txt_pdf, txt_xls, txt_label])

        root = Tk()
        root.title(nome_programma)
        root.resizable(0, 0)
    
        label = Label(root, text=txt_label)
        bot = Frame(root)
        bot.pack(side=BOTTOM)
        


        btn_pdf = Button(root, text = txt_pdf, command = lambda:caricaFile(btn_pdf, [(txt_pdf, "*.pdf")], nomi_file))
        btn_xls = Button(root, text = txt_xls, command = lambda:caricaFile(btn_xls, [(txt_xls, "*.xls"), (txt_xls, "*.xlsx")], nomi_file))

        buttons.extend([btn_pdf, btn_xls])
        progressBar = ttk.Progressbar(root, orient="horizontal", length=120,mode="determinate")

        
        btn_ripristina = Button(root, text ='RIPRISTINA', command = lambda:ripristina())
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([btn_ripristina, btn_conferma, btn_aggiungi], buttons, texts, valori_lettura, campi_extra, campi_extra2, campi_extra3))
        btn_aggiungi = Button(root, text ='AGGIUNGI', command = lambda:aggiungiCampo(root, campi_extra, campi_extra2, campi_extra3, label, frame))

        label.pack(side= LEFT,anchor = NW, pady = 12, padx = 15)
        
        btn_pdf.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        btn_xls.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        progressBar.pack(anchor = NW, pady = 10, padx = 10)

        btn_ripristina.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_conferma.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_aggiungi.pack(anchor = NW, pady = 10, padx = 10)
    
        root.mainloop()
        print(nomi_file, valori_lettura, progressBar)
        return nomi_file, valori_lettura, progressBar
    except Exception as erroreFrame:
        print(str(erroreFrame))
        return (str(erroreFrame))


RichiediFile("Programmino per Laura")