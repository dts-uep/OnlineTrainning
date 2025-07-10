# Set-ups
from flask import Blueprint, jsonify
from celery_app.task import app as Celery_app
import redis
import os


# Utils
from utils.db_handle import get_all_data


# Initiate
status_bp = Blueprint("status_bp", __name__)
r = redis.Redis(host='localhost', port=6379, db=0)


# Routes
# Get status using redis
@status_bp.route("result/<job_id>")
def result(job_id):

    try:
        from celery.result import AsyncResult

        task_id = r.get(f"jobs {job_id}")
        task = AsyncResult(task_id, app=Celery_app)

        return {
            'status':task.status,
            'result':str(task.result)
        }

    except Exception as e:
        return f"Error: {e}"

# Query full data from db
@status_bp.route("full/<job_id>")
def full_status(job_id):
    
    try:
        data = get_all_data(job_id)
        return jsonify({
            "JOB ID": data[0],
            "NAME": data[1],
            "# UTIL FILES": data[2],
            "SUBMITTED AT": data[3],
            "STARTED AT": data[4],
            "FINISHED AT": data[5],
            "# DATA FILES": data[6],
            "STATUS": data[7],
            "RUNTIME": data[8],
            "ERROR": data[9],
            "CALLBACK URL": data[10]
        })

    except Exception as e:
        return f"Error: {e}"