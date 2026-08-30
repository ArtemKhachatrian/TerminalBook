# TerminalBook

TerminalBook is a command-line personal assistant written in Python.

The application provides two main features:

* **Address Book** — manage contacts, phone numbers, and birthdays.
* **Notebook** — create, edit, search, delete, and organize notes using labels.

All data is stored locally using Python `pickle`, so contacts and notes remain available after restarting the application.

---

## Features

### Address Book

* Add new contacts.
* Add multiple phone numbers to a contact.
* Change an existing phone number.
* Remove contacts.
* Search contacts by name or part of a name.
* Add birthdays to contacts.
* Display birthdays.
* Find upcoming birthdays.
* Automatically move weekend birthday congratulations to Monday.
* Validate phone numbers and birthdays.

### Notebook

* Create notes.
* Edit notes.
* Delete notes.
* Search notes by text.
* Add multiple labels to notes.
* Search notes by labels.
* Sort notes by labels.
* Display all notes.

### Data Persistence

The application automatically saves data to local `.pkl` files when the program is closed:

```text
addressbook.pkl
notebook.pkl
```

The data is loaded automatically when the application starts.

---

## Technologies

* Python 3.10+
* Object-Oriented Programming
* `collections.UserDict`
* `datetime`
* `pickle`
* Regular expressions / input validation
* Command-line interface (CLI)

---

## Project Structure

```text
TerminalBook/
│
├── main.py
├── models.py
├── address_book.py
├── notebook.py
├── storage.py
│
├── addressbook.pkl
├── notebook.pkl
│
├── .gitignore
└── README.md
```

### Main files

**`main.py`**

Contains the CLI, command handlers, input processing, and the main application loop.

**`models.py`**

Contains the main data models:

* `Field`
* `Name`
* `Phone`
* `Birthday`
* `Record`
* `Note`

**`address_book.py`**

Contains the `AddressBook` class and contact-related operations.

**`notebook.py`**

Contains the `Notebook` class and note-related operations.

**`storage.py`**

Responsible for saving and loading application data using `pickle`.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ArtemKhachatrian/TerminalBook.git
```

Enter the project directory:

```bash
cd TerminalBook
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

No external dependencies are currently required.

---

## Running the Application

Start the application with:

```bash
python main.py
```

You should see:

```text
Welcome to the assistant bot!
Enter a command:
```

---

# Commands

## General

| Command | Description        |
| ------- | ------------------ |
| `hello` | Display a greeting |
| `close` | Save data and exit |
| `exit`  | Save data and exit |

---

# Address Book Commands

## Add a contact

```text
add John 1234567890
```

Result:

```text
Contact added.
```

If the contact already exists, the phone number is added to the existing contact.

---

## Add another phone number

```text
add John 0987654321
```

Result:

```text
Contact updated.
```

---

## Show contact phones

```text
phone John
```

Example:

```text
Contact name: John, phones: 1234567890; 0987654321
```

---

## Change a phone number

```text
change John 1234567890 1111111111
```

Result:

```text
Contact updated.
```

---

## Display all contacts

```text
all
```

Example:

```text
All contacts:
Contact name: John, phones: 1111111111; 0987654321
Contact name: Alice, phones: 2222222222
```

---

## Search contacts

The search supports partial and case-insensitive matching.

```text
search joh
```

This can find:

```text
John
Johnny
Johnson
```

---

## Delete a contact

```text
delete John
```

Result:

```text
Contact 'John' successfully deleted.
```

---

## Add a birthday

```text
add-birthday John 15.09.1995
```

The required format is:

```text
DD.MM.YYYY
```

---

## Show a birthday

```text
show-birthday John
```

Example:

```text
1995-09-15
```

---

## Find upcoming birthdays

By default, the application checks the next 7 days:

```text
birthdays
```

A custom period can also be specified:

```text
birthdays 30
```

This searches for birthdays occurring within the next 30 days.

If a birthday falls on Saturday or Sunday, the congratulation date is moved to Monday.

---

# Notebook Commands

## Create a note

```text
note shopping
```

The application will ask for the note text:

```text
Enter note text: Buy milk and bread
```

