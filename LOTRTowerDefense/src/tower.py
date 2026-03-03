import math
from bullet import Bullet   # only if Bullet is in separate file

class Tower:
    def __init__(self, x, y, tower_type=1):
        self.x = x
        self.y = y
        self.range = 150
        self.cooldown = 0
        self.tower_type = tower_type

        if self.tower_type == 1:
            self.color = (50, 50, 200)
            self.damage = 50
            self.cost = 50
        else:
            self.color = (150, 50, 200)
            self.damage = 100
            self.cost = 100

    def draw(self, win):
        import pygame
        pygame.draw.circle(win, self.color, (self.x, self.y), 15)

    def shoot(self, enemies, bullets):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if distance <= self.range:
                bullets.append(
                    Bullet(self.x, self.y, enemy, self.damage, self.color)
                )
                self.cooldown = 30
                break
