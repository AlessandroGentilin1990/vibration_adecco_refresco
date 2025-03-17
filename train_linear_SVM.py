import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import joblib
import tkinter as tk
from tkinter import messagebox

# 1. Carica i dati CSV
data_path = "c:\\device1\\data.csv"  # Sostituisci con il percorso del tuo CSV
data = pd.read_csv(data_path, header=None)

# 2. Separa il target dalle caratteristiche
X = data.iloc[:, 1:].values  # Caratteristiche (tutti i valori tranne il primo)
y = data.iloc[:, 0].values  # Target (primo valore in ogni riga)

# 3. Pre-elabora i dati (opzionale ma consigliato)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Normalizza le caratteristiche

# 4. Allena il modello SVM lineare utilizzando l'intero dataset
svm_model = svm.SVC(kernel='linear', random_state=42)
svm_model.fit(X_scaled, y)

# 5. Salva il modello addestrato
model_path = 'c:\\device1\\svm_model.pkl'
joblib.dump(svm_model, model_path)

print(f"Modello addestrato e salvato in {model_path}")
messagebox.showinfo("Stato", "Modello addestrato e aggiornato.")

# import pandas as pd
# from sklearn import svm
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# import joblib
#
# # 1. Carica i dati CSV
# data_path = "c:\\device1\\data.csv"  # Sostituisci con il percorso del tuo CSV
# data = pd.read_csv(data_path, header=None)
#
# # 2. Separa il target dalle caratteristiche
# X = data.iloc[:, 1:].values  # Caratteristiche (tutti i valori tranne il primo)
# y = data.iloc[:, 0].values  # Target (primo valore in ogni riga)
#
# # 3. Pre-elabora i dati (opzionale ma consigliato)
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)  # Normalizza le caratteristiche
#
# # 4. Dividi i dati in set di addestramento e test (opzionale, ma utile per valutare il modello)
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
#
# # 5. Allena il modello SVM lineare
# svm_model = svm.SVC(kernel='linear', random_state=42)
# svm_model.fit(X_train, y_train)
#
# # 6. Valutazione del modello (opzionale)
# y_pred = svm_model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy * 100:.2f}%")
#
# # 7. Salva il modello addestrato
# model_path = 'c:\\device1\\svm_model.pkl'
# joblib.dump(svm_model, model_path)
#
#
# # 8. Funzione per fare previsioni con il modello salvato
# def predict_new_data(features):
#     # Carica il modello salvato
#     model = joblib.load(model_path)
#
#     # Normalizza le nuove caratteristiche (assicurati che siano nello stesso formato di X_train)
#     features_scaled = scaler.transform([features])
#
#     # Fai una previsione
#     prediction = model.predict(features_scaled)
#     return prediction[0]
#
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
