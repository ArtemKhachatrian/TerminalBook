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

    def get_upcoming_birthdays(self, days = 7):
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

            if 0 <= days_until_birthday <= days:
                if birthday.isoweekday() == 6:
                    birthday += timedelta(days=2)
                elif birthday.isoweekday() == 7:
                    birthday += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": birthday.strftime("%Y.%m.%d")
                })

        return result
    
    
    
    def search_by_name(self, query: str):
        # Шукає контакти, ім'я яких містить пошуковий запит (нечутливо до регістру)
        query = query.lower()
        results = []
        for name, record in self.data.items():
            if query in name.lower():
                results.append(record)
        return results

    def delete_record(self, name: str) -> bool:
        # Видаляє контакт за іменем. Повертає True, якщо видалено, і False, якщо не знайдено
        if name in self.data:
            del self.data[name]
            return True
        return False