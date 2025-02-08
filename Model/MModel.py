import pygame
import random

class MModel:
    def __init__(self):
        self.player_x = 250
        self.player_y = 250
        self.speed = 5

    def move_player(self, dx, dy):  # Initial color (Green)
        
        self.player_x += dx * self.speed
        self.player_y += dy * self.speed

    

