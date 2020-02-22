import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle, os

app = Flask(__name__, template_folder='')
models_raw = os.listdir('../Models')

#Helper function to map a single feature to all the models at once
def to_list_model(path_model):
    model = pickle.load(open(os.path.join('../Models/',path_model),'rb'))
    return model

models = list(map(to_list_model,models_raw))

@app.route('/')
def home():
    return render_template('index.html')

def decypher_activity(x):
    labels_activity = ["Not Occupied", "Occupied"]
    return labels_activity[x]

@app.route('/results',methods=['POST'])
def results():
    data = request.get_json(force=True)
    features = [np.array(list(data.values()))]

    def predict_custom(model):
        predictions = model.predict(features)
        predict_proba = model.predict_proba(features)
        return {'prediction':predictions[0],'prediction_proba':predict_proba[0][0]}

    pred = list(map(predict_custom,models))
    
    return {'AdaBoostClassifier_prediction':int(pred[0]['prediction']),
            'DecisionTreeClassifier_prediction':int(pred[1]['prediction']),
            'SVC_prediction':int(pred[2]['prediction']),
            'LogisticRegression_prediction':int(pred[3]['prediction']),
            'GaussianNB_prediction':int(pred[4]['prediction']),
            'KNeighborsClassifier_prediction':int(pred[5]['prediction']),
            'MLPClassifier_prediction':int(pred[6]['prediction']),
            'RandomForestClassifier_prediction':int(pred[7]['prediction']),
            'AdaBoostClassifier_emptuness_proba':float(pred[1]['prediction_proba']),
            'DecisionTreeClassifier_emptuness_proba':float(pred[1]['prediction_proba']),
            'SVC_emptuness_proba':float(pred[2]['prediction_proba']),
            'LogisticRegression_emptuness_proba':float(pred[3]['prediction_proba']),
            'GaussianNB_emptuness_proba':float(pred[4]['prediction_proba']),
            'KNeighborsClassifier_emptuness_proba':float(pred[5]['prediction_proba']),
            'MLPClassifier_emptuness_proba':float(pred[6]['prediction_proba']),
            'RandomForestClassifier_emptuness_proba':float(pred[7]['prediction_proba'])}


if __name__ == "__main__":
    app.run(port=5001,debug=True)