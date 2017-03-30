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
    project[project_id] = request.args.get('project_id')
    project[project_path] = "/home/harshita/Documents/test"
    futils.moveProject(machine_info , project_path , project_id)
    futils.deployNodeJs(machine_info,project_id,"server.js")
    return render_template("deployments.html" , project_details = project)
