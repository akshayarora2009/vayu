from flask import Flask, render_template , request
from flask import make_response, redirect
import core.constants.local as constants
import core.local_utils as lutils
import core.fabric_scripts.utils as futils
from vayu.routes.projects import project_app
from vayu.routes.hosts import hosts_app
from vayu.routes.api import api_app
from vayu.routes.deployment import deployment_app
from vayu.core.VayuException import VayuException
from vayu.core.constants.model import machine_info
from vayu.core.constants.model import project_info
from multiprocessing import Pool

app = Flask(__name__)
app.register_blueprint(project_app)
app.register_blueprint(hosts_app)
app.register_blueprint(api_app)
app.register_blueprint(deployment_app)
machine_info = machine_info("root","139.59.35.6","ahjvayu2017")


@app.route('/')
def home():
    lutils.make_sure_vayu_root_exists()
    return redirect('/projects', 301)

def moveAndDeployProject(machine_info,project_info1):
    #file = open('/home/jatin/PycharmProjects/vayu/file', 'w')
    #futils.assignouterr(file)
    futils.moveProject(machine_info, project_info1)
    futils.deployCode(machine_info, project_info1)


@app.route('/deployments')
def deployments():
	return render_template("deployments.html")

@app.route("/deploy/<project_id>", methods=['POST'])
def deploy_project(project_id):
    """
    Deploy a project with particular id
    :return:
    """
    project = dict()
    project["deployment_language"] = request.form["deployment_language"]
    project["path"] = request.form["project_path"]
    project["id"] = project_id
    project["entry_point"] = request.form["entry_point"]
    project["port_number"] = request.form["port_number"]
    print(str(project))
    project_info1 = project_info(project_id, project["deployment_language"] , project["path"], project["entry_point"], project["port_number"])

    pool = Pool(processes=1) 
    pool.apply_async(moveAndDeployProject, [machine_info,project_info1])
    pool.close()
    return make_response("Success", 200)

@app.route('/monitoring')
def monitoring():
	return render_template("monitoring.html")


def callback():
    print("callback called")
    return make_response("Success", 200)

@app.errorhandler(VayuException)
def some_error_occurred(error):
	return make_response(error.to_json(), error.status_code)

if __name__ == "__main__":
	app.run("0.0.0.0",port=5050, debug=True)



