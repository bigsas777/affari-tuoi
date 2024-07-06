import csv
from tkinter import END, Checkbutton, Entry, Frame, BooleanVar, Label, PanedWindow, PhotoImage, Tk, messagebox, ttk, Button
from tkcalendar import DateEntry
from tkmacosx import Button as BtnMac
import pandas as pd
from datetime import date
from google.oauth2.service_account import Credentials
import gspread


def main():
    root.title(f"Affari Tuoi Manager - {today_str}")
    img = PhotoImage(file="amadeus.png")
    root.iconphoto(False, img)
    root.geometry("800x600")

    # Menu bottoni schermate
    paned_buttons = PanedWindow(root, orient="horizontal")

    btn_inserimento = Button(paned_buttons, text="Inserimento📥", command=(lambda: build_panel("ins")))
    btn_inserimento.pack(side="left")
    paned_buttons.add(btn_inserimento)

    '''
    btn_classifica = Button(paned_buttons, text="Classifica📊", command=(lambda: build_panel("clas")))
    btn_classifica.pack(side="left")
    paned_buttons.add(btn_classifica)
    '''

    btn_impostazioni = Button(paned_buttons, text="Impostazioni⚙️", command=(lambda: build_panel("imp")))
    btn_impostazioni.pack(side="left")
    paned_buttons.add(btn_impostazioni)

    # Label placeholder
    lbl_intro = Label(frame_panel, text="Scegli una schermata per cominciare...", font=("TkDefaultFont", 19), pady=30)
    lbl_intro.pack(side="top")

    paned_buttons.pack(side="top")
    frame_panel.pack(side="top")

    root.mainloop()

def build_panel(panel_id):
    # Pulisce il pannello per la prossima schermata
    for widget in frame_panel.winfo_children():
        widget.destroy()

    if panel_id == "ins":
        build_panel_inserimento()
    #elif panel_id == "clas" :
        #build_panel_classifica()
    elif panel_id == "imp":
        build_panel_impostazioni()
    else:
        messagebox.showerror("Errore", "Tipo di schermata non riconosciuto")

def build_panel_impostazioni():
    frm_impostazioni = Frame(frame_panel, pady=30)

    lbl_load = Label(frm_impostazioni, text="Carica da file", font=("TkDefaultFont", 19))
    lbl_load.pack(side="top")

    btn_load_csv = Button(frm_impostazioni, text="Carica partita da file CSV", command=(lambda: load_partita_from_file("csv")))
    btn_load_csv.pack(side="top")

    lbl_save = Label(frm_impostazioni, text="Salva su file", font=("TkDefaultFont", 19), pady=10)
    lbl_save.pack(side="top")

    btn_save_csv = Button(frm_impostazioni, text="Salva partita su file CSV", command=(lambda: save_partita_to_file("csv")))
    btn_save_csv.pack(side="top")

    frm_impostazioni.pack(side="top")

'''
def build_panel_classifica():
    frm_classifica = Frame(frame_panel, pady=30)
    lbl_classifica = Label(frm_classifica, text="Classifica", font=("TkDefaultFont", 19))
    lbl_classifica.grid(row=0, column=0)

    frm_classifica.pack(side="top")
'''

