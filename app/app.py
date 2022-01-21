# app.py is entry port for flask to run
import os
from flask import Flask, render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
import pickle
import numpy as np

#Loading model.py
model=pickle.load(open('model.pkl','rb'))

app = Flask(__name__)
#===========================================================================================#
# This is for upload.html page----check documentation : https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
app.secret_key =b'secret'

# print path: git bash type cd Project4-Team3/app/static/uploads then type pwd, FILES_UPLOADS is the folder name under app-static
FILES_UPLOADS = '/c/Users/Cecilia/Project4-Team3/app/static/uploads'
# FILES_UPLOADS = "/c/Users/Cecilia/Project4-Team3/app/static/files/uploads"  
ALLOWED_EXTENSION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' 'csv'}

app.config['FILES_UPLOADS'] = FILES_UPLOADS
app.config['ALLOWED_EXTENSION'] = ALLOWED_EXTENSION
# app.config["MAX_FILE-FILESIZE"] = 0.5 * 1024 * 1024

def allowed_files(filename: str) ->bool:
    print(filename)
    print('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

# def allowed_files_filesize(filesize):
#     if int(filesize) <= app.config["MAX_FILE-FILESIZE"]:
#         return True
#     else:
#         return False

#===========================================================================================#
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
@app.route('/upload', methods=['GET', 'POST'])
def index_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['FILES_UPLOADS'], filename))
            print('File uploaded successfully')
            return render_template("upload.html",fileupload=True,file_name=filename)
            # return redirect(url_for('download', name=filename))
        
    return render_template("upload.html",fileupload=False,file_name="freeai.png")


# @app.route('/download', methods=['Get'])
# def download():
#     return 'Download Page'
#==============================================================================================#
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
    return render_template('user.html', prediction_text='Employee will {}'.format(pred))

################SQL Database part##################################


#run
if __name__ =='__main__':
    app.run(debug=True)