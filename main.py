import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
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

# Zombie selection buttons
# UI Panels
PLANT_STORE_WIDTH = 200
ZOMBIE_PANEL_WIDTH = 200

# Plant store items
PLANT_STORE_RECT = pygame.Rect(0, 0, PLANT_STORE_WIDTH, HEIGHT)
PLANT_MONEY = 100
plant_buttons = {"Pistol": pygame.Rect(10, 100, 180, 30),
                 "Assault Rifle": pygame.Rect(10, 140, 180, 30),
                 "Shotgun": pygame.Rect(10, 180, 180, 30)}

# Zombie selection panel
ZOMBIE_PANEL_RECT = pygame.Rect(WIDTH - ZOMBIE_PANEL_WIDTH, 0, ZOMBIE_PANEL_WIDTH, HEIGHT)
# Zombie selection buttons
ZOMBIE_TYPES = ["Normal", "Fast", "Tank", "None"]
selected_zombie = None
selecting_zombie = True  # Track if the player is selecting a zombie type
buttons = {"Normal": pygame.Rect(WIDTH - 190, 100, 180, 30),
           "Fast": pygame.Rect(WIDTH - 190, 140, 180, 30),
           "Tank": pygame.Rect(WIDTH - 190, 180, 180, 30),
           "None": pygame.Rect(WIDTH - 190, 220, 180, 30)}


# Plant class
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_ready = False
        self.health = 10
        self.fire_rounds = 3
        self.shoot_timer = 0
        self.shots_fired = 0

    def move(self, y):
        self.rect.topleft = (PLANT_STORE_WIDTH, y)

    def start_shooting(self):
        if self.shoot_ready:
            self.shoot_timer = pygame.time.get_ticks()
            self.shots_fired = 0

    def shoot(self):
        if self.shoot_ready and self.shots_fired < self.fire_rounds:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > 500:
                self.shoot_timer = now
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 5, 0, 2, 500))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, -2, 1, 500))
                bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 4, 2, 1, 500))
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

    def move(self):
        if self.rect.x > GRID_SIZE:
            self.rect.x -= GRID_SIZE  # Moves one step forward per round
        else:
            if self.rect.y < plant.rect.y:
                self.rect.y += GRID_SIZE
            elif self.rect.y > plant.rect.y:
                self.rect.y -= GRID_SIZE

    def attack(self):
        if self.rect.colliderect(plant.rect):
            plant.health -= 1

    def draw_health(self, surface):
        health_text = FONT.render(str(self.health), True, WHITE)
        surface.blit(health_text, (self.rect.right - 20, self.rect.top))


# Game loop
running = True
clock = pygame.time.Clock()
player_turn = "plant"
plant = Plant(PLANT_STORE_WIDTH, GRID_SIZE)
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

while running:
    screen.fill((0, 0, 0))
    # pygame.draw.rect(screen, WHITE, (0, 50, WIDTH, HEIGHT - 50), 2)
    pygame.draw.rect(screen, WHITE, PLANT_STORE_RECT, 2)
    pygame.draw.rect(screen, WHITE, ZOMBIE_PANEL_RECT, 2)
    turn_text = FONT.render(f"Next Turn: {player_turn.capitalize()}", True, WHITE)
    screen.blit(turn_text, (WIDTH // 2 - 50, 10))

    # Draw plant store
    screen.blit(FONT.render(f"Plant Store", True, WHITE), (10, 10))
    screen.blit(FONT.render(f"Money: {PLANT_MONEY}", True, WHITE), (10, 50))
    for key, rect in plant_buttons.items():
        pygame.draw.rect(screen, WHITE, rect, 2)
        screen.blit(FONT.render(key, True, WHITE), (rect.x + 10, rect.y + 5))

    # Draw zombie selection panel
    screen.blit(FONT.render(f"Select Zombie", True, WHITE), (WIDTH - 190, 50))
    for key, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect, 2)
        screen.blit(FONT.render(key, True, WHITE), (rect.x + 10, rect.y + 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if player_turn == "zombie" and selecting_zombie:
                for key, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        selected_zombie = key
                        selecting_zombie = False
                        break
            elif player_turn == "zombie" and not selecting_zombie:
                grid_y = (my // GRID_SIZE) * GRID_SIZE
                if selected_zombie != "None":
                    health = 10 if selected_zombie == "Normal" else 5 if selected_zombie == "Fast" else 20
                    zombies.add(Zombie((COLS - 1) * GRID_SIZE + PLANT_STORE_WIDTH, grid_y, health))
                for zombie in zombies:
                    zombie.move()
                    zombie.attack()
                selecting_zombie = True
                player_turn = "plant"
                plant.shoot_ready = True
                plant.start_shooting()
            elif player_turn == "plant":
                plant.move((my // GRID_SIZE) * GRID_SIZE)
                player_turn = "zombie"
                selecting_zombie = True

    plant.shoot()

    # Update
    bullets.update()
    zombies.update()

    # Collision detection
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
        for zombie in hit_zombies:
            zombie.health -= bullet.damage
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
