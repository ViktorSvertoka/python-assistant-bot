import random
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

from models.address_book import AddressBook
from models.record import Record
from models.notes import Notes
from utils.storage import save_data, load_data
from utils.colorizer import Colorizer

not_found_message = "Contact does not exist, you can add it"

# List of tips
tips = [
    "Smile!!!",
    "Do 10 squats!!!",
    "Hold a plank for a minute!!!",
    "Take 5 deep breaths!!!",
    "Shake your body for a minute!!!",
    "Dance for 5 minute!!!"
]

# Command counter
command_count = 0
tip_interval = 5  # tip after every 5 commands


commands = [
    "hello",
    "exit",
    "close",
    "add-contact",
    "all-contacts",
    "change-contact",
    "find-contact",
    "delete-contact",
    "show-phone",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "show-email",
    "change-email",
    "delete-email",
    "add-address",
    "show-address",
    "delete-address",
    "add-note",
    "change-note",
    "delete-note",
    "find-note-by-title",
    "find-note-by-tag",
    "show-all-notes"
]


def get_contact_names(book):
    return [record.name.value for record in book.data.values()]


class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        buffer = text.split()

        if not buffer:
            options = commands[:]  # Show all commands
        else:
            cmd = buffer[0]  # Get the command typed so far

            if cmd == 'change-contact':
                if len(buffer) == 2:  # Suggest contact names
                    contact_names = get_contact_names(book)
                    options = [
                        name for name in contact_names if name.startswith(buffer[1])]
                elif len(buffer) == 3:  # Suggest field options
                    options = ['phone', 'email', 'name', 'birthday']
                else:
                    options = []
            elif cmd in {'find-contact', 'show-address', 'delete-contact', 'show-phone', 'add_birthday', 'show-birthday', 'add-email', 'show-email', 'delete-email', 'add-address', 'delete-address'} and len(buffer) == 2:
                contact_names = get_contact_names(book)
                options = [
                    name for name in contact_names if name.startswith(buffer[1])]
            else:
                # Show commands that start with the typed text
                options = [
                    command for command in commands if command.startswith(buffer[-1])]

        for option in options:
            yield Completion(option, start_position=-len(buffer[-1]))


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return Colorizer.error(str(e))
        except Exception as error:
            return Colorizer.error(str(error))
    return inner


def give_tip():
    return Colorizer.warn(random.choice(tips))


def complete(text, state):
    contacts = [record.name.value for record in book.data.values()]
    matches = [c for c in contacts if c.startswith(text)]
    return matches[state] if state < len(matches) else None


@input_error
def add_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 2:
        return Colorizer.error("Invalid number of arguments. Usage: add [name] [phone]")

    name, phone = args
    record = book.find(name)
    message = Colorizer.success("Contact updated.")
    if not isinstance(record, Record):
        record = Record(name)
        book.add_record(record)
        message = Colorizer.success("Contact added.")
    if phone:
        record.add_phone(phone)

    if command_count % tip_interval == 0:
        message += "\n" + give_tip()

    return message


@input_error
def all_contacts(book: AddressBook):
    global command_count
    command_count += 1
    if not book.data:
        return Colorizer.warn("No contacts found. You can add some.")
    if command_count % tip_interval == 0:
        return str(book) + "\n" + give_tip()
    return book


@input_error
def change_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 4:
        return Colorizer.error("Invalid number of arguments. Usage: change-contact [name] [field] [old_value] [new_value]")

    name, field, old_value, new_value = args
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message

    field = field.lower()
    if field == "phone":
        try:
            record.edit_phone(old_value, new_value)
        except ValueError as e:
            return Colorizer.error(str(e))
    elif field == "email":
        try:
            record.edit_email(old_value, new_value)
        except ValueError as e:
            return Colorizer.error(str(e))
    elif field == "name":
        try:
            record.change_name(new_value)
        except ValueError as e:
            return Colorizer.error(str(e))
    elif field == "birthday":
        try:
            record.add_birthday(new_value)
        except ValueError as e:
            return Colorizer.error(str(e))
    else:
        return Colorizer.error(f"Field '{field}' is not supported. Use 'phone', 'email', 'name', or 'birthday'.")

    if command_count % tip_interval == 0:
        return Colorizer.success(f"{field.capitalize()} changed") + "\n" + give_tip()
    return Colorizer.success(f"{field.capitalize()} changed")


@input_error
def show_phone(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: show-phone [name]")
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if record.phones:
        phones_str = (
            "Phones: " +
            "; ".join(p.value for p in record.phones)
        )
        return phones_str

    else:
        return Colorizer.error("Phone number not found for this contact.")


@input_error
def find_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) < 1:
        return Colorizer.error("Contact name/email is missing.")

    value = args[0]
    if command_count % tip_interval == 0:
        return str(book.find(value)) + "\n" + give_tip()
    return book.find(value)


