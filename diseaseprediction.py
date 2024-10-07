from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import csv,numpy as np,pandas as pd
import os
from sklearn import metrics

data = pd.read_csv("templates\Training.csv")
df = pd.DataFrame(data)
x = df.drop("prognosis",axis=1)
y = df['prognosis']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.978, random_state=0)

#DESCISION TREE
#print ("DecisionTree")
dt = DecisionTreeClassifier()
clf_dt=dt.fit(x_train,y_train)
Y1=clf_dt.score(x_test,y_test)
print ("Decision Tree Acurracy: ", clf_dt.score(x_test,y_test))

# with open('templates/Testing.csv', newline='') as f:
#         reader = csv.reader(f)
#         symptoms = next(reader)
#         symptoms = symptoms[:len(symptoms)-1]

#NAIVE BAYES
# Bayes’ Theorem
# Bayes’ Theorem finds the probability of an event occurring given the probability of another event that has already occurred. Bayes’ theorem is stated mathematically as the following equation:


# where A and B are events and P(B) ≠ 0
# P(A∣B)= P(B∣A)P(A)/P(B)

# Basically, we are trying to find probability of event A, given the event B is true. Event B is also termed as evidence.
# P(A) is the priori of A (the prior probability, i.e. Probability of event before evidence is seen). The evidence is an attribute value of an unknown instance(here, it is event B).
# P(B) is Marginal Probability: Probability of Evidence.
# P(A|B) is a posteriori probability of B, i.e. probability of event after evidence is seen.
# P(B|A) is Likelihood probability i.e the likelihood that a hypothesis will come true based on the evidence.
from sklearn.naive_bayes import GaussianNB
model=GaussianNB()
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
Y2=metrics.accuracy_score(y_test,y_pred)
print("Naive Bayes Accuracy:",metrics.accuracy_score(y_test,y_pred))
#SVM
#Import svm model
# dividing using hyperplane
from sklearn import svm
clf = svm.SVC(kernel='linear') # Linear Kernel
clf.fit(x_train, y_train)
Y_pred = clf.predict(x_test)
Y3=metrics.accuracy_score(y_test,y_pred)
print("Support Vector Accuracy:",metrics.accuracy_score(y_test,y_pred))

#RANDOM FOREST CLASSIFIER
rf_model = RandomForestClassifier(random_state=18)
rf_model.fit(x_train, y_train)
preds = rf_model.predict(x_test)
Y4=metrics.accuracy_score(y_test,y_pred)
print("Random Forest Acuuracy:",metrics.accuracy_score(y_test,y_pred))


indices = [i for i in range(132)]
symptoms = df.columns.values[:-1]

dictionary = dict(zip(symptoms,indices))

def dosomething(symptom):
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    X1=dt.predict(user_input_label)
    X2=model.predict(user_input_label)
    X3=clf.predict(user_input_label)
    if(len(user_input_symptoms)==0):
        return ;
    if Y1>=Y2 and Y1>=Y3 and Y1>=Y4:
        return X1;
    
    if Y3>=Y2 and Y3>=Y1 and Y3>=Y4:
        return X3;
    
    if Y2>=Y1 and Y2>=Y3 and Y2>=Y4:
        return X2;
    
    if Y4>=Y1 and Y4>=Y2 and Y4>=Y2:
        return X3
    
    return(dt.predict(user_input_label))

# print(dosomething(['headache','muscle_weakness','puffy_face_and_eyes','mild_fever','skin_rash']))
# prediction = []
# for i in range(7):
#     pred = dosomething(['headache'])   
#     prediction.append(pred) 
# print(prediction)