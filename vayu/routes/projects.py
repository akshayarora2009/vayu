from flask import Blueprint, render_template, request, make_response, jsonify
import os
import vayu.core.local_utils as lutils
import vayu.core.fabric_scripts.utils as futils
from vayu.core.constants.model import machine_info
from vayu.core.VayuException import VayuException
import vayu.core.constants.local as constants
import re

project_app = Blueprint('project_app', __name__)
machine_info = machine_info("root","139.59.35.6","ahjvayu2017")

@project_app.route('/projects', methods=['GET'])
def projects():
    all_projects = lutils.get_list_of_projects()
    if all_projects is None:
        all_projects = dict()
    return render_template("projects.html", data={'projects': all_projects})


@project_app.route('/projects/new', methods=['POST'])
def new_project():
    errors = []

    project_id = request.form["project_id"]
    if not project_id:
        errors.append("Project Id seems to be empty")

    project_path = request.form["project_path"]

    if "use_gitignore" in request.form:
        use_gitignore = request.form["use_gitignore"]
    else:
        use_gitignore = "off"

    if not os.path.isdir(project_path):
        print("Not a valid path to dir")
        errors.append("The path to directory is invalid")

    if use_gitignore == "on":
        if not os.path.isfile(project_path + '/.gitignore'):
            errors.append("You specify to use gitignore, but gitignore is not present in specified directory")
    else:
        if not os.path.isfile(project_path + '/.vayuignore'):
            open(project_path + '/.vayuignore', 'w')

    details = dict()
    details["path"] = project_path
    details["use_gitignore"] = use_gitignore

    if not errors:
        try:
            created_id = lutils.add_new_project(project_id, details)
        except ValueError as e:
            errors.append(str(e))

    if not errors:
        return make_response(created_id, 200)
    else:
        v = VayuException(400, "Please correct the errors", errors)
        return make_response(v.to_json(), 400)


@project_app.route("/projects/delete", methods=['POST'])
def delete_project():
    """
    Delete a project with particular id
    :return:
    """
    project_id = request.form["project_id"]
    lutils.delete_project(project_id)

    return make_response("Success", 200)


@project_app.route("/<uuid>", methods=['POST'])
def deploy_project(uuid):
    """
    Deploy a project with particular id
    :return:
    """
    project_id = request.form["project_id"]
    project_path = request.form["project_path"]
    futils.moveProject(machine_info , project_path , project_id)
    futils.deployNodeJs(machine_info,project_id,"app.js")
    return make_response("Success", 200)


@project_app.route('/projects/<project_id>')
@project_app.route('/projects/<project_id>/overview')
def project_overview(project_id):
    return render_template("project_overview.html")


@project_app.route('/projects/<project_id>/fleet')
def project_fleet(project_id):
    fleet_details = lutils.get_fleet_details(project_id)
    if not fleet_details:
        fleet_details = dict()
    return render_template("project_fleet.html", data={constants.FLEET: fleet_details})


@project_app.route('/projects/<project_id>/new-data-center', methods=['POST'])
def new_data_center(project_id):
    """
    Adds a new data center for the given project id
    :param project_id:
    :return:
    """
    errors = []
    data_center_id = request.form[constants.DATA_CENTER_ID]
    if not data_center_id:
        errors.append("Data Center ID seems to be empty")

    data_center_name = request.form[constants.DATA_CENTER_NAME]
    if not data_center_name:
        errors.append("Data Center Name seems to be empty")

    center_details = dict()
    center_details[constants.DATA_CENTER_ID] = data_center_id
    center_details[constants.DATA_CENTER_NAME] = data_center_name

    if not errors:
        try:
            lutils.add_new_data_center(project_id, center_details)
        except ValueError as e:
            errors.append(str(e))

    if not errors:
        return make_response("OK", 200)
    else:
        v = VayuException(400, "Please correct the errors", errors)
        return make_response(v.to_json(), 400)


@project_app.route('/projects/<project_id>/delete-data-center', methods=['POST'])
def delete_data_center(project_id):
    """
    This method deletes a data center associated with a particular project_id
    :param project_id:
    :return:
    """
    data_center_id = request.form[constants.DATA_CENTER_ID]
    if data_center_id:
        lutils.delete_data_center(project_id, data_center_id)

    return make_response("OK", 200)


@project_app.route('/projects/<project_id>/host/new', methods=['POST'])
def add_new_host_to_data_center(project_id):
    """
    Adds a new host to the data center associated with the project
    :param project_id:
    :return:
    """
    errors = []

    data_center_id = request.form[constants.DATA_CENTER_ID]
    host_id = request.form[constants.HOST_ID]
    host_alias = request.form[constants.HOST_ALIAS]
    auth_method = request.form[constants.AUTH_METHOD]
    host_auth_user = request.form[constants.HOST_AUTH_USER]
    host_auth_password = request.form[constants.HOST_AUTH_PASSWORD]

    req = dict()
    req[constants.HOST_ID] = host_id
    req[constants.HOST_ALIAS] = host_alias
    req[constants.AUTH_METHOD] = auth_method
    req[constants.HOST_AUTH_USER] = host_auth_user
    req[constants.HOST_AUTH_PASSWORD] = host_auth_password

    errors = lutils.validate_new_host_details(req)

    if not data_center_id:
        errors.append("Data Center ID cannot be empty")

    req[constants.DATA_CENTER_ID] = data_center_id

    host_details_known = request.form[constants.HOST_DETAILS]
    if host_details_known != 'true':
        errors.append("You must connect with the Host before adding it permanently")

    # TODO Implement SSH key based login as well. See upvoted answer to a stackoverflow question

    if not errors:
        try:
            hid = lutils.add_new_host(host_id, req)
            lutils.add_host_to_data_center(project_id, data_center_id, host_id)
        except ValueError, e:
            errors.append(str(e))

    if not errors:
        return make_response("OK", 201)
    else:
        v = VayuException(400, "Please Correct the errors", errors)
        return make_response(v.to_json(), v.status_code)


@project_app.route('/hosts', methods=['GET'])
def get_host_list():
    """
    Returns the list of all configured hosts.
    This endpoint is usually used by client side by an AJAX call
    :return: 
    """
    hosts = lutils.get_list_of_hosts()

    return make_response(jsonify(hosts), 200)
