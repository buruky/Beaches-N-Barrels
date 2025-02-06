import pygame
class MainView:
    def __init__(self, screen):
        self.screen = screen

    def draw(self, model):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        pygame.draw.rect(self.screen, (0, 255, 0), (model.player_x, model.player_y, 50, 50))
        pygame.display.flip()  # Update display