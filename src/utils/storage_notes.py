import pickle

from models.notes import Notes

NOTES_FILE = "notes.pkl"

def save_notes(notes, filename=NOTES_FILE):
    with open(filename, "wb") as file:
        pickle.dump(notes, file)

def load_notes(filename=NOTES_FILE):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return Notes()