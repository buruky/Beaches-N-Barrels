import pygame

COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
print("hehehe")
class MController:
    
    def __init__(self, player, view):
        self.keyHold = False
        self.player = player
        self.view = view
        pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)

        
    def ControllerTick(self):
        self.__handle_keyboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == COLOR_CHANGE_EVENT:
                self.view.myPlayerSprite.changeColor()
        return True
    
    def __handle_keyboard(self):
        """Handles keyboard input for moving the player rectangle."""
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1

        #updates both model and view
        self.player.movePlayer(dx, dy)
        self.view.myPlayerSprite.updatePosition(dx,dy)

        
