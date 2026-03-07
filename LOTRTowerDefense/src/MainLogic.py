import pygame
import math
import random
import time
import os
pygame.init()
# Load Base Sprite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def asset(path):
    # Try direct path relative to this file
    candidate = os.path.join(BASE_DIR, path)
    if os.path.exists(candidate):
        return candidate
    # Check common sibling and project dirs
    candidates = [
        os.path.join(BASE_DIR, '..', path),
        os.path.join(BASE_DIR, 'assets', path),
        os.path.join(BASE_DIR, 'images', path),
        os.path.join(os.getcwd(), path),
        os.path.join(os.getcwd(), 'assets', path),
        os.path.join(os.getcwd(), 'images', path),
    ]
    for c in candidates:
        c_abs = os.path.abspath(c)
        if os.path.exists(c_abs):
            return c_abs
    # Search recursively from BASE_DIR
    for root, dirs, files in os.walk(BASE_DIR):
        if path in files:
            return os.path.join(root, path)
    # Search parent directories up to a few levels
    cur = BASE_DIR
    for _ in range(4):
        for root, dirs, files in os.walk(cur):
            if path in files:
                return os.path.join(root, path)
        cur = os.path.dirname(cur)
    # Fallback to path in BASE_DIR (will raise if not found when loading)
    return os.path.join(BASE_DIR, path)

from enemy import Enemy
from tower import Tower
from bullet import Bullet

FONT = pygame.font.SysFont("arial", 24)
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("360 Defense")

CLOCK = pygame.time.Clock()
FPS = 60

CENTER = (WIDTH // 2, HEIGHT // 2)

WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)
BASE_RADIUS = 80
BASE_IMAGE = pygame.image.load(asset("towerlvl1.png")).convert_alpha()
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (BASE_RADIUS * 2, BASE_RADIUS * 2))
CANNON_IMAGE = pygame.image.load(asset("lvl1TowerCannon.png")).convert_alpha()
CANNON_IMAGE = pygame.transform.scale(CANNON_IMAGE, (125, 125))
FIREBALL_IMAGE = pygame.image.load(asset("FireBall.png")).convert_alpha()
FIREBALL_IMAGE = pygame.transform.scale(FIREBALL_IMAGE, (75, 75))
BASEFIREBALL_IMAGE = pygame.image.load(asset("FireBall.png")).convert_alpha()
BASEFIREBALL_IMAGE = pygame.transform.scale(BASEFIREBALL_IMAGE, (25, 25))

# Load all tower and base level images
BASE_IMAGES = []
TOWER_IMAGES = []

for i in range(1, 7):  # towerlvl1.png through towerlvl6.png
    try:
        img = pygame.image.load(asset(f"towerlvl{i}.png")).convert_alpha()
        img = pygame.transform.scale(img, (BASE_RADIUS * 2, BASE_RADIUS * 2))
        BASE_IMAGES.append(img)
    except:
        BASE_IMAGES.append(BASE_IMAGE)  # fallback

for i in range(1, 4):  # lvl1TowerCannon.png through lvl3TowerCannon.png
    try:
        img = pygame.image.load(asset(f"lvl{i}TowerCannon.png")).convert_alpha()
        img = pygame.transform.scale(img, (125, 125))
        TOWER_IMAGES.append(img)
    except:
        TOWER_IMAGES.append(CANNON_IMAGE)  # fallback
knight_frame1 = pygame.transform.scale(
    pygame.image.load(asset("knightenemy.png")).convert_alpha(), (100, 100)
)

knight_frame2 = pygame.transform.scale(
    pygame.image.load(asset("knightenemyRunning.png")).convert_alpha(), (100, 100)
)

hobbit_frame1 = pygame.transform.scale(
    pygame.image.load(asset("hobbitenemy.png")).convert_alpha(), (100, 100)
)

hobbit_frame2 = pygame.transform.scale(
    pygame.image.load(asset("hobbitenemyRunning.png")).convert_alpha(), (100, 100)
)

mage_frame1 = pygame.transform.scale(
    pygame.image.load(asset("mageenemy.png")).convert_alpha(), (100, 100)
)

