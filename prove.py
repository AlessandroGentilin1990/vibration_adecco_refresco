from flask import Flask, request, jsonify

app = Flask(__name__)

# Memorizza i dati ricevuti
data_store = {"device1": []}


@app.route('/device1', methods=['GET', 'POST'])
def device1():
    if request.method == 'POST':
        try:
            content = request.json
            if not isinstance(content, list) or not all(isinstance(i, (int, float)) for i in content):
                return jsonify({"error": "Invalid data format. Must be a list of numbers"}), 400

            data_store["device1"] = content
            return jsonify({"message": "Data stored successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Se è una richiesta GET, mostra i dati salvati
    return jsonify(data_store["device1"])


if __name__ == '__main__':
    app.run()

