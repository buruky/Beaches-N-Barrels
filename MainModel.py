import pygame
import random

class MainModel:
    def __init__(self):
        self.player_x = 250
        self.player_y = 250
        self.speed = 5

        self.color = (0, 255, 0)  # Initial color (Green)

    def move_player(self, dx, dy):
        self.player_x += dx * self.speed
        self.player_y += dy * self.speed

    def change_color(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))