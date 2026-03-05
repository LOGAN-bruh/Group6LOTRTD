import pygame
import math
import random


import random
import math
import pygame

class Enemy:
    def __init__(self, width, height, center, enemy_types,
                 health_multiplier=1, speed_multiplier=1):

        self.WIDTH = width
        self.HEIGHT = height
        self.CENTER = center

        # choose random type from what main passed in

        # Pick the enemy type
        enemy_type = random.choice(enemy_types)

        self.frames = enemy_type["frames"]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5

        self.image = self.frames[self.current_frame]  # initial frame


        self.name = enemy_type["name"]
        self.base_health = enemy_type["health"]
        self.base_speed = enemy_type["speed"]
        self.reward = enemy_type["reward"]

        self.health = self.base_health * health_multiplier
        self.speed = self.base_speed * speed_multiplier

        self.x, self.y = self.spawn_position()

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

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
