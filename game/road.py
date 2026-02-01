import pygame
import os
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Road:
    def __init__(self):
        # Зареждане на фоновата плочка (зелена поляна с къщи/дървета)
        self.bg_tile = pygame.image.load(os.path.join(BASE_DIR, "assets", "background_tile.png")).convert()
        self.bg_tile = pygame.transform.scale(self.bg_tile, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Зареждане на пътя с прозрачност отгоре
        self.road_image = pygame.image.load(os.path.join(BASE_DIR, "assets", "road.png")).convert_alpha()
        self.road_image = pygame.transform.scale(self.road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.tile_width = SCREEN_WIDTH
        self.tile_height = SCREEN_HEIGHT

    def draw(self, surface, offset):
        # Рисуване на фоновете (поляна + сгради)
        start_x = -offset[0] % self.tile_width
        start_y = -offset[1] % self.tile_height

        for x in range(int(start_x - self.tile_width), SCREEN_WIDTH + self.tile_width, self.tile_width):
            for y in range(int(start_y - self.tile_height), SCREEN_HEIGHT + self.tile_height, self.tile_height):
                surface.blit(self.bg_tile, (x, y))

        # Рисуване на пътя отгоре
        for x in range(int(start_x - self.tile_width), SCREEN_WIDTH + self.tile_width, self.tile_width):
            for y in range(int(start_y - self.tile_height), SCREEN_HEIGHT + self.tile_height, self.tile_height):
                surface.blit(self.road_image, (x, y))









