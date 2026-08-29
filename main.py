from address_book import AddressBook
from models import Record, Note
from storage import load_data, save_data
from notebook import Notebook


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

import re

@input_error
def add_email(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError

    name, email = args

    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format. Must contain '@' and a domain (e.g., user@example.com).")

    record = book.find(name)
    if record is None:
        return "Contact not found."

    record.add_email(email)
    return f"Email '{email}' added to contact '{name}'."


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

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays(int(args[0]))

    if not upcoming:
        return "No upcoming birthdays."

    result = []

    for item in upcoming:
        result.append(
            f"{item['name']}: {item['congratulation_date']}"
        )

    return "\n".join(result)


@input_error
def create_note(args, notebook: Notebook):
    name = args[0]

    if notebook.find(name) is not None:
        return "A note with this name already exists."

    text = input("Enter note text: ")

    add_label = input("Want to add label? ")

    label = []

    if add_label.lower() == "yes":
        label = input("Print your labels: ").split()

    note = Note(text, label)

    notebook.add(name, note)

    return "Note saved."


@input_error
def edit_note(args, notebook: Notebook):
    name = args[0]

    note = notebook.find(name)

    if note is None:
        return "No such note."

    print(f"Current note: {note}")

    new_text = input("Type your changes: ")

    note.edit(text=new_text)

    change_label = input("Want to change label? ")

    if change_label.lower() == "yes":
        new_label = input("Print your labels: ").split()
        note.edit(label=new_label)

    return "Note updated."


@input_error
def show_note(args, notebook: Notebook):
    name = args[0]

    note = notebook.find(name)

    if note is None:
        return "No such note."

    return str(note)


@input_error
def find_note(args, notebook: Notebook):
    query = " ".join(args).lower()

    result = []

    for name, note in notebook.items():
        if query in note.text.lower():
            result.append(f"{name}: {note}")

    if not result:
        return "No notes found."

    return "\n".join(result)


@input_error
def find_by_label(args, notebook: Notebook):
    labels = {label.lower() for label in args}
    result = []

    for name, note in notebook.items():
        note_labels = {
            label.lower()
            for label in note.label
        }
        if labels & note_labels:
            result.append(f"{name}: {note}")

    if not result:
        return "No notes found."

    return "\n".join(result)

@input_error
def sort_notes_by_label(args, notebook: Notebook):
    sorted_notes = notebook.sort_by_label()

    if not sorted_notes:
        return "No notes found."

    result = []

    for label, notes in sorted_notes.items():
        result.append(f"\n{label}:")

        for name, note in notes:
            result.append(f"{name}: {note}")

    return "\n".join(result)


@input_error
def delete_note(args, notebook: Notebook):
    name = args[0]

    if notebook.find(name) is None:
        return "No such note."

    notebook.delete(name)

    return "Note deleted."


def show_all_notes(args, notebook: Notebook):
    if not notebook:
        return "No notes found."

    result = ["All notes:"]

    for name, note in notebook.items():
        result.append(f"{name}: {note}")

    return "\n".join(result)


contact_handlers = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "hello": hello,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}


note_handlers = {
    "note": create_note,
    "edit-note": edit_note,
    "show-note": show_note,
    "find-note": find_note,
    "find-label": find_by_label,
    "sort-label": sort_notes_by_label,
    "delete-note": delete_note,
    "all-notes": show_all_notes,
}


def main():
    book = load_data("addressbook.pkl")

    if book is None:
        book = AddressBook()

    notebook = load_data("notebook.pkl")

    if notebook is None:
        notebook = Notebook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book, "addressbook.pkl")
            save_data(notebook, "notebook.pkl")

            print("Good bye!")
            break

        if command in contact_handlers:
            result = contact_handlers[command](args, book)
            print(result)
            continue

        if command in note_handlers:
            result = note_handlers[command](args, notebook)
            print(result)
            continue

        print("Invalid command.")


if __name__ == "__main__":
    main()
