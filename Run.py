
import pygame

pygame.init()
class Run:
    def ControllerTick():
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return 0
            elif event.type == MOUSEBUTTONDOWN:
                fist.punch()
            elif event.type is MOUSEBUTTONUP:
                fist.unpunch()
        return 1

    def ViewTick():
        #Draw Everything
        ...

    def main():
        ...
        while 1:

            if ControllerTick() == 0:
                return

            ViewTick()

