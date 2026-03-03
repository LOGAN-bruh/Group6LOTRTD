import math
import pygame
class Bullet:
    def __init__(self, x, y, target, damage, color):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = damage
        self.color = color

    def move(self):
        if self.target.health <= 0:
            return True

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return True

        self.x += self.speed * dx / distance
        self.y += self.speed * dy / distance

        if distance < 5:
            self.target.health -= self.damage
            return True

        return False

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 5)
