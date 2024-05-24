from models.address_book import AddressBook
from models.notes import Notes
import pickle

FILE_PKL = "data.pkl"

def save_address_book(address_book, filename=FILE_PKL):
    with open(filename, "wb") as file:
        data = {"address_book": address_book, "notes": []}
        pickle.dump(data, file)

def save_notes(notes, filename=FILE_PKL):
    with open(filename, "rb") as file:
        data = pickle.load(file)
        data["notes"] = notes
        with open(filename, "wb") as file:
            pickle.dump(data, file)

def save_data(address_book, notes, filename=FILE_PKL):
    with open(filename, "wb") as file:
        data = {"address_book": address_book, "notes": notes}
        pickle.dump(data, file)

def load_data(filename=FILE_PKL):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data.get("address_book", AddressBook()), data.get("notes", Notes())
    except FileNotFoundError:
        return AddressBook(), Notes()