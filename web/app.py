""" Employee API. """

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
import exceptions


# todo: write docstrings in all modules
# todo: separate post method into small functions
# todo: test api

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
    "index",
    "guid",
    "isActive",
    "balance",
    "company",
    "registered",
    "range",
    "id"
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
    "favoriteFruit"
]


class Employee(Resource):
    """ Employee data class. """
    def post(self):
        data_json = request.get_json()
        global company_employee_keys
        global personal_employee_keys

        try:
            data = helper.id_key_config(data_json)
        except KeyError:
            return jsonify({"message": "please enter '_id' key", "code": HTTPStatus.BAD_REQUEST})

        for dictionary in data:
            try:
                helper.validate_schema(schema, dictionary)
            except SchemaError as ex:
                return jsonify(
                    {
                        "message": ex.args[0],
                        "code": HTTPStatus.BAD_REQUEST
                    }
                )
            company_data, personal_data = helper.company_personal_lists_generator(
                dictionary, company_employee_keys, personal_employee_keys
            )

            try:
                company_object = CompanyEmployeeData(*company_data)
                personal_object = PersonalEmployeeData(*personal_data)
            except exceptions.DataException as ex:
                return jsonify({"message": ex.args[0], "code": ex.args[1]})

            is_ok, status = helper.find_validate_email(dictionary, personal_object)
            if not is_ok:
                return jsonify({"message": status[0], "code": status[1]})

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
