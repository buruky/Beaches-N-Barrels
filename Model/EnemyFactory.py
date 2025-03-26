from typing import Final
from .Enemy import Enemy
from .Crab import Crab
from .Pirate import Pirate
from .Seagull import Seagull
from .BeachBall import BeachBall
from .Barrel import Barrel
from .Shark import Shark
from .DungeonCharacterList import DungeonCharacterList
from .database import initialize_enemy_db
import sqlite3
import random
from ViewUnits import ViewUnits


class EnemyFactory():
    _instance = None  # Stores the single instance
    _DEFAULT_SPEED:Final = 2
    _DEFAULT_HEALTH:Final = 1
    _DEFAULT_ATTACK_DAMAGE:Final = 1
    
    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(EnemyFactory, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance
    def _init_once(self):
         #pass
         initialize_enemy_db("db/enemies.db")

    def load_enemy_data(self, enemy_type: str):
        """
        Loads enemy stats (attack, health, speed) from the SQL database.
        """
        try:
            connection = sqlite3.connect("db/enemies.db")
            cursor = connection.cursor()
            query = "SELECT attack, health, speed FROM enemy_data WHERE enemy_type = ? LIMIT 1"
            cursor.execute(query, (enemy_type,))
            row = cursor.fetchone()
            connection.close()
            if row:
                return {"attack": row[0], "health": row[1], "speed": row[2], }
        except Exception as e:
            print(f"Error loading enemy data for {enemy_type}: {e}")
        # default
        return {"attack": self._DEFAULT_ATTACK_DAMAGE,
                "health": self._DEFAULT_HEALTH,
                "speed": self._DEFAULT_SPEED}
    ### for creating enemy
    def create_enemy(self, enemy_type: str):
        data = self.load_enemy_data(enemy_type)
        attack = data["attack"]
        health = data["health"]
        speed = data["speed"]
        screen_width = ViewUnits.SCREEN_WIDTH - 150
        screen_height = ViewUnits.SCREEN_HEIGHT -150
        if enemy_type == "Pirate":
            return Pirate(attack, health, random.randint(0,screen_width), random.randint(0, screen_height), speed)
        elif enemy_type == "Crab":
            return Crab(attack, health, random.randint(0,screen_width), random.randint(0, screen_height), speed)
        elif enemy_type == "BeachBall": 
            return BeachBall(attack, health, random.randint(0,screen_width), random.randint(0, screen_height), speed)
        elif enemy_type == "Seagull":
            return Seagull(attack, health, random.randint(0,screen_width), random.randint(0, screen_height), speed)
        elif enemy_type == "Shark":
            return Shark(attack, health, screen_width, screen_height, speed)
        elif enemy_type == "Barrel":
            return Barrel(attack, health, screen_height/2, screen_width/2, speed)

        else:
            return None
    def test_database_connection(self):
        try:
            connection = sqlite3.connect("db/enemies.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM enemy_data")
            rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            connection.close()
        except Exception as e:
            print("Error connecting to database:", e)

    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance
    #### for creating enemy
    def createNormalTemplate(self,num):
        enemyList = DungeonCharacterList()
        enemy_templates = {
        1: ["Crab", "BeachBall"],   # Easy enemies
        2: ["BeachBall","BeachBall"], # just crab
        3: ["Seagull"],  # Seagulls add complexity
        4: ["Seagull", "Seagull"], # Stronger enemies
        5: ["Crab","Crab","BeachBall", "Seagull"],  # High difficulty room
        }
        # Retrieve the enemy names based on difficulty
        if num in enemy_templates:
            for enemy_name in enemy_templates[num]:
                enemyList.add_entity(self.create_enemy(enemy_name))

        return enemyList
    def createBossTemplate(self):
        enemyList = DungeonCharacterList()
        
        enemyList.add_entity(self.create_enemy("Shark"))
        return enemyList
    
    def createKeyTemplate(self):
        enemyList = DungeonCharacterList()
        enemyList.add_entity(self.create_enemy("Barrel"))
        return enemyList