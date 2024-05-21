from models.address_book import AddressBook
from models.record import Record
from utils.storage import save_data, load_data
from utils.colorizer import Colorizer
not_found_message = "Contact does not exist, you can add it"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = Colorizer.success("Contact updated.")
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = Colorizer.success("Contact added.")
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        return Colorizer.error("Invalid number of arguments. Usage: change [name] [old_number] [new_number]")
    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message
    else:
        record.edit_phone(old_number, new_number)
        return Colorizer.success("Phone changed")


@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if record is None:
        return not_found_message
    return record

@input_error
def find_contact(args, book: AddressBook):
    if len(args) < 1:
        raise InputError("Contact name/email is missing.")
    
    value = args[0]
    return book.find(value)

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-birthday [name] [date]"
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    else:
        return not_found_message


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        else:
            return "Birthday not added to this contact."
    else:
        return not_found_message


@input_error
def add_email(args, book: AddressBook):
    if len(args) != 2:
        return "Invalid number of arguments. Usage: add-email [name] [email]"
    name, email = args
    record = book.find(name)
    if record:
        if email in [e.value for e in record.emails]:
            return Colorizer.error("Email already exists for this contact.")
        record.add_email(email)
        return Colorizer.success("Email added.")
    else:
        return not_found_message


@input_error
def show_email(args, book: AddressBook):
    if len(args) != 1:
        return Colorizer.error("Invalid number of arguments. Usage: show-email [name]")
    name = args[0]
    record = book.find(name)
    if record:
        if record.emails:
            emails_str = '; '.join(email.value for email in record.emails)
            return f"Emails: {emails_str}"
        else:
            return 'Emails not added to this contact.'
    else:
        return not_found_message


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = load_data()
    print(Colorizer.highlight("Hello! I'm Lana, your personal assistant bot."))
    while True:
        user_input = input(Colorizer.info("Enter a command: "))
        command, *args = parse_input(user_input)

        match command:
            case "hello":
                print("How can I help you?")
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
                print(book)
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(book.get_upcoming_birthdays())
            case "add-email":
                print(add_email(args, book))
            case "show-email":
                print(show_email(args, book))
            case "find-contact":
                print(find_contact(args, book))    
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
