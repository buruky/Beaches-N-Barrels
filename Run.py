import pygame
from MainController import MainController
from MainView import MainView
from MainModel import MainModel
pygame.init()
class Run:
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))


    model = MainModel()
    view = MainView(screen)
    controller = MainController(model)
    # Create a clock object
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        if MainController.ControllerTick() == 0:
            running = False

        # Limit frame rate to 60 FPS
        clock.tick(60)

        # Render (draw to the screen)
        # ...

        # Update the display
        controller.handle_events()  # Update model based on input
        view.draw(model)  # Render the updated model

# Quit Pygame
    pygame.quit()
#python3 -m venv myenv
#source myenv/bin/activate