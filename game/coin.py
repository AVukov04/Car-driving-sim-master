import pygame
from game.settings import FPS


class Coin:
    """A collectible coin positioned in one of the road's traffic lanes."""

    LANES = (395, 515)
    SIZE = 28

    def __init__(self, player_y, spawn_distance, lane_index):
        self.lane_index = lane_index
        self.position = pygame.Vector2(self.LANES[lane_index], player_y - spawn_distance)
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def respawn(self, player_y, spawn_distance):
        # Every collected/passed coin switches to the other lane.
        self.lane_index = 1 - self.lane_index
        self.position.update(self.LANES[self.lane_index], player_y - spawn_distance)
        self._update_rect()

    def update(self, player_y, dt):
        # Coins remain in the world; the camera movement makes them approach.
        # Recycle missed coins so the road always has more to collect.
        if self.position.y > player_y + 420:
            return True
        self._update_rect()
        return False

    def _update_rect(self):
        self.rect.center = (round(self.position.x), round(self.position.y))

    def draw(self, surface, offset):
        x = round(self.position.x - offset[0])
        y = round(self.position.y - offset[1])
        radius = self.SIZE // 2
        # A small shadow and layered circles make the coin readable on asphalt.
        pygame.draw.circle(surface, (30, 30, 25), (x + 2, y + 3), radius + 1)
        pygame.draw.circle(surface, (176, 111, 12), (x, y), radius)
        pygame.draw.circle(surface, (255, 197, 35), (x, y), radius - 3)
        pygame.draw.circle(surface, (255, 224, 105), (x - 3, y - 4), radius - 7)
        pygame.draw.circle(surface, (183, 112, 9), (x, y), radius - 7, 2)
        # A simple embossed star-like mark.
        points = [
            (x, y - 6), (x + 2, y - 2), (x + 6, y - 1),
            (x + 3, y + 2), (x + 4, y + 6), (x, y + 4),
            (x - 4, y + 6), (x - 3, y + 2), (x - 6, y - 1),
            (x - 2, y - 2),
        ]
        pygame.draw.polygon(surface, (184, 112, 7), points)
