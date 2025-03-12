from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Variabile globale per memorizzare l'ultimo numero inviato
ultimo_numero = None

# HTML con layout grafico e refresh automatico ogni 1 secondo
html_template = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitoraggio Numero</title>
    <meta http-equiv="refresh" content="1"> <!-- Aggiunge il refresh automatico ogni 1 secondo -->
    <style>
        .button {
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .verde {
            background-color: green;
        }
        .rosso {
            background-color: red;
        }
        .blu {
            background-color: blue;
        }
    </style>
</head>
<body>
    <h1>Monitoraggio dell'ultimo numero inviato</h1>
    <p>Il bottone sotto cambia colore in base al numero inviato all'API.</p>
    <button class="button {{ colore }}">Numero inviato: {{ numero }}</button>
</body>
</html>
'''

# Route per gestire GET e POST su /numero
@app.route('/numero', methods=['GET', 'POST'])
def handle_number():
    global ultimo_numero

    if request.method == 'POST':
        # Riceve il numero dal body della richiesta POST (formato JSON)
        data = request.get_json()
        numero = data.get('numero')

        # Verifica se il numero è valido
        if numero is None or not isinstance(numero, (int, float)):
            return jsonify({'errore': 'Devi inviare un numero valido'}), 400

        # Salva il numero nella variabile globale
        ultimo_numero = numero

        # Risposta con il numero ricevuto
        # return jsonify({'messaggio': f'Hai inviato il numero {numero}'}), 200
        return jsonify({'numero': numero}), 200


    elif request.method == 'GET':
        # Restituisce l'ultimo numero inviato
        if ultimo_numero is not None:
            return str(ultimo_numero), 200  # Restituisce solo il numero come stringa
        else:
            return jsonify({'errore': 'Nessun numero inviato ancora'}), 400

# Route per la pagina di monitoraggio
@app.route('/monitoraggio')
def monitoraggio():
    global ultimo_numero

    # Determina il colore in base al numero inviato
    if ultimo_numero == 1:
        colore = "verde"
    elif ultimo_numero == 0:
        colore = "rosso"
    else:
        colore = "blu"

    # Renderizza la pagina HTML con il numero e il colore corretti
    return render_template_string(html_template, numero=ultimo_numero, colore=colore)

if __name__ == '__main__':
    app.run(debug=True)
