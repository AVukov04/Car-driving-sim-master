import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class World:
    def __init__(self, road):
        self.road = road

    def draw(self, surface, offset):
        self.road.draw(surface, offset)




