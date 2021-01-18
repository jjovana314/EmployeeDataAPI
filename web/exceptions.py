""" Exception classes. """

class SchemaError(Exception):
    """ General schema error. """


class TypeSchemaError(SchemaError):
    """ Raised if there is invalid type in data dictionary. """


class RequiredSchemaError(SchemaError):
    """ Raised if there is no required data in dictionary. """


class MinLengthSchemaError(SchemaError):
    """ Raised if length of string in data is less then minimum. """


class MaxLengthSchemaError(SchemaError):
    """ Raised if length of string in data is greater then maximum. """


class MinimumSchemaError(SchemaError):
    """ Raised if value in data is less then minimum. """


class MaximumSchemaError(SchemaError):
    """ Raised if value in data is greater then maximum. """


class EnumSchemaError(SchemaError):
    """ Raised if there is error with enum values from data. """


class DataException(Exception):
    """ General data exception. """


class NameException(DataException):
    """ Raised if employee name is not valid. """


class BalanceException(DataException):
    """ Raised if employee balance is not valid. """


class PhoneException(DataException):
    """ Raised if employee phone is not valid. """


class EmailException(DataException):
    """ Raised if employee email is not valid. """


class LatitudeLongitudeException(DataException):
    """ Raised if employee latitude or longitude is not valid. """


class RegisterException(DataException):
    """ Raised if employee register date is not valid. """


class PictureException(DataException):
    """ Raised if employee picture url is not valid. """


class AddressException(DataException):
    """ Raised if employee address is not valid. """
