from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

try:
    model = pickle.load(open('savedmodel.sav', 'rb'))
except FileNotFoundError:
    print("Erro: O arquivo 'savedmodel.sav' não foi encontrado.")
    print("Certifique-se de que ele está no mesmo diretório que 'deploy.py'.")
    exit()

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Nenhum dado JSON recebido.'}), 400

        feature_keys = [
            'ph', 'hardness', 'solids', 'chloramines', 'sulfate',
            'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity'
        ]
        
        features = [float(data[key]) for key in feature_keys]

        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        if prediction[0] == 1:
            output = "A água é potável"
        else:
            output = "A água não é potável"

        return jsonify({'prediction': output})

    except (ValueError, KeyError):
        return jsonify({'error': 'Erro: Por favor, preencha todos os campos corretamente.'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro inesperado no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)