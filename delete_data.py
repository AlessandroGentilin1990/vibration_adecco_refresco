import os
import tkinter as tk
from tkinter import messagebox

# Funzione per cancellare tutti i file nella cartella
def clear_folder():
    folder_path = r'C:\device1'

    # Controlla se la cartella esiste
    if os.path.exists(folder_path):
        # Elenca tutti i file nella cartella
        files = os.listdir(folder_path)
        # Variabile per sapere se è stato cancellato almeno un file
        files_deleted = False

        # Cancella ogni file nella cartella
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)

            # Verifica se è un file e non una cartella
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    files_deleted = True
                    print(f"File {file_name} rimosso con successo.")
                except Exception as e:
                    print(f"Errore durante la rimozione di {file_name}: {e}")

        # Mostra il messaggio di conferma solo se sono stati cancellati dei file
        if files_deleted:
            messagebox.showinfo("Stato", "Tutti i dati sono stati eliminati.")
        else:
            messagebox.showinfo("Stato", "Nessun file trovato da eliminare.")
    else:
        messagebox.showerror("Errore", f"La cartella {folder_path} non esiste.")

# Creiamo una finestra tkinter per attivare il codice
root = tk.Tk()
root.withdraw()  # Nasconde la finestra principale

# Chiamata alla funzione che elimina i file
clear_folder()

# Chiude la finestra tkinter dopo l'operazione
root.quit()
