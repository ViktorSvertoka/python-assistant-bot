import pickle
from models.address_book import AddressBook
from models.notes import Notes

FILE_PKL = "data.pkl"


class DataStorage:
    def __init__(self, address_book=None, notes=None):
        self.address_book = address_book if address_book is not None else AddressBook()
        self.notes = notes if notes is not None else Notes()


def save_data(storage, filename=FILE_PKL):
    with open(filename, "wb") as file:
        pickle.dump(storage, file)


def load_data(filename=FILE_PKL):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return DataStorage()
