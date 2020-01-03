import numpy as np
from KNNClassifier import KNNClassifier
import matplotlib.pyplot as plt
data = np.loadtxt(open("lab4_code\Task1\Lab4Data.csv", "rb"),
                  delimiter=";", skiprows=1)

scores = []
# Generate the K-range, always have an odd K to avoid ties

#======== MATPLOT SETTINGS ===========
kRange = np.arange(1, 50, 2)
legend = ["KNN"]
font = {'weight': 'bold',
        'size': 22}
plt.rc('font', **font)
plt.style.use('dark_background')

maxAccuracy = {"round": 0, "accuracy": 0}
for k in kRange:
    knnClassifier = KNNClassifier(data, k, "euclidean")
    score = knnClassifier.analyzeData(printStats=True) / 100
    scores.append(score)

    if score > maxAccuracy["accuracy"]:
        maxAccuracy["round"] = k
        maxAccuracy["accuracy"] = score
    print("K-value:{}".format(k))

legend[0] += " Max accuracy:{} K:{}".format(maxAccuracy["accuracy"],maxAccuracy["round"])
plt.plot(kRange, scores, 'go:')
plt.legend(legend)


plt.xlabel("K-Value")
plt.ylabel("Accuracy")
plt.show()
