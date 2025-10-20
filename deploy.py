from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Carrega o modelo
model = pickle.load(open('savedmodel.sav', 'rb'))

@app.route('/')
def home():
    return render_template('Index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(request.form.get(key)) for key in [
        'ph', 'hardness', 'solids', 'chloramines', 'sulfate',
        'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity'
    ]]

    final_features = [np.array(features)]

    prediction = model.predict(final_features)[0]

    if prediction == 1:
        output = "Água Potável"
    else:
        output = "Água Não Potável"

    return render_template('Index.html', result=output)

if __name__ == '__main__':
    app.run(debug=True)