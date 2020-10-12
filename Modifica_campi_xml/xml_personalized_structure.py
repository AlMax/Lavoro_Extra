import xml.etree.ElementTree as ET

def AgenziaSomministrazione(root, namespace, field):
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
    
def tag(root, namespace, field):
    
    for figli in root.findall(namespace + field):

        for i in range(len(figli)):
            print(figli[i].tag.replace(namespace, ""))

            try:
                for nipoti in figli.findall(namespace + figli[i].tag.replace(namespace, "")):
                    for j in range(len(nipoti)):
                        print("\t" + nipoti[j].tag.replace(namespace, ""))

                        try:
                            for pro_nipoti in nipoti.findall(namespace + nipoti[j].tag.replace(namespace, "")):
                                for k in range(len(pro_nipoti)):
                                    print("\t\t" + pro_nipoti[k].tag.replace(namespace, ""))
                        except:
                            print("errore1")
                            
            except:
                print("errore")


ET.register_namespace("", "http://servizi.lavoro.gov.it/unisomm")
tree = ET.parse("uni.xml")
root = tree.getroot()
namespace = "{http://servizi.lavoro.gov.it/unisomm}"

for uni in root.iter("{http://servizi.lavoro.gov.it/unisomm}UniSomm"):
    uni.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    uni.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")


AgenziaSomministrazione(root, namespace, "comune")
tag(root, namespace, "DittaUtilizzatrice")


tree.write("newitems.xml",encoding="utf-8", xml_declaration=True)

