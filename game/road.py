import random
import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Road:
    """Draw a scrolling road with deterministic roadside scenery."""

    def __init__(self):
        self.road_width = 220
        self.road_center_x = 455
        self.road_left = self.road_center_x - self.road_width // 2
        self.road_right = self.road_center_x + self.road_width // 2
        self.sidewalk_width = 24
        self.dash_height = 42
        self.dash_gap = 34
        self.scenery_spacing = 230

    def player_hit_edge(self, player_rect):
        """Return True when any part of the player's car leaves the asphalt."""
        return player_rect.left < self.road_left or player_rect.right > self.road_right

    def _draw_tree(self, surface, x, y, size):
        # Shadow, trunk and layered foliage give trees a simple top-down look.
        pygame.draw.ellipse(surface, (47, 104, 42), (x - size, y + size // 2, size * 2, size))
        pygame.draw.rect(surface, (105, 73, 43), (x - 4, y + size // 3, 8, size))
        pygame.draw.circle(surface, (37, 115, 48), (x, y), size)
        pygame.draw.circle(surface, (57, 142, 57), (x - size // 3, y - size // 4), max(4, size // 2))
        pygame.draw.circle(surface, (72, 155, 62), (x + size // 4, y - size // 3), max(4, size // 2))

    def _draw_house(self, surface, x, y, width, height, variant):
        # Draw a small house with a roof, door and windows.
        colors = [(220, 194, 151), (193, 208, 218), (218, 174, 157), (205, 207, 167)]
        wall_color = colors[variant % len(colors)]
        pygame.draw.ellipse(surface, (47, 105, 42), (x - width // 2 - 5, y + height // 2 - 2, width + 18, 14))
        pygame.draw.rect(surface, (94, 82, 72), (x - width // 2 - 4, y - height // 2 - 3, width + 8, height + 8))
        pygame.draw.rect(surface, wall_color, (x - width // 2, y - height // 2 + 7, width, height - 1))
        roof_points = [(x - width // 2 - 7, y - height // 2 + 8), (x, y - height // 2 - 12), (x + width // 2 + 7, y - height // 2 + 8)]
        pygame.draw.polygon(surface, (132, 58 + (variant % 2) * 12, 48), roof_points)
        pygame.draw.rect(surface, (102, 69, 47), (x - 5, y + height // 2 - 20, 11, 26))
        pygame.draw.rect(surface, (105, 174, 202), (x - width // 2 + 8, y - 4, 12, 12))
        pygame.draw.rect(surface, (105, 174, 202), (x + width // 2 - 20, y - 4, 12, 12))
        pygame.draw.line(surface, (235, 229, 211), (x - width // 2 + 14, y - 4), (x - width // 2 + 14, y + 8), 2)

    def _draw_scenery(self, surface, offset):
        # Generate scenery from a stable seed per world segment, so it does not
        # flicker or change while the camera moves.
        first_segment = int((offset[1] - SCREEN_HEIGHT) // self.scenery_spacing)
        last_segment = int((offset[1] + SCREEN_HEIGHT) // self.scenery_spacing) + 1
        for segment in range(first_segment, last_segment + 1):
            rng = random.Random(segment + 1741)
            world_y = segment * self.scenery_spacing + self.scenery_spacing // 2
            screen_y = int(world_y - offset[1])
            for side in (-1, 1):
                x = self.road_left - self.sidewalk_width - 55 if side < 0 else self.road_right + self.sidewalk_width + 55
                # Alternate houses and clusters of trees along both sides.
                choice = rng.randrange(4)
                if choice in (0, 1):
                    self._draw_house(surface, x, screen_y, rng.randint(48, 62), rng.randint(42, 54), rng.randrange(4))
                    self._draw_tree(surface, x + side * rng.randint(42, 58), screen_y + rng.randint(-45, 45), rng.randint(12, 18))
                else:
                    self._draw_tree(surface, x, screen_y, rng.randint(15, 22))
                    self._draw_tree(surface, x + side * rng.randint(38, 55), screen_y + rng.randint(-55, 55), rng.randint(11, 17))
                    if choice == 3:
                        self._draw_tree(surface, x - side * 25, screen_y + 65, rng.randint(10, 15))

    def draw(self, surface, offset):
        # Grass background and roadside details.
        surface.fill((77, 155, 63))
        self._draw_scenery(surface, offset)

        screen_road_left = int(self.road_left - offset[0])
        screen_road_right = int(self.road_right - offset[0])

        # Sidewalks and asphalt.
        pygame.draw.rect(
            surface, (190, 190, 180),
            (screen_road_left - self.sidewalk_width, 0,
             self.road_width + 2 * self.sidewalk_width, SCREEN_HEIGHT)
        )
        pygame.draw.rect(surface, (54, 57, 60),
                         (screen_road_left, 0, self.road_width, SCREEN_HEIGHT))

        # Road edges and dashed center line.
        pygame.draw.line(surface, (235, 235, 225),
                         (screen_road_left + 7, 0),
                         (screen_road_left + 7, SCREEN_HEIGHT), 3)
        pygame.draw.line(surface, (235, 235, 225),
                         (screen_road_right - 7, 0),
                         (screen_road_right - 7, SCREEN_HEIGHT), 3)

        pattern_height = self.dash_height + self.dash_gap
        start_y = int((-offset[1]) % pattern_height) - pattern_height
        center_x = int((screen_road_left + screen_road_right) / 2)
        for y in range(start_y, SCREEN_HEIGHT + pattern_height, pattern_height):
            pygame.draw.rect(surface, (230, 230, 215),
                             (center_x - 3, y, 6, self.dash_height))

        # Curb/guardrail posts make the road boundary visually obvious.
        for side_x in (screen_road_left - 5, screen_road_right + 5):
            pygame.draw.line(surface, (90, 92, 91), (side_x, 0), (side_x, SCREEN_HEIGHT), 5)
            post_spacing = 46
            post_start = int((-offset[1]) % post_spacing) - post_spacing
            for y in range(post_start, SCREEN_HEIGHT + post_spacing, post_spacing):
                pygame.draw.rect(surface, (215, 216, 205), (side_x - 3, y, 6, 17))
