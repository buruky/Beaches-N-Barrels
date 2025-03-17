import pygame
from ViewUnits import ViewUnits  # Assuming this exists
from .SpriteFactory import SpriteFactory

class UI:
    def __init__(self, screen):
        """Initializes the UI class with a reference to the screen."""
        self.screen = screen
        self.font_small = pygame.font.Font(None, 25)  # Small font for inventory
        self.font_large = pygame.font.Font(None, 50)  # Large font for health
        self.mySpriteFactory = SpriteFactory()
        self.inventory_start_x = 20  # Starting X position for the inventory
        self.inventory_start_y = ViewUnits.SCREEN_HEIGHT - 100  # Starting Y position (bottom left)

        self.inventory_icon_size = 50

    
    def draw_inventory(self, inventory):
        """Draw the player's inventory with a transparent background and transparent item images."""
        # Set the dimensions of the background for the inventory
        inventory_width = self.inventory_icon_size * 4 + 30  # 4 slots with spacing
        inventory_height = self.inventory_icon_size + 40  # Height for the slots + label space

        # Position for the inventory background
        x_offset = self.inventory_start_x
        y_offset = self.inventory_start_y

        # Create a surface for the inventory background with transparency
        inventory_surface = pygame.Surface((inventory_width + 10, inventory_height - 30), pygame.SRCALPHA)  # Use the SRCALPHA flag for transparency
        inventory_surface.fill((250, 250, 250, 150))  # Black background with alpha (transparency level: 150)

        # Draw the 4 slots inside the inventory with transparent white squares
        spacing = 10  # Space between items in the inventory
        slot_x_offset = 5  # Offset to avoid touching the edges
        slot_y_offset = 5
        for idx in range(4):  # We are always showing 4 slots
            # Check if there is an item in the current slot
            item = inventory[idx] if idx < len(inventory) else None  # If no item, the slot is empty

            # Draw the slot background (empty slot is a square with transparency)
            slot_rect = pygame.Rect(slot_x_offset + idx * (self.inventory_icon_size + spacing), slot_y_offset, self.inventory_icon_size, self.inventory_icon_size)
            pygame.draw.rect(inventory_surface, (255, 255, 255, 100), slot_rect)  # Semi-transparent white square for each slot

            # If the slot is not empty, draw the item image
            if item:
                if str(item) == "MockItem":
                    item_image = self.mySpriteFactory.healPotionImage  # Example: potion image from SpriteFactory
                elif str(item) == "InvincibilityItem":
                    item_image = self.mySpriteFactory.invincePotionImage
                elif str(item) == "SpeedItem":
                    item_image = self.mySpriteFactory.speedPotionImage
                else:
                    item_image = None  # Handle other item images if needed

                if item_image:
                    # Resize the item image to fit the inventory slot
                    item_image = pygame.transform.scale(item_image, (self.inventory_icon_size, self.inventory_icon_size))
                    inventory_surface.blit(item_image, (slot_x_offset + idx * (self.inventory_icon_size + spacing), slot_y_offset))

            # No label or "Empty" text for empty slots, just leave them blank

        # Now blit the transparent inventory surface onto the main screen
        self.screen.blit(inventory_surface, (x_offset, y_offset))


    def draw_health(self, player_health, max_health):
        """Draw the player's health as a bar, centered at the bottom of the screen."""
        
        # Set the dimensions of the health bar
        bar_width = 400  # Health bar width
        bar_height = 40  # Health bar height
        
        # Calculate x_offset so the health bar is centered horizontally
        x_offset = (ViewUnits.SCREEN_WIDTH - bar_width) - 10  # Position the bar at the center of the screen
        y_offset = ViewUnits.SCREEN_HEIGHT - bar_height - 10  # Position at the bottom of the screen with a small gap

        # Round the corners by setting the border_radius for rounded corners
        border_radius = 30  # Set the desired radius for the corners
        
        # Draw the background of the health bar (gray), with rounded corners
        pygame.draw.rect(self.screen, (50, 50, 50), (x_offset, y_offset, bar_width, bar_height), border_radius=border_radius)

        # Calculate the width of the health bar based on the current health
        health_percentage = player_health / max_health  # Calculate health percentage (0 to 1)
        health_bar_width = bar_width * health_percentage  # Scale the bar width based on health

        # Choose the color for the health bar (green for full, red for low)
        if player_health > 70:
            bar_color = (144, 238, 144)  
        elif player_health > 30:
            bar_color = (255, 255, 170)  
        else:
            bar_color = (255, 0, 0)  

        # Draw the foreground of the health bar (current health), with rounded corners
        pygame.draw.rect(self.screen, bar_color, (x_offset, y_offset, health_bar_width, bar_height), border_radius=border_radius)

        # Optional: Draw text on top of the health bar (e.g., health percentage)
        font = pygame.font.Font(None, 25)  # Smaller font size for text inside the bar
        text_surface = font.render(f"{player_health}/{max_health}", True, (0,0,0))  # White text
        text_rect = text_surface.get_rect(center=(x_offset + bar_width // 2, y_offset + bar_height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_boss_health(self, enemy_health, max_health):
        """Draw the enemy's health bar, placed at the top of the screen in boss rooms."""
        
        # Set the dimensions of the health bar
        bar_width = 800  # Health bar width, larger for a boss
        bar_height = 20  # Health bar height
        
        # Position the health bar at the top-center of the screen
        x_offset = (ViewUnits.SCREEN_WIDTH - bar_width) // 2  # Center the bar horizontally
        y_offset = 10  # Position it near the top of the screen
        
        # Round the corners by setting the border_radius for rounded corners
        border_radius = 10  # Set the desired radius for the corners
        
        # Draw the background of the health bar (gray)
        pygame.draw.rect(self.screen, (50, 50, 50), (x_offset, y_offset, bar_width, bar_height), border_radius=border_radius)
        
        # Calculate the width of the health bar based on the current health
        health_percentage = enemy_health / max_health  # Calculate health percentage (0 to 1)
        health_bar_width = bar_width * health_percentage  # Scale the bar width based on health
        

        bar_color = (250, 0, 0)  # Soft pastel red
        
        # Draw the foreground of the health bar (current health), with rounded corners
        pygame.draw.rect(self.screen, bar_color, (x_offset, y_offset, health_bar_width, bar_height), border_radius=border_radius)
        
        # Optional: Draw text on top of the health bar (e.g., health percentage)
        font = pygame.font.Font(None, 25)  # Smaller font size for text inside the bar
        text_surface = font.render(f"{enemy_health}/{max_health}", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(x_offset + bar_width // 2, y_offset + bar_height // 2))
        self.screen.blit(text_surface, text_rect)


    def draw_room_coordinates(self, cords):
        """Draw the room coordinates at the center of the screen."""
        if cords:
            text_surface = self.font_large.render(f"Room: {cords}", True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(center=(ViewUnits.SCREEN_WIDTH // 2, ViewUnits.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
