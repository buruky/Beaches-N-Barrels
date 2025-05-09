import sqlite3
import os

def initialize_enemy_db(db_path="db/enemies.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Drop the table to reset the data each time
    cursor.execute("DROP TABLE IF EXISTS enemy_data")
    
    cursor.execute("""
        CREATE TABLE enemy_data (
            enemy_type TEXT PRIMARY KEY,
            attack INTEGER,
            health INTEGER,
            speed INTEGER
        )
    """)
    
    # Insert default enemy data
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('Pirate', 20, 1, 2)")
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('Crab', 10, 1, 10)")
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('BeachBall', 20, 60, 3)")
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('Seagull', 30, 15, 1)")
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('Shark', 25, 1000, 2)")
    cursor.execute("INSERT INTO enemy_data (enemy_type, attack, health, speed) VALUES ('Barrel', 30, 500, 2)")
    
    connection.commit()
    connection.close()