def build_panel_inserimento():
    global list_cmb_pacchi, chk_sheets, chk_parquet, val_chk_sheets, val_chk_parquet
    list_cmb_pacchi = []
    val_chk_sheets = BooleanVar()
    val_chk_parquet = BooleanVar()

    frm_inserimento = Frame(frame_panel, pady=30)
    lbl_input_pacchi = Label(frm_inserimento, text="Inserimento pacchi", font=("TkDefaultFont", 19))
    lbl_input_pacchi.grid(row=0, column=0)

    global entry_data
    entry_data = DateEntry(frm_inserimento)
    entry_data.bind("<<DateEntrySelected>>", update_data)
    entry_data.grid(row=0, column=1)

    count = 1
    for i in range(2):
        for j in range(10):
            frm_pacco = Frame(frm_inserimento)
            lbl_pacco = Label(frm_pacco, text=str(count))

            cmb_pacco = ttk.Combobox(frm_pacco, state="readonly", postcommand=update_available_pacchi) # postcommand: eseguito prima che si generi la lista di opzioni
            cmb_pacco.bind("<<ComboboxSelected>>", lambda event, num_pacco=str(count): update_tonight_partita(event, num_pacco))
            cmb_pacco["values"] = POSSIBLE_PRIZES
            list_cmb_pacchi.append(cmb_pacco)

            lbl_pacco.grid(row=0, column=0)
            cmb_pacco.grid(row=0, column=1)
            frm_pacco.grid(row=j+1, column=i, padx=10, pady=5)

            count += 1

    frm_vincita = Frame(frm_inserimento)
    frm_vincita.grid(row=12,column=0)
    lbl_vincita = Label(frm_vincita, text="Vincita")
    lbl_vincita.grid(row=0, column=0)
    global entry_vincita
    entry_vincita = Entry(frm_vincita, width=13)
    entry_vincita.grid(row=0, column=1)
    btn_update_vincita = Button(frm_vincita, text="Conferma", command=lambda key="Vincita": update_tonight_partita(None, key))
    btn_update_vincita.grid(row=0, column=2)

    frm_tipo_vincita = Frame(frm_inserimento)
    frm_tipo_vincita.grid(row=13, column=0)
    lbl_tipo_vincita = Label(frm_tipo_vincita, text="Tipo vincita")
    lbl_tipo_vincita.grid(row=0, column=0)
    global cmb_tipo_vincita
    cmb_tipo_vincita = ttk.Combobox(frm_tipo_vincita, values=["Regione fortunata", "Offerta", "Pacco"], state="readonly")
    cmb_tipo_vincita.bind("<<ComboboxSelected>>", lambda event, key="Tipo vincita": update_tonight_partita(event, key))
    cmb_tipo_vincita.grid(row=0, column=1)

    frm_salvataggio = Frame(frm_inserimento)
    chk_sheets = Checkbutton(frm_salvataggio, text="Sheets", variable=val_chk_sheets, onvalue=True, offvalue=False)
    chk_sheets.grid(row=0, column=0)
    chk_parquet = Checkbutton(frm_salvataggio, text="Parquet", variable=val_chk_parquet, onvalue=True, offvalue=False)
    chk_parquet.grid(row=0, column=1)
    btn_salva_partita = BtnMac(frm_salvataggio, text="Salva partita💾", command=confirm_pacchi, foreground="white", background="#155CCC")
    btn_salva_partita.grid(row=0, column=2)
    frm_salvataggio.grid(row=14, column=1, pady=5)

    frm_inserimento.pack(side="top")

    inserimento_loaded_data() # Ripristina i valori delle Combobox se viene cambiata la schermata

def update_data(event):
    global selected_date, selected_date_str
    selected_date = event.widget.get_date()
    selected_date_str = selected_date.strftime("%d/%m/%Y")
    tonight_partita["Data"] = selected_date_str
    maschera_tonight_modified["Data"] = True

def update_tonight_partita(event, key):
    if key != "Tipo vincita":
        if key == "Vincita":
            val = entry_vincita.get()
        else:
            val = event.widget.get()

        tonight_partita[key] = pacco_to_float(val)
    else:
        tonight_partita[key] = event.widget.get()
    
    maschera_tonight_modified[key] = True

def update_available_pacchi():
    i = 0
    selected_prizes = []
    for cmb in list_cmb_pacchi:
        selected_prizes.insert(i, cmb.get())
        i += 1

    for cmb in list_cmb_pacchi:
        cmb["values"] = difference(POSSIBLE_PRIZES, selected_prizes)
    
def difference(l1, l2):
    tmp = []
    for element in l1:
        if element not in l2:
            tmp.append(element)
    return tmp

def confirm_pacchi():
    if messagebox.showwarning("Salvare la partita?", str_warning_salvataggio) == "ok":
        # Aggiorna il dataframe
        df_partite_affari_tuoi.loc[len(df_partite_affari_tuoi)] = tonight_partita
        df_partite_affari_tuoi["Data"] = pd.to_datetime(df_partite_affari_tuoi["Data"], format="%d/%m/%Y")
        df_partite_affari_tuoi.sort_values(by=["Data"], inplace=True) # Ordina per data
        df_partite_affari_tuoi["Data"] = df_partite_affari_tuoi["Data"].map(lambda x: x.strftime("%d/%m/%Y"))
        
        if val_chk_parquet.get():
            try: # Salvataggio in locale
                df_partite_affari_tuoi.to_parquet("dataset_affari_tuoi.parquet")
            except Exception as e:
                print(e)
                messagebox.showerror("Errore", f"Errore nel salvataggio in Parquet.\n {e}")

        
        index_tonight_partita = len(df_partite_affari_tuoi) # Dove verrà aggiunta la partita (Spoiler: in fondo)

        if val_chk_sheets.get():
            try: # Salvataggio in cloud (Google Sheets)
                sheet.update(range_name=f"A{index_tonight_partita}:W{index_tonight_partita}", values=[list(tonight_partita.values())])
            except Exception as e:
                print(e)
                messagebox.showerror("Errore", f"Errore nell'invio dei dati a Google Sheets.\n {e}")

