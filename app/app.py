# app.py is entry port for flask to run
import os
from flask import Flask, render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
# check documentation : https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
app.secret_key =b'secret'

# print path: git bash type cd app/static/files/uploads then type pwd, FILES_UPLOADS is the folder name under app-static
FILES_UPLOADS = "/c/Users/Cecilia/Project4-Team3/app/static/files/uploads"  
ALLOWED_EXTENSION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' 'csv'}

app.config['FILES_UPLOADS'] = FILES_UPLOADS
app.config['ALLOWED_EXTENSION'] = ALLOWED_EXTENSION
app.config["MAX_FILE-FILESIZE"] = 0.5 * 1024 * 1024

def allowed_files(filename: str) ->bool:
    print(filename)
    print('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def allowed_files_filesize(filesize):
    if int(filesize) <= app.config["MAX_FILE-FILESIZE"]:
        return True
    else:
        return False

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
# check documentation : https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def index_upload():
    if request.method == 'POST':
        if request.files:
            if allowed_files_filesize(request.cookies.get("filesize")):
                print("Fule exceeded maximum size")
                return redirect(request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['FILES_UPLOADS'], filename))
            print('File uploaded successfully')
            return redirect(url_for('download', name=filename))
    return render_template("upload.html")


@app.route('/download', methods=['Get'])
def download():
    return 'Download Page'

#run
if __name__ =='__main__':
    app.run(debug=True)