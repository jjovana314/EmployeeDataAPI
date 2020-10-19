import helper
from http import HTTPStatus


class PersonalEmployeeData:
    def __init__(
        self,
        name: dict,
        phone: str,
        address: str,
        email: str,
        picture: str,
        age: int,
        eye_color: str,
        about: str,
        latitude: str,
        longitude: str,
        tags: list,
        friends: list,
        greeting: str,
        favorite_fruit: str,
    ):
        self._name = name

        self.phone = phone
        self.address = address
        self.email = email
        self.picture = picture

        self._age = age
        self._eye_color = eye_color
        self._about = about

        self.latitude = latitude
        self.longitude = longitude

        self._tags = tags
        self._friends = friends
        self._greeting = greeting
        self._favorite_fruit = favorite_fruit

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    def eye_color(self) -> str:
        return self._eye_color

    @property
    def about(self) -> str:
        return self._about

    @property
    def tags(self) -> list:
        return self._tags

    @property
    def friends(self) -> list:
        return self._friends

    @property
    def greeting(self) -> str:
        return self._greeting

    @property
    def favorite_fruit(self) -> str:
        return self._favorite_fruit

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = helper.phone_validation(value)

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = helper.address_validation(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str, company_name: str) -> None:
        self._email = helper.email_validation(value, company_name)

    @property
    def picture(self) -> str:
        return self._picture

    @picture.setter
    def picture(self, value: str) -> None:
        self._picture = helper.picture_validation(value)

    @property
    def latitude(self) -> str:
        return self._latitude

    @latitude.setter
    def latitude(self, value: str) -> None:
        self._latitude = validators.latitude_longitude_validation(
            value, "latitude"
        )

    @property
    def longitude(self) -> str:
        return self._longitude

    @longitude.setter
    def longitude(self, value: str) -> None:
        self._longitude = helper.latitude_longitude_validation(
            value, "longitude"
        )

    def __repr__(self) -> str:
        return (
            f"{__class__.__name__}(name={self.name}, "
            f"phone={self.phone}, address={self.address}, "
            f"email={self.email}, picture={self.picture}, "
            f"age={self.age}, eye_color={self.eye_color}, "
            f"about={self.about}, latitude={self.latitude}, "
            f"longitude={self.longitude}, tags={self.tags}, "
            f"tags={self.tags}, friends={self.friends}, "
            f"greeting={self.greeting}, favorite_fruit={self.favorite_fruit})"
        )

    def __str__(self) -> str:
        return (
            f"User: {self.name}\nPhone number: {self.phone}\n"
            f"Address: {self.address}\nEmail: {self.email}\n"
            f"Picture: {self.picture}\nAge: {self.age}\n"
            f"Eye color: {self.eye_color}\nAbout: {self.about}\n"
            f"Latitude: {self.latitude}\nLongitude: {self.longitude}\n"
            f"Tags: {self.tags}\nFriends: {self.friends}\nGreeting={self.greeting}\n"
            f"Favorite fruit: {self.favorite_fruit}"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PersonalEmployeeData):
            return False
        return (
            self.name == other.name
            and self.phone == other.phone
            and self.email == other.email
            and self.picture == other.picture
            and self.age == other.age
            and self.eye_color == other.eye_color
            and self.about == other.about
            and self.latitude == other.latitude
            and self.longitude == other.longitude
            and self.tags == other.tags
            and self.friends == other.friends
            and self.greeting == other.greeting
            and self.favorite_fruit == other.favorite_fruit
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.phone,
                self.email,
                self.picture,
                self.age,
                self.eye_color,
                self.about,
                self.latitude,
                self.longitude,
                self.tags,
                self.friends,
                self.greeting,
                self.favorite_fruit,
            )
        )
