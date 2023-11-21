with open("Mapa.txt","r") as archivo:
    archivo = archivo.readlines()
import random
copia = []
for y, fila in enumerate(archivo):
    copia.append([])
    for x, elemento in enumerate(fila):
        if elemento == "0":
            copia[y].append(random.choice(["0","1"]))
        elif elemento == "1":
            copia[y].append("1")
        elif elemento == "2":
            copia[y].append("2")

with open("Mapa.txt","w") as archivo:
    for fila in copia:
        for elemento in fila:
            archivo.write(elemento)
        archivo.write("\n")
    
            
