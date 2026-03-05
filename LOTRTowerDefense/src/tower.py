import math
from bullet import Bullet   # only if Bullet is in separate file

class Tower:
    def __init__(self, x, y, tower_type=1, image=None, bullet_image=None):
        self.x = x
        self.y = y
        self.range = 150
        self.cooldown = 0
        self.tower_type = tower_type
        self.image = image
        self.bullet_image = bullet_image
        
        if self.tower_type == 1:
            self.color = (50, 50, 200)
            self.damage = 50
            self.cost = 50
        else:
            self.color = (150, 50, 200)
            self.damage = 100
            self.cost = 100

    def draw(self, win):
        if self.image:
            rect = self.image.get_rect(center=(self.x, self.y))
            win.blit(self.image, rect)
        else:
            import pygame
            pygame.draw.circle(win, (50, 50, 200), (self.x, self.y), 15)

    def shoot(self, enemies, bullets):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if distance <= self.range:
                bullets.append(
                    Bullet(self.x+25, self.y+35, enemy, self.damage, self.bullet_image)
                )
                self.cooldown = 30
                break