def pacco_to_float(pacco: str):
    return float(pacco.replace(".", ""))

def float_to_pacco(premio):
    premio = float(premio)
    return f"{premio:,.0f}".replace(",", ".")

def load_partita_from_file(file_format):
    global tonight_partita, maschera_tonight_modified

    if file_format == "csv": # Per future implementazioni di altri formati
        with open("saved_partita.csv", "r") as csv_data:
            reader = csv.reader(csv_data, delimiter=",")

            for key, loaded_val in zip(tonight_partita.keys(), next(reader)):
                if key == "Tipo vincita" or key == "Data":
                    tonight_partita[key] = loaded_val
                else:
                    tonight_partita[key] = float(loaded_val)
        
        for key in maschera_tonight_modified:
            maschera_tonight_modified[key] = True
    else:
        messagebox.showerror("Errore", "Tipo di file sconosciuto")

def inserimento_loaded_data():
    list_maschera = list(maschera_tonight_modified.values())

    for i, data in enumerate(tonight_partita.values()):
        if list_maschera[i]:
            if i == 0:
                entry_data.set_date(selected_date) # Aggiorna la data selezionata
            elif i > 0 and i < 21:
                list_cmb_pacchi[i-1].set(float_to_pacco(data)) # Aggiorna combobox pacchi
            elif i == 21:
                entry_vincita.delete(0, END) # Aggiorna entry vincita
                entry_vincita.insert(0, str(data))
            elif i == 22:
                cmb_tipo_vincita.set(data) # Aggiorna combobox tipo vincita
            i += 1

def save_partita_to_file(file_format):
    if file_format == "csv": # Per future implementazioni di altri formati
        with open("saved_partita.csv", "w", newline="") as csv_data:
            writer = csv.writer(csv_data, delimiter=",")
            writer.writerow(tonight_partita.values())
    else:
        messagebox.showerror("Errore", "Tipo di file sconosciuto")


# --- ENTRY POINT ---
if __name__ == "__main__":
    today = date.today()
    today_str = today.strftime("%d/%m/%Y")
    selected_date = today
    selected_date_str = selected_date.strftime("%d/%m/%Y")

    str_warning_salvataggio = f"La partita verrà salvata in locale e/o su Google Sheets."

    # Dataset contenente tutte le partite dal 12/02/24 ad oggi
    df_partite_affari_tuoi = pd.read_parquet("dataset_affari_tuoi.parquet")

    # Struttura dati che memorizza la partita su cui si sta lavorando
    tonight_partita = {"Data": today_str, "1": 0.0, "2": 0.0, "3": 0.0, "4": 0.0, "5": 0.0, "6": 0.0, "7": 0.0, 
                       "8": 0.0, "9": 0.0, "10": 0.0, "11": 0.0, "12": 0.0, "13": 0.0, "14": 0.0, "15": 0.0, "16": 0.0, 
                       "17": 0.0, "18": 0.0, "19": 0.0,"20": 0.0, "Vincita": "", "Tipo vincita": ""}
    
    # Maschera booleana per riconoscere quale widget del frm_inserimento è stato modificato
    maschera_tonight_modified = {"Data": False, "1": False, "2": False, "3": False, "4": False, "5": False, 
                                 "6": False, "7": False, "8": False, "9": False, "10": False, "11": False, 
                                 "12": False, "13": False, "14": False, "15": False, "16": False, "17": False, 
                                 "18": False, "19": False, "20": False, "Vincita": False, "Tipo vincita": False}
    
    list_cmb_pacchi = [] # Conserva tutte le Combobox dei pacchi
    POSSIBLE_PRIZES = ["0", "1", "5", "10", "20", "50", "75", "100", "200", "500", "5.000", "10.000", "15.000", "20.000", "30.000", 
                        "50.000", "75.000", "100.000", "200.000", "300.000"]
    val_chk_sheets = None # Valore associato al Checkbutton per il salvataggio in Google Sheets
    val_chk_parquet = None # Valore associato al Checkbutton per il salvataggio in Parquet

    # Google Sheets API config
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    try:
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_key("1kaKvRk6R95m9XySwtx_GQvxY2v3QQpTwTnWHPQveed8")
        sheet = workbook.worksheet("Dati")
    except Exception as e:
        print(e)
        messagebox.showerror("Errore", f"Errore Google Sheets\n{e}")

    # Public widgets
    root = Tk()
    frame_panel = Frame(root)
    entry_vincita = None
    cmb_tipo_vincita = None
    entry_data = None

    main()