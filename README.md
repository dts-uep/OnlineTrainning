## **Online Trainning Project**  
This project allows users to upload .ipynb or .py scripts via curl or a simple web interface, executes them safely inside Docker containers, and sends back results (Markdown). Task are managed with Celery and Redis. Results and job data are stored and tracked using SQLite. Docker containers handling run script task dynamically change based on time and selected using a demand analysis model that can be train periodically.  
  
### **Features**  
* Upload Jupyeter notebooks or Python scripts
* Secure, isolated Docker execution
* Time-limited sandbox execution with predicted CPU constraints
* Celery background scheduling tasks and Redis broker
* SQLite database for jobtracking and analysis
* Callback URL for webhook and notification
* Status tracking via routes
* Markdown download
* Secure file handling in system
  
## **Technologies**  
* Flask  
* Docker  
* Celery  
* Redis
* SQLite
* Jupyter nbconvert
* Guinicorn for WSGI
* Jupytext

## **Project Strucute**
```
project/
├── app.py                        # Flask app entrypoint
├── celery_app/
│   └── tasks.py                  # Celery task definition
├── utils/
│   ├── db_handle.py              # SQLite manage (insert, mark_done, etc.)
│   ├── run_and_export.py         # Run script task process
│   └── clean_up.py               # Temporary folder clean-up
├── routes/                       # Flask blueprints
│   ├── files.py                  # Upload, run scripts, download routes
│   ├── status.py                 # Status checking
│   └── errors.py                 # Error handlers
├── analysis/                     # ML & prediction
│   ├── OnlineTrainningDemand.ipynb  # Train and predict daily demand and CPU power
│   └── cpu_per_time_system.pkl      # Predict results
├── Dockerfile                   # Notebook runner image
├── requirements.txt
├── jobs.db                      # SQLite database
├── README.md
└── templates/                   # HTML forms
    ├── homepage.html
    ├── upload_data.html
    ├── upload_main.html
    └── upload_util.html
```


├── start_online_trainning.sh   # For quickly start the system.  
├── retrain_demand.sh           # For modifysing system to retrain model periodically.  

## **Start**
* Make .sh files executable  
chmod +x /home/your_user/path/to/project/start_online_trainning.sh  
chmod +x /home/your_user/path/to/project/retrain_demand.sh   

* Direct to project folder  
cd /home/your_user/path/to/project  

* Build Docker image (once)  
docker build -f Dockerfile.runner -t notebook-runner .  

* Run app  
./start_online_trainning.sh  

* Set periodic retrain everymonth  
crontab -e  
Add:
0 0 1 * * /bin/bash /home/your_user/path/to/project/retrain_demand.sh  

## **Example**
* Upload script  
curl -F "notebook.ipynb" http://localhost:5000/upload-main"  

* Download results  
curl -o result.md http://localhost:5000/files/download/<job_id>  

## **Modules & Versions**
* Python: 3.12.3
* Flask: 3.1.1
* Werkzeug: 3.1.3
* SQLite: 3.45.1
* numpy: 2.3.1
* pandas: 2.3.1
* matplotlib: 3.10.3
* seaborn: 0.13.2

## **Note**
* Data for analysis was simulated
