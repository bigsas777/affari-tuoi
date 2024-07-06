DESCRIZIONE DEI FILE

1- azioni_partite.json --> file utilizzato dal software di raccolta dati.
2- json_to_dataframe.py --> script per passare dal formato JSON al formato PARQUET, crea il file "azioni_partite.parquet".

3- azioni_partite_originale.parquet --> file contenente i dati raccolti nel file JSON.
4- azioni_partite_dati_derivati.parquet --> file ottenuto a partire da "azioni_partite_originale.parquet", contiene dati calcolati a partire dai dati originali, le operazioni effettuate si trovano nel file "dati_derivati.py".

5- pacchi_e_vincite.parquet --> dataset iniziale contenente solemanete pacchi, premi, vincite e tipo vincite