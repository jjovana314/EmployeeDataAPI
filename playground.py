from json import dumps, load, loads
from pprint import pprint
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from exception_messages import schema_errors, error_messages, schema_exceptions
from exceptions import SchemaError
from copy import copy


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
    "favoriteFruit",
]
data = []
schema = []

with open("data_employee.json", "r") as f:
    data = load(f)

with open("web/schema.json", "r") as f:
    schema = load(f)


def id_key_config(data: list):
    data_return = list()
    dict_return = dict()

    for dict_ in data:
        id_temp = dict_["_id"]

        dict_return = copy(dict_)
        del dict_return["_id"]
        dict_return["id"] = id_temp
        data_return.append(dict_return)

    return data_return


def validate_schema(schema: dict, data: dict) -> None:
    """ JSON schema validation.

    Arguments:
        schema {dict} -- valid dictionary
        data {dict} -- dictionary for validation

    Raises:
        SchemaError: if data dictionary is not valid
    """
    # we want json data, so we have to dump our data into json string
    data = dumps(data)
    try:
        # try to do validation for our json data
        validate(loads(data), schema)
    except ValidationError as ex:
        # ! here we do not except JSONDecodeError, remember that!
        ex_str = str(ex)
        for idx, value in enumerate(schema_errors):
            # create appropriate message for user
            # if there is exception occured
            if value in ex_str:
                raise schema_exceptions[idx](error_messages[idx])


# id_key_config(data)
# data_result = id_key_config(data)
# print(id_key_config(data))
# pprint(data_result)
# pprint(data)
# for dict_ in data_result:
    # try:
#     validate_schema(schema, dict_)
    # except SchemaError as ex:
    # print(ex)
d = {
    "_id": "5f88a81b003f97b13fc06493",
    "index": 0,
    "guid": "c02c4b0c-3771-4a7d-9444-50d23fdac1ff",
    "isActive": True,
    "balance": "$2,916.07",
    "picture": "http://placehold.it/32x32",
    "age": 27,
    "eyeColor": "blue",
    "name": {
            "first": "Sadie",
            "last": "Wilder"
    },
    "company": "SLUMBERIA",
    "email": "sadie.wilder@slumberia.co.uk",
    "phone": "+1 (896) 433-2272",
    "address": "776 Micieli Place, Barronett, Massachusetts, 8272",
    "about": "Pariatur tempor aliqua sint ex aute et esse ut non sint occaecat excepteur. Dolore pariatur velit occaecat enim velit excepteur voluptate consectetur ipsum nisi velit voluptate. Qui in culpa enim nostrud ex dolor occaecat adipisicing excepteur et mollit ipsum. Mollit elit minim quis mollit occaecat nostrud cupidatat laborum dolore labore. Sint nostrud aliqua et et ex consectetur duis proident amet deserunt excepteur ullamco.",
    "registered": "Monday, September 8, 2014 2:14 PM",
    "latitude": "77.487876",
    "longitude": "-25.902317",
    "tags": [
        "exercitation",
        "exercitation",
        "mollit",
        "proident",
        "irure"
    ],
    "range": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9
    ],
    "friends": [
        {
            "id": 0,
            "name": "Lilia Whitley"
        },
        {
            "id": 1,
            "name": "Jami Crosby"
        },
        {
            "id": 2,
            "name": "Stafford Dixon"
        }
    ],
    "greeting": "Hello, Sadie! You have 7 unread messages.",
    "favoriteFruit": "strawberry"
}

print(len(d.keys()))
    
# for dict_ in data_result:
#     company_data = []
#     personal_data = []
#     for key in dict_.keys():
#         if key in company_employee_keys:
#             # print("***COMPANY EMPLOYEE DATA***")
#             company_data.append((key, dict_.get(key)))
#         if key in personal_employee_keys:
#             # print("**PRESONAL EMPLOYEE DATA***")
#             personal_data.append((key, dict_.get(key)))
#     # pprint(company_data)
#     pprint(personal_data)
