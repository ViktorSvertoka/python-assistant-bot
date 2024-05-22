import random

from models.address_book import AddressBook
from models.record import Record
from utils.storage import save_data, load_data
from utils.colorizer import Colorizer

not_found_message = "Contact does not exist, you can add it"

# List of tips
tips = [
    "Smile!",
    "Do 10 squats!",
    "Hold a plank for a minute!",
    "Take 5 deep breaths!",
    "Shake your body for a minute!",
    "Dance for 5 minute!"
]

# Command counter
command_count = 0
tip_interval = 5 # tip after every 5 commands


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)
    return inner

def give_tip():
    return Colorizer.info(random.choice(tips))


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
        return not_found_message
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

        


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    global command_count
    book = load_data()
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
            case _:
                command_count += 1
                print("Invalid command.")
                if command_count % tip_interval == 0:
                    print(give_tip())


if __name__ == "__main__":
    main()
