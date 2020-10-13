import xml.etree.ElementTree as ET
import traceback

def findAgenziaSomministrazione(root, namespace, field):
    for figli in root.findall(namespace + "AgenziaSomministrazione"):
        for nipoti in figli.findall(namespace + "DatoreAnagraficaCompleta"):
            try:
                elemento = nipoti.find(namespace + field)
                elemento.text = "new text"
            except:
                try:
                    for pro_nipoti in nipoti.findall(namespace + "nascita"):
                        pro_nipoti = pro_nipoti.find(namespace + field)
                        pro_nipoti.text = "new text"
                except:
                    print("Non c'è nulla sotto nascita")
    
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


#ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
#tree = ET.parse("uni.xml")
#root = tree.getroot()
#namespace = "{http://servizi.lavoro.gov.it/unisomm}"

#for uni in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
#    uni.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
#    uni.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

#AgenziaSomministrazione = ["AgenziaSomministrazione"]
#Lavoratore = ["Lavoratore"]
#DittaUtilizzatrice = ["DittaUtilizzatrice"]
#TipoComunicazione = ["TipoComunicazione"]

#print(isinstance(agenzia[0], list))

#findAgenziaSomministrazione(root, namespace, "comune")

#print(estraiStrutturaTag(root, namespace, Lavoratore))


#tree.write("newitems.xml",encoding="utf-8", xml_declaration=True)

