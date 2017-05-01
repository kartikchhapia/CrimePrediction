import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
import numpy as np




dataLocation = "../data/TestDataSet/crime_landmarks_census.csv"

allData = pd.read_csv(dataLocation)


# Shuffle the data
allData = allData.sample(frac=1)


# All training data
allDataLandmarks = allData.iloc[:, 7:19]

# ALl predictors
violationGoldStandard    =  allData.iloc[:, 3:4]
felonyGoldStandard       =  allData.iloc[:, 4:5]
misdemeanorGoldStandard  =  allData.iloc[:, 5:6]


allData['sum'] = allData["FELONY CRIMES"] + allData["MISDEMEANOR CRIMES"] + allData["VIOLATION CRIMES"]


#print "crimes sum is ",   allData['sum']         
                

crimeThreshold = 0          
preditionColumn = allData['sum']
crimeThresholdMask = preditionColumn > crimeThreshold

allDataLandmarks = allDataLandmarks[crimeThresholdMask]
preditionColumn  = preditionColumn[crimeThresholdMask]

print "No of data points ", allDataLandmarks.shape[0]

columns = allDataLandmarks.columns



mae_scores = list()


############ SPLIT DATA INTO TRAIN AND TEST   ####################
X_train, X_test, y_train, y_test = train_test_split(allDataLandmarks, preditionColumn, test_size=0.3, random_state=0)



############ LINEAR REGRESSION  ################3


lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print "For Linear Regression", mean_absolute_error(y_test, y_pred)
mae_scores.append(mean_absolute_error(y_test, y_pred))


############  LASSO #################

"""
lasso = linear_model.Lasso()
lasso.fit(X_train, y_train)
y_pred = lasso.predict(X_test)
print "For Lasso", mean_absolute_error(y_test, y_pred)
mae_scores.append(mean_absolute_error(y_test, y_pred))
"""


############ SVM ##################

svr = svm.SVR(C = 2)
svr.fit(X_train, y_train)
y_pred = svr.predict(X_test)
print "For SVM ", mean_absolute_error(y_test, y_pred)
mae_scores.append(mean_absolute_error(y_test, y_pred))


############   RANDOM FOREST   ###############################
rf = RandomForestClassifier(n_estimators = 100, min_samples_split = 5)
#print (cross_val_score(rf, X_train, y_train, scoring = 'neg_mean_absolute_error', cv=10)).mean() 
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
print "For Random Forest", mean_absolute_error(y_test, y_pred)
mae_scores.append(mean_absolute_error(y_test, y_pred))





############ GET FEATURE IMPORTANCE WITH RANDOM FOREST  ##########################


importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X_train.shape[1]):
    print "f is ", f
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest

feature_importance_column_names = list()
for i in indices:
    feature_importance_column_names.append(columns[i])





####### PLOT FEATURE IMPORTANCE    ###########################
"""
plt.title("Feature importances")
plt.figure(figsize=(4,2))
plt.bar(range(X_train.shape[1]), importances[indices],
       color="r",  align="center", width = 0.4)
plt.xticks(range(X_train.shape[1]), feature_importance_column_names)
plt.xlim([-1, X_train.shape[1]])

"""



###########  PLOT MEAN ABSOLUTE ERROR WITH DIFFERENT MODELS   ##########################
objects = ('Linear Regression', 'Lasso', 'SVM', 'Random Forest')
objects = ('Linear Regression', 'SVM', 'Random Forest')

y_pos = np.arange(len(objects))
performance = mae_scores
plt.figure(figsize=(4,2)) 
plt.bar(y_pos, performance, align='center', alpha=0.5, color = 'r')
plt.xticks(y_pos, objects)
plt.ylabel('Mean Absolute Error')
 
plt.show()




#######   FEATURE SELECTION ##########################

"""

print "Using 100 estimators and 5 samples split"

for k in range(1,13):
     
    
    skb = SelectKBest(chi2, k=k)
    X_train_new = skb.fit_transform(X_train, y_train)

    #print "allDataLandmarks_new", allDataLandmarks_new

    score = (cross_val_score(rf, X_train_new, y_train, cv= 10, scoring='neg_mean_absolute_error').mean()) 
    print "For k: ", k ,"cross validation score is ", score
    
    rf.fit(X_train_new, y_train)
    
    X_test_new = skb.transform(X_test)
    
    y_pred = rf.predict(X_test_new)

    test_score = mean_absolute_error(y_test, y_pred)
    
    print "test score is ", test_score
    
    
"""

    


    
    
    


    
   






