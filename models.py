import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Address(Field):
    pass


class Email(Field):
    def __init__(self, value: str):
        pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"

        if not re.fullmatch(pattern, value):
            raise ValueError(
                "Invalid email format."
            )

        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "Phone number must contain 10 digits"
            )

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(
                value,
                "%d.%m.%Y"
            ).date()

        except ValueError:
            raise ValueError(
                "Birthday must be in DD.MM.YYYY format"
            )

        super().__init__(birthday)


class Record:
    def __init__(self,name: str,address: str = ""):
        self.name = Name(name)
        self.address = Address(address)

        self.phones = []
        self.birthday = None
        self.email = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        found = self.find_phone(phone)

        if found is None:
            raise ValueError("Phone number not found")

        self.phones.remove(found)

    def edit_phone(
        self,
        old_phone: str,
        new_phone: str
    ):
        found = self.find_phone(old_phone)

        if found is None:
            raise ValueError(
                "Old phone number not found"
            )

        found.value = Phone(new_phone).value

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item

        return None

    def add_email(self, email: str):
        self.email = Email(email)

    def add_address(self, address: str):
        self.address = Address(address)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday is None:
            return "Birthday is not set"

        return str(self.birthday)

    def __str__(self):
        phones = "; ".join(
            phone.value
            for phone in self.phones
        )

        email = (
            self.email.value
            if self.email
            else "Not set"
        )

        birthday = (
            self.birthday.value
            if self.birthday
            else "Not set"
        )

        address = (
            self.address.value
            if self.address.value
            else "Not set"
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"email: {email}, "
            f"birthday: {birthday}, "
            f"address: {address}"
        )


class Note:
    def __init__(
        self,
        text: str,
        label=None
    ):
        self.text = text
        self.label = (
            label
            if label is not None
            else []
        )

    def edit(
        self,
        text=None,
        label=None
    ):
        if text is not None:
            self.text = text

        if label is not None:
            self.label = label

    def __str__(self):
        if self.label:
            labels = ", ".join(self.label)
            return (
                f"{self.text} "
                f"[Labels: {labels}]"
            )

        return self.text