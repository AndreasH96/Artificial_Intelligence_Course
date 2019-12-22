import numpy as np
from KNNClassifier import KNNClassifier
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"), delimiter=";", skiprows=1)

knnClassifier = KNNClassifier(data)
knnClassifier.analyzeData(plot = True)
