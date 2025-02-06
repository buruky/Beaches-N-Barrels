import pygame
class MainView:
    def __init__(self):
        # self.screen = screen
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw(self, model):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        pygame.draw.rect(self.screen, model.color, (model.player_x, model.player_y, 50, 50))# pygame.display.update()
        pygame.display.flip()  # Update display
