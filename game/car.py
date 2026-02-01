import pygame
import os
import math

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PlayerCar:
    def __init__(self):
        self.original_image = pygame.image.load(os.path.join(BASE_DIR, "assets", "player_car.png"))
        self.original_image = pygame.transform.scale(self.original_image, (40, 83))
        self.image = self.original_image

        self.position = pygame.Vector2(420, 800)  # Централна лента
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.2
        self.max_speed = 5
        self.rotation_speed = 3
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        keys = pygame.key.get_pressed()

        min_turn_speed = 0.5
        if abs(self.speed) >= min_turn_speed:
            if keys[pygame.K_LEFT]:
                self.angle -= self.rotation_speed
            if keys[pygame.K_RIGHT]:
                self.angle += self.rotation_speed

        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        elif keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
        else:
            self.speed *= 0.95

        self.speed = max(-self.max_speed, min(self.speed, self.max_speed))

        rad = math.radians(self.angle)
        dx = math.sin(rad) * self.speed
        dy = math.cos(rad) * self.speed

        self.position.x += dx
        self.position.y -= dy  # минус защото y расте надолу

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)

        # Проверка за излизане от пътя
        if self.position.x < 385 or self.position.x > 525:
            self.speed = 0

    def draw(self, surface, offset):
        rect = self.image.get_rect(center=(self.position.x - offset[0], self.position.y - offset[1]))
        surface.blit(self.image, rect)

    def get_speed_kmh(self):
        return int(abs(self.speed) * 30)























