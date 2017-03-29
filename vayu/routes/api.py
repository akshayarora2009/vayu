from flask import Blueprint, render_template, request, make_response, jsonify
import os
import vayu.core.local_utils as lutils
import vayu.core.fabric_scripts.utils as futils
from vayu.core.constants.model import machine_info
from vayu.core.VayuException import VayuException
import vayu.core.constants.local as constants

api_app = Blueprint('api_app', __name__)


@api_app.route('/api/projects/<project_id>')
def get_project_details_by_id(project_id):
    """
    API method to return the details of project with the given id
    :param project_id: 
    :return: 
    """
    project_details = lutils.get_project_details_by_id(project_id)

    res = dict()

    if project_details is None:
        res[constants.ERROR] = dict()
        res[constants.ERROR][constants.CODE] = 400
        res[constants.ERROR][constants.ERRORS] = ["The project id is invalid"]
        return make_response(jsonify(res), 400)
    else:
        project_details[constants.PROJECT_ID] = project_id
        print(project_details)
        res[constants.DATA] = []
        res[constants.DATA].append(project_details)
        return make_response(jsonify(res), 200)
