class Player:
    def __init__(self, id, first_name, last_name, position):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position

    def __str__(self):
        return f"Player{{id={self.id}, firstName='{self.first_name}', lastName='{self.last_name}', position='{self.position}'}}"
