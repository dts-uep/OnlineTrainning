# Set-ups
from flask import jsonify, Blueprint

# Utils
from utils.db_handle import get_error

error_bp = Blueprint('error_bp', __name__)

# Routes
@error_bp.app_errorhandler(400)
def bad_request(e):
    return jsonify({
        "error":'Bad Request',
        "details":str(e)
    }, 400)

@error_bp.app_errorhandler(500)
def internal_error(e):
    return jsonify({
        "error":"Server Error",
        "details":str(e)
    }, 500)


@error_bp.route('/error-log/<job_id>')
def get_error_logs(job_id):

    error = get_error(job_id)
    if error:
        return jsonify({
            "error":"Execution Error",
            "details":str(error)
            })
    else:
        return "No Execution Error"
    

