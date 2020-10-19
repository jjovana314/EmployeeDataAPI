""" Validators for employee data. """
from http import HTTPStatus
import re
import validators


# todo: write documentation


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
    if value[0] != "+" and value[1] != "1":
        raise ValueError("phone number has invalid call number", HTTPStatus.BAD_REQUEST)
    regex = "\(w{3}\)\w{3}-\w{4}"

    if re.search(regex, value[3:].replace(" ", "")):
        return value
    raise ValueError("phone number is not in valid format", HTTPStatus.BAD_REQUEST)


def picture_validation(value: str) -> str:
    valid = validators.url(value)
    if valid == True:
        return value
    raise ValueError("url for picture is not valid", HTTPStatus.BAD_REQUEST)


def address_validation(value: str) -> str:
    def has_numbers(value):
        return bool(re.search(r"\d", value))
    if not has_numbers(value):
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
