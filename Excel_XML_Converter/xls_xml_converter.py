from xml.dom import minidom
from lxml import etree
import os
import funzioni as functions

documento = minidom.Document()
xml = documento.createElement('tis')
documento.appendChild(xml)

attributi_istanza = []
attributi_istanza.extend(["identificativoPratica", "denominazioneAPL", "ragioneSocialeUtilizzatore", "partitaIvaUtilizzatore", "matricolaInpsUtilizzatore", "codiceAtecoUtilizzatore", "sedeUnitaProduttiva", "mensilitaAggiuntive", "settoreRiferimento", "autocertificazioneSettimane", "note"])

dati_tutti_lavoratori = []
dati_tutti_lavoratori.extend(["annoRiferimento", "meseRiferimento", "codiceFiscale", "cognome", "nome", "tipologiaContratto", "sgraviAliquotaContributivaPrevidenziale", "retribuzioneMensileLorda", "retribuzioneTisRiconosciuta", "contribuzioneTisRiconosciuta", "quotaRateiMensilitaAggiuntive", "quotaRateiRolPermessiFerie", "totaleOreTisRiconosciute", "lavoratoreAlleDipendenze25Marzo"])

tutti_lavoratori = [[]]
tutti_clienti = [[]]
array = []
lista = []

#Lettura Excel
nomeExcel = "FORMAT RENDICONTAZIONE.xlsx"

indice = 0
for dato_lavoratori in dati_tutti_lavoratori:
    colonnaExcel = dato_lavoratori
    functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, "DATI LAVORATORI"), colonnaExcel, array)
    if indice == 0:
        tutti_lavoratori[0] = array.copy()
    else:
        lista = array.copy()
        tutti_lavoratori.append(lista)
    array.clear()
    indice += 1

indice = 0
for attributo in attributi_istanza:
    colonnaExcel = attributo
    functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, "DATI ISTANZE"), colonnaExcel, array)
    if indice == 0:
        tutti_clienti[0] = array.copy()
    else:
        lista = array.copy()
        tutti_clienti.append(lista)
    array.clear()
    indice += 1

indice_dato_cliente = 0
for cliente in range(len(tutti_clienti[0])):
    padre = documento.createElement('istanza')
    xml.appendChild(padre)

    indice_array_cliente = 0
    for attributo in attributi_istanza:
        figlio = documento.createElement(attributo)
        dato_cliente = tutti_clienti[indice_array_cliente]
        figlio.appendChild(documento.createTextNode(dato_cliente[indice_dato_cliente]))
        padre.appendChild(figlio)
        indice_array_cliente += 1
    indice_dato_cliente += 1

    figlio = documento.createElement('lavoratori')
    padre.appendChild(figlio)

    indice_dato_lavoratore = 0
    for lavoratore in range(len(tutti_lavoratori[2])):
        nipote = documento.createElement('lavoratore')
        figlio.appendChild(nipote)

        #qui servirebbe mettere un if che controlli l'identificativo pratica
        indice_array_lavoratore = 0
        for dati_lavoratore in dati_tutti_lavoratori:
            pro_nipote = documento.createElement(dati_lavoratore)
            dato_lavoratore = tutti_lavoratori[indice_array_lavoratore]
            pro_nipote.appendChild(documento.createTextNode(dato_lavoratore[indice_dato_lavoratore]))
            nipote.appendChild(pro_nipote)
            indice_array_lavoratore += 1
        indice_dato_lavoratore += 1




xml_str = documento.toprettyxml(indent="\t")


save_path_file = "test.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)

tree = etree.parse("test.xml")
string = etree.tostring(tree.getroot(), pretty_print = True, xml_declaration = True, standalone = True, encoding = "UTF-8")
with open("test.xml", "wb") as f:
    f.write(string)
