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

# Dropdown options for zombies
ZOMBIE_TYPES = ["Normal Zombie", "Fast Zombie", "Tank Zombie", "None"]
selected_zombie = "None"


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
        self.shoot_timer = 0
        self.shots_fired = 0

    def move(self, x, y):
        self.rect.topleft = (x, y)

    def start_shooting(self):
        if self.shoot_ready:
            self.shoot_timer = pygame.time.get_ticks()
            self.shots_fired = 0

    def shoot(self):
        if self.shoot_ready and self.shots_fired < self.fire_rounds:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > 500:  # Delay between shots
                self.shoot_timer = now
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 5, 0, 2, 200))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, -2, 1, 200))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, 2, 1, 200))
                self.shots_fired += 1
                if self.shots_fired >= self.fire_rounds:
                    self.shoot_ready = False

    def draw_health(self, surface):
        health_text = FONT.render(str(self.health), True, WHITE)
        surface.blit(health_text, (self.rect.right - 20, self.rect.top))


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, damage, range_):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.damage = damage  # Damage value of the bullet
        self.range = range_  # Maximum distance the bullet can travel
        self.start_x = x

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT or abs(
                self.rect.x - self.start_x) > self.range:
            self.kill()


# Zombie class
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health  # Each zombie has specified health

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

    # Display current player's turn at the top
    turn_text = FONT.render(f"Next Turn: {player_turn.capitalize()}", True, WHITE)
    screen.blit(turn_text, (WIDTH // 2 - 50, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_zombie = "Normal Zombie"
            elif event.key == pygame.K_2:
                selected_zombie = "Fast Zombie"
            elif event.key == pygame.K_3:
                selected_zombie = "Tank Zombie"
            elif event.key == pygame.K_0:
                selected_zombie = "None"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = (mx // GRID_SIZE) * GRID_SIZE
            grid_y = (my // GRID_SIZE) * GRID_SIZE

            if player_turn == "plant":
                plant.move(grid_x, grid_y)  # Move the plant
                player_turn = "zombie"
            elif player_turn == "zombie" and selected_zombie != "None":
                health = 10 if selected_zombie == "Normal Zombie" else 5 if selected_zombie == "Fast Zombie" else 20
                zombies.add(Zombie(grid_x, grid_y, health))
                player_turn = "plant"

                # Allow plant to shoot after zombie placement
                plant.shoot_ready = True
                plant.start_shooting()

                # Move zombies forward one step
                for zombie in zombies:
                    zombie.move_forward()

    # Let plant shoot with delays
    plant.shoot()

    # Update
    bullets.update()
    zombies.update()

    # Collision detection
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
        for zombie in hit_zombies:
            zombie.health -= bullet.damage  # Apply bullet damage
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
