import pandas as pd
import numpy as np
import csv
from collections import defaultdict

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import metrics

def dosomething(symptom):
    print("sheikh ameenulnhai")
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1

    user_input_label = pd.DataFrame([user_input_label], columns=x.columns)


    if len(user_input_label) == 0:
        return 
    
    X1 = dt.predict(user_input_label)
    X2 = model.predict(user_input_label)
    X3 = clf.predict(user_input_label)
    X4 = rf_model.predict(user_input_label)

    vote_dict = defaultdict(int)
    for prediction in [X1, X2, X3, X4]:
        vote_dict[prediction[0]] += 1

    final_prediction = max(vote_dict, key=vote_dict.get)
    print("Final Prediction:", final_prediction)
    return final_prediction


def main():
    # Load and prepare the data
    data = pd.read_csv("Training.csv")
    df = pd.DataFrame(data)

    global dt, model, clf, rf_model, dictionary  # make models and dict available in dosomething()

    x = df.drop("prognosis", axis=1)
    y = df["prognosis"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    # Decision Tree
    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    y_pred_dt = dt.predict(x_test)
    print("Decision Tree Accuracy:", metrics.accuracy_score(y_test, y_pred_dt))

    # Naive Bayes
    model = GaussianNB()
    model.fit(x_train, y_train)
    y_pred_nb = model.predict(x_test)
    print("Naive Bayes Accuracy:", metrics.accuracy_score(y_test, y_pred_nb))

    # SVM
    clf = svm.SVC(kernel='linear')
    clf.fit(x_train, y_train)
    y_pred_svm = clf.predict(x_test)
    print("SVM Accuracy:", metrics.accuracy_score(y_test, y_pred_svm))

    # Random Forest
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(x_train, y_train)
    y_pred_rf = rf_model.predict(x_test)
    print("Random Forest Accuracy:", metrics.accuracy_score(y_test, y_pred_rf))

    # Symptom Index Dictionary
    symptoms = df.columns.values[:-1]
    dictionary = dict(zip(symptoms, range(132)))

    # Call dosomething from main
    test_symptoms = ['headache', 'muscle_weakness', 'puffy_face_and_eyes', 'mild_fever', 'skin_rash']
    prediction = dosomething(test_symptoms)
    print("Predicted disease for input symptoms:", prediction)


if __name__ == "__main__":
    main()
