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
        self.demo_button = pygame.Rect(center_x, start_y + 2 * button_spacing, self.demo_image.get_width(), self.demo_image.get_height()) 
        self.quit_button = pygame.Rect(center_x, start_y + 3 * button_spacing, self.quit_image.get_width(), self.quit_image.get_height())
        self.guide_button = pygame.Rect(
                    ViewUnits.SCREEN_WIDTH - self.guide_image.get_width() - 20,  # 20px from the right
                    20,  # 20px from the top
                    self.guide_image.get_width(),
                    self.guide_image.get_height()
                )
    def load_assets(self):
        """Loads all images from the Assets folder."""
        current_directory = os.path.dirname(__file__)
        assets_path = os.path.join(current_directory, '..', 'Assets')
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(assets_path, "boom.mp3"))  # Beach wave sound

        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        # Load background
        self.background = pygame.image.load(os.path.join(assets_path, 'Goat.jpg'))
        self.background = pygame.transform.scale(self.background, (ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT))

        # Load title image
        self.title_image = pygame.image.load(os.path.join(assets_path, 'Title.png'))
        self.title_image = pygame.transform.scale(self.title_image, (ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 6))
        self.title_x = (ViewUnits.SCREEN_WIDTH - self.title_image.get_width()) // 2
        self.title_y = ViewUnits.SCREEN_HEIGHT // 6  

        # Load button images
        self.start_image = pygame.image.load(os.path.join(assets_path, 'start.png'))
        self.load_image = pygame.image.load(os.path.join(assets_path, 'Load.png'))
        self.quit_image = pygame.image.load(os.path.join(assets_path, 'exit.png'))
        self.demo_image = pygame.image.load(os.path.join(assets_path, 'demo.png'))
        self.back_image = pygame.image.load(os.path.join(assets_path, 'back.png'))
        self.guide_image = pygame.image.load(os.path.join(assets_path, 'back.png'))  # NEW Guide button image

        # Resize buttons if necessary
        button_width = ViewUnits.SCREEN_WIDTH // 4
        button_height = ViewUnits.SCREEN_HEIGHT // 8
        self.start_image = pygame.transform.scale(self.start_image, (button_width, button_height))
        self.load_image = pygame.transform.scale(self.load_image, (button_width, button_height))
        self.quit_image = pygame.transform.scale(self.quit_image, (button_width, button_height))
        self.demo_image = pygame.transform.scale(self.demo_image, (button_width, button_height))
        self.back_image = pygame.transform.scale(self.back_image, (button_width // 1.5, button_height // 1.5))  
        self.guide_image = pygame.transform.scale(self.guide_image, (button_width, button_height))  # NEW Guide button

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
        demo_img = self.create_hover_effect(self.demo_image, self.demo_button, mouse_pos)  
        guide_img = self.create_hover_effect(self.guide_image, self.guide_button, mouse_pos)  # NEW

        # Draw buttons
        self.screen.blit(start_img, self.start_button.topleft)
        self.screen.blit(load_img, self.load_button.topleft)
        self.screen.blit(demo_img, self.demo_button.topleft)
        self.screen.blit(quit_img, self.quit_button.topleft)
        self.screen.blit(guide_img, self.guide_button.topleft)  # NEW

        pygame.display.flip()

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
                        selected_character = self.character_selection_screen()  
                        if selected_character:
                            return selected_character  
                    elif self.load_button.collidepoint(event.pos):
                        return "Load"  
                    elif self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    elif self.demo_button.collidepoint(event.pos):  
                        selected_character = self.character_selection_screen()  
                        if selected_character:
                            return selected_character + "Demo"  
                    elif self.guide_button.collidepoint(event.pos):  # NEW handle guide button click
                        self.show_guide_screen()

    def show_guide_screen(self):
        """Displays the guide screen with fun animations and visuals."""
        
        # Load assets (icons for keys and background images)
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")

        wave_background = pygame.image.load(os.path.join(assets_path, "beach.png"))  # Add a wave-themed background
        wave_background = pygame.transform.scale(wave_background, (ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT))


        # Resize icons
        guide_text = [
            ("Welcome to Beaches-N-Barrels!", None),
            ("1. Use W, A, S, D to move your character.",None),
            ("2. Press E to activate your character's ability.", None),
            ("3. Use 1 - 4 to activate items from your inventory.", None),
            ("4. Hold Left Shift to toggle the minimap view.", None),
            ("5. Use Arrow Keys to shoot.",None),
            ("6. Press L to save the game at any time.", None),
            ("7. Defeat enemies, and survive!", None),
            ("8. Good luck and have fun!", None)
        ]

        # Back button with hover effect
        back_button = pygame.Rect(20, 20, self.back_image.get_width(), self.back_image.get_height())

        wave_offset = 0  # Used for wave animation
        font_title = pygame.font.Font(None, 60)
        font_text = pygame.font.Font(None, 36)

        while True:
            # Animated waves effect
            wave_offset = (wave_offset + 1) % ViewUnits.SCREEN_HEIGHT
            self.screen.blit(wave_background, (0, wave_offset - ViewUnits.SCREEN_HEIGHT))
            self.screen.blit(wave_background, (0, wave_offset))  # Looping waves

            # Draw semi-transparent text box
            text_box_width = ViewUnits.SCREEN_WIDTH // 1.5
            text_box_height = len(guide_text) * 50 + 60  # Adjust height based on text length
            text_box_x = (ViewUnits.SCREEN_WIDTH - text_box_width) // 2
            text_box_y = 100  

            text_box_surface = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
            text_box_surface.fill((250,250,250, 180))  # Black with 70% opacity
            self.screen.blit(text_box_surface, (text_box_x, text_box_y))

            # Draw the title with a glowing effect
            title_surface = font_title.render("Beaches-N-Barrels Guide", True, (255, 215, 0))  # Gold text
            title_rect = title_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, text_box_y - 30))
            self.screen.blit(title_surface, title_rect)

            # Display guide text with icons
            y_offset = text_box_y + 20  

            for line, icon in guide_text:
                text_surface = font_text.render(line, True, (0,0,0))  # White text
                text_rect = text_surface.get_rect(topleft=(text_box_x + 20, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 50  

            # Animated glowing back button
            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                glow_surface = pygame.Surface((self.back_image.get_width() + 10, self.back_image.get_height() + 10), pygame.SRCALPHA)
                glow_surface.fill((255, 255, 255, 50))  # Light white glow
                self.screen.blit(glow_surface, (back_button.x - 5, back_button.y - 5))

            self.screen.blit(self.back_image, back_button.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        return  # Return to title screen


                        
    def create_hover_effect(self, image, button_rect, mouse_pos):
        """Applies transparency effect when the mouse hovers over a button."""
        temp_image = image.copy()
        if button_rect.collidepoint(mouse_pos):
            temp_image.set_alpha(180)  # Slightly transparent when hovered
        else:
            temp_image.set_alpha(255)  # Fully visible otherwise
        return temp_image
    def character_selection_screen(self):
        """Displays the character selection screen and returns the chosen class or None if 'Back' is pressed."""
        current_directory = os.path.dirname(__file__)
        assets_path = os.path.join(current_directory, '..', 'Assets')

        # Load character selection images
        dolphin_img = pygame.image.load(os.path.join(assets_path, 'Dolphin.png'))
        buddha_img = pygame.image.load(os.path.join(assets_path, 'Buddha.png'))
        astronaut_img = pygame.image.load(os.path.join(assets_path, 'Astronaut.jpg'))

        # Scale images to fit
        img_width = ViewUnits.SCREEN_WIDTH // 4
        img_height = ViewUnits.SCREEN_HEIGHT // 5
        dolphin_img = pygame.transform.scale(dolphin_img, (img_width, img_height))
        buddha_img = pygame.transform.scale(buddha_img, (img_width, img_height))
        astronaut_img = pygame.transform.scale(astronaut_img, (img_width, img_height))

        # Button positions
        spacing = ViewUnits.SCREEN_WIDTH // 10
        start_x = (ViewUnits.SCREEN_WIDTH - (3 * img_width + 2 * spacing)) // 2
        center_y = ViewUnits.SCREEN_HEIGHT // 2

        dolphin_button = pygame.Rect(start_x, center_y, img_width, img_height)
        buddha_button = pygame.Rect(start_x + img_width + spacing, center_y, img_width, img_height)
        astronaut_button = pygame.Rect(start_x + 2 * (img_width + spacing), center_y, img_width, img_height)

        # Back button
        back_button = pygame.Rect(0, 0,
                                  self.back_image.get_width(), self.back_image.get_height())
        

        while True:
            self.screen.blit(self.background, (0, 0))  # Redraw background

            # Draw character buttons
            self.screen.blit(dolphin_img, dolphin_button.topleft)
            self.screen.blit(buddha_img, buddha_button.topleft)
            self.screen.blit(astronaut_img, astronaut_button.topleft)

            # Draw back button
            self.screen.blit(self.back_image, back_button.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dolphin_button.collidepoint(event.pos):
                        return "Dolphin"
                    elif buddha_button.collidepoint(event.pos):
                        return "Buddha"
                    elif astronaut_button.collidepoint(event.pos):
                        return "Astronaut"
                    elif back_button.collidepoint(event.pos):
                        return None  # Return to title screen
