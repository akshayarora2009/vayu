from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/deployments')
def deployments():
    return render_template("deployments.html")


@app.route('/monitoring')
def monitoring():
    return render_template("monitoring.html")

if __name__ == "__main__":
    app.run("0.0.0.0")
