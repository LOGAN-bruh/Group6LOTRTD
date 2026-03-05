import pygame
import math
import random
import time
pygame.init()
# Load Base Sprite

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
BASE_IMAGE = pygame.image.load("towerlvl1.png").convert_alpha()
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (BASE_RADIUS * 2, BASE_RADIUS * 2))
CANNON_IMAGE = pygame.image.load("lvl1TowerCannon.png").convert_alpha()
CANNON_IMAGE = pygame.transform.scale(CANNON_IMAGE, (125, 125))
FIREBALL_IMAGE = pygame.image.load("FireBall.png").convert_alpha()
FIREBALL_IMAGE = pygame.transform.scale(FIREBALL_IMAGE, (75, 75))
BASEFIREBALL_IMAGE = pygame.image.load("FireBall.png").convert_alpha()
BASEFIREBALL_IMAGE = pygame.transform.scale(BASEFIREBALL_IMAGE, (25, 25))
knight_frame1 = pygame.transform.scale(
    pygame.image.load("knightenemy.png").convert_alpha(), (100, 100)
)

knight_frame2 = pygame.transform.scale(
    pygame.image.load("knightenemyRunning.png").convert_alpha(), (100, 100)
)

hobbit_frame1 = pygame.transform.scale(
    pygame.image.load("hobbitenemy.png").convert_alpha(), (67, 67)
)

hobbit_frame2 = pygame.transform.scale(
    pygame.image.load("hobbitenemyRunning.png").convert_alpha(), (100, 100)
)

mage_frame1 = pygame.transform.scale(
    pygame.image.load("mageenemy.png").convert_alpha(), (100, 100)
)

mage_frame2 = pygame.transform.scale(
    pygame.image.load("mageenemyRunning.png").convert_alpha(), (100, 100)
)



ENEMY_TYPES = [
    {
        "name": "Knight",
        "frames": [knight_frame1, knight_frame2],
        "health": 150,
        "speed": 2,
        "reward": 25
    },
    {
        "name": "Hobbit",
        "frames": [hobbit_frame1, hobbit_frame2],
        "health": 150,
        "speed": 2,
        "reward": 25
    },
    {
        "name": "Mage",
        "frames": [mage_frame1, mage_frame2],
        "health": 150,
        "speed": 2,
        "reward": 25
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

TOWER_IMAGE_1 = pygame.image.load("lvl1TowerCannon.png").convert_alpha()
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

                elif can_place_tower(x, y) and not upgrade_mode:
                    temp_tower = Tower(x, y, tower_type=1, image=CANNON_IMAGE, bullet_image=FIREBALL_IMAGE)


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
        base_rect = BASE_IMAGE.get_rect(center=(CENTER[0], CENTER[1] - 40))
        WIN.blit(BASE_IMAGE, base_rect)
        # Draw objects
        for tower in towers:
            tower.draw(WIN)

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


        if error_timer > 0:
            error_text = FONT.render(error_message, True, (255, 0, 0))
            WIN.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, 50))
            error_timer -= 1
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
