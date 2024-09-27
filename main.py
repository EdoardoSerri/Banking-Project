# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def importi_in_float(list_importi):
    importi_float = []
    for stringa in list_importi:
        if stringa[0] != 0:
            stringa_punto = str(stringa[0])
            if '.' in stringa_punto:
                stringa_punto = stringa_punto.replace('.', '')
            stringa_punto = stringa_punto.replace(',', '.')
            importi_float.append(float(stringa_punto))
        else:
            importi_float.append(float(stringa[0]))
    importi_float = np.array(importi_float).reshape(-1,1)
    return importi_float   

def ID_trasazione(list_transazioni):
    dict_transazione = {}
    ID = 0
    lista_ID_transazioni = []
    for transazione in tipo_transazione:
        if str(transazione) not in dict_transazione:
            dict_transazione[str(transazione)] = ID
            ID = ID+1
        lista_ID_transazioni = np.append(lista_ID_transazioni,dict_transazione[str(transazione)])
    return lista_ID_transazioni

#df1 = pd.read_excel('movimenti_marzo_maggio_2024.xlsx')
df2 = pd.read_csv('ListaTransazioni_20240101_20240331.csv', sep=';')

# togli NaN e sostiutisci con gli zeri
df2 = df2.fillna(0)

# passa da DataFrame a Matrice
matrice = df2.to_numpy()

#Pulisci la matrice dalle date che non servono (Data valuta) e dalla Descizione dell'operazione
nuova_matrice = matrice[1:-1,1:-1]

#Dividi in 3 array: Tipi di Transizione, Entrate e Uscite
date = nuova_matrice[:,0:1]
tipo_transazione = nuova_matrice[:,-1:]
entrate = nuova_matrice[:, 2:3]
uscite = nuova_matrice[:,1:2]

#Converti Entrate e Uscite in array di float e dai un ID per ogni tipo di transazione
entrate_float = importi_in_float(entrate)
uscite_float = importi_in_float(uscite)
lista_ID_transazioni = ID_trasazione(tipo_transazione)
    
lista_ID_transazioni = lista_ID_transazioni.reshape(-1,1)
#kmeans = KMeans(n_clusters=ID, random_state=0).fit(lista_ID_transazioni)

# Assegna ogni punto al suo cluster
#y_kmeans = kmeans.predict(lista_ID_transazioni)

#print(y_kmeans)
#print(lista_ID_transazioni)

# Assicurati che il vettore abbia la stessa dimensione della prima dimensione della matrice
#vettore = y_kmeans.reshape(-1, 1)  # Trasforma in colonna
matrice_nuova = np.hstack((date, uscite_float, entrate_float, tipo_transazione, lista_ID_transazioni))

# Sostituiamo i NaN con zero

df_movimenti = pd.DataFrame(matrice_nuova,columns=['Data','Uscita','Entrata','Transazione', 'ID Transazione'])

df_movimenti['Data'] = pd.to_datetime(df_movimenti['Data'])

df_movimenti['Mese'] = df_movimenti['Data'].dt.month


# Raggruppa per mese e calcola la media
grouped = df_movimenti.groupby(df_movimenti['Mese'])['Uscita'].sum()
grouped1 = df_movimenti.groupby(df_movimenti['Mese'])['Entrata'].sum()

print(grouped)
print(grouped1)

grouped.plot(kind='bar')
grouped1.plot(kind='bar')
plt.xlabel('Mese')
plt.show()





