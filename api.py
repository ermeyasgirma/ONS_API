from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Please add a case_id"


@app.route("/<case_id>")
def get_case_id(case_id):
    
