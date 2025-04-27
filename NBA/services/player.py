# class Player:
#     def __init__(self, id, first_name, last_name, position):
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.position = position
#
#     def __str__(self):
#         return f"Player{{id={self.id}, firstName='{self.first_name}', lastName='{self.last_name}', position='{self.position}'}}"



from home.services.strategies.player_favorite_strategy import PlayerFavoriteStrategy

class Player:
    def __init__(self, id, first_name, last_name, position, favorite_strategy=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.favorite_strategy = favorite_strategy or PlayerFavoriteStrategy()

    def favorite(self):
        self.favorite_strategy.favorite(self)

    def unfavorite(self):
        self.favorite_strategy.unfavorite(self)
