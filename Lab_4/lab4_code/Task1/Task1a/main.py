import numpy as np
from KNNClassifier import KNNClassifier
import matplotlib.pyplot as plt
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"), delimiter=";", skiprows=1)

resultingAccuracys = []
#Generate the K-range, always have an odd K to avoid ties
kRange = np.arange(1,5,2)
print (kRange)
for k in kRange:
    knnClassifier = KNNClassifier(data,k)
    resultingAccuracys.append(knnClassifier.analyzeData(printStats=True))
    print("K-value:{}".format(k))

plt.plot(kRange,resultingAccuracys,'go:')
plt.xticks(np.arange(min(kRange), max(kRange)+1, 4.0))

plt.title("KNN-Classifier")
plt.xlabel("K-Value")
plt.ylabel("Accuracy in %")
plt.show()
