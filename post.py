import requests

# URL dell'API
BASE_URL = "https://gentilin.pythonanywhere.com/device1"

# Creazione di un array di 60 numeri (ad esempio da 0 a 59)
data_to_send = [i for i in range(60)]

# Invia la richiesta POST con l'array come JSON
response_post = requests.post(BASE_URL, json=data_to_send)

# Stampa la risposta del server
if response_post.status_code == 200:
    print("Dati inviati con successo.")
else:
    print(f"Errore nella richiesta POST: {response_post.status_code}")
    print(response_post.json())
