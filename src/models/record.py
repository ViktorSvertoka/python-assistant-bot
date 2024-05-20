from phone import Phone
from name import Name
from birthday import Birthday


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        contact_info = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

        if self.birthday:
            contact_info += f", birthday: {self.birthday}"

        return contact_info

    def add_phone(self, number: str):
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        self.phones = list(filter(lambda phone: phone == number, self.phones))

    def edit_phone(self, old_number: str, new_number: str):
        found = False

        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                found = True
                break
        if not found:
            raise KeyError(
                "The specified number does not exist or the contact has no phone numbers."
            )

    def find_phone(self, number):

        for phone in self.phones:
            if phone.value == number:
                return phone

    def add_birthday(self, date):
        self.birthday = Birthday(date)
