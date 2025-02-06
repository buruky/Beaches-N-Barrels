import pygame

COLOR_CHANGE_EVENT = pygame.USEREVENT + 1

class MainController:
    
    def __init__(self, model):
        self.model = model
        pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)

        
    def ControllerTick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            #     self.handle_keyboard(event)
            elif event.type == COLOR_CHANGE_EVENT:
                self.model.change_color()  # Change the rectangle's color when the event fires
        self.handle_keyboard()
        return True
    
    def handle_keyboard(self):
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

        self.model.move_player(dx, dy)
    

        
