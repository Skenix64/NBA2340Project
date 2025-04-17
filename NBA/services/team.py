class Team:
    def __init__(self, id, name, city):
        self.id = id
        self.name = name
        self.city = city

    def __str__(self):
        return f"Team{{id={self.id}, name='{self.name}', city='{self.city}'}}"
