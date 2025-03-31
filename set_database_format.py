import pandas as pd

# Percorso del file CSV
data_path = "c:\\device1\\data.csv"  # Sostituisci con il percorso del tuo CSV

# Leggi il CSV
data = pd.read_csv(data_path, header=None)

# Dizionario di mappatura per i valori da sostituire
options = {
    "Fermo": 0,
    "Acceso": 1,
    "Processo 1": 2,
    "Processo 2": 3,
    "Processo 3": 4
}

# Modifica il primo elemento di ogni riga
for index, row in data.iterrows():
    if row[0] in options:  # Se il valore nel primo elemento è una delle opzioni
        data.at[index, 0] = options[row[0]]  # Sostituisci con il valore numerico

# Riscrivi il CSV modificato (con lo stesso nome o un nuovo nome)
modified_data_path = "c:\\device1\\formatted_data.csv"  # Percorso per il nuovo CSV
data.to_csv(modified_data_path, header=False, index=False)

print(f"CSV modificato salvato in {modified_data_path}")
