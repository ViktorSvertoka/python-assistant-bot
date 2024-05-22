from models.field import Field

class Title(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Note title cannot be empty.")
        if len(value) > 255:
            raise ValueError("Note title cannot exceed 255 characters.")
        
class Content(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) > 255:
            raise ValueError("Note content cannot exceed 255 characters.")

class Tags(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValueError("Note tags cannot be empty.")
        if len(value) > 255:
            raise ValueError("Note tags cannot exceed 255 characters.")