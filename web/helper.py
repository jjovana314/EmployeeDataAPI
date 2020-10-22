""" Validators for employee data. """
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
    # if value[0] != "+" and value[1] != "1":
    #     raise ValueError("phone number has invalid call number", HTTPStatus.BAD_REQUEST)

    # todo: fix regex formating
    regex = r"\(\w{3}\)\w{3}-\w{4}"

    # value[3:] is phone number without call number (+1)
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
    company_org = "@" + company_lower + ".org"
    company_co_uk = "@" + company_lower + ".co.uk"
    company_com = "@" + company_lower + ".com"

    if (
        company_org not in company_lower
        or company_co_uk not in company_lower
        or company_com not in company_lower
    ):
        raise ValueError("email you sent is not valid", HTTPStatus.BAD_REQUEST)
    return value


def latitude_longitude_validation(value: str, caller_name: str) -> str:
    try:
        value = float(value)
    except ValueError:
        raise ValueError(f"'{caller_name}' is not valid", HTTPStatus.BAD_REQUEST)
    else:
        return value
