from flask import Blueprint, render_template, request, make_response
import os

from vayu.core.VayuException import VayuException

project_app = Blueprint('project_app', __name__)


@project_app.route('/projects', methods=['GET'])
def projects():
    return render_template("projects.html")


@project_app.route('/projects/new', methods=['POST'])
def new_project():
    project_id = request.form["project_id"]
    project_path = request.form["project_path"]

    if "use_gitignore" in request.form:
        use_gitignore = request.form["use_gitignore"]

    if not os.path.isdir(project_path):
        print("not a valid path")
        raise VayuException(400, "Invalid Input")

    if not os.path.isfile(project_path + '/.gitignore'):
        print("gitignore not present")
        vayuignore = file(project_path + '/.vayuignore', 'a+')

    return make_response("ok", 200)
