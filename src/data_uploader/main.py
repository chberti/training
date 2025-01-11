# main.py
from flask import Flask, request, render_template, session, redirect
from pathlib import Path
from mimetypes import MimeTypes
import pandas as pd
from werkzeug.utils import secure_filename
from modules.csv_importer import csv_parse
from modules.xlsx_importer import xlsx_parse
from modules.postgresql_exporter import load_data

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = Path(__file__).parent / "uploads"
app.config['BASE_URL'] = "http://localhost:5000"
app.secret_key = 'This is my secret key to utilize session in Flask Data Uploader'

@app.route("/")
def index():
    return redirect(location = f"{app.config['BASE_URL']}/upload", code = 302)

@app.route("/person", methods=["GET"])
def show_person():
    pg_data = load_data(table = "person")
    show_user = pg_data.describe()
    return render_template('show_csv_data.html', data_var=show_user)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    match request.method:
        case "POST":
            f = request.files.get('file')
            data_filename = secure_filename(f.filename)
            staging_path = app.config['UPLOAD_FOLDER'] / data_filename
            # Extracting uploaded file name
            f.save( app.config['UPLOAD_FOLDER'] / data_filename)
            # session['uploaded_data_file_path'] =  os.path.join(app.config['UPLOAD_FOLDER'],  data_filename)

            mime = MimeTypes()
            mime_type = mime.guess_type(staging_path)[0]
            match mime_type:
                case 'text/csv':
                    (nb_lines, schema) = csv_parse(staging_path)
                    return render_template('success_csv.html', nb_lines = nb_lines, schema = schema)
                case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    (nb_lines, schema) = xlsx_parse(staging_path)
                    return render_template('success_xlsx.html', nb_lines=nb_lines, schema=schema)

            return render_template('success_upload.html', mime_type = mime_type)
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