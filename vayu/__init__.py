from flask import Flask, render_template , request
from flask import make_response, redirect
import core.constants.local as constants
import core.local_utils as lutils
import core.fabric_scripts.utils as futils
from vayu.routes.projects import project_app
from vayu.routes.hosts import hosts_app
# from vayu.routes.api import api_app
# from vayu.routes.deployment import deployment_app
from vayu.core.VayuException import VayuException
from vayu.core.constants.model import machine_info

app = Flask(__name__)
app.register_blueprint(project_app)
app.register_blueprint(hosts_app)
# app.register_blueprint(api_app)
# app.register_blueprint(deployment_app)

machine_info = machine_info("root","139.59.35.6","ahjvayu2017")

@app.route('/')
def home():
    lutils.make_sure_vayu_root_exists()
    return redirect('/projects', 301)


@app.route('/deployments')
def deployments():
	return render_template("deployments.html")


@app.route('/deployments/<uuid>')
def deployments_uuid(uuid):
    project = dict()
    project["id"] = request.args.get('project_id')
    project["deployment_language"] = request.args.get('deployment_language')
    project["language_version"] = request.args.get('language_version_id')
    project["language_prod"] = request.args.get('language_prod_id')
    project["path"] = "/home/harshita/Documents/test"
    # futils.moveProject(machine_info , project_path , project_id)
    # futils.deployNodeJs(machine_info,project_id,"server.js")
    return render_template("deployments.html" , project = project)
    # futils.moveProject(machine_info , project['path'] , project['id'])
    # futils.deployNodeJs(machine_info, project['id'] ,"server.js")

@app.route("/abc", methods=['POST'])
def deploy_project():
    """
    Deploy a project with particular id
    :return:
    """
    project_id = request.form["project_id"]
    project_path = request.form["project_path"]
    futils.moveProject(machine_info , project_path , project_id)
    futils.deployNodeJs(machine_info,project_id,"server.js")
    return render_template("deployments.html")

@app.route('/monitoring')
def monitoring():
	return render_template("monitoring.html")


@app.errorhandler(VayuException)
def some_error_occurred(error):
	return make_response(error.to_json(), error.status_code)

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