@input_error
def delete_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: delete-contact [name]")

    name = args[0]
    record = book.find(name)
    if record:
        book.delete_contact(name)
        if command_count % tip_interval == 0:
            return Colorizer.success(f"Contact '{name}' successfully deleted") + "\n" + give_tip()
        return Colorizer.success(f"Contact '{name}' successfully deleted")
    else:
        return Colorizer.warn(f"No contact with the name '{name}' exists")


@input_error
def add_birthday(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 2:
        return Colorizer.error("Invalid number of arguments. Usage: add-birthday [name] [DD.MM.YYYY]")
    name, date = args
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message

    if record.birthday:
        return Colorizer.error("Birthday already exists for this contact. Use 'change-birthday' to modify it.")

    try:
        record.add_birthday(date)
        if command_count % tip_interval == 0:
            return Colorizer.success("Birthday added.") + "\n" + give_tip()
        return Colorizer.success("Birthday added.")
    except ValueError as e:
        return Colorizer.error(str(e))


@input_error
def show_birthday(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if record.birthday:
        smiley = "🎂"
        formatted_birthday = record.birthday.value.date().strftime("%d.%m.%Y")
        if command_count % tip_interval == 0:
            return f"{smiley} {formatted_birthday}" + "\n" + give_tip()
        return f"{smiley} {formatted_birthday}"
    if command_count % tip_interval == 0:
        return Colorizer.warn("Birthday not added to this contact.") + "\n" + give_tip()
    return Colorizer.warn("Birthday not added to this contact.")


@input_error
def birthdays(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1 or not args[0].isdigit():
        return Colorizer.error("Invalid arguments. Usage: birthdays [the number of days from today's date]")
    days_from_today = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthdays(days_from_today)

    if command_count % tip_interval == 0:
        return upcoming_birthdays + "\n" + give_tip()
    return upcoming_birthdays


@input_error
def add_email(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 2:
        return Colorizer.error("Invalid number of arguments. Usage: add-email [name] [email]")
    name, email = args
    record = book.find(name)
    if not isinstance(record, Record):
        return Colorizer.error("Contact not found.")
    if email in [e.value for e in record.emails]:
        return Colorizer.error("Such email already exists for this contact.")
    record.add_email(email)
    if command_count % tip_interval == 0:
        return Colorizer.success("Email added.") + "\n" + give_tip()
    return Colorizer.success("Email added.")


@input_error
def show_email(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: show-email [name]")
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if record.emails:
        emails_str = '; '.join(email.value for email in record.emails)
        if command_count % tip_interval == 0:
            return f"Emails: {emails_str}" + "\n" + give_tip()
        return f"Emails: {emails_str}"
    if command_count % tip_interval == 0:
        return Colorizer.warn('Emails not added to this contact.') + "\n" + give_tip()
    return Colorizer.warn('Emails not added to this contact.')


@input_error
def change_email(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 3:
        return Colorizer.error("Invalid number of arguments. Usage: change-email [name] [old_email] [new_email]")
    name, old_email, new_email = args
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if old_email not in [e.value for e in record.emails]:
        return Colorizer.error("Such email does not exist for this contact.")
    record.edit_email(old_email, new_email)
    message = Colorizer.success("Email changed.")
    if command_count % tip_interval == 0:
        message += "\n" + give_tip()
    return message

@input_error
def delete_email(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if not isinstance(record, Record):
            return not_found_message
        if record.emails:
            record.emails = []
            if command_count % tip_interval == 0:
                return Colorizer.success("Emails deleted for this contact.") + "\n" + give_tip()
            return Colorizer.success("Emails deleted for this contact.")
        else:
            return Colorizer.warn("No emails to delete for this contact.")

    elif len(args) == 2:
        name, email = args
        record = book.find(name)
        if not isinstance(record, Record):
            return not_found_message
        if email not in [e.value for e in record.emails]:
            return Colorizer.error("Email does not exist for this contact.")
        record.delete_email(email)
        if command_count % tip_interval == 0:
            return Colorizer.success("Email deleted.") + "\n" + give_tip()
        return Colorizer.success("Email deleted.")

    else:
        return Colorizer.error("Invalid number of arguments. Usage: delete-email [name] [email]")

@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        return "Invalid number of arguments. Usage: add-address [name] [address]"
    
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not isinstance(record, Record):
        return "Contact not found."
    if record.address and record.address == address:
        return f"Address '{address}' already exists for this contact."
    record.add_address(address)
    return "Address added."

@input_error
@input_error
def delete_address(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: delete-address [name]")

    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return Colorizer.warn(f"No contact with the name '{name}' exists")

    if record.address:
        record.delete_address()
        if command_count % tip_interval == 0:
            return Colorizer.success("Address deleted.") + "\n" + give_tip()
        return Colorizer.success("Address deleted.")
    else:
        return Colorizer.error("Address not found for this contact.")


@input_error
def show_address(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: show-address [name]")
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if record.address:
        if command_count % tip_interval == 0:
            return f"Address: {record.address}" + "\n" + give_tip()
        return f"Address: {record.address}"
    if command_count % tip_interval == 0:
        return Colorizer.warn("Address not added to this contact.") + "\n" + give_tip()
    return Colorizer.warn("Address not added to this contact.")


@input_error
def add_note(notes: Notes):
    title = input(Colorizer.highlight("Enter a title: "))

    if notes.find_note_by_title(title):
        return Colorizer.error(f"Note with title '{title}' already exists.")
    text = input(Colorizer.highlight("Enter a text: "))
    tags = input(Colorizer.highlight("Enter tags (comma separated): "))
    try:
        notes.add_note(title, text, tags)
        return Colorizer.success(f"Note with title: '{title}' successfully added.")
    except ValueError as e:
        return Colorizer.error(str(e))


@input_error
def delete_note(notes: Notes):
    title = input(Colorizer.highlight("Enter a title: "))
    note = notes.find_note_by_title(title)
    if note:
        notes.notes.remove(note)
        if notes.find_note_by_title(title):
            return Colorizer.error(f"Note with title: '{title}' not found.")
        else:
            return Colorizer.success(f"Note with title: '{title}' successfully deleted.")
    else:
        return Colorizer.error(f"Note with title: '{title}' not found.")


@input_error
def change_note(notes: Notes):
    title = input(Colorizer.highlight("Enter a title: "))
    new_content = input(Colorizer.highlight("Enter new content: "))
    new_tags = input(Colorizer.highlight("Enter new tags: "))

    note = notes.find_note_by_title(title)

    if note:
        if new_content:
            note.content = new_content

        if new_tags:
            note.tags = [tag.strip() for tag in new_tags.split(",")]

        return Colorizer.success(f"Note with title '{title}' successfully edited.")
    else:
        return Colorizer.error(f"Note with title '{title}' not found.")


@input_error
def find_note_by_title(notes: Notes):
    title = input(Colorizer.highlight("Enter the title to search for: "))
    note = notes.find_note_by_title(title)
    if note:
        return note
    else:
        return Colorizer.error(f"Note with title '{title}' not found.")


@input_error
def find_note_by_tag(notes: Notes):
    tag = input(Colorizer.highlight("Enter the tag to search for: "))
    notes_with_tag = notes.find_note_by_tag(tag)
    if notes_with_tag:
        return "\n".join(str(note) for note in notes_with_tag)
    else:
        return Colorizer.error(f"No notes found with tag '{tag}'.")


@input_error
def show_all_notes(notes: Notes):
    return notes.show_all_notes()


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    global command_count
    global book
    book, notes = load_data()
    session = PromptSession()
    completer = CommandCompleter()
    print(Colorizer.highlight(
        "Hello! I'm Lana, your personal assistant bot. Smile!😃 Today is the best day ever!"))

    while True:
        user_input = session.prompt(
            "Enter a command: ", completer=completer)
        if not user_input.strip():
            print(Colorizer.warn("Please enter a command."))
            continue
        
        command, *args = parse_input(user_input)

        match command:
            case "hello":
                command_count += 1
                print("How can I help you?")
                if command_count % tip_interval == 0:
                    print(give_tip())
            case "close" | "exit":
                save_data(book, notes)
                print(Colorizer.highlight("Good bye!👋"))
                break
            case "add-contact":
                print(add_contact(args, book))
            case "all-contacts":
                print(all_contacts(book))
            case "change-contact":
                print(change_contact(args, book))
            case "show-phone":
                print(show_phone(args, book))
            case "find-contact":
                print(find_contact(args, book))
            case "delete-contact":
                print(delete_contact(args, book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(args, book))
            case "add-email":
                print(add_email(args, book))
            case "show-email":
                print(show_email(args, book))
            case "change-email":
                print(change_email(args, book))
            case "delete-email":
                print(delete_email(args, book))
            case "add-address":
                print(add_address(args, book))
            case "delete-address":
                print(delete_address(args, book))    
            case "show-address":
                print(show_address(args, book))
            case "add-note":
                print(add_note(notes))
            case "delete-note":
                print(delete_note(notes))
            case "change-note":
                print(change_note(notes))
            case "find-note-by-title":
                print(find_note_by_title(notes))
            case "find-note-by-tag":
                print(find_note_by_tag(notes))
            case "show-all-notes":
                print(show_all_notes(notes))
            case _:
                command_count += 1
                print("Invalid command.")
                if command_count % tip_interval == 0:
                    print(give_tip())


if __name__ == "__main__":
    main()
