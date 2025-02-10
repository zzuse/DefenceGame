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
FONT = pygame.font.Font(None, 24)


# Plant class
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_ready = False  # Shoots only after zombie placement
        self.health = 10  # Each plant has 10 health
        self.fire_rounds = 3  # Number of fire rounds per turn

    def move(self, x, y):
        self.rect.topleft = (x, y)

    def shoot(self):
        if self.shoot_ready:
            for _ in range(self.fire_rounds):
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 5, 0))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, -2))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, 2))
            self.shoot_ready = False  # Reset shooting ability until next round

    def draw_health(self, surface):
        health_text = FONT.render(str(self.health), True, WHITE)
        surface.blit(health_text, (self.rect.right - 20, self.rect.top))


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
        self.health = 10  # Each zombie has 10 health

    def move_forward(self):
        self.rect.x -= GRID_SIZE  # Moves one step forward per round
        if self.rect.x < 0:
            pygame.quit()
            quit()

    def draw_health(self, surface):
        health_text = FONT.render(str(self.health), True, WHITE)
        surface.blit(health_text, (self.rect.right - 20, self.rect.top))


# Groups
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
plant = Plant(GRID_SIZE, GRID_SIZE)  # One plant instance

# Game loop
running = True
clock = pygame.time.Clock()
player_turn = "plant"  # Alternates between "plant" and "zombie"

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = (mx // GRID_SIZE) * GRID_SIZE
            grid_y = (my // GRID_SIZE) * GRID_SIZE

            if player_turn == "plant":
                plant.move(grid_x, grid_y)  # Move the plant
                player_turn = "zombie"
            elif player_turn == "zombie":
                zombies.add(Zombie(grid_x, grid_y))
                player_turn = "plant"

                # Allow plant to shoot after zombie placement
                plant.shoot_ready = True

                # Move zombies forward one step
                for zombie in zombies:
                    zombie.move_forward()

    # Let plant shoot only once per round
    plant.shoot()

    # Update
    bullets.update()
    zombies.update()

    # Collision detection
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
        for zombie in hit_zombies:
            zombie.health -= 1
            bullet.kill()
            if zombie.health <= 0:
                zombie.kill()

    # Draw everything
    screen.blit(plant.image, plant.rect)
    bullets.draw(screen)
    zombies.draw(screen)

    # Draw health bars
    plant.draw_health(screen)
    for zombie in zombies:
        zombie.draw_health(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
