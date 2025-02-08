import pygame
import random

COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
print("hehehe")
class MController:
    
    def __init__(self, player, view):
        self.player = player
        self.view = view
        self.key_map = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT"
        }
        self.holding_click = False
        self.sign = 1
        self.num1 = random.randint(0, 500)
        self.num2 = random.randint(0, 500)
        pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)
     
    def ControllerTick(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == COLOR_CHANGE_EVENT:
                self.view.myPlayerSprite.changeColor()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:  # press left or right click
                    self.holding_click = True
                    if event.button == 1: 
                        self.sign = 1
                    else:
                        self.sign = -1
                
            elif event.type == pygame.MOUSEBUTTONUP:  # release left or right click
                if event.button == 1 or event.button == 3:
                    self.num1 = random.randint(0, 500)
                    self.num2 = random.randint(0, 500)
                    self.holding_click = False
        
        self.__handle_keyboard()
        self.__handle_mouse(self.sign)
        return True
 
    def __handle_keyboard(self):
        """Handles keyboard input for moving the player rectangle."""
        keys = pygame.key.get_pressed()
        directions = []

        for key, direction in self.key_map.items():
            if keys[key]:
                directions.append(direction)

        #updates both model and view
        self.player.movePlayer(directions)
        
        self.view.myPlayerSprite.updatePosition(self.player.player_x, self.player.player_y)
    
    def __handle_mouse(self, sign):
        if self.holding_click:
            if sign > 0:
                self.player.moveTo(self.num1, self.num2)
                self.view.myPlayerSprite.updatePosition(self.num1, self.num2)
            else:
                self.player.moveTo(0,0)
                self.view.myPlayerSprite.updatePosition(0,0)

        
