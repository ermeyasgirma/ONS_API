from flask import Flask
import json
from ons_api import mainAPI

app = Flask(__name__)

@app.route("/")
def index():
    return "Please add a case_id"


@app.route("/<case_id>")
def get_case_id(case_id):
    print(case_id)
    mainAPI(str(case_id))
    with open("output.json") as j:
        data = json.load(j)
    return data
