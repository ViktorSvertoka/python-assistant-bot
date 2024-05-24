from models.phone import Phone
from models.name import Name
from models.birthday import Birthday
from models.email import Email
from models.address import Address
from utils.colorizer import Colorizer


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

    def __str__(self):
        divider_str = "*" * 20
        emails_str = (
            "Emails: " +
            "; ".join(e.value for e in self.emails) if self.emails else ""
        )
        birthday_str = (
            f"Birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
            if self.birthday
            else ""
        )
        phones_str = (
            "Phones: " +
            "; ".join(p.value for p in self.phones) if self.phones else ""
        )
        address_str = f"Address: {self.address.value}" if isinstance(self.address, Address) else ""

        contact_info_parts = [
            divider_str,
            f"Contact name: {self.name.value}",
            phones_str,
            emails_str,
            birthday_str,
            address_str,
            divider_str,
        ]
        contact_info = "\n".join(part for part in contact_info_parts if part)
        return contact_info

    def add_phone(self, number: str):
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        self.phones = list(
            filter(lambda phone: phone.value != number, self.phones))

    def edit_phone(self, old_number: str, new_number: str):
        found = False

        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                found = True
                break
        if not found:
            raise KeyError(
                Colorizer.error(
                    "The specified number does not exist or the contact has no phone numbers."
                )
            )

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone

    def delete_contact(self, name):
        del self.data[name]

    def change_name(self, new_name):
        self.name = Name(new_name)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_email(self, email):
        self.emails.append(Email(email))

    def edit_email(self, old_email, new_email):
        for email in self.emails:
            if email.value == old_email:
                email.value = new_email
                return
        raise ValueError(f"Email '{old_email}' not found in contact.")

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

    def add_address(self, address):
        self.address = Address(address)

    def delete_address(self):
        self.address = None