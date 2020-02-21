# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:51:12 2020

@author: julien.nyambal
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import os
import time

from prettytable import PrettyTable
sns.set(style="ticks")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


from sklearn.utils import shuffle
from sklearn.metrics import balanced_accuracy_score, accuracy_score, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
#from imblearn.over_sampling import SMOTE # doctest: +NORMALIZE_WHITESPACE

import mlflow
import mlflow.sklearn

def eval_metrics(actual, pred):
    bacc = balanced_accuracy_score(actual, pred)
    f1 = f1_score(actual, pred, average='weighted')
    acc = accuracy_score(actual, pred)
    prec = precision_score(actual, pred, average='weighted')
    recall = recall_score(actual, pred, average='weighted')
    return bacc, f1, acc, prec, recall

def test_nulls(df):
  dataNulls = df.isnull().sum().sum()
  assert dataNulls == 0, "Nulls in engineered data."
  print('Engineered features do not contain nulls.')

def normalizeData(arr):
  stdArr = np.std(arr)
  meanArr = np.mean(arr)
  arr = (arr-meanArr)/stdArr
  return arr

data_train = pd.read_csv("Dataset/datatraining.txt")
data_test_1 = pd.read_csv("Dataset/datatest.txt")
data_test_2 = pd.read_csv("Dataset/datatest2.txt")

names = ["Nearest Neighbors", "Linear SVM", "Decision Tree", "Random Forest",
          "Neural Net", "AdaBoost","Naive Bayes", "Logistic Regression"]

classifiers = [
    KNeighborsClassifier(5),
    SVC(kernel="linear", C=0.025, probability=True),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=100, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    LogisticRegression()
    ]


non_occupied_room = data_train[data_train.Occupancy == 0][['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']]
occupied_room = data_train[data_train.Occupancy == 1][['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']]

indexes_outliers_non_occupied = non_occupied_room[non_occupied_room.Light > 0].index.values
non_occupied_room.drop(indexes_outliers_non_occupied, inplace=True)

occupied_room = occupied_room.append(data_test_2[['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']][data_test_2.Occupancy == 1],sort=True)
occupied_room = occupied_room.append(occupied_room[:1382])
zero_light_occupied = occupied_room[occupied_room.Light < 200].index.values
occupied_room.drop(zero_light_occupied, inplace=True)

non_occupied_room = shuffle(non_occupied_room)
non_occupied_room['Occupancy'] = 0
occupied_room = shuffle(occupied_room)
occupied_room['Occupancy'] = 1

data = shuffle(non_occupied_room.append(occupied_room,'sort=True'))
#X_train = data[['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']]
X_train = data[['Temperature', 'Humidity', 'Light', 'CO2']]
#X_train = normalizeData(X_train)
y_train = data.Occupancy

data_test_1 = shuffle(data_test_1[['Temperature', 'Humidity', 'Light', 'CO2', 'Occupancy']])
X_test = data_test_1.iloc[:,:-1]
#X_test = normalizeData(X_test)
y_test= data_test_1.Occupancy

#Just to chech that The Model folder exists
if 'Models' not in os.listdir():
    os.mkdir('Models')
else:
    print("Models folder already exists")

estimators_names = [""]
balanced_accuracy = ["Balanced Accuracy"]
f1_results = ["F1"]
accuracy_results = ["Accuracy"]
conf_matrices_train = ["Confusion Matrix Train"]
conf_matrices_test = ["Confusion Matrix Test"]
training_time_in_sec = ["Training time (s)"]

for i in range(len(classifiers)):
    with mlflow.start_run():
        clf = classifiers[i]
        start_training_time = time.time()
        clf.fit(X_train, y_train)
        training_time = time.time() - start_training_time
        predicted_qualities = np.clip(np.round(clf.predict(X_test)), 0, 1)
        #print(confusion_matrix(np.array(y_train), np.clip(np.round(clf.predict(X_train)), 0, 1)))
        #print(confusion_matrix(np.array(y_test), predicted_qualities))
        (bacc, f1, acc, prec, recall) = eval_metrics(np.array(y_test), predicted_qualities)
        mlflow.log_param("Model_Name", names[i])
        mlflow.log_metric("bacc", bacc)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("acc", acc)
        mlflow.log_metric("prec", f1)
        mlflow.log_metric("recall", acc)
        mlflow.sklearn.log_model(clf, names[i])
        print("End training of %s" % names[i])
        filename = 'Models/%s.pkl' % names[i]
        pickle.dump(clf, open(filename, 'wb'))
        #For drawing the resulting table having the metrics
        estimators_names.append(names[i])
        balanced_accuracy.append(bacc)
        f1_results.append(f1)
        accuracy_results.append(acc)
        training_time_in_sec.append(training_time)
        conf_matrices_train.append(confusion_matrix(np.array(y_train), 
                               np.clip(np.round(clf.predict(X_train)), 0, 1)))
        conf_matrices_test.append(confusion_matrix(np.array(y_test), predicted_qualities))
        print("------------------------------")

t = PrettyTable(estimators_names)
t.add_row(balanced_accuracy)
t.add_row(f1_results)
t.add_row(accuracy_results)
t.add_row(training_time_in_sec)
t.add_row(conf_matrices_train)
t.add_row(conf_matrices_test)
print(t)


# clf = classifiers[0]
# clf.fit(X_train, y_train)
# predicted_qualities = clf.predict(X_test)
# print(confusion_matrix(np.array(y_train), 
#                         np.clip(np.round(clf.predict(X_train)), 0, 1)))
# print(confusion_matrix(np.array(y_test), predicted_qualities))
