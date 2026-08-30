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
            return True
        return False
    def search_by_name(self, query: str) -> list[Record]:
        query = query.lower()
        return [
            record
            for name, record in self.data.items()
            if query in name.lower()
        ]

    def get_upcoming_birthdays(self, days: int = 7):
        today = datetime.now().date()
        result = []

        for record in self.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            congratulation_date = birthday

            if congratulation_date.isoweekday() == 6:
                congratulation_date += timedelta(days=2)

            elif congratulation_date.isoweekday() == 7:
                congratulation_date += timedelta(days=1)

            days_until_congratulation = (
                    congratulation_date - today
            ).days

            if 0 <= days_until_congratulation <= days:
                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })

        return result
