from flask import Flask, render_template
from vayu.fabric_scripts import sample
app = Flask(__name__)


@app.route('/')
def hello():

    return render_template("index.html")

if __name__ == "__main__":
    app.run("0.0.0.0")
