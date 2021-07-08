import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import *
from sklearn.linear_model import *
from sklearn.discriminant_analysis import *
from sklearn.neighbors import *
from sklearn.tree import *
from sklearn.naive_bayes import *
from sklearn.svm import *
from sklearn.preprocessing import LabelEncoder
import keras.utils
import tensorflow

data = pd.read_csv("nflstats.csv")
array = data.values
x = array[:, 3:232]
rawWins = array[:, 2]
labelEncoder = LabelEncoder()
y = labelEncoder.fit_transform(rawWins) # Assign each win total to a unique number

# Print which win total is associated with each number
temp = []
for i in range(len(y)):
    if y[i] not in temp:
        temp.append(y[i])
        print(y[i], "=", rawWins[i])

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)
models = [] # Append various models to check
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(("LDA", LinearDiscriminantAnalysis()))
models.append(("KNN", KNeighborsClassifier()))
models.append(("CART", DecisionTreeClassifier()))
models.append(("NB", GaussianNB()))
models.append(("SVM", SVC(gamma="auto")))
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True) # Split the data into 10 random groupings so all models have the same data
    cvResults = cross_val_score(model, xTrain, yTrain, cv=kfold, scoring="accuracy") # Score each model
    results.append(cvResults)
    names.append(name)
    print(name, cvResults.mean(), cvResults.std()) # Print the results of each model
# Plot the final results
plt.boxplot(results, labels=names)
plt.title('Algorithm Comparison')
plt.show()
