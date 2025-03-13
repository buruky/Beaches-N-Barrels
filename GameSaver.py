import pickle
import os
import pprint
from Model.GameWorld import GameWorld

class GameSaver:
    """Handles saving and loading the entire game state."""

    SAVE_FILE = "game_save.pkl"

    @classmethod
    def save_game(cls):
        """Saves the entire game state, including the player, world, and inventory."""
        game_world = GameWorld.getInstance()

        save_data = {
            "world": game_world.to_dict(),  # Serialize entire GameWorld
            "player": game_world.getPlayer().to_dict(),
        }

        try:
            with open(cls.SAVE_FILE, "wb") as file:
                pickle.dump(save_data, file)
            # pprint.pprint(save_data, width=120)  # Pretty-print saved data)
            print(" Game saved successfully!")
        except Exception as e:
            print(f" Error saving game: {e}")

    @classmethod
    def load_game(cls):
        """Loads the entire game state from a save file."""
        if not os.path.exists(cls.SAVE_FILE):
            print(" No saved game found.")
            return None

        try:
            with open(cls.SAVE_FILE, "rb") as file:
                save_data = pickle.load(file)
                
            # pprint.pprint(save_data, width=120)  # Pretty-print saved data)
            game_world = GameWorld.getInstance()
            game_world.load_from_dict(save_data["world"])

            if save_data.get("player"):
                from Model.Player import Player
                game_world.setPlayer(Player.from_dict(save_data["player"]))
            
            print(" Game loaded successfully!")
            return game_world
        except Exception as e:
            print(f" Error loading game: {e}")
            return None