import pandas as pd
import json

# Carica i dati dal file JSON
with open('azioni_partite.json', 'r') as file:
    data = json.load(file)

# Lista per contenere i dati delle azioni
azioni_list = []

# Itero attraverso i dati per creare le righe del DataFrame
for partita in data:
    data_partita = partita['data']
    for azione in partita['azioni']:
        id_azione = azione['id']
        tipo_azione = azione['tipoAzione']
        num_pacco_concorrente = azione['numPaccoConcorrente']
        args = azione['args']
        
        # Crea un dizionario per ogni azione
        azione_dict = {
            'data': data_partita,
            'idAzione': id_azione,
            'tipoAzione': tipo_azione,
            'numPaccoConcorrente': num_pacco_concorrente,
        }
        
        # Aggiunge gli argomenti se presenti
        azione_dict.update(args)
        
        # Aggiunge il dizionario dell'azione alla lista di azioni
        azioni_list.append(azione_dict)

# Crea il DataFrame dalle azioni
df = pd.DataFrame(azioni_list)

# Impostiamo l'indice del DataFrame con la data e l'id dell'azione
df.set_index(['data', 'idAzione'], inplace=True)

# ------------------ Pulizia dati -------------------
# Sistemazione tipi di dato dell'indice
df.index = df.index.set_levels([pd.to_datetime(df.index.levels[0], format='%d/%m/%Y'), df.index.levels[1].astype("Int64")])

# Sistemazione tipi di dato
df["tipoAzione"] = df["tipoAzione"].astype("string")
df["numPaccoConcorrente"] = df["numPaccoConcorrente"].astype("Int64")
df["numPaccoAperto"] = df["numPaccoAperto"].astype("Int64")
df["valPaccoAperto"] = df["valPaccoAperto"].astype("Int64")
df["valOfferta"] = df["valOfferta"].astype("Int64")
df["statoOfferta"] = df["statoOfferta"].astype("string")
df["statoCambio"] = df["statoCambio"].astype("string")
df["numVecchioPacco"] = df["numVecchioPacco"].astype("Int64")
df["numNuovoPacco"] = df["numNuovoPacco"].astype("Int64")
df["tipoFine"] = df["tipoFine"].astype("string")
df["vincita"] = df["vincita"].astype("Int64")

df = df.sort_index(level="data")

df.to_parquet("azioni_partite.parquet")