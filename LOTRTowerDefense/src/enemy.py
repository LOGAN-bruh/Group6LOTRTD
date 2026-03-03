import pygame
import math
import random

class Enemy:
    def __init__(self, width, height, center, enemy_image,
                 health_multiplier=1, speed_multiplier=1):

        self.WIDTH = width
        self.HEIGHT = height
        self.CENTER = center
        self.image = enemy_image

        self.x, self.y = self.spawn_position()
        self.base_speed = 3
        self.base_health = 100

        self.speed = self.base_speed * speed_multiplier
        self.health = self.base_health * health_multiplier
        self.radius = 10
        self.spawn_pos = (self.x, self.y)

    def spawn_position(self):
        directions = [
            (self.WIDTH//2, 0),
            (self.WIDTH, 0),
            (self.WIDTH, self.HEIGHT//2),
            (self.WIDTH, self.HEIGHT),
            (self.WIDTH//2, self.HEIGHT),
            (0, self.HEIGHT),
            (0, self.HEIGHT//2),
            (0, 0)
        ]
        return random.choice(directions)

    def move(self):
        dx = self.CENTER[0] - self.x
        dy = self.CENTER[1] - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def reached_base(self, base_radius):
        return math.hypot(self.x - self.CENTER[0],
                          self.y - self.CENTER[1]) <= base_radius

    def draw(self, win):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        win.blit(self.image, rect)
