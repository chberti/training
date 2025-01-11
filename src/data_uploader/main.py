# main.py
from flask import Flask, request, render_template, session, redirect
from pathlib import Path
import os
from werkzeug.utils import secure_filename
import pandas as pd
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = Path(__file__).parent / "uploads"
app.config['BASE_URL'] = "http://localhost:5000"
app.secret_key = 'This is my secret key to utilize session in Flask Data Uploader'

@app.route("/")
def index():
    return redirect(location = f"{app.config['BASE_URL']}/upload", code = 302)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    match request.method:
        case "POST":
            f = request.files.get('file')
            # Extracting uploaded file name
            data_filename = secure_filename(f.filename)
            f.save( app.config['UPLOAD_FOLDER'] / data_filename)

            session['uploaded_data_file_path'] =  os.path.join(app.config['UPLOAD_FOLDER'],  data_filename)

            return render_template('success_upload.html')
        case "GET":
            return render_template("upload_page.html")
            #return f"Now I should render template located at {templates_directory}"
@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',
                           data_var=uploaded_df_html)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)