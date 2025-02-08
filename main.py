import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 80
ROWS = 5
COLS = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plants vs Zombies Clone")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)


# Plant class
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_timer = 0

    def update(self):
        # Shoot bullets periodically
        self.shoot_timer += 1
        if self.shoot_timer >= 60:  # Fire every second
            bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 5, 0))  # Straight
            bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, -2))  # Diagonal Up
            bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, 2))  # Diagonal Down
            self.shoot_timer = 0


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


# Zombie class
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= 1
        if self.rect.x < 0:
            pygame.quit()
            quit()


# Groups
plants = pygame.sprite.Group()
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
zombie_spawn_timer = 0

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = (mx // GRID_SIZE) * GRID_SIZE
            grid_y = (my // GRID_SIZE) * GRID_SIZE
            plants.add(Plant(grid_x, grid_y))

    # Spawn zombies
    zombie_spawn_timer += 1
    if zombie_spawn_timer >= 120:
        zombies.add(Zombie(WIDTH - GRID_SIZE, random.randint(0, ROWS - 1) * GRID_SIZE))
        zombie_spawn_timer = 0

    # Update
    plants.update()
    bullets.update()
    zombies.update()

    # Collision detection
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, True)
        if hit_zombies:
            bullet.kill()

    # Draw everything
    plants.draw(screen)
    bullets.draw(screen)
    zombies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
