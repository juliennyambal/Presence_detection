# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:59:59 2020

@author: julien.nyambal
"""

from tpot import TPOTClassifier
import pandas as pd
from sklearn.utils import shuffle

data_train = pd.read_csv("Dataset/datatraining.txt")
data_test_1 = pd.read_csv("Dataset/datatest.txt")
data_test_2 = pd.read_csv("Dataset/datatest2.txt")

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

pipeline_optimizer = TPOTClassifier(verbosity=2, 
      scoring='accuracy', 
      random_state=32, 
      periodic_checkpoint_folder='tpot_results.txt', 
      n_jobs=-1, 
      generations=10, 
      population_size=20,
      early_stop=5)

pipeline_optimizer.fit(X_train, y_train)
print(pipeline_optimizer.score(X_test, y_test))
pipeline_optimizer.export('tpot_exported_pipeline.py')