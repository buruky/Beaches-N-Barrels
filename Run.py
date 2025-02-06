import pygame
from MainController import MainController
from MainView import MainView
from MainModel import MainModel

pygame.init()
class Run:
    model = MainModel()
    view = MainView()
    controller = MainController(model)
    
    # Create a clock object
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        if controller.ControllerTick() == False:
            running = False

        # Limit frame rate to 60 FPS
        clock.tick(60)
        # Render (draw to the screen)
        view.draw(model)  # Render the updated model        

# Quit Pygame
    pygame.quit()
#python3 -m venv myenv
#source myenv/bin/activate