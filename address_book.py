from collections import UserDict
from datetime import datetime, timedelta

from models import Record


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True

        return False

    def search_by_name(self,query: str) -> list[Record]:
        query = query.lower()

        results = []

        for name, record in self.data.items():
            if query in name.lower():
                results.append(record)

        return results

    def get_upcoming_birthdays(self,days: int = 7) -> list[dict]:
        today = datetime.now().date()
        result = []

        for record in self.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value

            try:
                birthday = birthday.replace(
                    year=today.year
                )
            except ValueError:
                birthday = birthday.replace(
                    year=today.year,
                    day=28
                )

            if birthday < today:
                try:
                    birthday = birthday.replace(
                        year=today.year + 1
                    )
                except ValueError:
                    birthday = birthday.replace(
                        year=today.year + 1,
                        day=28
                    )

            days_until_birthday = (
                birthday - today
            ).days

            if 0 <= days_until_birthday <= days:
                congratulation_date = birthday

                if birthday.isoweekday() == 6:
                    congratulation_date += timedelta(
                        days=2
                    )

                elif birthday.isoweekday() == 7:
                    congratulation_date += timedelta(
                        days=1
                    )

                result.append({
                    "name": record.name.value,
                    "congratulation_date":
                        congratulation_date.strftime(
                            "%Y.%m.%d"
                        )
                })

        return result