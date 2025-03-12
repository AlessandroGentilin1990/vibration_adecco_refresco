import requests
import matplotlib.pyplot as plt

# URL dell'API
BASE_URL = "https://gentilin.pythonanywhere.com/device1"

# Invia la richiesta GET all'endpoint per ottenere i dati
response_get = requests.get(BASE_URL)

# Controlla se la risposta è stata positiva (status code 200)
if response_get.status_code == 200:
    # Estrai i dati JSON dalla risposta
    data_received = response_get.json()

    # Stampa i dati ricevuti
    print("Dati ricevuti dall'API:")
    print(data_received)

    # Conta il numero di elementi nell'array
    number_of_elements = len(data_received)
    print(f"Numero di elementi nell'array: {number_of_elements}")

    # Dividi i primi 900 elementi in 3 array (x, y, z)
    x = data_received[0:300]
    y = data_received[300:600]
    z = data_received[600:900]

    # Creazione dei subplot per visualizzare i segnali x, y, z
    fig, axs = plt.subplots(3, 1, figsize=(10, 6))

    # Plot per x
    axs[0].plot(x)
    axs[0].set_title('Segnale x (Elementi 1-300)')
    axs[0].set_xlabel('Indice')
    axs[0].set_ylabel('Valore')

    # Plot per y
    axs[1].plot(y)
    axs[1].set_title('Segnale y (Elementi 301-600)')
    axs[1].set_xlabel('Indice')
    axs[1].set_ylabel('Valore')

    # Plot per z
    axs[2].plot(z)
    axs[2].set_title('Segnale z (Elementi 601-900)')
    axs[2].set_xlabel('Indice')
    axs[2].set_ylabel('Valore')

    # Mostra i grafici
    plt.tight_layout()
    plt.show()

else:
    print(f"Errore nella richiesta GET: {response_get.status_code}")
    print(response_get.json())
