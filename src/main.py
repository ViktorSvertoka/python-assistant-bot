import random
import readline
import sys

from models.address_book import AddressBook
from models.record import Record
from models.notes import Notes
from utils.storage import save_data, load_data
from utils.storage_notes import save_notes, load_notes
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
tip_interval = 5 # tip after every 5 commands


commands = [
    "hello",
    "exit",
    "add",
    "change",
    "phone",
    "all",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "show-email",
    "find-contact",
    "delete-contact"
]

def get_contact_names(book):
    return [record.name.value for record in book.data.values()]


def completer(text, state):
    buffer = readline.get_line_buffer().split()
    if len(buffer) == 0:
        options = commands[:]
    else:
        cmd = buffer[0]
        if cmd == 'find-contact' and len(buffer) == 2:
            contact_names = get_contact_names(book)
            options = [name for name in contact_names if name.startswith(text)]
        else:
            options = [command for command in commands if command.startswith(text)]
    
    if state < len(options):
        return options[state]
    else:
        return None
    
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")    




def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)
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
def change_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 3:
        return Colorizer.error("Invalid number of arguments. Usage: change [name] [old_number] [new_number]")
    name, old_number, new_number = args
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    else:
        record.edit_phone(old_number, new_number)
        if command_count % tip_interval == 0:
            return Colorizer.success("Phone changed") + "\n" + give_tip()
        return Colorizer.success("Phone changed")
            


@input_error
def show_phone(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return "Invalid number of arguments. Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if command_count % tip_interval == 0:
        return str(record) + "\n" + give_tip()
    return record

@input_error
def find_contact(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) < 1:
        raise InputError("Contact name/email is missing.")
    
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
    if name in book:
        book.delete(name)
        if command_count % tip_interval == 0:
            return f"Contact '{name}' successfully deleted" + "\n" + give_tip()
        return f"Contact '{name}' successfully deleted"
    else:
        raise KeyError(f"No contact with the name '{name}' exists")
    

@input_error
def add_birthday(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [date]"
    name, date = args
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    record.add_birthday(date)
    if command_count % tip_interval == 0:
        return "Birthday added." + "\n" + give_tip()
    return "Birthday added."
    
        


@input_error
def show_birthday(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if not isinstance(record, Record):
        return not_found_message
    if record.birthday:
            if command_count % tip_interval == 0:
                return record.birthday + "\n" + give_tip()
            return record.birthday
    if command_count % tip_interval == 0:
        return "Birthday not added to this contact." + "\n" + give_tip()
    return "Birthday not added to this contact."
    
        


@input_error
def add_email(args, book: AddressBook):
    global command_count
    command_count += 1

    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-email [name] [email]"
    name, email = args
    record = book.find(name)
    if not isinstance(record, Record):
        return "Contact not found."
    if email in [e.value for e in record.emails]:
        return Colorizer.error("Email already exists for this contact.")
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
        return 'Emails not added to this contact.' + "\n" + give_tip()
    return 'Emails not added to this contact.'




@input_error
def add_note(notes: Notes):
    title = input(Colorizer.highlight("Enter a title: "))
    text = input(Colorizer.highlight("Enter a text: "))
    tags = input(Colorizer.highlight("Enter tags: "))
    try:
        notes.add_note(title, text, tags)
        return Colorizer.success(f"Note with title: '{title}' successfully added.")
    except ValueError as e:
        return Colorizer.error(str(e))





@input_error
def delete_note(notes: Notes):
    title = input(Colorizer.highlight("Enter a title: "))
    notes.delete_note(title)
    if notes.find_note_by_title(title):
        return Colorizer.error(f"Note with title: '{title}' not found.")
    else:
        return Colorizer.success(f"Note with title: '{title}' successfully deleted.")




@input_error
def edit_note(notes: Notes):
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
    



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    global command_count
    global book
    book = load_data()
    notes = load_notes()
    print(Colorizer.highlight("Hello! I'm Lana, your personal assistant bot. Smile! Today is the best day ever!"))
    
    while True:
        user_input = input(Colorizer.info("Enter a command: "))
        command, *args = parse_input(user_input)

        match command:
            case "hello":
                command_count += 1
                print("How can I help you?")
                if command_count % tip_interval == 0:
                    print(give_tip())
            case "close" | "exit":
                save_data(book)
                save_notes(notes)
                print("Good bye!")
                break
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                command_count += 1
                print(book)
                if command_count % tip_interval == 0:
                    print(give_tip())
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                command_count += 1
                print(book.get_upcoming_birthdays())
                if command_count % tip_interval == 0:
                    print(give_tip())
            case "add-email":
                print(add_email(args, book))
            case "show-email":
                print(show_email(args, book))
            case "find-contact":
                print(find_contact(args, book))    
            case "delete-contact":
                print(delete_contact(args, book))
            case "add-note":
                print(add_note(notes))
            case "delete-note":
                print(delete_note(notes))
            case "edit-note":
                print(edit_note(notes)) 
            case _:
                command_count += 1
                print("Invalid command.")
                if command_count % tip_interval == 0:
                    print(give_tip())


if __name__ == "__main__":
    main()
