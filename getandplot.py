import requests
import matplotlib.pyplot as plt

# URL di destinazione
url = "https://gentilin.pythonanywhere.com/device1"

# Effettua una richiesta GET per ottenere i dati
response = requests.get(url)

# Verifica se la richiesta ha avuto successo
if response.status_code == 200:
    # Estrai il contenuto come stringa
    content = response.text

    # Rimuovi eventuali spazi vuoti extra e dividi la stringa in numeri
    numbers = content.split(',')

    # Conta il numero di elementi nella lista
    num_count = len(numbers)
    print(f"Ci sono {num_count} numeri nel contenuto.")

    # Assumiamo che il numero di elementi sia almeno 3000 (1000 per ogni segnale)
    if num_count >= 3000:
        # Pulisci i numeri da eventuali caratteri indesiderati come parentesi, spazi, e newline
        cleaned_numbers = [num.strip('[]\n') for num in numbers]  # Rimuove parentesi quadre, newline e spazi

        try:
            # Converte i numeri puliti in float
            X = [float(cleaned_numbers[i]) for i in range(1000)]
            Y = [float(cleaned_numbers[i]) for i in range(1000, 2000)]
            Z = [float(cleaned_numbers[i]) for i in range(2000, 3000)]

            # Crea un grafico con i tre segnali
            plt.figure(figsize=(10, 6))
            plt.plot(X, label="Segnale X", color='blue')
            plt.plot(Y, label="Segnale Y", color='green')
            plt.plot(Z, label="Segnale Z", color='red')

            # Aggiungi titolo e etichette
            plt.title('Plottaggio dei segnali X, Y e Z')
            plt.xlabel('Indice')
            plt.ylabel('Valore')

            # Aggiungi una legenda
            plt.legend()

            # Mostra il grafico
            plt.show()

        except ValueError as e:
            print(f"Errore di conversione: {e}")
    else:
        print("I dati non contengono almeno 3000 numeri.")
else:
    print(f"Errore nella richiesta: {response.status_code}")
