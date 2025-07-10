# Set-ups
from flask import Flask,render_template
from routes.files import file_bp
from routes.errors import error_bp
from routes.status import status_bp
import os


# Initiate
app = Flask(__name__)
app.register_blueprint(file_bp, url_prefix='/files')
app.register_blueprint(error_bp, url_prefix='/error')
app.register_blueprint(status_bp, url_prefix='/status')


# Interface
@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/upload-main')
def upload_main_page():
    return render_template("upload_main.html")

@app.route('/upload-util/<job_id>')
def upload_script_page(job_id):
    return render_template("upload_util.html", job_id=job_id)

@app.route('/upload-data/<job_id>')
def upload_data_page(job_id):
    return render_template("upload_data.html", job_id=job_id)


#if __name__ == "__main__":
 #   app.run(debug=True)