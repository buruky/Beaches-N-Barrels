import pygame
import os
from Model.EventManager import EventManager  # Import the event system
from CustomEvents import CustomEvents  # Import custom event names
from ViewUnits import ViewUnits  # Reference existing universal units

class TitleScreen:
    def __init__(self, screen):
        """Initializes the title screen UI with image-based buttons."""
        self.screen = screen
        self.load_assets()  # Load images at startup

        # Define button positions
        button_spacing = ViewUnits.SCREEN_HEIGHT // 8  # Space between buttons
        center_x = (ViewUnits.SCREEN_WIDTH - self.start_image.get_width()) // 2
        start_y = ViewUnits.SCREEN_HEIGHT // 2

        # Create button rects
        self.start_button = pygame.Rect(center_x, start_y, self.start_image.get_width(), self.start_image.get_height())
        self.load_button = pygame.Rect(center_x, start_y + button_spacing, self.load_image.get_width(), self.load_image.get_height())
        self.quit_button = pygame.Rect(center_x, start_y + 2 * button_spacing, self.quit_image.get_width(), self.quit_image.get_height())

    def load_assets(self):
        """Loads all images from the Assets folder."""
        current_directory = os.path.dirname(__file__)
        assets_path = os.path.join(current_directory, '..', 'Assets')

        # Load background
        self.background = pygame.image.load(os.path.join(assets_path, 'Goat.jpg'))
        self.background = pygame.transform.scale(self.background, (ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT))

        # Load title image
        self.title_image = pygame.image.load(os.path.join(assets_path, 'Title.png'))
        self.title_image = pygame.transform.scale(self.title_image, (ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 6))
        self.title_x = (ViewUnits.SCREEN_WIDTH - self.title_image.get_width()) // 2
        self.title_y = ViewUnits.SCREEN_HEIGHT // 6  # Position title at top 1/6th of the screen

        # Load button images
        self.start_image = pygame.image.load(os.path.join(assets_path, 'start.png'))
        self.load_image = pygame.image.load(os.path.join(assets_path, 'Load.png'))
        self.quit_image = pygame.image.load(os.path.join(assets_path, 'exit.png'))

        # Resize buttons if necessary
        button_width = ViewUnits.SCREEN_WIDTH // 4
        button_height = ViewUnits.SCREEN_HEIGHT // 8
        self.start_image = pygame.transform.scale(self.start_image, (button_width, button_height))
        self.load_image = pygame.transform.scale(self.load_image, (button_width, button_height))
        self.quit_image = pygame.transform.scale(self.quit_image, (button_width, button_height))

    def draw(self):
        """Draws the title screen UI elements with images."""
        self.screen.blit(self.background, (0, 0))  # Draw background
        self.screen.blit(self.title_image, (self.title_x, self.title_y))  # Draw title

        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Change button transparency when hovering
        start_img = self.create_hover_effect(self.start_image, self.start_button, mouse_pos)
        load_img = self.create_hover_effect(self.load_image, self.load_button, mouse_pos)
        quit_img = self.create_hover_effect(self.quit_image, self.quit_button, mouse_pos)

        # Draw buttons
        self.screen.blit(start_img, self.start_button.topleft)
        self.screen.blit(load_img, self.load_button.topleft)
        self.screen.blit(quit_img, self.quit_button.topleft)

        pygame.display.flip()

    def create_hover_effect(self, image, button_rect, mouse_pos):
        """Applies transparency effect when the mouse hovers over a button."""
        temp_image = image.copy()
        if button_rect.collidepoint(mouse_pos):
            temp_image.set_alpha(180)  # Slightly transparent when hovered
        else:
            temp_image.set_alpha(255)  # Fully visible otherwise
        return temp_image

    def run(self):
        """Handles the title screen loop and waits for user input."""
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return  # Exit title screen and start game
                    elif self.load_button.collidepoint(event.pos):
                        print("Load button clicked! (No function yet)")  # Placeholder action
                    elif self.quit_button.collidepoint(event.pos):
                        print("Quit button clicked!")  # Debugging line
                        Quit_event = pygame.event.Event(EventManager.event_types[CustomEvents.QUIT])
                        pygame.event.post(Quit_event)
                        exit()