mage_frame2 = pygame.transform.scale(
    pygame.image.load(asset("mageenemyRunning.png")).convert_alpha(), (100, 100)
)



ENEMY_TYPES = [
    {
        "name": "Knight",
        "frames": [knight_frame1, knight_frame2],
        "health": 200,
        "speed": 1,
        "reward": 50
    },
    {
        "name": "Hobbit",
        "frames": [hobbit_frame1, hobbit_frame2],
        "health": 50,
        "speed": 3,
        "reward": 10
    },
    {
        "name": "Mage",
        "frames": [mage_frame1, mage_frame2],
        "health": 150,
        "speed": 2,
        "reward": 30
    }
]

# knight_enemy= pygame.transform.scale(
#         pygame.image.load("knightenemy.png").convert_alpha(), (125, 125)
#     )
# hobbit_enemy= pygame.transform.scale(
#         pygame.image.load("hobbitenemy.png").convert_alpha(), (75, 75)
#     )
# mage_enemy= pygame.transform.scale(
#         pygame.image.load("mageenemy.png").convert_alpha(), (125, 125)
#     )

# ENEMY_TYPES = [
#     {
#         "name": "Knight",
#         "image": knight_enemy,
#         "health": 250,
#         "speed": 0.75,
#         "reward": 50
#     },
#     {
#         "name": "Hobbit",
#         "image": hobbit_enemy,
#         "health": 75,
#         "speed": 5,
#         "reward": 35
#     },
#     {
#         "name": "Mage",
#         "image": mage_enemy,
#         "health": 175,
#         "speed": 1.5,
#         "reward": 45
#     }
# ]

TOWER_IMAGE_1 = pygame.image.load(asset("lvl1TowerCannon.png")).convert_alpha()
TOWER_IMAGE_1 = pygame.transform.scale(TOWER_IMAGE_1, (100,100))
#TODO: ADD BARRIERS
#UPGRADES?
#DIFFICULTY INCREASES? - done
#ENEMY PATHFINDING AROUND BARRIERS?
#ENEMY TYPES? (FAST LOW HEALTH, SLOW HIGH HEALTH, SPLIT ON DEATH, ETC)-done
#PUT IN SPRITES

