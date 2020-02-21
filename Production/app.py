import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__, template_folder='')
model = pickle.load(open('./Models/Random Forest.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

def decypher_activity(x):
    labels_activity = ["Not Occupied", "Occupied"]
    return labels_activity[x]

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    predictions = model.predict(final_features)
    predict_proba = model.predict_proba(final_features)
    print("Features: %s " % final_features)
    # Read the results like this [Not Occupied, Occupied]
    print("(Read the results like this [Not Occupied, Occupied]) --> Predictions probabilities: %s"  % predict_proba)
    print ("Predictions: %s" % predictions)
    predicted_class = int(predictions)
    print(decypher_activity(predicted_class))
    output = decypher_activity(predicted_class)

    return render_template('index.html', prediction_text='The room should be <b>{}</b> right about now. <br> Probablity of the room being empty: {}.'.format(output,predict_proba[0][0]))

@app.route('/results',methods=['POST'])
def results():
    data = request.get_json(force=True)
    features = [np.array(list(data.values()))]
    prediction = model.predict(features)
    predict_proba = model.predict_proba(features)
    output = prediction[0]
    return {'status':output.item(),'emptyness_proba':predict_proba[0][0],'model':model.__class__.__name__}

if __name__ == "__main__":
    app.run(debug=True)