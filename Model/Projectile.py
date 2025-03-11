import pygame

class Projectile:
    def __init__(self, x, y, direction, speed=5):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.rect = pygame.Rect(x, y, 10, 10)  # Example size of the projectile

    def update(self):
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Draw as a red rectangle