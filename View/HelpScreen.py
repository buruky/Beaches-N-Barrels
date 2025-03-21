import pygame
import os
from ViewUnits import ViewUnits


def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

class HelpScreen:
    def __init__(self, screen, font_small, font_med, back_image):
        self.screen = screen
        self.font_small = font_small
        self.font_med = font_med
        self.back_image = back_image

        current_directory = os.path.dirname(__file__)
        assets_path = os.path.join(current_directory, '..', 'Assets')

        # Use the main menu background instead of moving waves
        self.background = pygame.image.load(os.path.join(assets_path, "goat.jpg"))
        self.background = pygame.transform.scale(self.background, (ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT))

        self.char_images = {
            "DolphinBoy": pygame.image.load(os.path.join(assets_path, 'Dolphin.png')),
            "Baywatch Buddha": pygame.image.load(os.path.join(assets_path, 'Buddha.png')),
            "Astro Surfer": pygame.image.load(os.path.join(assets_path, 'Astronaut.png')),
        }

        char_x = ViewUnits.SCREEN_WIDTH - 130
        char_y_start = ViewUnits.SCREEN_HEIGHT - 400  # Adjusted starting position
        spacing = 100  # Increased spacing to prevent cut-off

        self.char_buttons = {
            "DolphinBoy": pygame.Rect(char_x, char_y_start, 80, 80),
            "Baywatch Buddha": pygame.Rect(char_x, char_y_start + spacing, 80, 80),
            "Astro Surfer": pygame.Rect(char_x, char_y_start + 2 * spacing, 80, 80),
        }

        self.guide_sections = [
            ("CONTROLS", [
                "Move: W / A / S / D",
                "Shoot: Arrow Keys",
                "Use Items: 1–4",
                "Toggle Minimap: Hold Left Shift"
            ]),
            ("ABILITIES", [
                "Use Ability: SPACEBAR"
            ]),
            ("MISC", [
                "Save Game: L",
                "Goal: Defeat enemies and survive!",
                "Good luck and have fun!"
            ])
        ]

    def run(self):
        back_button = pygame.Rect(20, 20, self.back_image.get_width(), self.back_image.get_height())

        while True:
            self.screen.blit(self.background, (0, 0))  # Static background

            # Create a semi-transparent rounded rectangle behind text
            overlay = pygame.Surface((600, 410), pygame.SRCALPHA)
            draw_rounded_rect(overlay, (250, 250, 250, 150), overlay.get_rect(), radius=15)
            self.screen.blit(overlay, (ViewUnits.SCREEN_WIDTH // 2 - 300, 100))

            # Create a semi-transparent rounded rectangle behind characters
            char_overlay = pygame.Surface((100, 320), pygame.SRCALPHA)
            draw_rounded_rect(char_overlay, (250,250,250, 150), char_overlay.get_rect(), radius=20)
            self.screen.blit(char_overlay, (ViewUnits.SCREEN_WIDTH - 140, ViewUnits.SCREEN_HEIGHT - 420))

            y_offset = 120
            for title, lines in self.guide_sections:
                header = self.font_med.render(title, True, (255, 170, 0))
                header_rect = header.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(header, header_rect)
                y_offset += 40
                for line in lines:
                    text = self.font_small.render(line, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, y_offset))
                    self.screen.blit(text, text_rect)
                    y_offset += 30
                y_offset += 20

            for name, rect in self.char_buttons.items():
                image = pygame.transform.scale(self.char_images[name], (rect.width, rect.height))
                self.screen.blit(image, rect.topleft)

            self.screen.blit(self.back_image, back_button.topleft)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        return
                    for name, rect in self.char_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.show_character_info(name)

    def show_character_info(self, character_name):
        character_details = {
            "DolphinBoy": {
                "ability": "Tsunami Swim: Gains bonus speed.",
                "passive": "Higher move speed and attack speed",
                "lore": "Born from the fastest ocean currents, DolphinBoy is a guardian of the shores. After stealing the legendary Fin, he gained unmatched speed, using it to defend the coasts from the Red Tide Gang. A blur on land and sea, he fights to protect Beaches and Barrels.",
                "background": "ocean_background.png",
                "music":"dolphin.mp3"
            },
            "Baywatch Buddha": {
                "ability": "Zen Burst: Gains temporary imortality.",
                "passive": "Higher health pool",
                "lore": "Once a master of the pacifist fighting style, Baywatch Buddha trained warriors to find strength through peace. His greatest student, Mark the Shark, was corrupted by an alien force and now terrorizes the beaches of the Barrel Belt. To restore balance, Baywatch Buddha has returned to defend the shores and reclaim his fallen apprentice. He doesn’t seek revenge. He seeks redemption — for his apprentice, and for the shores he once vowed to protect.",
                "background": "temple_background.png",
                "music":"buddha.mp3"

            },
            "Astro Surfer": {
                "ability": "Gravity Slash: Dashes forward at blinding speed.",
                "passive": "Does bonus damage",
                "lore": "Once a stellar peacekeeper aboard the orbital station Eclipse Tide, Astro Surfer patrolled the galaxy’s wildest sectors, keeping balance across planetary worlds. But during a routine mission in the Nebular Drift, she encountered something no one expected: Entity 9, a shape-shifting alien parasite drawn to strong minds and stronger egos. Astro Surfer barely survived the encounter. Her ship was shattered. Her squad lost. And Entity 9 vanished—slipping away like oil into water. Tracking the signal to Earth, Astro Surfer crash-landed near the Barrel Belt, only to discover the parasite had found a new host: Mark the Shark, a warrior once rooted in peace but now completely overtaken.",
                "background": "space_background.png",
                "music": "astro.mp3"
            }
        }

        details = character_details.get(character_name, {
            "ability": "Unknown",
            "passive": "None",
            "lore": "No lore available.",
            "background": "default_background.png"
        })
        music_path = os.path.join(os.path.dirname(__file__), '..', 'Assets/sounds', details.get("music", "default_theme.ogg"))

        pygame.mixer.music.load(music_path)
        if details.get("music") is "astro.mp3":
            pygame.mixer.music.set_volume(0.05)
        else:
            pygame.mixer.music.set_volume(0.1)

        pygame.mixer.music.play(-1)  # loop indefinitely
        bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'Assets', details["background"]))
        bg_image = pygame.transform.scale(bg_image, (ViewUnits.SCREEN_WIDTH, ViewUnits.SCREEN_HEIGHT))

        def wrap_text(text, max_width):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font_small.size(test_line)[0] < max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
            return lines

        while True:
            self.screen.blit(bg_image, (0, 0))
            title = self.font_med.render(character_name, True, (255, 255, 255))
            title_rect = title.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, 150))
            self.screen.blit(title, title_rect)

            ab_lines = wrap_text(f"Ability: {details['ability']}", 800)
            ps_lines = wrap_text(f"Passive: {details['passive']}", 800)
            lore_lines = wrap_text(details['lore'], 800)

            y = 200
            for line in ab_lines:
                ab_text = self.font_small.render(line, True, (250, 250, 255))
                ab_rect = ab_text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, y))
                self.screen.blit(ab_text, ab_rect)
                y += 25

            for line in ps_lines:
                ps_text = self.font_small.render(line, True, (200, 255, 200))
                ps_rect = ps_text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, y))
                self.screen.blit(ps_text, ps_rect)
                y += 25

            box_height = 25 * len(lore_lines) + 20
            box_surface = pygame.Surface((790, box_height), pygame.SRCALPHA)
            draw_rounded_rect(box_surface, (0, 0, 0, 180), box_surface.get_rect(), radius=12)
            box_x = (ViewUnits.SCREEN_WIDTH - 790) // 2
            self.screen.blit(box_surface, (box_x, y))

            lore_y = y + 10
            for line in lore_lines:
                lore_text = self.font_small.render(line, True, (160, 160, 160))
                lore_rect = lore_text.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, lore_y))
                self.screen.blit(lore_text, lore_rect)
                lore_y += 25

            self.screen.blit(self.back_image, (20, 20))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(20, 20, self.back_image.get_width(), self.back_image.get_height()).collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.mixer.init()
                        assets_path = os.path.join(os.path.dirname(__file__), '..', 'Assets/sounds')
                        pygame.mixer.music.load(os.path.join(assets_path, "waves.mp3"))  # Beach wave sound
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)  # Loop indefinitely
                        return