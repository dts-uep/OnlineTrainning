# Set-ups
import requests
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import subprocess
import traceback
import os
import pickle as pkl
import datetime

# Utils
from utils.db_handle import mark_done, mark_started, get_callback_url, insert_cpu_power

# Initiate
app = Celery("task",
            broker="redis://localhost:6379/0",
            backend="redis://localhost:6379/0")


# Functions for error log
def log_error(job_id):

    with open(f"errors/{job_id}.log", 'w') as f:
        f.write(traceback.format_exc())


# Tasks
@app.task(bind=True, soft_time_limit=60, time_limit=65, max_retries=3, retry_backoff=True)
def run_task(self, in_nb, out_md, job_id):
    
    try:    

        # Get cpu_power
        project_path = os.path.dirname(os.getcwd())
        demand_path = os.path.join(project_path,"project", "analysis", "cpu_per_time_system.pkl")
        with open(demand_path, 'rb') as f:
            demand = pkl.load(f)

        cpu_per_timestep = demand["Max"] # Using max demand
        #cpu_per_timestep = demand["H-W"] # Using demand forecast using Holt-Winters
        time_gap = demand["time_gap"]
        num_time_step = demand["num_time_step"]

        current_time_step = int((datetime.datetime.now().hour * num_time_step/24) + (datetime.datetime.now().minute // time_gap) + 1)
        cpu_power = cpu_per_timestep[current_time_step-1]

        # Insert cpu power
        insert_cpu_power(job_id, cpu_power)

        # Run the task
        mark_started(job_id)

        subprocess.run([
            "docker", "run", f"--cpus={cpu_power}" ,"--rm",
            "-v", f"{os.getcwd()}/temp/{job_id}_workplace:/sandbox/workplace",
            "-v", f"{os.getcwd()}/results/{job_id}_results:/sandbox/results",
            "-v", f"{os.getcwd()}/errors:/sandbox/errors",
            "notebook-runner", in_nb, out_md
        ], check=True, timeout=60)

        mark_done(job_id, "SUCCESS")

        # Trigger callback
        callback_url = get_callback_url(job_id)
        if callback_url:
            try:
                requests.post(callback_url,          
                              json={
                                  "job_id": job_id,     
                                  "status": "SUCCESS",
                                  "result": out_md
                              }, timeout=5)
            
            except Exception as e:
                with open(f"errors/{job_id}.log", "w") as errorlog:
                    errorlog.write(f"Success run but callback error: {str(e)}")

        return {"status":"done", "out_path":out_md}

    except SoftTimeLimitExceeded as e:
        log_error(job_id)
        raise self.retry(exc=e)

    except Exception as e:
        mark_done(job_id, "FAILURE", error=str(e))
        # Trigger callback
        callback_url = get_callback_url(job_id)
        if callback_url:
            try:
                requests.post(callback_url,
                              json={
                                  "job_id": job_id,
                                  "status": "FAILURE",
                                  "error": str(e)
                              }, timeout=5)
            
            except Exception as e:
                with open(f"errors/{job_id}.log", "w") as errorlog:
                    errorlog.write(f"Failed with callback error: {str(e)}")

        log_error(job_id)
        raise self.retry(exc=e)