Then it asks whether labels should be added:

```text
Want to add labels? yes
```

Enter labels separated by commas:

```text
Print your labels: shopping,buy,food
```

Result:

```text
Note saved.
```

---

## Show a note

```text
show-note shopping
```

Example:

```text
Buy milk and bread [Labels: shopping, buy, food]
```

---

## Display all notes

```text
all-notes
```

Example:

```text
All notes:
shopping: Buy milk and bread [Labels: shopping, buy, food]
work: Finish Python homework [Labels: python, work, study]
```

---

## Search notes by text

```text
find-note python
```

The search is case-insensitive and supports partial text matching.

For example:

```text
find-note homework
```

can find:

```text
Finish Python homework
```

---

## Search notes by label

```text
find-label shopping
```

Multiple labels can be searched simultaneously:

```text
find-label shopping food
```

The current implementation uses **OR logic**: a note is returned if it contains at least one of the requested labels.

---

## Sort notes by label

```text
sort-label
```

Example:

```text
food:
shopping: Buy milk and bread [Labels: shopping, buy, food]

python:
work: Finish Python homework [Labels: python, work, study]

shopping:
shopping: Buy milk and bread [Labels: shopping, buy, food]

work:
work: Finish Python homework [Labels: python, work, study]
```

A note with multiple labels appears in each corresponding label group.

---

## Edit a note

```text
edit-note shopping
```

The application allows you to change:

* note text;
* note labels.

Labels are entered using commas:

```text
groceries,food,shopping
```

---

## Delete a note

```text
delete-note shopping
```

Result:

```text
Note deleted.
```

---

# Input Validation

The application validates user input.

### Phone numbers

A phone number must:

* contain exactly 10 characters;
* contain digits only.

Valid:

```text
1234567890
```

Invalid:

```text
123456789
12345678901
12345abcde
```

### Birthdays

The required format is:

```text
DD.MM.YYYY
```

Valid:

```text
15.09.1995
```

Invalid:

```text
15-09-1995
1995.09.15
31.02.1995
```

---

# Error Handling

Most command handlers use a common input error decorator.

Incorrect input is handled without terminating the application:

```text
Input error. Incorrect data, please input data
```

The application continues running and waits for the next command.

---

# Data Storage

TerminalBook uses Python's `pickle` module for local data persistence.

The following files are created automatically:

```text
addressbook.pkl
notebook.pkl
```

They contain the serialized `AddressBook` and `Notebook` objects.

These files should normally be excluded from Git:

```gitignore
*.pkl
.venv/
__pycache__/
.idea/
```

---

# Example Session

```text
Welcome to the assistant bot!

Enter a command: add John 1234567890
Contact added.

Enter a command: add John 0987654321
Contact updated.

Enter a command: add-birthday John 15.09.1995
Birthday added.

Enter a command: phone John
Contact name: John, phones: 1234567890; 0987654321

Enter a command: search joh
Contact name: John, phones: 1234567890; 0987654321

Enter a command: note shopping
Enter note text: Buy milk and bread
Want to add labels? yes
Print your labels: shopping,buy,food
Note saved.

Enter a command: find-label shopping
Buy milk and bread [Labels: shopping, buy, food]

Enter a command: all-notes
All notes:
shopping: Buy milk and bread [Labels: shopping, buy, food]

Enter a command: exit
Good bye!
```

---

# Architecture

The project separates responsibilities between several classes.

```text
                    TerminalBook
                         │
              ┌──────────┴──────────┐
              │                     │
        AddressBook              Notebook
              │                     │
           Record                  Note
              │
       ┌──────┼──────┐
       │      │      │
      Name  Phone  Birthday
```

`main.py` handles user interaction, while the model and collection classes contain the application logic.

---

# Future Improvements

Possible future improvements include:

* Better support for full names containing multiple words.
* More advanced contact search.
* Search contacts by phone number.
* Search notes by multiple labels using AND logic.
* Improved date handling for February 29 birthdays.
* Export/import data in JSON format.
* Unit tests.
* More detailed command help.
* Automatic note title generation.
* Improved CLI interface.

---

## License

This project is intended as an educational Python project.