def main_menu():
    running = True

    play_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)

    while running:
        CLOCK.tick(FPS)
        WIN.fill((30, 30, 30))

        title_text = FONT.render("LORD OF THE RINGS DEFENSE", True, WHITE)
        WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))

        pygame.draw.rect(WIN, GREEN, play_button)
        play_text = FONT.render("PLAY", True, BLACK)
        WIN.blit(play_text, (
            play_button.x + play_button.width//2 - play_text.get_width()//2,
            play_button.y + play_button.height//2 - play_text.get_height()//2
        ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if play_button.collidepoint(mouse_pos):
                    main()  # Start the game

        pygame.display.update()

def main():
    
    enemies = []
    towers = []
    bullets = []
    selected_tower_type = 1  # 1 = blue 2 = purple
    killcount = 0
    spawn_timer = 0
    base_health = 2
    money = 200
    TOWER_COST = 50
    base_range = 500
    base_cooldown = 0
    BASE_FIRE_RATE = 0.5
    BASE_DAMAGE = 1
    base_level = 1  # Track base level (1-6)
    error_message = ""
    error_timer = 0
    running = True
    upgrade_mode = False
    button1_rect = pygame.Rect(150, 720, 150, 50)
    upgrade_button_rect = pygame.Rect(325, 720, 150, 50)
    button2_rect = pygame.Rect(500, 720, 150, 50)
    while running:
        CLOCK.tick(FPS)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            def can_place_tower(x, y):
                dx = x - CENTER[0]
                dy = y - CENTER[1]
                distance = math.hypot(dx, dy)
                return 75 < distance < 150
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

            

                if button1_rect.collidepoint(x, y):
                    selected_tower_type = 1

                elif button2_rect.collidepoint(x, y):
                    selected_tower_type = 2

                elif upgrade_button_rect.collidepoint(x, y):
                    upgrade_mode = not upgrade_mode

                elif upgrade_mode:
                    # Handle upgrades in upgrade mode
                    # Check if clicking on base
                    base_distance = math.hypot(x - CENTER[0], y - CENTER[1])
                    if base_distance <= BASE_RADIUS:
                        base_upgrade_cost = base_level * 100  # Increasing cost per level
                        if money >= base_upgrade_cost and base_level < 6:
                            money -= base_upgrade_cost
                            base_level += 1
                            # Upgrade base stats
                            BASE_DAMAGE = int(BASE_DAMAGE * 1.5)
                            BASE_FIRE_RATE = max(0.1, BASE_FIRE_RATE * 0.8)
                            base_range += 50
                            error_message = f"Base upgraded to level {base_level}!"
                            error_timer = 60
                        elif base_level >= 6:
                            error_message = "Base is at maximum level!"
                            error_timer = 60
                        else:
                            error_message = f"Need ${base_upgrade_cost} to upgrade base!"
                            error_timer = 60
                    
                    # Check if clicking on a tower
                    else:
                        for tower in towers:
                            tower_distance = math.hypot(x - tower.x, y - tower.y)
                            if tower_distance <= 40:  # Click radius for towers
                                upgrade_cost = tower.level * 75  # Increasing cost per level
                                if money >= upgrade_cost and tower.level < 3:
                                    money -= upgrade_cost
                                    tower.upgrade()
                                    # Update tower image based on new level
                                    if tower.level <= len(TOWER_IMAGES):
                                        tower.image = TOWER_IMAGES[tower.level - 1]
                                    error_message = f"Tower upgraded to level {tower.level}!"
                                    error_timer = 60
                                elif tower.level >= 3:
                                    error_message = "Tower is at maximum level!"
                                    error_timer = 60
                                else:
                                    error_message = f"Need ${upgrade_cost} to upgrade tower!"
                                    error_timer = 60
                                break

                elif can_place_tower(x, y) and not upgrade_mode:

                    temp_tower = Tower(x, y, CENTER, tower_type=selected_tower_type, image=TOWER_IMAGES[0], bullet_image=FIREBALL_IMAGE)

                    if money >= temp_tower.cost:
                        towers.append(temp_tower)
                        money -= temp_tower.cost
                    else:
                        error_message = "Not Enough Money!"
                        error_timer = 60


        pygame.draw.circle(WIN, (180, 180, 180), CENTER, 150, 2)
        pygame.draw.circle(WIN, (180, 180, 180), CENTER, 75, 2)
        # Spawn enemies
        
        # ---------------- BASE SHOOTING ----------------
        if base_cooldown > 0:
            base_cooldown -= 1
        else:
            closest_enemy = None
            closest_distance = float("inf")

            for enemy in enemies:
                distance = math.hypot(enemy.x - CENTER[0], enemy.y - CENTER[1])
                if distance < closest_distance and distance <= base_range:
                    closest_distance = distance
                    closest_enemy = enemy

            if closest_enemy:
                bullets.append(
                    Bullet(
                        CENTER[0],
                        CENTER[1]-21,
                        closest_enemy,
                        BASE_DAMAGE,
                        BASEFIREBALL_IMAGE
                    )
                )
                base_cooldown = BASE_FIRE_RATE
            # Update enemies
        for enemy in enemies[:]:
            if not upgrade_mode:
                enemy.move()
                enemy.animate()
            enemy.draw(WIN)
            if enemy.reached_base(BASE_RADIUS):
                base_health -= 1
                enemies.remove(enemy)
            elif enemy.health <= 0:
                enemies.remove(enemy)
                killcount += 1
                money += enemy.reward        # After enemy updates, after killcount increases
        difficulty_level = killcount // 10
        multiplier = 1 + (difficulty_level * 0.05)
        spawn_interval = max(90 - difficulty_level * 5, 15)        

        if not upgrade_mode:
            spawn_timer += 1
            if spawn_timer > spawn_interval:
                enemy_type = random.choice(ENEMY_TYPES)

                enemies.append(
                    Enemy(WIDTH, HEIGHT, CENTER, [enemy_type], multiplier, multiplier)
                )
                spawn_timer = 0
        # Towers
        if not upgrade_mode:
            for tower in towers:
                tower.shoot(enemies, bullets)

        # Bullets
        if not upgrade_mode:
            for bullet in bullets[:]:
                if bullet.move():
                    bullets.remove(bullet)

        # Draw base
        current_base_image = BASE_IMAGES[min(base_level - 1, len(BASE_IMAGES) - 1)]
        base_rect = current_base_image.get_rect(center=(CENTER[0], CENTER[1] - 40))
        WIN.blit(current_base_image, base_rect)
        
        if upgrade_mode:
            # Show base level
            base_level_display = FONT.render(f"Base Lv.{base_level}", True, (0, 0, 0))
            WIN.blit(base_level_display, (CENTER[0] - 40, CENTER[1] - 80))
            
            if base_level < 6:
                base_cost_display = FONT.render(f"${base_level * 100}", True, (255, 0, 0))
                WIN.blit(base_cost_display, (CENTER[0] - 25, CENTER[1] + 20))
        # Draw objects
        for tower in towers:
            tower.draw(WIN)
            if upgrade_mode:
                # Show tower level and upgrade cost
                level_text = FONT.render(f"Lv.{tower.level}", True, (0, 0, 0))
                WIN.blit(level_text, (tower.x - 15, tower.y - 50))
                
                if tower.level < 3:
                    cost_text = FONT.render(f"${tower.level * 75}", True, (255, 0, 0))
                    WIN.blit(cost_text, (tower.x - 15, tower.y + 40))

        for enemy in enemies:
            enemy.draw(WIN)

        for bullet in bullets:
            bullet.draw(WIN)
        money_text = FONT.render(f"Money: ${money}", True, BLACK)
        WIN.blit(money_text, (10, 10))
        health_text = FONT.render(f"Health: {base_health}", True, BLACK)
        WIN.blit(health_text, (10, 40))
        kill_count_text = FONT.render(f"Kills: {killcount}", True, BLACK)
        WIN.blit(kill_count_text, (10, 70))
        difficulty_text = FONT.render(f"Difficulty: {difficulty_level}", True, BLACK)
        WIN.blit(difficulty_text, (10, 100))
        base_level_text = FONT.render(f"Base Level: {base_level}", True, BLACK)
        WIN.blit(base_level_text, (10, 130))
        # Draw Buttons
        pygame.draw.rect(WIN, BLUE if selected_tower_type == 1 else (100,100,100), button1_rect)
        pygame.draw.rect(WIN, (150,50,200) if selected_tower_type == 2 else (100,100,100), button2_rect)
        pygame.draw.rect(WIN, (255,200,0) if upgrade_mode else (100,100,100),upgrade_button_rect)


        text1 = FONT.render("Tower 1", True, WHITE)
        text2 = FONT.render("Tower 2", True, WHITE)

        WIN.blit(text1, (button1_rect.x + 25, button1_rect.y + 10))
        WIN.blit(text2, (button2_rect.x + 25, button2_rect.y + 10))
        upgrade_text = FONT.render("Upgrade", True, BLACK)
        WIN.blit(upgrade_text, (upgrade_button_rect.x + 25, upgrade_button_rect.y + 10))


        if upgrade_mode:
            upgrade_instructions = FONT.render("UPGRADE MODE: Click towers or base to upgrade", True, (255, 100, 100))
            WIN.blit(upgrade_instructions, (WIDTH // 2 - upgrade_instructions.get_width() // 2 + 50, 10))
            
            base_upgrade_cost = base_level * 100 if base_level < 6 else 0
            base_cost_text = FONT.render(f"Base Upgrade: ${base_upgrade_cost}", True, (100, 100, 255))
            WIN.blit(base_cost_text, (WIDTH // 2 - base_cost_text.get_width() // 2 + 50, 35))
        # pygame.display.update()

        if base_health <= 0:
            print("Game Over")
            error_text = FONT.render("Game Over", True, (255, 0, 0))
            WIN.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, 50))
            error_timer -= 1
            pygame.display.update()
            time.sleep(2)
            running = False
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main_menu()
