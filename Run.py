import pygame
from Controller.MController import MController
from View import *
from Model import *
from typing import Final

pygame.init()
class Run:
    __myController: Final = MController()
    __myClock: Final = pygame.time.Clock()
    __myRunning = True
    while __myRunning:
        if __myController.ControllerTick() == False:
            __myRunning = False
        __myClock.tick(60)

    pygame.quit()

"""
For resident linux user, pls dont delete! :d
python3 -m venv myenv
source myenv/bin/activate
"""