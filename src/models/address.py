from models.field import Field


class Address(Field):
    def __init__(self, address: str):
        self.value = address
