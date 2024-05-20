import pickle

from address_book import AddressBook

FILE_PKL = "addressbook.pkl"


def save_data(book, filename=FILE_PKL):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename=FILE_PKL):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
