""" Validator and helper for employee data. """
from http import HTTPStatus
from exception_messages import (
    schema_errors, error_messages, schema_exceptions
)
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json import dumps, loads
import re
import validators
import exceptions


# todo: write documentation

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


def balance_validation(value: str) -> bool:
    if value[0] != "$":
        raise ValueError(
            f"invalid currency (expected '$', not {value[0]})",
            HTTPStatus.BAD_REQUEST
        )

    try:
        value_num = float(value[1:].replace(",","_"))
    except ValueError:
        raise ValueError("balance is not valid", HTTPStatus.BAD_REQUEST)
    else:
        return value


def phone_validation(value: str) -> str:
    for num in value:
        if num == " ":
            index_call_number = value.index(num)
            break
    # phone number without call number
    phone_number = value[index_call_number:]

    regex = r"\(\w{3}\)\w{3}-\w{4}"

    if re.search(regex, value[3:].replace(" ", "")):
        return value
    raise ValueError("phone number is not in valid format", HTTPStatus.BAD_REQUEST)


def picture_validation(value: str) -> str:
    valid = validators.url(value)
    if valid == True:
        return value
    raise ValueError("url for picture is not valid", HTTPStatus.BAD_REQUEST)


def address_validation(value: str) -> str:
    has_numbers = bool(re.search(r"\d", value))
    if not has_numbers:
        raise ValueError("address is not valid, please enter numbers in it", HTTPStatus.BAD_REQUEST)
    return value


def email_validation(value: str, company_name: str) -> str:
    company_lower = company_name.lower()

    email_companies = email_generator(
        company_lower,
        "org",
        "co.uk",
        "com",
        "io",
        "biz",
        "tv"
    )

    if any(email_companies):
        return value

    raise ValueError(
        (
            f"email you sent is not valid, you sent {value}",
            f" company is {company_name}"
        ),
        HTTPStatus.BAD_REQUEST
    )


def email_generator(company_lower: str, *args, **kwargs) -> list:
    return ["@" + company_lower + "." + arg for arg in args]


def latitude_longitude_validation(value: str, caller_name: str) -> str:
    try:
        value = float(value)
    except ValueError:
        raise ValueError(f"'{caller_name}' is not valid", HTTPStatus.BAD_REQUEST)
    else:
        return value


def generate_data(
    personal_keys: list, company_keys: list,
    personal_object: object, company_object: object
) -> tuple:
    personal_values = personal_object.return_values_personal()
    company_values = company_object.return_values_company()
    
    all_personal_dicts = []
    all_company_dicts = []

    personal_dicts = dict(zip(personal_keys, personal_values))
    company_dicts = dict(zip(company_keys, company_values))
    all_personal_dicts.append(personal_dicts)
    all_company_dicts.append(company_dicts)
    return all_personal_dicts, all_company_dicts
