from flask import Flask, render_template
from flask import make_response
import core.constants.local as constants
import core.local_utils as lutils

from vayu.routes.projects import project_app
from vayu.core.VayuException import VayuException
app = Flask(__name__)
app.register_blueprint(project_app)


@app.route('/')
def home():
    lutils.make_sure_vayu_root_exists()
    return render_template("index.html")


@app.route('/deployments')
def deployments():
    return render_template("deployments.html")


@app.route('/monitoring')
def monitoring():
    return render_template("monitoring.html")


@app.errorhandler(VayuException)
def some_error_occurred(error):
    return make_response(error.to_json(), error.status_code)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
