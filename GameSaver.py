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

        save_data = game_world.to_dict()  # Serialize entire GameWorld

        try:
            with open(cls.SAVE_FILE, "wb") as file:
                pickle.dump(save_data, file)
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")

    @classmethod
    def load_game(cls):
        """Loads the entire game state from a save file."""
        if not os.path.exists(cls.SAVE_FILE):
            print("No saved game found.")
            return None

        try:
            with open(cls.SAVE_FILE, "rb") as file:
                save_data = pickle.load(file)
                
            game_world = GameWorld.getInstance()
            game_world.load_from_dict(save_data)  # Restore game world
            
            print("Game loaded successfully!")
            game_world.loadWorld()
            return game_world
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
