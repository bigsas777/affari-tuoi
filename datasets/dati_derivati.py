import pandas as pd
import numpy as np

# Lettura dataframe originale e variabili
df_azioni = pd.read_parquet("azioni_partite_otiginale.parquet")
premi_possibili = np.array([0, 1, 5, 10, 20, 50, 75, 100, 200, 500, 5000, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000])




# Aggiunta pacchi rimanenti ad ogni azione
tutte_azioni_rimasti = []

for i, date_index in enumerate(df_azioni.index.levels[0]):
    partita = df_azioni.loc[date_index]
    premi_rimasti = premi_possibili.copy()
    rimasti_azione = []
    
    for id_azione in partita.index:
        azione = partita.loc[id_azione]
        tipo_azione = azione['tipoAzione']
        
        if tipo_azione == 'Apertura':
            index = np.argwhere(premi_rimasti == azione['valPaccoAperto'])
            premi_rimasti = np.delete(premi_rimasti, index)
        
        rimasti_azione.append(premi_rimasti.copy())
    
    tutte_azioni_rimasti.extend(rimasti_azione)

df_azioni['premiRimasti'] = tutte_azioni_rimasti



# Calcolo media premi rimasti in gioco ad ogni azione
medie_premi_rimasti = []

for arr_rimasti in df_azioni['premiRimasti']:
    if arr_rimasti.size != 0:
        media_approx_intera = int(round(np.mean(arr_rimasti)))
        medie_premi_rimasti.append(media_approx_intera)
    else:
        medie_premi_rimasti.append(pd.NA)

df_azioni['mediaPremiRimasti'] = medie_premi_rimasti
df_azioni['mediaPremiRimasti'] = df_azioni['mediaPremiRimasti'].astype("Int64")



# Aggiunta premio in mano al concorrente ad ogni azione
df_azioni['premioManoConcorrente'] = None

for i, date_index in enumerate(df_azioni.index.levels[0]): # per ogni partita + un indice numerico
    partita = df_azioni.loc[date_index]
    premio_mano_concorrente = None
    
    for id_azione in partita.index: # per ogni azione
        azione = partita.loc[id_azione]
        num_pacco_concorrente = azione['numPaccoConcorrente']
        
        # Trova il premio del pacco in mano al concorrente
        premio_concorrente = partita[partita['numPaccoAperto'] == num_pacco_concorrente]['valPaccoAperto'].values
        
        if premio_concorrente.size > 0:
            premio_mano_concorrente = premio_concorrente[0]
        
        # Assegna il premio corrente alla colonna premioManoConcorrente
        df_azioni.at[(date_index, id_azione), 'premioManoConcorrente'] = premio_mano_concorrente

df_azioni['premioManoConcorrente'] = df_azioni['premioManoConcorrente'].astype("Int64")




# Salvataggio dataframe con nuovi dati
df_azioni.to_parquet("azioni_partite_dati_derivati.parquet")