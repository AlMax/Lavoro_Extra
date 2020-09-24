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

#Lettura Excel
nomeExcel = "FORMAT RENDICONTAZIONE.xlsx"
indice = 0
for dato_lavoratori in dati_tutti_lavoratori:
    colonnaExcel = dato_lavoratori
    functions.leggiExcel_colonna(functions.leggiExcel(nomeExcel, "DATI LAVORATORI"), colonnaExcel, tutti_lavoratori[indice])
    indice += 1

print(tutti_lavoratori)

padre = documento.createElement('istanza')
xml.appendChild(padre)

for attributo in attributi_istanza:
    figlio = documento.createElement(attributo)
    figlio.appendChild(documento.createTextNode('test prodcut'))
    padre.appendChild(figlio)

figlio = documento.createElement('lavoratori')
padre.appendChild(figlio)

for lavoratore in tutti_lavoratori:
    nipote = documento.createElement('lavoratore')
    figlio.appendChild(nipote)

    for dati_lavoratore in dati_tutti_lavoratori:
        pro_nipote = documento.createElement(dati_lavoratore)
        pro_nipote.appendChild(documento.createTextNode('test prodcut'))
        nipote.appendChild(pro_nipote)

xml_str = documento.toprettyxml(indent="\t")


save_path_file = "test.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)

tree = etree.parse("test.xml")
string = etree.tostring(tree.getroot(), pretty_print = True, xml_declaration = True, standalone = True, encoding = "UTF-8")
with open("test.xml", "wb") as f:
    f.write(string)