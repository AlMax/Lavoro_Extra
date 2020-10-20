from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('/Users/almax/Desktop/Varie/GitHub/MAW/RicercaPdf_Specifica'):
    #if filenames[-4:] == ".pdf":
    f.extend(filenames[-4:])
    break

print("\n")
print(f)