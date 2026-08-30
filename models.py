from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits")

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format")


class Email(Field):
    pass



class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None  

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        found = self.find_phone(phone)

        if found:
            self.phones.remove(found)

    def edit_phone(self, old_phone: str, new_phone: str):
        found = self.find_phone(old_phone)

        if found is None:
            raise ValueError("Old phone number not found")

        found.value = Phone(new_phone).value

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item

        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday is None:
            return "Birthday is not set"

        return str(self.birthday)

    def add_email(self, email: str):  
        self.email = Email(email)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        email_str = f", email: {self.email.value}" if self.email else ""  

        return f"Contact name: {self.name.value}, phones: {phones}{email_str}"