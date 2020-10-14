import xml.etree.ElementTree as ET
import traceback
import frames as frame

def modificaCampo(root, namespace, coordinate, nrElementi):
    for coordinataElemento in range(nrElementi):
        i = coordinataElemento
        for figli in root.findall(namespace + coordinate[i]):
            i += nrElementi
            if coordinate[i] == "":
                for nipoti in figli.findall(namespace + coordinate[i]):
                    try:
                        i += nrElementi
                        elemento = nipoti.find(namespace + coordinate[i])
                        elemento.text = "new text"
                    except:
                        try:
                            i += nrElementi
                            for pro_nipoti in nipoti.findall(namespace + coordinate[i]):
                                i += nrElementi
                                pro_nipoti = pro_nipoti.find(namespace + coordinate[i])
                                pro_nipoti.text = "new text"
                        except:
                            print("Non c'è nulla sotto nascita")
            else:
                
    
def estraiStrutturaTag(root, namespace, field):
    indice_nipoti = 0

    try:
        for figli in root.findall(namespace + field[0]):
            for i in range(len(figli)):
                if i == 0:
                    field.append([])
                field[1].append(figli[i].tag.replace(namespace, ""))
                indice_pro_nipoti = 0

                try:
                    for nipoti in figli.findall(namespace + figli[i].tag.replace(namespace, "")):
                        for j in range(len(nipoti)):
                            if j == 0:
                                field[1].append([])
                                indice_nipoti += 1
                            field[1][indice_nipoti].append(nipoti[j].tag.replace(namespace, ""))
                            
                            try:
                                for pro_nipoti in nipoti.findall(namespace + nipoti[j].tag.replace(namespace, "")):
                                    for k in range(len(pro_nipoti)):
                                        if k == 0:
                                            field[1][indice_nipoti].append([])
                                            indice_pro_nipoti += 1
                                        field[1][indice_nipoti][indice_pro_nipoti].append(pro_nipoti[k].tag.replace(namespace, ""))
                                indice_pro_nipoti += 1
                            except:
                                print(traceback.format_exc())
                    
                    indice_nipoti += 1
                except:
                    print(traceback.format_exc())
            
    except:
        print(traceback.format_exc())

    return field


ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
tree = ET.parse("uni.xml")
root = tree.getroot()
namespace = "{http://servizi.lavoro.gov.it/unisomm}"

for uni in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
    uni.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    uni.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

AgenziaSomministrazione = ["AgenziaSomministrazione"]
Lavoratore = ["Lavoratore"]
DittaUtilizzatrice = ["DittaUtilizzatrice"]
TipoComunicazione = ["TipoComunicazione"]

modificaCampo(root, namespace, ['AgenziaSomministrazione', 'DatoreAnagraficaCompleta', 'cognome', '', ''], 1)

tree.write("newitems.xml",encoding="utf-8", xml_declaration=True)



#https://stackabuse.com/reading-and-writing-xml-files-in-python/