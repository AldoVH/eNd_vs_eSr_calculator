import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

datos = pd.read_csv('C:\\Users\\aldo2\\OneDrive\\Documents\\sem9\\petro ignea\\eNd_vs_eSr\\datos_isotopicos.csv', encoding='latin-1')

padreSr = datos['87Rb/86Sr']
padreNd = datos['147Sm/144Nd']
hijoSri = datos['87Sr/86Sr']
hijoNdi = datos['143Nd/144Nd']
edad = datos['Edad (Ma)']
roca = datos['Roca']
decaimientoSr = 0.0000000000142
decaimientoNd = 0.00000000000654

padreSr = padreSr.tolist()
padreNd = padreNd.tolist()
hijoSri = hijoSri.tolist()
hijoNdi = hijoNdi.tolist()
edad = edad.tolist()
#Jala los datos del csv y los convierte de un dataframe a una lista

eSr = []
eNd = []
#crea dos listas
for e in edad:
    eSr.append(math.exp(e * decaimientoSr))
    eNd.append(math.exp(e * decaimientoNd))
#agrega el resultado de la expresion para cada elemento a las listas creadas, donde e representa cada elemento

hijoSrm = [hijo + padre * (e - 1) for hijo, padre, e in zip(hijoSri, padreSr, eSr)]
hijoNdm = [hijo + padre * (e - 1) for hijo, padre, e in zip(hijoNdi, padreNd, eNd)]
#aplica la formula a cada elemento de las listas declaradas

churSr = 0.7045
churNd = 0.512638

epsilonSr = []
for e in hijoSrm:
    epsilonSr.append(((e / churSr)-1)*10000)
#aplica la formula a cada elemento de las lista declarada

epsilonNd = []
for e in hijoNdm:
    epsilonNd.append(((e / churNd)-1)*10000)
#aplica la formula a cada elemento de las listas declarada

litologia = roca.unique()
#obtiene los valores de la columna 'Roca' sin repeticiones para determinar con cuantos tipos de roca se esta trabajando
roca_color = {}
roca_simbolo = {}

for e in litologia:
    roca_color[e] = np.random.rand(3,)
    roca_simbolo[e] = np.random.choice(['s', 'o', '^', 'v', 'd'])
#asigna un codigo RGB y un simbolo aleatorio por cada elemento en la lista litologia

colores = [roca_color[e] for e in roca]
simbolos = [roca_simbolo[e] for e in roca]

plt.figure(figsize=(10, 8))
#especifica el tamano de la figura

epsilonSr = pd.Series(epsilonSr)
epsilonNd = pd.Series(epsilonNd)
#convierte epsilonSr y epsilonNd de lista a serie

for tipo_roca in litologia:
    indices = roca == tipo_roca
    x = epsilonSr[indices]
    y = epsilonNd[indices]
    colores = roca_color[tipo_roca]
    marker = roca_simbolo[tipo_roca]
    plt.scatter(x, y, color=colores, marker=marker, label=tipo_roca)
#asocia un color y simbolo a cada tipo de roca y los plotea

simbologia = []
for tipo_roca in litologia:
    colores = roca_color[tipo_roca]
    marker = roca_simbolo[tipo_roca]
    simbologia.append(plt.Line2D([0], [0], marker=marker, color='w', label=tipo_roca, markerfacecolor=colores, markersize=10))
#asocia un color y simbolo a cada tipo de roca para imprimir la simbologia

plt.legend(handles=simbologia)

x_min = -50
x_max = 300
y_min = -15
y_max = 15

#limites de los ejes x y
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
#dividen el grafico en cuadrantes

plt.xlabel('εSr')
plt.ylabel('εNd')
plt.title('εNd vs εSr')
plt.grid(True)

plt.savefig('output.png', dpi=300, bbox_inches='tight')
#guarda la grafia resultante

plt.show()
