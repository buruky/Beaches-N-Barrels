import pygame
from Model.Floor import Generate 
from Model.Room import Room

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

# Load dungeon and connect rooms
my_dungeon = Generate()
my_dungeon.connect_rooms() 
grid = my_dungeon.get_dungeon()
my_dungeon.print_dungeon()

ROOM_SIZE = Generate.ROOM_SIZE
GRAY = (100, 100, 100)
RED = (255, 0, 0)

player_x, player_y = my_dungeon.start_pos
player_pos = pygame.Vector2(player_x * ROOM_SIZE + ROOM_SIZE // 2 - ROOM_SIZE/4, player_y * ROOM_SIZE + ROOM_SIZE // 2 - ROOM_SIZE/4)
player_speed = 30 

def draw_dungeon(screen, grid):
    for row in range(my_dungeon.grid_height):
        for col in range(my_dungeon.grid_width):
            room = grid[row][col]
            if isinstance(room, Room):
                room.draw(screen) 


def check_player_collision_with_doors(player_rect):
    player_pos
    collided_doors = [door for door in Room.all_doors if player_rect.colliderect(door.rect)]
    for door in collided_doors:
        print(f"Player collided with {door.direction} door")
    
        if door.direction == "N":
            player_pos.y -= ROOM_SIZE/2 - ROOM_SIZE/4 + ROOM_SIZE/15 
        elif door.direction == "S":
            player_pos.y += ROOM_SIZE/2 - ROOM_SIZE/4 + ROOM_SIZE/15 
        elif door.direction == "W":
            player_pos.x -= ROOM_SIZE/2 - ROOM_SIZE/4 + ROOM_SIZE/15 
        elif door.direction == "E":
            player_pos.x += ROOM_SIZE/2 - ROOM_SIZE/4 + ROOM_SIZE/15

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        player_pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player_pos.x += player_speed * dt
    
    player_rect = pygame.Rect(int(player_pos.x - 5), int(player_pos.y - 5), 10, 10)
    check_player_collision_with_doors(player_rect)

    # Draw everything
    screen.fill(GRAY)
    draw_dungeon(screen, grid)
    pygame.draw.circle(screen, RED, (int(player_pos.x), int(player_pos.y)), 5)  # Draw player

    # Update display
    pygame.display.flip()
    dt = clock.tick(30) / 1000 

pygame.quit()
