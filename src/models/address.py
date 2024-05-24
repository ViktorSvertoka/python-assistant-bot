from models.field import Field
from utils.colorizer import Colorizer


class Address(Field):
    def __init__(self, address: str):
        self.value = self.validate_address(address)

    @staticmethod
    def validate_address(address: str) -> str:
        if not isinstance(address, str):
            raise ValueError(Colorizer.error("Address must be a string."))
        if not (5 <= len(address) <= 100):
            raise ValueError(Colorizer.error(
                "Address must be between 5 and 100 characters long."))
        return address
