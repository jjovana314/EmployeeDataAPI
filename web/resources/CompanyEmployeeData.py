from helper import balance_validation
from http import HTTPStatus
from datetime import datetime


class CompanyEmployeeData:
    def __init__(
        self,
        id_: str,
        index: int,
        guid: str,
        is_active: bool,
        balance: str,
        company: str,
        registered: str,
        range_: list,
    ):
        self._id = id_
        self._index = index
        self._guid = guid
        self._is_active = is_active
        self.balance = balance
        self._company = company
        self.registered = registered
        self._range = range_

    @property
    def id_(self):
        return self._id

    @property
    def index(self):
        return self._index

    @property
    def guid(self):
        return self._guid

    @property
    def is_active(self):
        return self._is_active

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: str):
        self.balance = balance_validation(value)

    @property
    def company(self):
        return self._company

    @property
    def registered(self):
        return self._registered

    @registered.setter
    def registered(self, value: str):
        try:
            date_registered = datetime.strptime(value, "%A, %B %d, %Y %I:%M %p")
        except ValueError:
            raise ValueError("invalid date format", HTTPStatus.BAD_REQUEST) from None
        else:
            self.registered = date_registered

    @property
    def range_(self):
        return self._range

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
            f"Date of registration: {self.registered}\nEmployee range: {self.range_}"
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
                self.range_,
            )
        )
