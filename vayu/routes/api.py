from flask import Blueprint, render_template, request, make_response, jsonify
import os
import  core.local_utils as lutils
import  core.fabric_scripts.utils as futils
from  core.constants.model import machine_info
from  core.VayuException import VayuException
import  core.constants.local as constants

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
        
        host_details_wanted = request.args.get("host_details")
        if host_details_wanted == "true":
            all_hosts = []
            if constants.FLEET in project_details:
                for key, value in project_details[constants.FLEET].iteritems():
                    if constants.HOSTS in value:
                        all_hosts.extend(value[constants.HOSTS])

            host_details = lutils.get_hosts_details(all_hosts)
            project_details[constants.HOST_DETAILS] = host_details

        project_details[constants.PROJECT_ID] = project_id
        res[constants.DATA] = []
        res[constants.DATA].append(project_details)
        return make_response(jsonify(res), 200)
