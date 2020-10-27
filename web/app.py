from flask import jsonify, Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from exceptions import SchemaError
from datetime import datetime
from resources.CompanyEmployeeData import CompanyEmployeeData
from resources.PersonalEmployeeData import PersonalEmployeeData
from http import HTTPStatus
import json
import helper

# todo: write docstrings in all modules

app = Flask(__name__)
api = Api(app)

mongo_client = MongoClient("mongodb://db:27017")
db = mongo_client.EmployeeData
personal = db["Personal"]
company = db["Company"]

schema = {}
with open("schema.json", "r") as f:
    schema = json.load(f)

company_employee_keys = [
    "_id",
    "index",
    "guid",
    "isActive",
    "balance",
    "company",
    "registered",
    "range",
]

personal_employee_keys = [
    "picture",
    "age",
    "eyeColor",
    "name",
    "phone",
    "address",
    "about",
    "latitude",
    "longitude",
    "tags",
    "friends",
    "greeting",
    "favoriteFruit",
]


class Employee(Resource):
    def post(self):
        data = request.get_json()
        global company_employee_keys
        global personal_employee_keys
        # todo: separate this into small functions

        for dictionary in data:
            company_data = []
            personal_data = []
            try:
                helper.validate_schema(schema, dictionary)
            except SchemaError as ex:
                return jsonify({"message": ex.args[0], "code": HTTPStatus.BAD_REQUEST})

            for key in dictionary.keys():
                # keys validation
                if key in company_employee_keys:
                    company_data.append(dictionary.get(key))
                if key in personal_employee_keys:
                    personal_data.append(dictionary.get(key))

            try:
                company_object = CompanyEmployeeData(*company_data)
                personal_object = PersonalEmployeeData(*personal_data)
            except ValueError as ex:
                return jsonify({"message": ex.args[0], "code": ex.args[1]})

            for key, value in dictionary.items():
                # iterate thru inner dictionary
                if key == "email":
                    try:
                        # calling email setter
                        personal_object.email_set(value, dictionary["company"])
                    except ValueError as ex:
                        return jsonify({"message": ex.args[0], "code": ex.args[1]})

            all_personal_dicts, all_company_dicts = helper.generate_data(
                personal_employee_keys, company_employee_keys,
                personal_object, company_object
            )
            personal.insert(all_personal_dicts)
            company.insert(all_company_dicts)

        return jsonify({"message": "data saved in database successfully", "code": HTTPStatus.OK})


api.add_resource(Employee, "/employee_data")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
