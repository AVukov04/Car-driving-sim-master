import pygame
from game.settings import *
from game.road import Road
from game.car import PlayerCar
from game.npc import NPCCar
from game.world import World

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Driving Simulator")
clock = pygame.time.Clock()

# Обекти
road = Road()
world = World(road)
player_car = PlayerCar()
npc_car = NPCCar()
npc_car.reset(player_car.position.y)

font = pygame.font.SysFont("Arial", 24)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновяване на логика
    player_car.update()
    npc_car.update(player_car.position.y)

    # Сблъсък
    if player_car.rect.colliderect(npc_car.rect):
        player_car.speed = 0
        npc_car.speed = 0

    # Камера (центрирана спрямо играча)
    camera_offset = (
        player_car.position.x - SCREEN_WIDTH // 2,
        player_car.position.y - SCREEN_HEIGHT // 2,
    )

    # Рендиране
    world.draw(screen, camera_offset)
    npc_car.draw(screen, camera_offset)
    player_car.draw(screen, camera_offset)

    # --- HUD ---
    speed_kmh = player_car.get_speed_kmh()
    distance_m = int(player_car.position.y)

    hud_surface = pygame.Surface((SCREEN_WIDTH, 40))
    hud_surface.set_alpha(180)
    hud_surface.fill((0, 0, 0))

    speed_text = font.render(f"Скорост: {speed_kmh} km/h", True, (255, 255, 255))


    hud_surface.blit(speed_text, (10, 5))
    screen.blit(hud_surface, (0, 0))

    pygame.display.flip()

pygame.quit()



















