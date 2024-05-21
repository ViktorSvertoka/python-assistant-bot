import re
from models.field import Field


class Email(Field):
    def __init__(self, value: str):
        if self.validate_email(value):
            self.value = value
        else:
            raise ValueError("Invalid email. Please provide a correct email address")

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
