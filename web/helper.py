""" Validator and helper for employee data. """

from http import HTTPStatus
from exception_messages import (
    schema_errors, error_messages, schema_exceptions
)
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json import dumps, loads
from copy import copy
from datetime import datetime
import re
import validators
import exceptions


def validate_schema(schema: dict, data: dict) -> None:
    """ JSON schema validation.

    Arguments:
        schema {dict}: valid dictionary
        data {dict}: dictionary for validation

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


def name_validation(value: dict) -> dict:
    """ Employee name validation.

    Arguments:
        value {dict}: dictionary with first and last name

    Raises:
        NameException: if dictionary is not valid

    Returns:
        value {dict}: if dictionary is valid

    Note:
        example:
            {'first': 'John', 'last': 'Doe'} is valid

            {'first': 'John'} is not valid
            {'last': 'Doe'} is not valid
            {'f': 'John', 'l': 'Doe'} is not valid
    """
    first = value.get("first", None)
    last = value.get("last", None)
    if not(first and last):
        raise exceptions.NameException(
            "'name' must contain 'first' and 'last' fields",
            HTTPStatus.BAD_REQUEST
        )
    return value


def balance_validation(value: str) -> bool:
    """ Employee balance validation.

    Arguments:
        value {str}: balance in string format (dollar sign at the beginning)

    Raises:
        BalanceException: if balance is not valid

    Returns:
        value_num {float}: balance value in float format if value is valid

    Note:
        example:
            '$1,234.12' is valid
            '$3,000.00' is valid
            '$5,127' is valid

            '1,234.12' is not valid
            '€1,456.00' is not valid
            '$123456' is not valid
    """
    if value[0] != "$":
        # dollar is expected currency
        raise exceptions.BalanceException(
            f"invalid currency (expected '$', not {value[0]})",
            HTTPStatus.BAD_REQUEST
        )

    try:
        # ! work in python 3+
        value_num = float(value[1:].replace(",","_"))
    except ValueError:
        raise exceptions.BalanceException(
            "balance is not valid", HTTPStatus.BAD_REQUEST
        ) from None
    else:
        return value_num


def phone_validation(value: str) -> str:
    """ Eployee phone number validation.

    Arguments:
        value {str}: phone number for validation

    Raises:
        PhoneException: if phone number is not valid

    Returns:
        value {str}: phone number if phone number is valid

    Note:
        example:
            '+1 (234) 456-7890' is valid
            '+1 (234)456-7890' is valid
            '+12 (234) 456-7890' is valid

            '+1 234 456-7890' is not valid
    """
    for num in value:
        if num == " ":
            # we expect that phone number start with call number
            # and take index of first space after call number
            index_call_number = value.index(num)
            break
    # phone number without call number
    phone_number = value[index_call_number:]

    # format of phone number without call number
    regex = re.compile("\(\d{3}\)\d{3}-\d{4}")

    # removing all spaces
    if re.search(regex, value[index_call_number:].replace(" ", "")):
        return value
    # if phone number does not match to regex format
    raise exceptions.PhoneException(
        "phone number is not in valid format", HTTPStatus.BAD_REQUEST
    )


def picture_validation(value: str) -> str:
    """ Employee picture validation.

    Arguments:
        value {str}: picture's url

    Raises:
        PictureException: if url is not valid

    Returns:
        value {str}: picture's url if url is valid
    """
    valid = validators.url(value)
    if valid == True:
        return value
    raise exceptions.PictureException(
        "url for picture is not valid", HTTPStatus.BAD_REQUEST
    )


def address_validation(value: str) -> str:
    """ Employee address validation.

    Arguments:
        value {str}: address for validation

    Raises:
        AddressException: if address is not valid

    Returns:
        value {str}: address if addres is valid

    Note:
        address is valid if it has numbers in it
    """
    has_numbers = bool(re.search(r"\d", value))
    # validation is based on checking if there are numbers in address
    if not has_numbers:
        raise exceptions.AddressException(
            "address is not valid, please enter numbers in it", HTTPStatus.BAD_REQUEST
        )
    return value


def email_validation(value: str, company_name: str) -> str:
    """ Employee email address validation.

    Arguments:
        value {str}: email address for validation
        company_name {str}: company name for current employee

    Raises:
        EmailException: if email address is not valid

    Returns:
        value {str}: email address if email address is valid

    Note:
        examples:
            'john.doe@microsoft.com' is valid if company name is Microsoft
            'johndoe@schneider.org' is valid if company name is Schneider
    """
    company_lower = company_name.lower()
    local_part = value.split("@")[0]

    email_companies = _email_generator(
        company_lower,
        "org",
        "co.uk",
        "com",
        "io",
        "biz",
        "tv",
        "me",
        "info",
        "net",
        "us"
    )

    for email in email_companies:
        email = local_part + email
        if email == value:
            return value

    raise exceptions.EmailException(
        f"email you sent is not valid, you sent {value}, company is {company_name}",
        HTTPStatus.BAD_REQUEST
    )


def _email_generator(company_lower: str, *args) -> list:
    """ Generate email addres by given company name and domain (without local part).

    Arguments:
        company_lower {str}: companyu name in lower case
        args: additional arguments (domains)

    Returns:
        list with valid email address (without local part)

    Note:
        example:
            company_lower = 'fiat'
            args[0] = '.com'
            list_return = ['@fiat.com']
    """
    return ["@" + company_lower + "." + arg for arg in args]


def latitude_longitude_validation(value: str, caller_name: str) -> str:
    """ Validation for latitude and longitude.

    Arguments:
        value {str}: value for latitude and longitude
        caller_name {str}: name of method that is callig function

    Raises:
        LatitudeLongitudeException: if latitude or longitude is not valid

    Returns:
        value {float}: if latitude or longitude is valid (can be converted to float)
    """
    try:
        value = float(value)
    except ValueError:
        raise exceptions.LatitudeLongitudeException(
            f"'{caller_name}' is not valid", HTTPStatus.BAD_REQUEST
        ) from None
    else:
        return value


def register_validation(value: str) -> datetime:
    """ Employee register date validation.

    Arguments:
        value {str}: date in string format

    Raises:
        ValueError: if date format is invalid

    Returns:
        register date converted to datetime format
    """
    try:
        registered = datetime.strptime(value, "%A, %B %d, %Y %I:%M %p")
    except ValueError:
        raise exceptions.RegisterException(
            "invalid date format", HTTPStatus.BAD_REQUEST
        ) from None
    else:
        return registered


def id_key_config(data: list) -> list:
    """ Configuration for id key.

    Arguments:
        data {list}: all data from server

    Returns:
        all data with modified id key ('id' instead of '_id')
    """
    data_return = list()
    dict_return = dict()

    for dict_ in data:
        id_temp = dict_["_id"]

        dict_return = copy(dict_)
        # removing '_id' from shallow copy
        del dict_return["_id"]
        dict_return["id"] = id_temp
        data_return.append(dict_return)

    return data_return


def find_validate_email(dictionary: dict, personal_object: object) -> tuple:
    """ Find email value and call function for validation.

    Arguments:
        dictionary {dict}: dictionary with employee data
        personal_object {object}: PersonalEmployeeData instance

    Returns:
        tuple: boolean value (True if data is valid, False otherwise) and
               exception arguments if ValueError exception occures or
               None if data is valid
    """
    for key, value in dictionary.items():
        if key == "email":
            try:
                personal_object.email_set(value, dictionary.get("company"))
            except exceptions.EmailException as ex:
                return False, ex.args
    return True, None


def company_personal_lists_generator(
    dictionary: dict, company_employee_keys: list, personal_employee_keys: list
) -> tuple:
    """ Generate company and personal lists.

    Arguments:
        dictionary {dict}: dictionary with employee data
        company_employee_keys {list}: all valid employee data keys
        personal_employee_keys {list}: all valid personal data keys

    Returns:
        tuple: list with company data and list with personal data
    """
    company_data = []
    personal_data = []

    for key in dictionary.keys():
        # keys validation
        if key in company_employee_keys:
            company_data.append(dictionary.get(key))
        if key in personal_employee_keys:
            personal_data.append(dictionary.get(key))
    return company_data, personal_data


def generate_data(
    personal_keys: list, company_keys: list,
    personal_object: object, company_object: object
) -> tuple:
    """ Generate all data.

    Arguments:
        personal_keys {list}: all valid personal data keys
        company_keys {list}: all valid company data keys
        personal_object {object}: PersonalEmployeeData instance
        company_object {object}: CompanyEmployeeData instance

    Returns:
        tuple with two dictionaries:
        first with all personal data, second with all company data
    """
    personal_values = personal_object.return_values_personal()
    company_values = company_object.return_values_company()
    
    all_personal_dicts = []
    all_company_dicts = []

    personal_dicts = dict(zip(personal_keys, personal_values))
    company_dicts = dict(zip(company_keys, company_values))
    all_personal_dicts.append(personal_dicts)
    all_company_dicts.append(company_dicts)
    return all_personal_dicts, all_company_dicts
