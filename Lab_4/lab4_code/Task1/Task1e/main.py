import numpy as np
from KNNRegression import KNNRegression
import matplotlib.pyplot as plt
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"), delimiter=";", skiprows=1)

resultingAccuracys = []
#Generate the K-range, always have an odd K to avoid ties
kRange = np.arange(1,50,2)


font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font',**font)
plt.style.use('dark_background')


maxAccuracy = {"K":0,"accuracy":0}

for k in kRange:
    knnRegressor = KNNRegression(data,7,k,'euclidean')
    resultingAccuracy = knnRegressor.analyzeData(printStats=True)
    resultingAccuracys.append(resultingAccuracy)
    print("K-value:{}".format(k))
    if resultingAccuracy > maxAccuracy["accuracy"]:
        maxAccuracy["K"] = k
        maxAccuracy["accuracy"] = resultingAccuracy 

plt.plot(kRange,resultingAccuracys,'go:')
plt.xticks(np.arange(min(kRange), max(kRange)+1, 4.0))

legend = ["Max accuracy:{}, K:{}".format(round(maxAccuracy["accuracy"],4), maxAccuracy["K"])]


plt.xlabel("K-Value")
plt.ylabel("Accuracy")
plt.legend(legend)
plt.show()
