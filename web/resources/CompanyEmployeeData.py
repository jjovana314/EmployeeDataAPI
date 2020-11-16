from helper import balance_validation, register_validation
from http import HTTPStatus
from datetime import datetime


class CompanyEmployeeData:
    """ Company employee data. """
    def __init__(
        self,
        index: int,
        guid: str,
        is_active: bool,
        balance: str,
        company: str,
        registered: str,
        range_: list,
        id_: str
    ):
        """
        Arguments:
            index {int}: employee index
            guid {str}: globally unique identifier
            is_active {bool}: True if employee is currently active, False otherwise
            balance {str}: balance on employee account
            company {str}: employee company name
            registered {str}: string format date of employment
            range_ {list}: employee range
            id_ {str}: employee id
        """
        self._id = id_
        self._index = index
        self._guid = guid
        self._is_active = is_active
        self.balance = balance
        self._company = company
        self.registered = registered
        self._range = range_

    @property
    def id_(self) -> str:
        """
        Returns:
            str: employee id
        """
        return self._id

    @property
    def index(self) -> int:
        """
        Returns:
            int: employee index
        """
        return self._index

    @property
    def guid(self) -> str:
        """
        Returns:
            str: globally unique identifier
        """
        return self._guid

    @property
    def is_active(self) -> bool:
        """
        Returns:
            bool: True if employee is currently active, False otherwise
        """
        return self._is_active

    @property
    def balance(self) -> float:
        """
        Returns:
            float: converted employee balance
        """
        return self._balance

    @balance.setter
    def balance(self, value: str):
        """
        Arguments:
            value {str}: employee balance value (string format)
        """
        self._balance = balance_validation(value)

    @property
    def registered(self) -> datetime:
        """
        Returns:
            datetime: date of employment
        """
        return self._registered

    @property
    def company(self) -> str:
        """
        Returns:
            str: company name
        """
        return self._company

    @registered.setter
    def registered(self, value: str):
        """
        Arguments:
            value {str}: string format date of employment
        """
        self._registered = register_validation(value)

    @property
    def range_(self) -> list:
        """
        Returns:
            list: employee range
        """
        return self._range

    def return_values_company(self) -> list:
        """
        Returns:
            list: list with all values for current instance
        """
        return [
            self.id_,
            self.index,
            self.guid,
            self.is_active,
            self.balance,
            self.company,
            self.registered,
            self.range_
        ]

    def __repr__(self):
        return (
            f"{__class__.__name__}(id_={self.id_}, "
            f"index={self.index}, guid={self.guid}, "
            f"is_active={self.is_active}, balance={self.balance}, "
            f"company={self.company}, registered={self.registered}, "
            f"range={self.range_})"
        )

    def __str__(self):
        return (
            f"Employee id: {self.id_}\nEmployee index: {self.index}\n"
            f"Guid: {self.guid}\nIs active: {self.is_active}\n"
            f"Employee balance: {self.balance}\nCompany: {self.company}\n"
            f"Date of registration: {self.registered}\nEmployee range: {self.range_}\n"
        )

    def __eq__(self, other):
        if not isinstance(other, CompanyEmployeeData):
            return False
        return (
            self.id_ == other.id_
            and self.index == other.index
            and self.guid == other.guid
            and self.is_active == other.is_active
            and self.balance == other.balance
            and self.company == other.company
            and self.registered == other.registered
            and self.range_ == other.range_
        )

    def __hash__(self):
        return hash(
            (
                self.id_,
                self.index,
                self.guid,
                self.is_active,
                self.balance,
                self.company,
                self.registered,
                self.range_
            )
        )
