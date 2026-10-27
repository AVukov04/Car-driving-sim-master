import math
import os
import pygame
from game.settings import FPS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PlayerCar:
    def __init__(self):
        self.original_image = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "player_car.png")
        ).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 83))
        self.image = self.original_image
        self.start_position = (420, 800)
        self.position = pygame.Vector2(self.start_position)
        self.angle = 0
        self.speed = 0.0
        self.acceleration = 0.2
        self.max_speed = 5.0
        self.rotation_speed = 3.0
        self.rect = self.image.get_rect(center=self.position)

    def reset(self):
        self.position = pygame.Vector2(self.start_position)
        self.angle = 0
        self.speed = 0.0
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        frame_factor = min(dt * FPS, 3.0)

        min_turn_speed = 0.5
        if abs(self.speed) >= min_turn_speed:
            turn_direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            self.angle += turn_direction * self.rotation_speed * frame_factor

        if keys[pygame.K_UP]:
            self.speed += self.acceleration * frame_factor
        elif keys[pygame.K_DOWN]:
            self.speed -= self.acceleration * frame_factor
        else:
            self.speed *= 0.95 ** frame_factor

        self.speed = max(-self.max_speed, min(self.speed, self.max_speed))

        radians = math.radians(self.angle)
        self.position.x += math.sin(radians) * self.speed * frame_factor
        self.position.y -= math.cos(radians) * self.speed * frame_factor

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)


    def draw(self, surface, offset):
        rect = self.image.get_rect(
            center=(self.position.x - offset[0], self.position.y - offset[1])
        )
        surface.blit(self.image, rect)

    def get_speed_kmh(self):
        return int(abs(self.speed) * 30)
