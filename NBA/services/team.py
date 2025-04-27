# class Team:
#     def __init__(self, id, name, city):
#         self.id = id
#         self.name = name
#         self.city = city
#
#     def __str__(self):
#         return f"Team{{id={self.id}, name='{self.name}', city='{self.city}'}}"



from home.services.strategies.team_favorite_strategy import TeamFavoriteStrategy

class Team:
    def __init__(self, id, name, city, favorite_strategy=None):
        self.id = id
        self.name = name
        self.city = city
        self.favorite_strategy = favorite_strategy or TeamFavoriteStrategy()

    def favorite(self):
        self.favorite_strategy.favorite(self)

    def unfavorite(self):
        self.favorite_strategy.unfavorite(self)

    def __str__(self):
        return f"Team{{id={self.id}, name='{self.name}', city='{self.city}'}}"
