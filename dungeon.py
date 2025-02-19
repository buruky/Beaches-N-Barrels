# Example file showing a circle moving on screen
import pygame
from dungeongen1 import Generate 
from Room import Room
#from dungeongen1 import connect_rooms 

# Pygame setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200  # Adjusted for better visibility
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

# Load dungeon and connect rooms
my_dungeon = Generate()
my_dungeon.connect_rooms()  # Ensure rooms have doors
grid = my_dungeon.get_dungeon()
my_dungeon.print_dungeon()

# Player setup
player_pos = pygame.Vector2(my_dungeon.start_pos[0] * 100 + 25, my_dungeon.start_pos[1] * 100 +25)
player_speed = 39  # Movement speed
ROOM_SIZE = 50  # Size of a room in pixels
DOOR_WIDTH = 20
DOOR_HEIGHT = 7
WALL_THICKNESS = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

def draw_dungeon(screen, grid):
    for row in range(my_dungeon.grid_height):
        for col in range(my_dungeon.grid_width):
            room = grid[col][row]
            if isinstance(room, Room):
                x, y, z, w = room.x, room.y, room.width, room.height
                pygame.draw.rect(screen, WHITE, (x, y, z, w), 2)  # Draw room

                if room.doors["N"]:  # North door
                    pygame.draw.rect(screen, BLACK, (x + (ROOM_SIZE // 2) - (DOOR_WIDTH // 2), y - WALL_THICKNESS, DOOR_WIDTH, DOOR_HEIGHT))  
                if room.doors["S"]:  # South door
                    pygame.draw.rect(screen, BLACK, (x + (ROOM_SIZE // 2) - (DOOR_WIDTH // 2), y + ROOM_SIZE - WALL_THICKNESS, DOOR_WIDTH, DOOR_HEIGHT))  
                if room.doors["W"]:  # West door
                    pygame.draw.rect(screen, BLACK, (x - WALL_THICKNESS, y + (ROOM_SIZE // 2) - (DOOR_WIDTH // 2), DOOR_HEIGHT, DOOR_WIDTH))  
                if room.doors["E"]:  # East door
                    pygame.draw.rect(screen, BLACK, (x + ROOM_SIZE - WALL_THICKNESS, y + (ROOM_SIZE // 2) - (DOOR_WIDTH // 2), DOOR_HEIGHT, DOOR_WIDTH))   

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        player_pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player_pos.x += player_speed * dt

    # Draw everything
    screen.fill(GRAY)
    draw_dungeon(screen, grid)  # Draw the dungeon
    pygame.draw.circle(screen, RED, (int(player_pos.x), int(player_pos.y)), 5)  # Draw player

    # Update display
    pygame.display.flip()
    dt = clock.tick(30) / 1000  # Maintain frame rate

pygame.quit()
