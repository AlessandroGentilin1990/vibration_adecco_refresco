import joblib
import numpy as np
import requests
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import messagebox

# Carica il modello salvato
model_path = 'c:\\device1\\svm_model.pkl'
svm_model = joblib.load(model_path)

# Crea un oggetto StandardScaler per normalizzare i dati (deve essere lo stesso usato nel training)
scaler = StandardScaler()

# BASE_URL per la richiesta all'API
BASE_URL = "https://gentilin.pythonanywhere.com/device1"

# Percorso del file dove salvare la predizione
prediction_path = 'c:\\device1\\prediction.txt'

# Funzione per calcolare le 87 caratteristiche statistiche
def calculate_features(signal):
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

# Funzione per fare previsioni con il modello SVM
def predict_new_data(features):
    # Normalizza le nuove caratteristiche (assicurati che siano nello stesso formato di X_train)
    features_scaled = scaler.fit_transform([features])

    # Fai una previsione
    prediction = svm_model.predict(features_scaled)
    return prediction[0]

# Funzione per eseguire la richiesta GET, processare i dati e fare la previsione
def fetch_and_predict():
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

        # Unisci tutte le features in un unico array
        all_features = x_features + y_features + z_features

        # Fai una previsione
        prediction = predict_new_data(all_features)
        print(f"Prediction: {prediction}")

        # Scrivi la predizione nel file di testo
        # Scrivi solo la predizione nel file di testo
        with open(prediction_path, 'w') as file:
            file.write(f"{prediction}\n")  # Scrive solo il valore della predizione

        # Esegui la predizione
        messagebox.showinfo("Stato", f"Prediction: {prediction}")


    else:
        print(f"Errore nella richiesta GET: {response_get.status_code}")
        print(response_get.json())

# Esegui la funzione per fare la previsione
fetch_and_predict()


# import joblib
# import numpy as np
# from sklearn.preprocessing import StandardScaler
#
# # 1. Carica il modello salvato
# model_path = 'c:\\device1\\svm_model.pkl'
# svm_model = joblib.load(model_path)
#
# # 2. Crea un oggetto StandardScaler per normalizzare i dati (deve essere lo stesso usato nel training)
# scaler = StandardScaler()
#
# # Funzione per fare previsioni con il modello
# def predict_new_data(features):
#     # Normalizza le nuove caratteristiche (assicurati che siano nello stesso formato di X_train)
#     features_scaled = scaler.fit_transform([features])
#
#     # Fai una previsione
#     prediction = svm_model.predict(features_scaled)
#     return prediction[0]
#
# # Esempio di utilizzo: previsioni per nuove caratteristiche
# new_features = [0.9444800000000002, 0.04008236852615706, 0.832, 1.04, 0.944, 0.20800000000000007,
#                 0.001606596266666666, 0.928, 0.944, 0.976, 0.8936490666666664, 283.34400000000005,
#                 0.9444800000000002, 0.00010702341137123755, 13.727999999999996, -0.19200000000000006,
#                 0.16000000000000003, 0.045913043478260855, 0.0034059015894676785, 142.3586133333332,
#                 0.0, 1.0, 0.0, 0.4066666666666667, 0.5933333333333334, 1.0, 0.0, 0.058360102719817744,
#                 0.045913043478260855, 16.184853333333333, 0.05785238533447785, 16.016, 16.4, 16.176,
#                 0.38400000000000034, 0.0033468984888889077, 16.16, 16.176, 16.208, 261.95282432, 4855.456,
#                 16.184853333333333, -5.351170568561283e-05, 17.93600000000005, -0.3039999999999985,
#                 0.240000000000002, 0.059986622073578764, 0.006629455330477321, 2436.0132799999997,
#                 0.0, 1.0, 0.0, 0.4766666666666667, 0.5233333333333333, 1.0, 0.0, 0.081421467258195,
#                 0.059986622073578764, 3.3532561983471076, 0.049315400663202856, 3.184, 3.472, 3.36,
#                 0.2879999999999998, 0.0024320087425722284, 3.328, 3.36, 3.392, 11.246759140495866,
#                 405.744, 3.3532561983471076, -0.0005333333333333338, 6.464000000000001, -0.1599999999999997,
#                 0.19199999999999973, 0.05386666666666668, 0.004428515555555555, 204.7662809917355,
#                 0.0, 1.0, 0.0, 0.5619834710743802, 0.4380165289256198, 1.0, 0.0, 0.0665470927656164,
#                 0.05386666666666668]
#
# prediction = predict_new_data(new_features)
# print(f"Prediction: {prediction}")
