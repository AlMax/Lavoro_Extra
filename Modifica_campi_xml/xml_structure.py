import traceback

def modificaCampo(root, namespace, coordinate, nuovo_testo):
    coordinata = ""
    for tag in coordinate:
        if not tag == "":
            coordinata += namespace + tag + "/"
    coordinata = coordinata[:-1]
    root.find(coordinata).text = nuovo_testo
                
    
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


#https://stackabuse.com/reading-and-writing-xml-files-in-python/