# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:51:12 2020

@author: julien.nyambal
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
sns.set(style="ticks")

import matplotlib.pyplot as plt

data_train = pd.read_csv("Dataset/datatraining.txt")
data_test_1 = pd.read_csv("Dataset/datatest.txt")
data_test_2 = pd.read_csv("Dataset/datatest2.txt")

#create Plots directory
if 'Plots' not in os.listdir():
    os.mkdir('Plots')
else:
    print("Plots folder already exists")

columns = ["Temperature","Humidity","Light","CO2","HumidityRatio","Occupancy"]
dpi = 600

#original train data count
ax = data_train.Occupancy.value_counts().plot(kind='bar')
plt.title("Original Train Data Distribution")
ax.set_xticklabels(["Not Occupied", "Occupied"])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("Plots/Original Train Data Count.png", dpi=dpi)

#original Test 1 data count
ax = data_test_1.Occupancy.value_counts().plot(kind='bar')
plt.title("Original Test 1 Data Distribution")
ax.set_xticklabels(["Not Occupied", "Occupied"])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("Plots/Original Test 1 Data Count.png", dpi=dpi)

#original Test 2 data count
ax = data_test_2.Occupancy.value_counts().plot(kind='bar')
plt.title("Original Test 2 Data Distribution")
ax.set_xticklabels(["Not Occupied", "Occupied"])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("Plots/Original Test 2 Data Count.png", dpi=dpi)

data_train[columns].hist()
plt.tight_layout(pad=1, w_pad=1, h_pad=1.0)
plt.title("All histograms Train")
plt.tight_layout()
plt.savefig("Plots/All_histograms_train.png", dpi=dpi)

data_test_1[columns].hist()
plt.tight_layout(pad=1, w_pad=1, h_pad=1.0)
plt.title("All histograms Test 1")
plt.tight_layout()
plt.savefig("Plots/All_histograms_test_1.png", dpi=dpi)

data_test_2[columns].hist()
plt.tight_layout(pad=1, w_pad=1, h_pad=1.0)
plt.title("All histograms Test 2")
plt.savefig("Plots/All_histograms_test_2.png", dpi=dpi)

ax = sns.pairplot(data_train[columns], hue='Occupancy')
# replace labels
new_labels = ["Not Occupied", "Occupied"]
for t, l in zip(ax._legend.texts, new_labels): t.set_text(l)
#Move the legend a bit to the right
ax.fig.get_children()[-1].set_bbox_to_anchor((1.05, 0.5, 0, 0))
plt.savefig("Plots/Pair_plot_Train.png", dpi=dpi)

sns.pairplot(data_test_1[columns], hue='Occupancy')
for t, l in zip(ax._legend.texts, new_labels): t.set_text(l)
#Move the legend a bit to the right
ax.fig.get_children()[-1].set_bbox_to_anchor((1.05, 0.5, 0, 0))
plt.savefig("Plots/Pair_plot_Test1.png", dpi=dpi)

sns.pairplot(data_test_2[columns], hue='Occupancy')
for t, l in zip(ax._legend.texts, new_labels): t.set_text(l)
#Move the legend a bit to the right
ax.fig.get_children()[-1].set_bbox_to_anchor((1.05, 0.5, 0, 0))
plt.savefig("Plots/Pair_plot_Test2.png", dpi=dpi)