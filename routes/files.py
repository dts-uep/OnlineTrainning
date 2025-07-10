# Set-ups
from flask import Blueprint, request, send_file, abort
import uuid
import shutil
from werkzeug.utils import secure_filename
import redis
import os


# Utils
from celery_app.task import run_task
from utils.db_handle import insert_job, count_data,\
      count_util, get_filename
from utils.clean_up import clean_up_temp_folder


# Configure
ALLOWED_SCRIPT_EXTENTIONS = ("ipynb", "py")
ALLOWED_DATA_EXTENTIONS = ("csv", "xlsx")
ALLOWED_UTILS_EXTENTIONS = ("py")
MAX_SCRIPT_SIZE_MB = 50
MAX_DATA_SIZE_MB = 1000


# Initiate
file_bp = Blueprint("file_bp", __name__)
r = redis.Redis(host='localhost', port=6379, db=0)


# Functions
def allowed_code(filename:str, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def save_file(file, save_folder):
    
    # Get safename
    safename = secure_filename(file.filename)
    save_path = os.path.join(save_folder, safename)

    # Save file
    with open(save_path, 'wb') as f:
        f.write(file.read())
    

# Routes 
# Upload files
@file_bp.route("/upload-main", methods=['POST'])
def upload_main():

    try:
        # Create temporary folders (recreate if lost or missing)
        os.makedirs("temp", exist_ok=True)
        os.makedirs("results", exist_ok=True)
        os.makedirs("errors", exist_ok=True)

        # Clean-up
        clean_up_temp_folder(folder='temp', age_minutes=0.1)
        clean_up_temp_folder(folder='results', age_minutes=0.2)
        clean_up_temp_folder(folder='errors', age_minutes=0.33)

        # Save callback url for webhook
        callback_url = request.form.get("callback_url")

        # Upload files
        file = request.files["file"]

        # Check file
        if not allowed_code(file.filename, ALLOWED_SCRIPT_EXTENTIONS):
            abort (400, description="Invalide file type")
        
        file.seek(0, os.SEEK_END)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)

        if size_mb >  MAX_SCRIPT_SIZE_MB:
            abort(400, description=f"File too large: {file.filename}")
        
        # Create temporary workplace folder
        job_id = str(uuid.uuid4())

        workplace_name = f"{job_id}_workplace"
        workplace_path = os.path.join("temp", workplace_name)
        os.makedirs(workplace_path, exist_ok=False)
        os.makedirs(os.path.join(workplace_path, "utils"), exist_ok=True)
        os.makedirs(os.path.join(workplace_path, "data"), exist_ok=True)
        os.makedirs(os.path.join("results", f"{job_id}_results"), exist_ok=False)

        # Save upload files
        save_file(file, workplace_path)

        # Insert job to jobs_db
        insert_job(job_id, secure_filename(file.filename), callback_url)

        return f"Message: Upload Received, Job ID: {job_id}" 
    
    except Exception as e:
        return f"Message: Error Encountered {str(e)}"


@file_bp.route("/upload-utils/<job_id>", methods=["POST"])
def upload_utils(job_id):

    # Upload files
    files = request.files.getlist("files")

    # Check files
    for file in files:
        if not allowed_code(file.filename, ALLOWED_UTILS_EXTENTIONS):
            abort (400, description="Invalide file type")
        
        file.seek(0, os.SEEK_END)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)

        if size_mb >  MAX_SCRIPT_SIZE_MB:
            abort(400, description=f"File too large: {file.filename}")
        
    # Save upload files
    util_path = os.path.join("temp", f"{job_id}_workplace", "utils")

    for file in files:
        save_file(file, util_path)

    # Insert count utils to db
    count_files = len(files)
    count_util(job_id, count_files)

    return f"Message: Upload Received, Number of Util FIles: {count_files}"


@file_bp.route("/upload-data/<job_id>", methods=["POST"])
def upload_data(job_id):

    # Upload files
    files = request.files.getlist('files')

    # Check files
    if len(files)==0:
        return "Message: No file uploaded"

    for file in files:
        if not allowed_code(file.filename, ALLOWED_DATA_EXTENTIONS):
            abort (400, description="Invalide file type")
        
        file.seek(0, os.SEEK_END)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)

        if size_mb >  MAX_SCRIPT_SIZE_MB:
            abort(400, description=f"File too large: {file.filename}")
    
    script_path = os.path.join("temp", f"{job_id}_workplace", "data")

    # Save upload files
    for file in files:
        save_file(file, script_path)
    
    # Insert count data to db
    count_files = len(files)
    count_data(job_id, count_files)

    return f"Message: Upload Received, Number of Data Files: {count_files}"     
    

# Run file
@file_bp.route("/run-script/<job_id>")
def run_script(job_id):

    # Get paths
    filename = get_filename(job_id)
    if filename:
        inpath = os.path.join('workplace', filename)
    else:
        return f"Message: No main script"
    outpath = os.path.join('results', 'output.md')

    # Run Celery task 
    result = run_task.delay(inpath, outpath, job_id)
    result.get(timeout=100) 

    # Map job id with Celeary task id
    task_id = result.id
    r.set(f"jobs {job_id}", task_id)


    return f"Message: Job Running"

# Send back zip file to client
@file_bp.route("/download/<job_id>")
def download(job_id):

    # Zip result folder
    result_path = os.path.join('results', f"{job_id}_results")
    zip_path = os.path.join('results', f'{job_id}.zip')

    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', result_path)

    # Send file
    if os.path.isfile(zip_path):
        return send_file(zip_path, as_attachment=True, download_name="result.zip")
    else:
        return "Error: File not Exist"