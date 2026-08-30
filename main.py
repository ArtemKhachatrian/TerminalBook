from difflib import get_close_matches

from address_book import AddressBook
from models import Record, Note
from notebook import Notebook
from storage import load_data, save_data


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (ValueError, IndexError) as error:
            return str(error)

    return inner


@input_error
def parse_input(user_input: str):
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
        return "The contact has not been changed.Incorrect name."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def add_email(args, book: AddressBook):
    name, email = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_email(email)

    return (
        f"Email '{email}' added "
        f"to contact '{name}'."
    )


@input_error
def add_address(args,book: AddressBook):
    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    address = " ".join(args[1:])

    if not address.strip():
        raise ValueError(
            "Address cannot be empty."
        )

    record.add_address(address)

    return (
        f"Address added to contact "
        f"'{name}'."
    )


@input_error
def show_phone(args, book: AddressBook):
    name = " ".join(args)

    record = book.find(name)

    if record is None:
        return (
            "The contacts do not contain "
            "the specified user."
        )

    return str(record)


def show_all(args, book: AddressBook):
    if not book:
        return "No contacts found."

    result = ["All contacts:"]

    for record in book.values():
        result.append(str(record))

    return "\n".join(result)


def hello(args,book: AddressBook):
    return "How can I help you?"


@input_error
def add_birthday(args,book: AddressBook):
    name, birthday = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args,book: AddressBook):
    name = " ".join(args)

    record = book.find(name)

    if record is None:
        return "Contact not found."

    return record.show_birthday()


@input_error
def birthdays(args,book: AddressBook):
    days = int(args[0]) if args else 7

    if days < 0:
        raise ValueError(
            "Number of days cannot be negative."
        )

    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return "No upcoming birthdays."

    result = []

    for item in upcoming:
        result.append(
            f"{item['name']}: "
            f"{item['congratulation_date']}"
        )

    return "\n".join(result)


@input_error
def create_note(args,notebook: Notebook):
    name = args[0]

    if notebook.find(name) is not None:
        return (
            "A note with this name "
            "already exists."
        )

    text = input("Enter note text: ")

    add_label = input(
        "Want to add labels? "
    )

    label = []

    if add_label.lower() == "yes":
        label = input(
            "Print your labels: "
        ).split(",")

        label = [
            item.strip()
            for item in label
            if item.strip()
        ]

    note = Note(text, label)

    notebook.add(name, note)

    return "Note saved."


@input_error
def edit_note(args,notebook: Notebook):
    name = args[0]

    note = notebook.find(name)

    if note is None:
        return "No such note."

    print(f"Current note: {note}")

    new_text = input(
        "Type your changes: "
    )

    if new_text.strip():
        note.edit(text=new_text)

    change_label = input(
        "Want to change labels? "
    )

    if change_label.lower() == "yes":
        new_label = input(
            "Print your labels: "
        ).split(",")

        new_label = [
            item.strip()
            for item in new_label
            if item.strip()
        ]

        note.edit(label=new_label)

    return "Note updated."


@input_error
def show_note(args,notebook: Notebook):
    name = args[0]

    note = notebook.find(name)

    if note is None:
        return "No such note."

    return str(note)


@input_error
def find_note(args,notebook: Notebook):
    query = " ".join(args).lower()

    if not query:
        return "Enter text to search for."

    result = []

    for name, note in notebook.items():
        if query in note.text.lower():
            result.append(
                f"{name}: {note}"
            )

    if not result:
        return "No notes found."

    return "\n".join(result)


@input_error
def find_by_label(args,notebook: Notebook):
    labels = {
        label.lower()
        for label in args
        if label.strip()
    }

    if not labels:
        return "Enter a label to search for."

    result = []

    for name, note in notebook.items():
        note_labels = {
            label.lower()
            for label in note.label
        }

        if labels & note_labels:
            result.append(
                f"{name}: {note}"
            )

    if not result:
        return "No notes found."

    return "\n".join(result)


@input_error
def sort_notes_by_label(args,notebook: Notebook):
    sorted_notes = notebook.sort_by_label()

    if not sorted_notes:
        return "No notes found."

    result = []

    for label, notes in sorted_notes.items():
        result.append(f"\n{label}:")

        for name, note in notes:
            result.append(
                f"{name}: {note}"
            )

    return "\n".join(result)


@input_error
def delete_note(args,notebook: Notebook):
    name = " ".join(args)

    if notebook.delete(name):
        return "Note deleted."

    return "No such note."


@input_error
def show_all_notes(args,notebook: Notebook):
    if not notebook:
        return "No notes found."

    result = ["All notes:"]

    for name, note in notebook.items():
        result.append(
            f"{name}: {note}"
        )

    return "\n".join(result)


@input_error
def search_contact(args,book: AddressBook):
    if not args:
        return (
            "Enter a name or part "
            "of a name to search for."
        )

    query = " ".join(args)

    found_records = book.search_by_name(query)

    if not found_records:
        return (
            f"Contacts related to the "
            f"search query '{query}' not found."
        )

    return "\n".join(
        str(record)
        for record in found_records
    )


@input_error
def delete_contact(args,book: AddressBook):
    if not args:
        return (
            "Enter the name of the contact "
            "you want to delete."
        )

    name = " ".join(args)

    if book.delete(name):
        return (
            f"Contact '{name}' "
            f"successfully deleted."
        )

    return (
        f"Contact with the name "
        f"'{name}' not found."
    )


contact_handlers = {
    "add": add_contact,
    "change": change_contact,
    "add-email": add_email,
    "add-address": add_address,
    "phone": show_phone,
    "all": show_all,
    "hello": hello,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "search": search_contact,
    "delete": delete_contact,
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


def suggest_command(command: str) -> str:
    all_commands = (
            list(contact_handlers)
            + list(note_handlers)
            + ["hello", "close", "exit"]
    )

    matches = get_close_matches(
        command,
        all_commands,
        n=1,
        cutoff=0.5
    )

    if matches:
        return (
            f"Invalid command. "
            f"Did you mean '{matches[0]}'?"
        )

    return "Invalid command."


def main():
    book = load_data("addressbook.pkl")

    if book is None:
        book = AddressBook()

    notebook = load_data("notebook.pkl")

    if notebook is None:
        notebook = Notebook()

    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input(
                "Enter a command: "
            )

            if not user_input.strip():
                continue

            command, *args = parse_input(
                user_input
            )

            if command in ("close", "exit"):
                break

            if command in contact_handlers:
                result = contact_handlers[command](
                    args,
                    book
                )
                print(result)
                continue

            if command in note_handlers:
                result = note_handlers[command](
                    args,
                    notebook
                )
                print(result)
                continue
            print(suggest_command(command))
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        save_data(
            book,
            "addressbook.pkl"
        )

        save_data(
            notebook,
            "notebook.pkl"
        )

        print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()
