import pygame
import os
import random

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NPCCar:
    def __init__(self):
        self.images = [
            pygame.image.load(os.path.join(BASE_DIR, "assets", "npc_car_red.png")),
            pygame.image.load(os.path.join(BASE_DIR, "assets", "npc_car_blue.png")),
            pygame.image.load(os.path.join(BASE_DIR, "assets", "npc_car_yellow.png")),
            pygame.image.load(os.path.join(BASE_DIR, "assets", "npc_car_green.png"))
        ]
        self.image = None
        self.lane_x = 380  # Позиция по оста X
        self.position = pygame.Vector2(self.lane_x, 0)
        self.speed = 0
        self.rect = None
        self.reset(0)  # Първоначален spawn

    def reset(self, player_y):
        spawn_distance = random.randint(600, 1200)
        self.position = pygame.Vector2(self.lane_x, player_y - spawn_distance)

        self.image = random.choice(self.images)
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.image = pygame.transform.rotate(self.image, 180)

        self.speed = random.uniform(2.5, 3.5)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, player_y):
        self.position.y += self.speed
        if self.position.y > player_y + 600:
            self.reset(player_y)
        self.rect.center = self.position

    def draw(self, surface, offset):
        screen_pos = (self.position.x - offset[0], self.position.y - offset[1])
        surface.blit(self.image, self.image.get_rect(center=screen_pos))
























