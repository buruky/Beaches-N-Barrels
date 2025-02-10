import pygame
from Controller.MController import MController
from View import *
from Model import *
from typing import Final

pygame.init()
class Run:
    __myView: Final = MView()
    __myController: Final = MController(__myView)
    __myClock: Final = pygame.time.Clock()
    __myRunning = True

    while __myRunning:
        if __myController.ControllerTick() == False:
            __myRunning = False
        __myClock.tick(60)
        __myView.viewTick()

    pygame.quit()

"""
For resident linux user, pls dont delete! :d
python3 -m venv myenv
source myenv/bin/activate
"""