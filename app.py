import csv
from flask import Flask, render_template,request,redirect,url_for
import diseaseprediction
import pandas as pd
import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
import test
import json
# Autocomplete a query
import requests
import geocoder
# jdhfdjhdfjh
#import mySQLdb


app = Flask(__name__, static_folder='static')
#conn = MySQLdb.connect(host='localhost',user='root',password='',db='disease_database')
client = MongoClient("mongodb+srv://sheikhhaji18:18shakila@cluster0.2akiep0.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NON");
db = client.disease
todos = db.disease_info

with open("Training.csv", newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]
        #print(symptoms)
        data=pd.read_csv("Training.csv")
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
    # print(request.form["search_doctor_near_me"])
    # print(request.form["search_doctor"])
    location1 = request.form['doctor']
    response = requests.get("http://api.openweathermap.org/geo/1.0/direct?q="+location1+"&limit=5&appid=697f16a5b41aa5208bcda6f326c84b4a")
    json_data = json.loads(response.text)
    direction_hospital=[]
    list_hospital=[]
    if len(json_data)!=0:
        lng=json_data[0]["lon"]
        lat=json_data[0]["lat"]
        response1 = requests.get("https://api.olamaps.io/places/v1/nearbysearch?layers=venue&types=hospital&location="+str(lat)+","+str(lng)+"&api_key=UkUs3JeMNDj7LCtp5b23WQCZXC6qdoIaxqwCaXhn")
        json_data1 = json.loads(response1.text)
        # print(json_data1)
        
        
        if json_data1['status']=="ok":
            for i in json_data1["predictions"]:
                print(i["description"])
                print(i["distance_meters"])
                item=i["description"]+',Distance='+str(i["distance_meters"])+'m'
                list_hospital.append(item)
        if json_data1['status']=="ok":
            for i in json_data1["predictions"]:
                item="https://www.google.com/maps/dir/"+i["description"]
                direction_hospital.append(item)
                print(item)
       
    else:
        lng=77.57
        lat=8.08
    print("longitude=",lng)
    print("latitude=",lat)
    hospital_data = zip(list_hospital, direction_hospital)
    return render_template('find_doctor.html',lng=lng,lat=lat,hospital_data=hospital_data)

@app.route('/find_doctor1', methods=['POST'])
def get_location1():
    list_hospital=[]
    direction_hospital=[]
    # g = geocoder.ip('me')
    # lng=g.latlng[1]
    # lat=g.latlng[0]
    # data = request.get_json()
    # print(data)
    lng=request.form.get("long")
    lat=request.form.get("lat")
    # print("latitude",lat)
    # print("longitude",lng)
    if(lng==None):
        lng=80.216064
    if(lat==None):
        lat=13.0318336
    response1 = requests.get("https://api.olamaps.io/places/v1/nearbysearch?layers=venue&types=hospital&location="+str(lat)+","+str(lng)+"&api_key=UkUs3JeMNDj7LCtp5b23WQCZXC6qdoIaxqwCaXhn")
    json_data1 = json.loads(response1.text)
        # print(json_data1)
        
        
    if json_data1['status']=="ok":
        for i in json_data1["predictions"]:
            print(i["description"])
            print(i["distance_meters"])
            item=i["description"]+',Distance='+str(i["distance_meters"])+'m'
            list_hospital.append(item)
    if json_data1['status']=="ok":
        for i in json_data1["predictions"]:
            item="https://www.google.com/maps/dir/"+i["description"]
            direction_hospital.append(item)
            print(item)
    hospital_data = zip(list_hospital, direction_hospital)
    return render_template('find_doctor.html',lng=lng,lat=lat,hospital_data=hospital_data)
# @app.route('/drug', methods=['POST'])
# def drugs():
#     medicine = request.form['medicine']
#     return render_template('homepage.html',medicine=medicine,symptoms=symptoms,disease_array=disease_array)

@app.route('/remedy',methods=['POST'])
def remedy():
    medicine = request.form['medicine']
    list=todos.find({"name":medicine});
 
    return render_template('remedy.html',list=list,symptoms=symptoms,disease_array=disease_array)
if __name__ == '__main__':
    app.run(host="localhost",port=5000,debug=True)
