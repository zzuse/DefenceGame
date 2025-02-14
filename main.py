import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load Sounds
bullet_sound = pygame.mixer.Sound("bullet.wav")
plant_place_sound = pygame.mixer.Sound("plant_place.wav")
zombie_place_sound = pygame.mixer.Sound("zombie_place.wav")
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
plant_buttons = {"Pistol": pygame.Rect(10, 100, 180, 60),
                 "Assault Rifle": pygame.Rect(10, 170, 180, 60),
                 "Shotgun": pygame.Rect(10, 240, 180, 60),
                 "None": pygame.Rect(10, 310, 180, 60)}
selected_weapon = "Pistol"
selecting_weapon = True
owned_weapons = {"Pistol": True, "Assault Rifle": False, "Shotgun": False, "None": True}
weapon_prices = {"Pistol": 100, "Assault Rifle": 200, "Shotgun": 300, "None": 0}

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

# Weapon properties
weapon_stats = {
    "Pistol": {"range": 400, "rounds": 3, "angles": [0], "damage": 1},
    "Assault Rifle": {"range": 600, "rounds": 5, "angles": [-5, 0, 5], "damage": 10},
    "Shotgun": {"range": 300, "rounds": 5, "angles": [-10, -5, 0, 5, 10], "damage": 5},
    "None": {"range": 0, "rounds": 0, "angles": [0], "damage": 0},
}


# Plant class
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_ready = False
        self.health = 10
        # self.fire_rounds = 3
        self.shoot_timer = 0
        self.shots_fired = 0

    def move(self, y):
        self.rect.topleft = (PLANT_STORE_WIDTH, y)
        plant_place_sound.play()

    def start_shooting(self):
        if self.shoot_ready:
            self.shoot_timer = pygame.time.get_ticks()
            self.shots_fired = 0

    def shoot(self):
        if self.shoot_ready and self.shots_fired < weapon_stats[selected_weapon]["rounds"]:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > 500:
                self.shoot_timer = now
                for angle in weapon_stats[selected_weapon]["angles"]:
                    bullets.add(Bullet(self.rect.right, self.rect.y + GRID_SIZE // 2, 5, angle,
                                       weapon_stats[selected_weapon]["damage"], weapon_stats[selected_weapon]["range"]))
                bullet_sound.play()
                self.shots_fired += 1
                if self.shots_fired >= weapon_stats[selected_weapon]["rounds"]:
                    self.shoot_ready = False
        if self.shoot_ready and selected_weapon == "None":
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

    def __init__(self, x, y, health, zombie_type):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.zombie_type = zombie_type
        zombie_place_sound.play()

    def take_damage(self, damage):
        global PLANT_MONEY
        self.health -= damage
        if self.health <= 0:
            reward = 10 if self.zombie_type == "Normal" else 5 if self.zombie_type == "Fast" else 20
            PLANT_MONEY += reward
            self.kill()

    def move(self):
        if self.rect.x > plant.rect.x + GRID_SIZE:
            self.rect.x -= GRID_SIZE  # Moves one step forward per round
        elif self.rect.x == plant.rect.x + GRID_SIZE:
            self.rect.x -= GRID_SIZE // 5
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
        screen.blit(FONT.render(f"${weapon_prices.get(key, 0)}", True, WHITE), (rect.x + 130, rect.y + 5))
        screen.blit(FONT.render("Owned" if owned_weapons.get(key, False) else "Not Owned", True, WHITE), (rect.x + 90, rect.y + 25))

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
            if player_turn == "plant" and selecting_weapon:
                for key, rect in plant_buttons.items():
                    if rect.collidepoint(mx, my):
                        if not owned_weapons[key] and PLANT_MONEY >= weapon_prices[key]:
                            PLANT_MONEY -= weapon_prices[key]
                            owned_weapons[key] = True
                        if owned_weapons[key]:
                            selected_weapon = key
                            selecting_weapon = False
                        break
            elif player_turn == "plant" and not selecting_weapon:
                plant.move((my // GRID_SIZE) * GRID_SIZE)
                player_turn = "zombie"
                selecting_zombie = True
                selecting_weapon = True
            elif player_turn == "zombie" and selecting_zombie:
                for key, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        selected_zombie = key
                        selecting_zombie = False
                        break
            elif player_turn == "zombie" and not selecting_zombie:
                grid_y = (my // GRID_SIZE) * GRID_SIZE
                if selected_zombie != "None":
                    health = 10 if selected_zombie == "Normal" else 5 if selected_zombie == "Fast" else 20
                    zombies.add(Zombie((COLS - 1) * GRID_SIZE + PLANT_STORE_WIDTH, grid_y, health, selected_zombie))
                for zombie in zombies:
                    zombie.move()
                    zombie.attack()
                selecting_zombie = True
                player_turn = "plant"
                plant.shoot_ready = True
                plant.start_shooting()

    plant.shoot()

    # Update
    bullets.update()
    zombies.update()

    # Collision detection
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
        for zombie in hit_zombies:
            zombie.take_damage(bullet.damage)
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

    if plant.health <= 0:
        plant.kill()
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
