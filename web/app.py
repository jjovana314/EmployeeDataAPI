from flask import jsonify, Flask
from flask_restful import Resources, Api
from pymongo import MongoClient

# todo: write docstrings and comments in all modules
# TODO: finish API

app = Flask(__main__)
api = Api(app)

mongo_client = MongoClient("mongodb:/db:27017")
db = mongo_client.EmployeeData
personal = db["Personal"]
company = db["Company"]


class Employee(Resources):
    def post(self):
        pass


api.add_resource("/employee_data", Employee)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")