from flask import Blueprint, render_template, request, make_response, jsonify
import os
import vayu.core.local_utils as lutils
from vayu.core.VayuException import VayuException
import vayu.core.constants.local as constants
import re
import vayu.core.fabric_scripts.utils as futils
from vayu.core.constants.model import machine_info

deployment_app = Blueprint('deployment_app', __name__)
machine_info = machine_info("root","139.59.35.6","ahjvayu2017")

@deployment_app.route('/deployments/<uuid>')
def deployments_uuid(uuid):
    project = dict()
    project["id"] = request.args.get('project_id')
    project["path"] = request.args.get('project_path')
    project["deployment_language"] = request.args.get('deployment_language')
    project["language_version"] = request.args.get('language_version_id')
    project["language_prod"] = request.args.get('language_prod_id')
    project["port_number"] = request.args.get('port_number')
    project["git_ignore"] = request.args.get('git_ignore')
    project["host"] = request.args.get('host')
    return render_template("deployments.html" , project = project)
