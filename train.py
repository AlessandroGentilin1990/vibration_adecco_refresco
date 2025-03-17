import tkinter as tk
from tkinter import Menu, Label, Canvas, Toplevel, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
import requests
import numpy as np
import csv
import subprocess
import sys
import threading
import time
import tkinter.messagebox as messagebox

# URL dell'API
BASE_URL = "https://gentilin.pythonanywhere.com/device1"
# Percorso per il file CSV
csv_path = "c:\\device1\\data.csv"
# Percorso per il file di predizione
prediction_path = 'c:\\device1\\prediction.txt'

# Funzione per scrivere le features in un file CSV
def write_features_to_csv(label, x_features, y_features, z_features):
    # Verifica se la directory esiste, altrimenti la crea
    directory = os.path.dirname(csv_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Controlliamo se il file CSV esiste, se no lo creiamo e aggiungiamo l'intestazione
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Aggiungiamo il label e i dati delle features
        row = [label] + x_features + y_features + z_features  # Prima il label, poi tutte le features
        writer.writerow(row)
        messagebox.showinfo("Stato", "Salvato.")
        subprocess.run([sys.executable, 'train_linear_SVM.py'])

# Funzione per calcolare le statistiche
def calculate_features(signal):
    # Calcoliamo 30 statistiche su ciascun segnale
    features = [
        np.mean(signal),  # Media
        np.std(signal),  # Deviazione standard
        np.min(signal),  # Minimo
        np.max(signal),  # Massimo
        np.median(signal),  # Mediana
        np.ptp(signal),  # Scarto interquartile
        np.var(signal),  # Varianza
        np.percentile(signal, 25),  # Percentile 25
        np.percentile(signal, 50),  # Percentile 50 (mediana)
        np.percentile(signal, 75),  # Percentile 75
        np.mean(signal ** 2),  # Media dei quadrati (energia)
        np.sum(signal),  # Somma totale dei valori
        np.mean(np.abs(signal)),  # Media dei valori assoluti
        np.mean(np.diff(signal)),  # Media delle differenze consecutive
        np.sum(np.abs(np.diff(signal))),  # Somma delle differenze assolute
        np.min(np.diff(signal)),  # Minimo delle differenze
        np.max(np.diff(signal)),  # Massimo delle differenze
        np.mean(np.sqrt(np.diff(signal) ** 2)),  # Media delle differenze quadratiche
        np.var(np.diff(signal)),  # Varianza delle differenze
        np.mean(np.cumsum(signal)),  # Media della somma cumulativa
        np.mean(signal < 0),  # Percentuale dei valori negativi
        np.mean(signal > 0),  # Percentuale dei valori positivi
        np.median(np.diff(signal)),  # Mediana delle differenze
        np.mean(signal > np.mean(signal)),  # Percentuale sopra la media
        np.mean(signal < np.mean(signal)),  # Percentuale sotto la media
        np.sum(signal > 0) / len(signal),  # Frequenza positiva
        np.sum(signal < 0) / len(signal),  # Frequenza negativa
        np.std(np.diff(signal)),  # Deviazione standard delle differenze
        np.mean(np.abs(np.diff(signal)))  # Media delle differenze assolute
    ]
    return features

# Funzione per eseguire la richiesta GET, processare i dati e inserire le features
def fetch_and_process_data(label):
    response_get = requests.get(BASE_URL)

    if response_get.status_code == 200:
        data_received = response_get.json()

        # Dividi i primi 900 elementi in 3 array (x, y, z)
        x = data_received[0:300]
        y = data_received[300:600]
        z = data_received[600:900]

        # Calcoliamo le features statistiche per ogni array
        x_features = calculate_features(np.array(x))
        y_features = calculate_features(np.array(y))
        z_features = calculate_features(np.array(z))

        # Salva le features nel file CSV con il label
        write_features_to_csv(label, x_features, y_features, z_features)
        print(f"Features salvate nel file CSV con label: {label}")

    else:
        print(f"Errore nella richiesta GET: {response_get.status_code}")
        print(response_get.json())

# Funzione per eseguire una sola volta la richiesta e salvare le features
def train_model(label):
    fetch_and_process_data(label)  # Processa i dati e salva le features una sola volta

class ConveyorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Nastro Trasportatore")
        self.root.attributes('-fullscreen', True)  # Imposta la finestra a schermo intero

        # Canvas per l'immagine di sfondo
        self.canvas = Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        img_path = os.path.abspath("nastro.png")  # Percorso assoluto per evitare errori
        self.original_image = Image.open(img_path)

        # Adatta l'immagine alla finestra ridimensionata
        self.update_image()
        self.root.bind("<Configure>", self.update_image)

        # Spie luminose all'inizio del nastro
        self.status_label = Label(root, text="Stato Macchina: --", bg="yellow", font=("Arial", 12), width=20)
        self.status_label.place(x=10, y=420)

        self.result_label = Label(root, text="Risultato: --", bg="red", font=("Arial", 12), width=20)
        self.result_label.place(x=10, y=450)

        # Menu a cascata
        self.menu_button = tk.Menubutton(root, text="Menu", relief=tk.RAISED)
        self.menu_button.place(x=10, y=10)

        self.menu = Menu(self.menu_button, tearoff=0)
        self.menu.add_command(label="Train", command=self.open_selection_menu)
        self.menu.add_command(label="Use", command=self.start_use_model)
        self.menu.add_command(label="Clear", command=self.clear_process)

        self.menu_button.config(menu=self.menu)

        # Variabili di controllo per il ciclo di "Use"
        self.use_model_running = False
        self.use_model_thread = None

        # Variabili di controllo per il ciclo di "Train"
        self.train_model_running = False
        self.train_model_thread = None

    def update_image(self, event=None):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()

        resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.resized_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.resized_image)
        self.canvas.config(width=new_width, height=new_height)

    def run_use_model(self):
        subprocess.run([sys.executable, 'use_model.py'])

    def start_use_model(self):
        if not self.use_model_running:
            self.use_model_running = True
            self.use_model_thread = threading.Thread(target=self.use_model_loop)
            self.use_model_thread.start()
            # Aggiungi un pulsante per fermare manualmente il ciclo
            self.stop_button = tk.Button(self.root, text="Stop Use", command=self.stop_use_model)
            self.stop_button.place(x=100, y=10)
        else:
            print("Il modello è già in esecuzione.")

    def use_model_loop(self):
        while self.use_model_running:
            self.run_use_model()  # Avvia il modello
            self.read_prediction()  # Leggi il file prediction.txt
            time.sleep(10)  # Aspetta 10 secondi

    def stop_use_model(self):
        self.use_model_running = False
        if self.use_model_thread.is_alive():
            self.use_model_thread.join()
        print("Ciclo di 'Use' fermato manualmente.")
        self.stop_button.place_forget()  # Nascondi il pulsante di stop

    def read_prediction(self):
        if os.path.exists(prediction_path):
            with open(prediction_path, 'r') as file:
                prediction = file.read().strip()  # Leggi il contenuto del file
                if prediction:
                    self.status_label.config(text=f"Stato Macchina: {prediction}", bg="green")
                else:
                    self.status_label.config(text="Stato Macchina: --", bg="yellow")

    def start_train_model(self, label):
        if not self.train_model_running:
            self.train_model_running = True
            self.train_model_thread = threading.Thread(target=self.train_model_loop, args=(label,))
            self.train_model_thread.start()
            # Aggiungi un pulsante per fermare manualmente il ciclo
            self.stop_train_button = tk.Button(self.root, text="Stop Train", command=self.stop_train_model)
            self.stop_train_button.place(x=200, y=10)
        else:
            print("Il modello di training è già in esecuzione.")

    def train_model_loop(self, label):
        while self.train_model_running:
            train_model(label)  # Avvia il modello di training
            time.sleep(10)  # Aspetta 10 secondi

    def stop_train_model(self):
        self.train_model_running = False
        if self.train_model_thread.is_alive():
            self.train_model_thread.join()
        print("Ciclo di 'Train' fermato manualmente.")
        self.stop_train_button.place_forget()  # Nascondi il pulsante di stop

    def open_selection_menu(self):
        self.selection_window = Toplevel(self.root)
        self.selection_window.title("Seleziona Stato")
        self.selection_window.geometry("300x200")

        options = ["Fermo", "Acceso", "Processo 1", "Processo 2", "Processo 3"]
        self.selected_option = StringVar()
        self.selected_option.set(options[0])

        Label(self.selection_window, text="Seleziona lo stato:", font=("Arial", 12)).pack(pady=10)
        OptionMenu(self.selection_window, self.selected_option, *options).pack()

        tk.Button(self.selection_window, text="Conferma", command=self.confirm_selection).pack(pady=10)

    def confirm_selection(self):
        selected_state = self.selected_option.get()
        self.status_label.config(text=f"Stato Macchina: {selected_state}", bg="green")
        self.selection_window.destroy()

        # Esegui il modello con il label selezionato
        self.start_train_model(selected_state)

    def clear_process(self):
        print("Clear avviato")
        self.status_label.config(text="Stato Macchina: --", bg="yellow")
        self.result_label.config(text="Risultato: --", bg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConveyorGUI(root)
    root.mainloop()


# import tkinter as tk
# from tkinter import Menu, Label, Canvas, Toplevel, StringVar, OptionMenu
# from PIL import Image, ImageTk
# import os
# import requests
# import numpy as np
# import csv
# import subprocess
# import sys
# import threading
# import time
# import tkinter as tk
# from tkinter import messagebox
#
# # URL dell'API
# BASE_URL = "https://gentilin.pythonanywhere.com/device1"
# # Percorso per il file CSV
# csv_path = "c:\\device1\\data.csv"
#
# # Funzione per scrivere le features in un file CSV
# def write_features_to_csv(label, x_features, y_features, z_features):
#     # Verifica se la directory esiste, altrimenti la crea
#     directory = os.path.dirname(csv_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     # Controlliamo se il file CSV esiste, se no lo creiamo e aggiungiamo l'intestazione
#     file_exists = os.path.isfile(csv_path)
#
#     with open(csv_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         # Aggiungiamo il label e i dati delle features
#         row = [label] + x_features + y_features + z_features  # Prima il label, poi tutte le features
#         writer.writerow(row)
#         messagebox.showinfo("Stato", "Salvato.")
#         subprocess.run([sys.executable, 'train_linear_SVM.py'])
#
# # Funzione per calcolare le statistiche
# def calculate_features(signal):
#     # Calcoliamo 30 statistiche su ciascun segnale
#     features = [
#         np.mean(signal),  # Media
#         np.std(signal),  # Deviazione standard
#         np.min(signal),  # Minimo
#         np.max(signal),  # Massimo
#         np.median(signal),  # Mediana
#         np.ptp(signal),  # Scarto interquartile
#         np.var(signal),  # Varianza
#         np.percentile(signal, 25),  # Percentile 25
#         np.percentile(signal, 50),  # Percentile 50 (mediana)
#         np.percentile(signal, 75),  # Percentile 75
#         np.mean(signal ** 2),  # Media dei quadrati (energia)
#         np.sum(signal),  # Somma totale dei valori
#         np.mean(np.abs(signal)),  # Media dei valori assoluti
#         np.mean(np.diff(signal)),  # Media delle differenze consecutive
#         np.sum(np.abs(np.diff(signal))),  # Somma delle differenze assolute
#         np.min(np.diff(signal)),  # Minimo delle differenze
#         np.max(np.diff(signal)),  # Massimo delle differenze
#         np.mean(np.sqrt(np.diff(signal) ** 2)),  # Media delle differenze quadratiche
#         np.var(np.diff(signal)),  # Varianza delle differenze
#         np.mean(np.cumsum(signal)),  # Media della somma cumulativa
#         np.mean(signal < 0),  # Percentuale dei valori negativi
#         np.mean(signal > 0),  # Percentuale dei valori positivi
#         np.median(np.diff(signal)),  # Mediana delle differenze
#         np.mean(signal > np.mean(signal)),  # Percentuale sopra la media
#         np.mean(signal < np.mean(signal)),  # Percentuale sotto la media
#         np.sum(signal > 0) / len(signal),  # Frequenza positiva
#         np.sum(signal < 0) / len(signal),  # Frequenza negativa
#         np.std(np.diff(signal)),  # Deviazione standard delle differenze
#         np.mean(np.abs(np.diff(signal)))  # Media delle differenze assolute
#     ]
#     return features
#
# # Funzione per eseguire la richiesta GET, processare i dati e inserire le features
# def fetch_and_process_data(label):
#     response_get = requests.get(BASE_URL)
#
#     if response_get.status_code == 200:
#         data_received = response_get.json()
#
#         # Dividi i primi 900 elementi in 3 array (x, y, z)
#         x = data_received[0:300]
#         y = data_received[300:600]
#         z = data_received[600:900]
#
#         # Calcoliamo le features statistiche per ogni array
#         x_features = calculate_features(np.array(x))
#         y_features = calculate_features(np.array(y))
#         z_features = calculate_features(np.array(z))
#
#         # Salva le features nel file CSV con il label
#         write_features_to_csv(label, x_features, y_features, z_features)
#         print(f"Features salvate nel file CSV con label: {label}")
#
#     else:
#         print(f"Errore nella richiesta GET: {response_get.status_code}")
#         print(response_get.json())
#
# # Funzione per eseguire una sola volta la richiesta e salvare le features
# def train_model(label):
#     fetch_and_process_data(label)  # Processa i dati e salva le features una sola volta
#
# class ConveyorGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Monitor Nastro Trasportatore")
#         self.root.attributes('-fullscreen', True)  # Imposta la finestra a schermo intero
#
#         # Canvas per l'immagine di sfondo
#         self.canvas = Canvas(root)
#         self.canvas.pack(fill=tk.BOTH, expand=True)
#
#         img_path = os.path.abspath("nastro.png")  # Percorso assoluto per evitare errori
#         self.original_image = Image.open(img_path)
#
#         # Adatta l'immagine alla finestra ridimensionata
#         self.update_image()
#         self.root.bind("<Configure>", self.update_image)
#
#         # Spie luminose all'inizio del nastro
#         self.status_label = Label(root, text="Stato Macchina: --", bg="yellow", font=("Arial", 12), width=20)
#         self.status_label.place(x=10, y=420)
#
#         self.result_label = Label(root, text="Risultato: --", bg="red", font=("Arial", 12), width=20)
#         self.result_label.place(x=10, y=450)
#
#         # Menu a cascata
#         self.menu_button = tk.Menubutton(root, text="Menu", relief=tk.RAISED)
#         self.menu_button.place(x=10, y=10)
#
#         self.menu = Menu(self.menu_button, tearoff=0)
#         self.menu.add_command(label="Train", command=self.open_selection_menu)
#         self.menu.add_command(label="Use", command=self.start_use_model)
#         self.menu.add_command(label="Clear", command=self.clear_process)
#
#         self.menu_button.config(menu=self.menu)
#
#         # Variabili di controllo per il ciclo di "Use"
#         self.use_model_running = False
#         self.use_model_thread = None
#
#         # Variabili di controllo per il ciclo di "Train"
#         self.train_model_running = False
#         self.train_model_thread = None
#
#     def update_image(self, event=None):
#         new_width = self.root.winfo_width()
#         new_height = self.root.winfo_height()
#
#         resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
#         self.resized_image = ImageTk.PhotoImage(resized)
#
#         self.canvas.delete("all")
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.resized_image)
#         self.canvas.config(width=new_width, height=new_height)
#
#     def run_use_model(self):
#         subprocess.run([sys.executable, 'use_model.py'])
#
#     def start_use_model(self):
#         if not self.use_model_running:
#             self.use_model_running = True
#             self.use_model_thread = threading.Thread(target=self.use_model_loop)
#             self.use_model_thread.start()
#             # Aggiungi un pulsante per fermare manualmente il ciclo
#             self.stop_button = tk.Button(self.root, text="Stop Use", command=self.stop_use_model)
#             self.stop_button.place(x=100, y=10)
#         else:
#             print("Il modello è già in esecuzione.")
#
#     def use_model_loop(self):
#         while self.use_model_running:
#             self.run_use_model()  # Avvia il modello
#             time.sleep(10)  # Aspetta 10 secondi
#
#
#     def stop_use_model(self):
#         self.use_model_running = False
#         if self.use_model_thread.is_alive():
#             self.use_model_thread.join()
#         print("Ciclo di 'Use' fermato manualmente.")
#         self.stop_button.place_forget()  # Nascondi il pulsante di stop
#
#     def start_train_model(self, label):
#         if not self.train_model_running:
#             self.train_model_running = True
#             self.train_model_thread = threading.Thread(target=self.train_model_loop, args=(label,))
#             self.train_model_thread.start()
#             # Aggiungi un pulsante per fermare manualmente il ciclo
#             self.stop_train_button = tk.Button(self.root, text="Stop Train", command=self.stop_train_model)
#             self.stop_train_button.place(x=200, y=10)
#         else:
#             print("Il modello di training è già in esecuzione.")
#
#     def train_model_loop(self, label):
#         while self.train_model_running:
#             train_model(label)  # Avvia il modello di training
#             time.sleep(10)  # Aspetta 10 secondi
#
#     def stop_train_model(self):
#         self.train_model_running = False
#         if self.train_model_thread.is_alive():
#             self.train_model_thread.join()
#         print("Ciclo di 'Train' fermato manualmente.")
#         self.stop_train_button.place_forget()  # Nascondi il pulsante di stop
#
#     def open_selection_menu(self):
#         self.selection_window = Toplevel(self.root)
#         self.selection_window.title("Seleziona Stato")
#         self.selection_window.geometry("300x200")
#
#         options = ["Fermo", "Acceso", "Processo 1", "Processo 2", "Processo 3"]
#         self.selected_option = StringVar()
#         self.selected_option.set(options[0])
#
#         Label(self.selection_window, text="Seleziona lo stato:", font=("Arial", 12)).pack(pady=10)
#         OptionMenu(self.selection_window, self.selected_option, *options).pack()
#
#         tk.Button(self.selection_window, text="Conferma", command=self.confirm_selection).pack(pady=10)
#
#     def confirm_selection(self):
#         selected_state = self.selected_option.get()
#         self.status_label.config(text=f"Stato Macchina: {selected_state}", bg="green")
#         self.selection_window.destroy()
#
#         # Esegui il modello con il label selezionato
#         self.start_train_model(selected_state)
#
#     def clear_process(self):
#         print("Clear avviato")
#         self.status_label.config(text="Stato Macchina: --", bg="yellow")
#         self.result_label.config(text="Risultato: --", bg="red")
#
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ConveyorGUI(root)
#     root.mainloop()
