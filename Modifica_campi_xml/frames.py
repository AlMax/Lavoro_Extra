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

    def conferma(bottoni_da_disabilitare, all_buttons, all_texts, valori_lettura, campi_extra, campi_extra2, campi_extra3, testo_field):
        for campo in campi_extra:
            valori_lettura.append(campo.get())
            campo['state'] = "disabled"

        for campo2 in campi_extra2:
            valori_lettura.append(campo2.get())
            campo2['state'] = "disabled"

        for campo3 in campi_extra3:
            valori_lettura.append(campo3.get())
            campo3['state'] = "disabled"

        for testo in testo_field:
            valori_lettura.append(testo.get())
            
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"

        for button in all_buttons:
            button['state'] = "disabled"

        root.quit()

    def campo_valorizzato(campo, campo2, valori):
        print("Selected!" + str(campo.get()))
        valori.append("okkkkkkk")
        campo2.configure(values = valori)

    def aggiungiCampo(root, campi_extra, campi_extra2,campi_extra3, label, frame, testo_field):
        if len(campi_extra) >= 10:
            print("Ve ne servono davvero così tanti?")
        else:
            top = Frame(root)
            top.pack(side=TOP)
            frame.append(top)

            campi_extra.append(ttk.Combobox(root, values = ["ciao", "buongiorno", "arrivederci"],state='readonly'))
            campi_extra[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra[-1], campi_extra2[-1], valori))
            valori = ["arigatou", "bon", "urco"]
            campi_extra2.append(Combobox(root, values = ["ci vediamo", "buonasera", "addio"],state='readonly'))
            campi_extra2[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra2[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra[-1], campi_extra2[-1], valori))
            
            
            campi_extra3.append(Combobox(root, values = valori,state='readonly'))
            campi_extra3[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra3[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra3[-1], campi_extra2[-1], valori))

            label.config(text = label['text'] + "\n\n\nciaoyeyhs5tesy5" + str(len(campi_extra)))
            
            testo_field.append(StringVar())
            field_txt = Entry(root, textvariable=testo_field[-1], width = 15)
            field_txt.pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)

    try:
        buttons = []
        texts = []
        valori_lettura = []
        nomi_file = []
        campi_extra = []
        campi_extra2 = []
        campi_extra3 = []
        frame = []
        testo_field = []
        
        
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

        
        btn_exit = Button(root, text ='ESCI', command = lambda:sys.exit(0))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([btn_exit, btn_conferma, btn_aggiungi], buttons, texts, valori_lettura, campi_extra, campi_extra2, campi_extra3, testo_field))
        btn_aggiungi = Button(root, text ='AGGIUNGI', command = lambda:aggiungiCampo(root, campi_extra, campi_extra2, campi_extra3, label, frame, testo_field))

        label.pack(side= LEFT,anchor = NW, pady = 12, padx = 15)
        
        btn_pdf.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        btn_xls.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        progressBar.pack(anchor = NW, pady = 10, padx = 10)

        btn_exit.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_conferma.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_aggiungi.pack(anchor = NW, pady = 10, padx = 10)
    
        root.mainloop()
        print(nomi_file, valori_lettura, progressBar)
        return nomi_file, valori_lettura, progressBar
    except Exception as erroreFrame:
        print(str(erroreFrame))
        return (str(erroreFrame))


RichiediFile("Programmino per Laura")