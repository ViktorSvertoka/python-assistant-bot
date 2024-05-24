from datetime import datetime, timedelta
from collections import UserDict
from utils.colorizer import Colorizer
import sys
import os

# Додаємо шлях до кореневої директорії проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import DATE_FORMAT

class AddressBook(UserDict):

    def __str__(self):
        lines = [str(record) for record in self.data.values()]
        return "\n".join(lines)

    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, value: str):
        for name, record in self.data.items():
            if value == name or any(value == email.value for email in record.emails):
                return record
        return "Contact not found."

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days_from_today):
        today_date = datetime.today().date()
        upcoming_birthdays = []
        divider_str = "*" * 40

        for name, record in self.data.items():
            if record.birthday:
                birthday_date = record.birthday.value.replace(
                    year=today_date.year
                ).date()
                timedelta_days = (birthday_date - today_date).days

                if 0 <= timedelta_days <= days_from_today:
                    birthday_str = birthday_date.strftime(DATE_FORMAT)
                    upcoming_birthdays.append(f"""
{divider_str}
Name: {name}, 
Congratulation date: {birthday_str}
{divider_str}
""")  
        if not upcoming_birthdays:
            return f"\nNo upcoming birthdays within the next {days_from_today} days.\n"
    
        return "\n".join(upcoming_birthdays)             
