from collections import UserDict
from datetime import datetime, timedelta

from models import Record


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def birthdays(self):
        return self.get_upcoming_birthdays()

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        result = []

        for record in self.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            birthday = birthday.replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            days_until_birthday = (birthday - today).days

            if 0 <= days_until_birthday <= 7:
                if birthday.isoweekday() == 6:
                    birthday += timedelta(days=2)
                elif birthday.isoweekday() == 7:
                    birthday += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": birthday.strftime("%Y.%m.%d")
                })

        return result