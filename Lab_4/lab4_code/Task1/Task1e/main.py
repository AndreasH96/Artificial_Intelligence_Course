import numpy as np
from KNNRegression import KNNRegression
import matplotlib.pyplot as plt
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"), delimiter=";", skiprows=1)

resultingAccuracys = []
#Generate the K-range, always have an odd K to avoid ties
kRange = np.arange(1,10,2)


params = {'legend.fontsize': 16,
          'legend.handlelength': 2}
plt.rcParams.update(params) 
plt.style.use('dark_background')

maxAccuracy = {"K":0,"accuracy":0}
for k in kRange:
    
    knnRegressor = KNNRegression(data,7,k,'euclidean')
    resultingError = knnRegressor.analyzeData(printStats=True)
    resultingAccuracys.append(resultingError)
    print("K-value:{}".format(k))
    if resultingError > maxAccuracy["accuracy"]:
        maxAccuracy["K"] = k
        maxAccuracy["accuracy"] = resultingError 

plt.plot(kRange,resultingAccuracys,'go:')
plt.xticks(np.arange(min(kRange), max(kRange)+1, 4.0))

legend = ["Max accuracy:{}, K:{}".format(round(maxAccuracy["accuracy"],4), maxAccuracy["K"])]


plt.title("KNN-Regression")
plt.xlabel("K-Value")
plt.ylabel("Accuracy")
plt.legend(legend)
plt.show()
