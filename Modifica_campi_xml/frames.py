from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import sys
import os
from tkinter.filedialog import askopenfilename
import xml_personalized_structure as strutturaXML
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
tree = ET.parse("uni.xml")
rootXML = tree.getroot()
namespace = "{http://servizi.lavoro.gov.it/unisomm}"

for uni in rootXML.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
    uni.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    uni.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

AgenziaSomministrazione = ["AgenziaSomministrazione"]
Lavoratore = ["Lavoratore"]
DittaUtilizzatrice = ["DittaUtilizzatrice"]
TipoComunicazione = ["TipoComunicazione"]

def RichiediFile(nome_programma):

    def caricaFile(button, fileType, valori_lettura):
        file = askopenfilename(filetypes = fileType)
        if file != "":
            valori_lettura.append(file)
            button['text'] = os.path.basename(file)
            button['state'] = "disabled"
            return valori_lettura
        button['text'] = "Errore! Riprovare"

    def conferma(bottoni_da_disabilitare, all_buttons, all_texts, valori_lettura, campi_extra1, campi_extra2, campi_extra3, testo_field):
        for campo1 in campi_extra1:
            valori_lettura.append(campo1.get())
            campo1['state'] = "disabled"

        for campo2 in campi_extra2:
            valori_lettura.append(campo2.get())
            campo2['state'] = "disabled"

        for campo3 in campi_extra3:
            valori_lettura.append(campo3.get())
            campo3['state'] = "disabled"

        for campo4 in campi_extra4:
            valori_lettura.append(campo4.get())
            campo4['state'] = "disabled"

        for testo in testo_field:
            valori_lettura.append(testo.get())
            
        for button in bottoni_da_disabilitare:
            button['state'] = "disabled"

        for button in all_buttons:
            button['state'] = "disabled"

        root.quit()

    def campo_valorizzato(campo1, campo2, campo3, campo4, field_txt):
        valori2 = []
        valori3 =[]
        valori4 = []
        padre = []
        figlio_precedente = ""
        nipote_precedente = ""

        if campo1.get() == "AgenziaSomministrazione":
            padre = AgenziaSomministrazione.copy()
        elif campo1.get() == "Lavoratore":
            padre = Lavoratore.copy()
        elif campo1.get() == "DittaUtilizzatrice":
            padre = DittaUtilizzatrice.copy()
        elif campo1.get() == "TipoComunicazione":
            padre = TipoComunicazione.copy()

        strutturaXML.estraiStrutturaTag(rootXML, namespace, padre)
        print(padre)

        try:
            if isinstance(padre[1], list):
                for figlio in padre[1]:
                    if not isinstance(figlio, list):
                        valori2.append(figlio)
                        campo2['state'] = "readonly"
                    else:
                        for nipote in figlio:
                            if not isinstance(nipote, list) and campo2:
                                try:
                                    if figlio_precedente == campo2.get():
                                        valori3.append(nipote)
                                        campo3['state'] = "readonly"
                                except:
                                    print("ok")
                            else:
                                if campo3:
                                    try:
                                        if nipote_precedente == campo3.get():
                                            for pro_nipote in nipote:
                                                valori4.append(pro_nipote)
                                                campo4['state'] = "readonly"
                                    except:
                                        print("ok2")
                            nipote_precedente = nipote
                    figlio_precedente = figlio
        except:
            field_txt['state'] = "enabled"
            btn_aggiungi['state'] = "enabled"
            print("Non ha altro")

        if campo2:
            campo2.configure(values = valori2)

            if campo3:
                stato = str(campo3['state'])
                if stato == "disabled":
                    field_txt['state'] = "enabled"
                    btn_aggiungi['state'] = "enabled"
            campo1['state'] = "disabled"

        if campo3:
            campo3.configure(values = valori3)

            if campo4:
                stato = str(campo4['state'])
                if  stato == "disabled":
                    field_txt['state'] = "enabled"
                    btn_aggiungi['state'] = "enabled"
            campo2['state'] = "disabled"
            
        if campo4:
            campo4.configure(values = valori4)
            campo3['state'] = "disabled"
            

    def compileTxt(field, campo):
        field['state'] = "enabled"
        campo['state'] = "disabled"
        btn_aggiungi['state'] = "enabled"


    def aggiungiCampo(root, campi_extra1, campi_extra2, campi_extra3, campi_extra4, label, frame, testo_field):
        if len(campi_extra1) >= 5:
            btn_aggiungi['state'] = "disabled"
            btn_aggiungi.configure(text = "TROPPI CAMPI!")
        else:
            top = Frame(root)
            top.pack(side=TOP)
            frame.append(top)

            campi_extra1.append(ttk.Combobox(root, values = ["AgenziaSomministrazione", "Lavoratore", "DittaUtilizzatrice", "TipoComunicazione"],state='readonly'))
            campi_extra1[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra1[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra1[-1], campi_extra2[-1], [], [], field_txt))

            campi_extra2.append(Combobox(root, values = [],state='readonly'))
            campi_extra2[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra2[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra1[-1], campi_extra2[-1], campi_extra3[-1], [], field_txt))
            campi_extra2[-1]['state'] = "disabled"

            campi_extra3.append(Combobox(root, values = [],state='readonly'))
            campi_extra3[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra3[-1].bind("<<ComboboxSelected>>", lambda _ : campo_valorizzato(campi_extra1[-1], campi_extra2[-1], campi_extra3[-1], campi_extra4[-1], field_txt))
            campi_extra3[-1]['state'] = "disabled"

            campi_extra4.append(Combobox(root, values = [],state='readonly'))
            campi_extra4[-1].pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            campi_extra4[-1].bind("<<ComboboxSelected>>", lambda _ : compileTxt(field_txt, campi_extra4[-1]))
            campi_extra4[-1]['state'] = "disabled"

            label.config(text = label['text'] + "\n\n\nCampo " + str(len(campi_extra1)))
            
            testo_field.append(StringVar())
            field_txt = Entry(root, textvariable=testo_field[-1], width = 15)
            field_txt.pack(anchor = NW, pady = 12, padx = 10, in_=top, side = LEFT)
            field_txt['state'] = "disabled"

            btn_aggiungi['state'] = "disabled"

    try:
        buttons = []
        texts = []
        valori_lettura = []
        nomi_file = []
        campi_extra1 = []
        campi_extra2 = []
        campi_extra3 = []
        campi_extra4 = []
        frame = []
        testo_field = []
        
        
        txt_zip = "Seleziona il file ZIP"
        txt_label = "Selezionare lo ZIP\n\n\nBarra del Progresso\n\n\nCrea un nuovo campo"
        texts.extend([txt_zip, txt_label])

        root = Tk()
        root.title(nome_programma)
        root.resizable(0, 0)
    
        label = Label(root, text=txt_label)
        bot = Frame(root)
        bot.pack(side=BOTTOM)


        btn_zip = Button(root, text = txt_zip, command = lambda:caricaFile(btn_zip, [(txt_zip, "*.zip")], nomi_file))

        buttons.extend([btn_zip])
        progressBar = ttk.Progressbar(root, orient="horizontal", length=200,mode="determinate") #760

        
        btn_exit = Button(root, text ='ESCI', command = lambda:sys.exit(0))
        btn_conferma = Button(root, text ='CONFERMA', command = lambda:conferma([btn_exit, btn_conferma, btn_aggiungi], buttons, texts, valori_lettura, campi_extra1, campi_extra2, campi_extra3, testo_field))
        btn_aggiungi = Button(root, text ='AGGIUNGI SELEZIONE TAG', command = lambda:aggiungiCampo(root, campi_extra1, campi_extra2, campi_extra3, campi_extra4, label, frame, testo_field))

        label.pack(side= LEFT,anchor = NW, pady = 12, padx = 15)
        
        btn_zip.pack(side = TOP, anchor = NW, pady = 10, padx = 10)
        progressBar.pack(anchor = NW, pady = 10, padx = 10)

        btn_exit.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_conferma.pack(anchor = NW, pady = 10, padx = 10, in_=bot, side = LEFT)
        btn_aggiungi.pack(anchor = NW, pady = 10, padx = 10)
    
        #aggiungiCampo(root, campi_extra1, campi_extra2, campi_extra3, campi_extra4, label, frame, testo_field)
        root.mainloop()
        print(nomi_file, len(campi_extra1), valori_lettura, progressBar)
        return nomi_file, len(campi_extra1), valori_lettura, progressBar
    except Exception as erroreFrame:
        print(str(erroreFrame))
        return (str(erroreFrame))


#RichiediFile("Programmino per Laura")