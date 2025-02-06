import pygame
class MainController:
    def ControllerTick():
    #Handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        return 1
    def __init__(self, model):
        self.model = model

    def handle_events(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        self.model.move_player(dx, dy)