from models.phone import Phone
from models.name import Name
from models.birthday import Birthday
from models.email import Email


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None

    def __str__(self):
        divider_str = "*" * 20
        emails_str = (
            "Emails: " + "; ".join(e.value for e in self.emails) if self.emails else ""
        )
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else ""
        phones_str = (
            "Phones: " + "; ".join(p.value for p in self.phones) if self.phones else ""
        )

        contact_info = f"""
{divider_str}
Contact name: {self.name.value}
{phones_str}
{emails_str}
{birthday_str}
{divider_str}
"""
        return contact_info

    def add_phone(self, number: str):
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        self.phones = list(filter(lambda phone: phone.value != number, self.phones))

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

    def add_email(self, email):
        self.emails.append(Email(email))

    def delete_email(self, email):
        found_email = False
        email_to_delete = None
        for e in self.emails:
            if e.value == email:
                found_email = True
                email_to_delete = e
                break
        if found_email:
            self.emails.remove(email_to_delete)
        else:
            raise ValueError(
                "The specified email does not exist or the contact has no email addresses."
            )
