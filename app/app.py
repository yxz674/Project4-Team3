# app.py is entry port for flask to run
import os
from flask import Flask, render_template,request,flash,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pickle
import numpy as np
import psycopg2
import urllib.request

##This is for user.html page, connect to actual machine learning model----Loading model.py
model=pickle.load(open('model.pkl','rb'))

connection = psycopg2.connect(
    host = 'project4postgresdb.cec7i89ma4zy.us-east-2.rds.amazonaws.com',
    port = 5432,
    user = 'root',
    password = 'project4',
    database='project_4_db'
    )
cursor=connection.cursor()

app = Flask(__name__)
#==============================================================================================#
# This is for upload.html page----check documentation : https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
#check youtube video as well https://www.youtube.com/watch?v=SYP4huDHLz4
app.secret_key =b'secret'

# # print path: git bash type cd Project4-Team3/app/static/uploads then type pwd, FILES_UPLOADS is the folder name under app-static

#connect to local path: 
# UPLOAD_FOLDER= r'C:\Users\xxx\Project4-Team3\app\static\uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 1. connect to Postgresql:
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:postgres@localhost:5432/hr_database'

# db = SQLAlchemy(app)

#2. connect to local path: 
# UPLOAD_FOLDER= r'C:\Users\Cecilia\Project4-Team3\app\static\uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ALLOWED_EXTENSIONS = set(['txt', 'xlsx', 'png', 'jpg', 'jpeg', 'gif'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################Postgresql Database part#######################################################
# Step1 create database called hr_database，then create table called prediction in Postgres
#     CREATE TABLE prediction(
#     id serial PRIMARY KEY,
#     fname VARCHAR(40) NOT NULL,
#     lname VARCHAR(40) NOT NULL,
#     upload_file VARCHAR(40) NOT NULL
#     );
# Step2 run app.py
# class Prediction(db.Model):
#     __tablename__ = 'prediction'

#     id = db.Column(db.Integer,primary_key=True)
#     fname=db.Column(db.String(40))
#     lname=db.Column(db.String(40))
#     upload_file=db.Column(db.String(40))

#     def __init__(self,fname,lname,upload_file):
#         self.fname=fname
#         self.lname=lname
#         self.upload_file=upload_file    
#==============================================================================================#
# set individual html route
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/visual')
def index_visual():
    return render_template("visual.html")

@app.route('/user')
def index_user():
    return render_template("user.html")

@app.route('/data')
def index_data():
    return render_template("data.html")
#==============================================================================================#
# This is for upload.html page----check documentation : https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
#check youtube video as well https://www.youtube.com/watch?v=SYP4huDHLz4 or https://tutorial101.blogspot.com/2021/05/upload-file-and-validate-before-save-to.html

# @app.route('/upload', methods=['GET', 'POST'])
# def index_upload():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         fname=request.form['fname']
#         lname=request.form['lname']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             ################Postgresql Database part######################
#             # newFile=Prediction(upload_file=file.filename,fname=fname,lname=lname)
#             # db.session.add(newFile)
#             # db.session.commit()
#             ###############################################################            
#             flash('File uploaded successfully'+ file.filename + '!') 
#             return render_template("upload.html")
#     else:
#         flash('Invalid Upload only txt,pdf,png,jpg,jpeg,gif')
#     return render_template("upload.html")

#==============================================================================================#
#This is for user.html page, connect to actual machine learning model
@app.route('/predict', methods=['POST'])
def index_predict():
    data1 = request.form['employee_satifaction']
    data2 = request.form['employees_last_evaluation']
    data3 = request.form['number_of_employee_projects']
    data4 = request.form['average_hours_per_month']
    data5 = request.form['years_of_service']
    data6 = request.form['empoyee_has_had_accident']
    data7 = request.form['empoyeed_salary_range']
    arr = np.array([[data1, data2, data3, data4, data5, data6, data7]])
    pred = model.predict(arr)
    if pred == 0:
         result = "stay"
    else:
        result="leave"
    query = "INSERT INTO model_input (employee_satisfaction, employees_last_evaluation, number_of_employee_projects, average_hours_per_month, years_of_service, employee_has_had_accident, empoyeed_salary_range, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data1, data2, data3, data4, data5, data6, data7, result)
    cursor.execute(query, values)
    connection.commit()
    return render_template('user.html', prediction_text=pred)

# create insert query to sql database using the data1, data2, data3, data4, data5, data6, data7 variables
# def insert_data(data1, data2, data3, data4, data5, data6, data7):
#     print("Record inserted successfully into project_4_db table")

#run
if __name__ =='__main__':
    app.run(debug=True)