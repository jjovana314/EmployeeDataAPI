import helper
from http import HTTPStatus


class PersonalEmployeeData:
    """ Personal employee data. """
    def __init__(
        self,
        picture: str,
        age: int,
        eye_color: str,
        name: dict,
        phone: str,
        address: str,
        about: str,
        latitude: str,
        longitude: str,
        tags: list,
        friends: list,
        greeting: str,
        favorite_fruit: str
    ):
        """
        Arguments:
            picture {str}: picture's url
            age {str}: employee age
            eye_color {str}: employee eye color
            name {str}: employee name (first and last)
            phone {str}: employee phone number
            address {str}: employee address
            about {str}: some employee data
            latitude {str}: coordinates of employee city
            longitude {str}: coordinates of employee city
            tags {list}: employee labels
            friends {list}: list of employee friends
            greeting {str}: employee greeting message
            favorite_fruit {str}: employee favorite fruit
        """
        self.name = name

        self.phone = phone
        self.address = address
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
        """
        Returns:
            str: employee name
        """
        return self._name

    @name.setter
    def name(self, value: dict) -> None:
        """
        Arguments:
            value {dict}: employee first and last name
        """
        self._name = helper.name_validation(value)

    @property
    def age(self) -> int:
        """
        Returns:
            int: employee age
        """
        return self._age

    @property
    def eye_color(self) -> str:
        """
        Returns:
            str: employee eye color
        """
        return self._eye_color

    @property
    def about(self) -> str:
        """
        Returns:
            str: data about employee
        """
        return self._about

    @property
    def tags(self) -> list:
        """
        Returns:
            list: employee tags
        """
        return self._tags

    @property
    def friends(self) -> list:
        """
        Returns:
            list: employee friend's list ( if he has one 3:) )
        """
        return self._friends

    @property
    def greeting(self) -> str:
        """
        Returns:
            str: employee greeting message
        """
        return self._greeting

    @property
    def favorite_fruit(self) -> str:
        """
        Returns:
            str: employee favorite fruit
        """
        return self._favorite_fruit

    @property
    def phone(self) -> str:
        """
        Returns:
            str: employee phone number
        """
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """
        Arguments:
            value {str}: employee phone number
        """
        self._phone = helper.phone_validation(value)

    @property
    def address(self) -> str:
        """
        Returns:
            str: employee address
        """
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """
        Arguments:
            value {str}: employee address
        """
        self._address = helper.address_validation(value)

    @property
    def email(self) -> str:
        """
        Returns:
            str: employee email address
        """
        return self._email

    def email_set(self, value: str, company_name: str) -> None:
        """
        Arguments:
            value {str}: employee email address
            company_name {str}: employee company name
        """
        self._email = helper.email_validation(value, company_name)

    @property
    def picture(self) -> str:
        """
        Returns:
            str: url of employee picture
        """
        return self._picture

    @picture.setter
    def picture(self, value: str) -> None:
        """
        Arguments:
            value {str}: url of employee picture
        """
        self._picture = helper.picture_validation(value)

    @property
    def latitude(self) -> str:
        """
        Returns:
            str: coordinates of employee city
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value: str) -> None:
        """
        Arguments:
            value {str}: coordinates of employee city
        """
        self._latitude = helper.latitude_longitude_validation(value, "latitude")

    @property
    def longitude(self) -> str:
        """
        Returns:
            str: coordinates of employee city
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value: str) -> None:
        """
        Arguments:
            value {str}: coordinates of employee city
        """
        self._longitude = helper.latitude_longitude_validation(value, "longitude")

    def return_values_personal(self):
        """ Return list with all personal values from class instance. """
        return [
            self.name,
            self.phone,
            self.address,
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
            self.favorite_fruit
        ]

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
            f"Favorite fruit: {self.favorite_fruit}\n"
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
                self.favorite_fruit
            )
        )
