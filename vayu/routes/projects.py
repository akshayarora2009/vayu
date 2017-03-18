from flask import Blueprint, render_template, request, make_response
import os
import vayu.core.local_utils as lutils
from vayu.core.VayuException import VayuException

project_app = Blueprint('project_app', __name__)


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

