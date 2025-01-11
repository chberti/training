# main.py
from flask import Flask, request, render_template, session
from pathlib import Path
import os
from werkzeug.utils import secure_filename
import pandas as pd
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World! Please go to /upload endpoint to try the API"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    match request.method:
        case "POST":
            f = request.files.get('file')
            # Extracting uploaded file name
            data_filename = secure_filename(f.filename)

            f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                data_filename))

            session['uploaded_data_file_path'] =  os.path.join(app.config['UPLOAD_FOLDER'],  data_filename)

            return render_template('index2.html')
        case "GET":
            return render_template("upload_page.html")
            #return f"Now I should render template located at {templates_directory}"