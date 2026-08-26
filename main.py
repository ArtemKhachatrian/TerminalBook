from address_book import AddressBook
from models import Record
from storage import load_data, save_data


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Input error. Incorrect data, please input data"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()

    cmd = cmd.strip().lower()

    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        return "The contact has not been changed. Incorrect name."

    record.edit_phone(old_phone, new_phone)

    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]

    record = book.find(name)

    if record is None:
        return "The contacts do not contain the specified user."

    return str(record)


def show_all(args, book: AddressBook):
    if not book:
        return "No contacts found."

    result = ["All contacts:"]

    for record in book.values():
        result.append(str(record))

    return "\n".join(result)


def hello(args, book: AddressBook):
    return "How can I help you?"


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    return record.show_birthday()


def birthdays(args, book: AddressBook):
    upcoming = book.birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    result = []

    for item in upcoming:
        result.append(
            f"{item['name']}: {item['congratulation_date']}"
        )

    return "\n".join(result)


handlers = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "hello": hello,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}


def main():
    book = load_data()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break

        handler = handlers.get(command)

        if handler:
            print(handler(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
