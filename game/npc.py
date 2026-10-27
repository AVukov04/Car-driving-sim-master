import os
import random
import pygame
from game.settings import FPS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NPCCar:
    """A traffic car that drives down the road and respawns ahead of the player."""

    LANES = (395, 515)

    def __init__(self):
        self.images = [
            pygame.image.load(os.path.join(BASE_DIR, "assets", filename)).convert_alpha()
            for filename in (
                "npc_car_red.png",
                "npc_car_blue.png",
                "npc_car_yellow.png",
                "npc_car_green.png",
            )
        ]
        self.position = pygame.Vector2(self.LANES[0], 0)
        self.speed = 0.0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=self.position)
        self.reset(800)

    def reset(self, player_y, spawn_distance=None, lane_x=None):
        """Place the car safely ahead of the player, optionally in a chosen lane."""
        if spawn_distance is None:
            spawn_distance = random.randint(750, 1500)
        if lane_x is None:
            lane_x = random.choice(self.LANES)

        self.position = pygame.Vector2(lane_x, player_y - spawn_distance)
        image = random.choice(self.images)
        self.image = pygame.transform.scale(image, (40, 80))
        self.image = pygame.transform.rotate(self.image, 180)
        self.speed = random.uniform(2.2, 3.4)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, player_y, dt):
        frame_factor = min(dt * FPS, 3.0)
        self.position.y += self.speed * frame_factor

        # Recycle cars after they have passed well behind the player.
        if self.position.y > player_y + 650:
            self.reset(player_y)

        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface, offset):
        screen_pos = (self.position.x - offset[0], self.position.y - offset[1])
        surface.blit(self.image, self.image.get_rect(center=screen_pos))
