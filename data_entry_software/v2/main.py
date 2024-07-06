import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class AggiungiPartitaApp:
    def __init__(self, root):
        self.root = root
        img = tk.PhotoImage(file="amadeus.png")
        self.root.iconphoto(False, img)
        self.root.resizable(False, False)
        self.root.title("Affari Tuoi Data Entry")
        self.root.geometry("400x570")

        # Variabili per la partita corrente e le azioni
        self.partita_corrente = {"data": "", "azioni": []}
        self.partite = self.carica_partite()

        # Campo per la data della partita
        tk.Label(root, text="Data (dd/mm/yyyy)").pack()
        self.data_entry = tk.Entry(root)
        self.data_entry.pack()

        # Dropdown per selezionare il tipo di azione
        tk.Label(root, text="Tipo di Azione").pack()
        self.tipo_azione_var = tk.StringVar()
        self.tipo_azione_combobox = ttk.Combobox(root, textvariable=self.tipo_azione_var, state="readonly")
        self.tipo_azione_combobox['values'] = ["Inizio", "Apertura", "Offerta", "Cambio", "Fine"]
        self.tipo_azione_combobox.pack()
        self.tipo_azione_combobox.bind("<<ComboboxSelected>>", self.update_action_fields)

        # Campo per il numero del pacco concorrente
        tk.Label(root, text="Numero Pacco Concorrente").pack()
        self.num_pacco_concorrente_entry = tk.Entry(root, state=tk.DISABLED)
        self.num_pacco_concorrente_entry.pack()

        # Campo per il numero del pacco aperto
        tk.Label(root, text="Numero Pacco Aperto").pack()
        self.num_pacco_aperto_entry = tk.Entry(root, state=tk.DISABLED)
        self.num_pacco_aperto_entry.pack()

        # Campo per il valore del pacco aperto
        tk.Label(root, text="Valore Pacco Aperto").pack()
        self.val_pacco_aperto_entry = tk.Entry(root, state=tk.DISABLED)
        self.val_pacco_aperto_entry.pack()

        # Campo per il valore dell'offerta
        tk.Label(root, text="Valore Offerta").pack()
        self.val_offerta_entry = tk.Entry(root, state=tk.DISABLED)
        self.val_offerta_entry.pack()

        # Dropdown per lo stato dell'offerta
        tk.Label(root, text="Stato Offerta").pack()
        self.stato_offerta_var = tk.StringVar()
        self.stato_offerta_combobox = ttk.Combobox(root, textvariable=self.stato_offerta_var, state=tk.DISABLED)
        self.stato_offerta_combobox['values'] = ["Accettata", "Rifiutata"]
        self.stato_offerta_combobox.pack()

        # Dropdown per lo stato del cambio
        tk.Label(root, text="Stato Cambio").pack()
        self.stato_cambio_var = tk.StringVar()
        self.stato_cambio_combobox = ttk.Combobox(root, textvariable=self.stato_cambio_var, state=tk.DISABLED)
        self.stato_cambio_combobox['values'] = ["Accettato", "Rifiutato"]
        self.stato_cambio_combobox.pack()

        # Campo per il tipo di fine
        tk.Label(root, text="Tipo Fine").pack()
        self.tipo_fine_var = tk.StringVar()
        self.combo_tipo_fine = ttk.Combobox(root, textvariable=self.tipo_fine_var, state=tk.DISABLED)
        self.combo_tipo_fine['values'] = ["Regione fortunata", "Pacco", "Offerta"]
        self.combo_tipo_fine.pack()

        # Campo per il valore di vincita
        tk.Label(root, text="Valore Vincita").pack()
        self.valore_vincita_entry = tk.Entry(root, state=tk.DISABLED)
        self.valore_vincita_entry.pack()

        # Pulsante per aggiungere azione
        self.aggiungi_azione_button = tk.Button(root, text="Aggiungi Azione", command=self.aggiungi_azione)
        self.aggiungi_azione_button.pack()

        # Pulsante per salvare la partita
        self.salva_partita_button = tk.Button(root, text="Salva Partita", command=self.salva_partita)
        self.salva_partita_button.pack()

    def carica_partite(self):
        if os.path.exists("azioni_partite.json"):
            with open("azioni_partite.json", "r") as file:
                return json.load(file)
        else:
            return []

    def update_action_fields(self, event):
        tipo_azione = self.tipo_azione_var.get()
        if tipo_azione == "Inizio":
            self.toggle_fields(True, False, False, False, False, False, False, False)
        elif tipo_azione == "Apertura":
            self.toggle_fields(True, True, True, False, False, False, False, False)
        elif tipo_azione == "Offerta":
            self.toggle_fields(True, False, False, True, True, False, False, False)
        elif tipo_azione == "Cambio":
            self.toggle_fields(True, False, False, False, False, True, False, False)
        elif tipo_azione == "Fine":
            self.toggle_fields(True, False, False, False, False, False, True, True)

    def toggle_fields(self, pacco_concorrente, pacco_aperto, val_pacco, val_offerta, stato_offerta, stato_cambio, tipo_fine, valore_vincita):
        self.num_pacco_concorrente_entry.config(state=tk.NORMAL if pacco_concorrente else tk.DISABLED)
        self.num_pacco_aperto_entry.config(state=tk.NORMAL if pacco_aperto else tk.DISABLED)
        self.val_pacco_aperto_entry.config(state=tk.NORMAL if val_pacco else tk.DISABLED)
        self.val_offerta_entry.config(state=tk.NORMAL if val_offerta else tk.DISABLED)
        self.stato_offerta_combobox.config(state="readonly" if stato_offerta else tk.DISABLED)
        self.stato_cambio_combobox.config(state="readonly" if stato_cambio else tk.DISABLED)
        self.combo_tipo_fine.config(state="readonly" if tipo_fine else tk.DISABLED)
        self.valore_vincita_entry.config(state=tk.NORMAL if valore_vincita else tk.DISABLED)

    def aggiungi_azione(self):
        tipo_azione = self.tipo_azione_var.get()
        num_pacco_concorrente = self.num_pacco_concorrente_entry.get()
        num_pacco_aperto = self.num_pacco_aperto_entry.get()
        val_pacco_aperto = self.val_pacco_aperto_entry.get()
        val_offerta = self.val_offerta_entry.get()
        stato_offerta = self.stato_offerta_var.get()
        stato_cambio = self.stato_cambio_var.get()
        tipo_fine = self.tipo_fine_var.get()
        valore_vincita = self.valore_vincita_entry.get()

        if not num_pacco_concorrente:
            messagebox.showerror("Errore", "Inserisci il numero del pacco del concorrente.")
            return

        azione = {
            "id": len(self.partita_corrente["azioni"]), 
            "tipoAzione": tipo_azione, "args": {}, 
            "numPaccoConcorrente": int(num_pacco_concorrente)
            }

        if tipo_azione == "Apertura":
            azione["args"]["numPaccoAperto"] = int(num_pacco_aperto)
            azione["args"]["valPaccoAperto"] = int(val_pacco_aperto)
        elif tipo_azione == "Offerta":
            azione["args"]["valOfferta"] = int(val_offerta)
            azione["args"]["statoOfferta"] = stato_offerta
        elif tipo_azione == "Cambio":
            azione["args"]["statoCambio"] = stato_cambio
            azione["args"]["numVecchioPacco"] = self.partita_corrente["azioni"][len(self.partita_corrente["azioni"]) - 1]["numPaccoConcorrente"]
            azione["args"]["numNuovoPacco"] = int(num_pacco_concorrente)
        elif tipo_azione == "Fine":
            azione["args"]["tipoFine"] = tipo_fine
            azione["args"]["vincita"] = int(valore_vincita)

        self.partita_corrente["azioni"].append(azione)
        messagebox.showinfo("Successo", "Azione aggiunta con successo!")
        self.clear_fields()

    def clear_fields(self):
        self.tipo_azione_combobox.set("")
        self.num_pacco_concorrente_entry.delete(0, tk.END)
        self.num_pacco_aperto_entry.delete(0, tk.END)
        self.val_pacco_aperto_entry.delete(0, tk.END)
        self.val_offerta_entry.delete(0, tk.END)
        self.stato_offerta_combobox.set("")
        self.stato_cambio_combobox.set("")
        self.combo_tipo_fine.set("")
        self.valore_vincita_entry.delete(0, tk.END)

    def salva_partita(self):
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Errore", "Inserisci la data della partita.")
            return

        self.partita_corrente["data"] = data
        self.partite.append(self.partita_corrente)

        with open("azioni_partite.json", "w") as file:
            json.dump(self.partite, file, indent=4)

        messagebox.showinfo("Successo", "Partita salvata con successo!")
        self.partita_corrente = {"data": "", "azioni": []}
        self.data_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AggiungiPartitaApp(root)
    root.mainloop()
