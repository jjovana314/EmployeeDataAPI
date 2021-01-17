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


# todo: write comments
# todo: separate post method into small functions
# todo: test api
# todo: fix bugs!

app = Flask(__name__)
api = Api(app)

mongo_client = MongoClient("mongodb://db:27017")
db = mongo_client.EmployeeData
personal = db["Personal"]
company = db["Company"]

schema = {}
with open("schema.json", "r") as f:
    schema = json.load(f)

# we are separating keys into two lists because they will be sent
# to the classes that has to validate values

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


def schema_validation_caller(schema: dict, curr_dict: dict) -> tuple:
        """ Calling validate_schema function from helper modlue.

        Arguments:
            schema {dict}: schema for validation
            curr_dict {dict}: current dictionary for validation

        Returns:
            tuple with exception's first argument and boolean False value
            if exception occures. Otherwise, we return empty string and
            boolean value True (ie if exception didn't occured)
        """
        try:
            helper.validate_schema(schema, curr_dict)
        except exceptions.SchemaError as ex:
            return ex.args[0], False
        else:
            return "", True


def separate_data(company_data: list, personal_data: list) -> tuple:
    """ Separate data into two different classes.

    Arguments:
        company_data {list}: data that we consider as data important for company
        personal_data {list}: data with user's personal informations

    Returns:
        tuple with exception arguments if data is not valid,
        otherwise, tuple with CompanyEmployeeData instance and
        PersonalEmployeeData instance
    """
    try:
        company_object = CompanyEmployeeData(*company_data)
        personal_object = PersonalEmployeeData(*personal_data)
    except exceptions.DataException as ex:
        return ex.args[0], ex.args[1]
    else:
        return company_object, personal_object


class Employee(Resource):
    """ Employee data class. """
    def post(self):
        data_json = request.get_json()
        global company_employee_keys
        global personal_employee_keys

        # key 'id' needs to be validated in specific way
        # because original 'id' name of key needs to be replaced
        # with '_id' in order to put value in database
        try:
            data = helper.id_key_config(data_json)
        except KeyError:
            return jsonify(
                {"message": "please enter '_id' key", "code": HTTPStatus.BAD_REQUEST}
            )

        # iterate through data and validate all dictionaries
        for dictionary in data:

            result, status = schema_validation_caller(schema, dictionary)
            if status is False:
                return jsonify({"message": result, "code": HTTPStatus.BAD_REQUEST})

            company_data, personal_data = helper.company_personal_lists_generator(
                dictionary, company_employee_keys, personal_employee_keys
            )

            maybe_company_obj, maybe_personal_obj = separate_data(company_data, personal_data)
            if not (isinstance(maybe_company_obj, CompanyEmployeeData) and isinstance(maybe_personal_obj, PersonalEmployeeData)):
                # exception occured, maybe_company_obj and maybe_personal_obj are exception instances
                return jsonify({"message": maybe_company_obj, "code": maybe_personal_obj})

            is_ok, status = helper.find_validate_email(dictionary, maybe_personal_obj)
            if not is_ok:
                return jsonify({"message": status[0], "code": status[1]})

            # prepare all data for database
            all_personal_dicts, all_company_dicts = helper.generate_data(
                personal_employee_keys, company_employee_keys, maybe_personal_obj, maybe_company_obj
            )
            # insert data into database for current dictionary
            personal.insert(all_personal_dicts)
            company.insert(all_company_dicts)

        return jsonify(
            {"message": "data saved in database successfully", "code": HTTPStatus.OK}
        )


api.add_resource(Employee, "/employee_data")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
