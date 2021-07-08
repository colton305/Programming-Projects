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
import pickle

data = pd.read_csv("nflstats.csv")
array = data.values
x = array[:, 3:232]
gang = array[:, 2]
labelEncoder = LabelEncoder()
y = labelEncoder.fit_transform(gang)

dank = []
for i in range(len(y)):
    if y[i] not in dank:
        dank.append(y[i])
        print(y[i], "=", gang[i])

realData = pd.read_csv("data.csv")
array2 = realData.values
x2 = array2[:, 2:230]
model = pickle.load(open("14win(12.5).sav ", 'rb'))
results = model.predict(x2)
print(results)

'''xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(("LDA", LinearDiscriminantAnalysis()))
models.append(("KNN", KNeighborsClassifier()))
models.append(("CART", DecisionTreeClassifier()))
models.append(("NB", GaussianNB()))
models.append(("SVM", SVC(gamma="auto")))'''

'''best = 0
saved = 0
for i in range(1000):
    model = GaussianNB()
    model.fit(xTrain, yTrain)
    predictions = model.predict(xTest)
    if accuracy_score(yTest, predictions) > best:
        best = accuracy_score(yTest, predictions)
        saved = predictions
        pickle.dump(model, open("unknown_bias.sav", 'wb'))

print(confusion_matrix(yTest, saved))
print(classification_report(yTest, saved))
print(accuracy_score(yTest, saved))'''

'''reg = LinearRegression()
reg.fit(xTrain, yTrain)
print('Coefficients: \n', reg.coef_)
print('Variance score: {}'.format(reg.score(xTest, yTest)))
plt.style.use('fivethirtyeight')
plt.scatter(reg.predict(xTrain), reg.predict(xTrain) - yTrain,
   color = "green", s = 10, label = 'Train data')
plt.scatter(reg.predict(xTest), reg.predict(xTest) - yTest)
plt.hlines(y = 0, xmin = 0, xmax = 50, linewidth = 2)
plt.legend(loc = 'upper right')
plt.title("Residual errors")
plt.show()'''

'''results = []
names = []
iterations = 0
for name, model in models:
    print(iterations)
    kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
    cvResults = cross_val_score(model, xTrain, yTrain, cv=kfold, scoring="accuracy")
    results.append(cvResults)
    names.append(name)
    print(name, cvResults.mean(), cvResults.std())
    iterations += 1
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()'''
