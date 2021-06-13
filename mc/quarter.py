# -*- coding: utf-8 -*-
"""Copy of data_preprocessing_template.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ryZD7fZfvTa_7I_TcbhvZcPDD1ir4qm3

# Customer Segmentation

## Importing the libraries
"""

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

"""## Importing the dataset and Selecting R, F, M Values"""

dataset = pd.read_csv('./mc/sales_data_sample.csv')
columns = dataset.columns.values

#print(columns)
rfm_list = []
R = 'MONTH_ID' #input("Select R Value = ")
rfm_list.append(R)
R_Index = columns.tolist().index(R)
F = 'TRANSACTION COUNT' #input("Select F Value = ")
rfm_list.append(F)
F_Index = columns.tolist().index(F)
M = 'PRICE'  #input("Select M Value = ")
rfm_list.append(M)
M_Index = columns.tolist().index(M)

# rfm_list

"""## Preprocessng

"""

# Check if any entry NaN
def hasNoNaN():
  return (dataset[[R, F, M]].isna().sum() <= 0).all

def preProcessData():

  # Check for NaN Values in the dataset
  if hasNoNaN():
    # print('No NaN')
    return


  # Encode Non Numerical Values to Numerical if any present
  for attribute in rfm_list:
    if dataset[[attribute]].dtypes.all == np.object:
      labelEncoder = LabelEncoder()
      labelEncoder.fit(dataset[[attribute]])
      dataset[[attribute]] = labelEncoder.transform(dataset[[attribute]])

  # Replace NaN Values with mean value of respective columns
  dataset[[R, F, M]].fillna(dataset[[R, F, M]].mean(), inplace = True)

# preProcessData()
# dataset[[R, F, M]].head()

"""## Split Into Time Frames"""

quarters = []
for year in dataset['YEAR_ID'].unique():
  temp = dataset[dataset['YEAR_ID'] == year]
  for quarter in temp['QTR_ID'].unique():
    qtr = temp[temp['QTR_ID'] == quarter]
    quarters.append(qtr)

# quarters

# Split dataset into Training and Test Set
X_train, X_test = train_test_split(quarters, test_size = 0.2, random_state = 0)
# print("Test = ", X_test)
# print("Train = ",  X_train)

"""## Normalizing Data"""

# Scale the data to transform it into values between 0 and 1
def normalize(data):
  scaler = MinMaxScaler()
  scaler.fit(data)
  transform = scaler.transform(data)
  return transform
  
# normalize(X_train[0])

"""## Elbow Method"""

#pip install kneed
from kneed import KneeLocator

# Elbow Method to find optimum number of clusters
def optimumClusters(data):
  error = []
  k_range = range(1, 10)
  for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    error.append(kmeans.inertia_)
  
  kn = KneeLocator(k_range, error, curve='convex', direction='decreasing')
  '''plt.xlabel('K')
  plt.ylabel('Sum of Squared Error')
  plt.plot(k_range, error)
  plt.show()'''
  return kn.knee

# optimumClusters(X_train[0])

"""## Clustering The Data

"""

y_predicted = []

quarters = []
for year in dataset['YEAR_ID'].unique():
  temp = dataset[dataset['YEAR_ID'] == year]
  for quarter in temp['QTR_ID'].unique():
    qtr = temp[temp['QTR_ID'] == quarter]
    quarters.append(qtr)

# Retrieve Saved Model

import random

k_values = []
for qtr in quarters:
  data = qtr.iloc[:, [R_Index, F_Index, M_Index]].values
  normalized_qtr = normalize(data)
  cluster_count = optimumClusters(normalized_qtr)
  k_values.append(cluster_count)

km = KMeans(n_clusters=min(k_values), init='k-means++', max_iter=600)

startid=0
for qtr in quarters:
  ids=range(startid,startid+len(qtr))
  data = qtr.iloc[:, [R_Index, F_Index, M_Index]].values
  normalized_qtr = normalize(data)
  km = km.fit(normalized_qtr)

  # retrievedModel = retrievedModel.fit()
  clusters = km.predict(normalized_qtr)
  qtr['Clusters'] = clusters
  qtr['id']=ids
  startid=len(qtr)
  y_predicted.append(clusters)

# quarters

"""## Save Quarter Data"""

for qtr in quarters:
  qtr_name = qtr['QTR_ID'].unique()[0]
  year_name = qtr['YEAR_ID'].unique()[0]
  name = f"{year_name}-{qtr_name}"
  json = qtr.to_csv(f"./mc/{name}.csv")

"""## Plot Clustered Data

"""

''' for qtr in y_predicted:
  datasetArray = []
  index = []
  for i in np.unique(qtr):
    index.append(f"Cluster {i}")
    datasetArray.append(len(qtr[qtr== i]))
  
  fig = plt.figure()
  ax = fig.add_axes([0,0,1,1])
  ax.bar(index, datasetArray)
  plt.show() '''

for i in range(min(k_values)):
  x_axis = []
  y_axis = []
  for qtr in quarters:
    qtr_name = qtr['QTR_ID'].unique()[0]
    year_name = qtr['YEAR_ID'].unique()[0]
    name = f"{year_name}-{qtr_name}"
    x_axis.append(name)
    y_axis.append(len(qtr[qtr['Clusters'] == i]))
    
  '''plt.plot(x_axis, y_axis, label=f"Cluster {i}")

plt.legend()
plt.show()'''

"""## Quarter Details Request"""

import json
result = []
for qtr in quarters:
  year = str(qtr['YEAR_ID'].unique()[0])
  qtr_number = str(qtr['QTR_ID'].unique()[0])
  rows = len(qtr)
  obj = {
      'date' : f"{year}-{qtr_number}",
      'rows' : rows
  }
  result.append(obj)

json_array = json.dumps(result)
print(json_array)

"""## Cluster Graph Request
### Paramenters - [Year, Quarter Number]
"""
'''
import json

result = []
year = '2003'
qtr_name = '1'
name = f"{year}-{qtr_name}.csv"
qtr = pd.read_csv(name)

cluster_size_index = qtr.columns.values.tolist().index('Clusters')
for cluster in qtr['Clusters'].unique():
  sub_data = qtr[qtr['Clusters'] == cluster].values
  obj = {
    'cluster name' : f"Cluster {cluster}",
    'clusterSize' : len(sub_data),
    'year' : year,
    'quarter' : qtr_name
  }
  result.append(obj)

json_array = json.dumps(result)
print (json_array)

"""## Trends Request"""

import json
result = []
for qtr in quarters:
  qtr_name = str(qtr['QTR_ID'].unique()[0])
  year_name = str(qtr['YEAR_ID'].unique()[0])
  for cluster in qtr['Clusters'].unique():
    sub_data = qtr[qtr['Clusters'] == cluster].values
    obj = {
      'cluster name' : f"Cluster {cluster}",
      'clusterSize' : len(sub_data),
      'year' : year_name,
      'quarter' : qtr_name
    }
    result.append(obj)

json_array = json.dumps(result)
print(json_array) '''