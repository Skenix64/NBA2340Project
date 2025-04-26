from NBA.services.player import Player
from NBA.services.team import Team

class NBAEntityFactory:
    @staticmethod
    def create_entity(data: dict, entity_type: str):
        if entity_type == 'player':
            return Player(
                id=data.get('id'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                position=data.get('position', 'Unknown')  # fallback for missing field
            )
        elif entity_type == 'team':
            return Team(
                id=data.get('id'),
                name=data.get('full_name'),
                city=data.get('city', 'Unknown')
            )
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
