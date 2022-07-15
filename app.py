import csv
from flask import Flask, render_template,request,redirect,url_for
import diseaseprediction
import pandas as pd
import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId

#import mySQLdb

app = Flask(__name__)
#conn = MySQLdb.connect(host='localhost',user='root',password='',db='disease_database')
client = MongoClient("mongodb+srv://sheikhhaji18:18shakila@cluster0.2akiep0.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NON");
db = client.disease
todos = db.disease_info

with open('templates/Training.csv', newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]
        #print(symptoms)
        data=pd.read_csv("templates/Training.csv")
        data=data["prognosis"]
        data=data.unique()
        data1=np.array(data)
        np.transpose(data1)
        #print(data1.shape)
        disease_array=data1.tolist()
        print(disease_array)
        #print(data.shape)

@app.route('/', methods=['GET'])
def dropdown():
        return render_template('home.html', symptoms=symptoms,disease_array=disease_array)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    # disease_list = []
    # for i in range(7):
    #     disease = diseaseprediction.dosomething(selected_symptoms)
    #     disease_list.append(disease)
    # return render_template('disease_predict.html',disease_list=disease_list)
    if(len(selected_symptoms)==0):
        return render_template('home.html', symptoms=symptoms,disease_array=disease_array)

    disease = diseaseprediction.dosomething(selected_symptoms)
    if(disease==''):
        return render_template('disease_predict.html',disease=disease,symptoms=symptoms,disease_array=disease_array)
    else:
        return render_template('disease_predict.html',disease=disease,symptoms=symptoms,disease_array=disease_array)

# @app.route('/default')
# def default():
#         return render_template('includes/default.html')

@app.route('/find_doctor', methods=['POST'])
def get_location():
    location = request.form['doctor']
    return render_template('find_doctor.html',location=location,symptoms=symptoms,disease_array=disease_array)

# @app.route('/drug', methods=['POST'])
# def drugs():
#     medicine = request.form['medicine']
#     return render_template('homepage.html',medicine=medicine,symptoms=symptoms,disease_array=disease_array)

@app.route('/remedy',methods=['POST'])
def remedy():
    medicine = request.form['medicine']
    array1=[];
    for i in range(0,10):
        array1.append(disease_array[i]);
    j=-1;
    for i in range(0,10):
        if(array1[i]==medicine):
            j=i;break;
    hi=""
    if(j==-1):
        list={"name":medicine,"treatment":"get a good sleep and rest"};
        hi="1";
    else:
        list=todos.find({"name":medicine});
        hi="2";
    return render_template('remedy.html',list=list,symptoms=symptoms,disease_array=disease_array,temp=hi)
if __name__ == '__main__':
    app.run("localhost",5000,debug=True)
