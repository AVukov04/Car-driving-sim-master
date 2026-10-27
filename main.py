import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.road import Road
from game.car import PlayerCar
from game.npc import NPCCar
from game.world import World
from game.coin import Coin


def create_game():
    road = Road()
    world = World(road)
    player_car = PlayerCar()
    # Start with several cars spaced out along the road, alternating lanes.
    traffic = []
    spawn_distances = (700, 1250, 1800, 2350)
    lanes = NPCCar.LANES
    for index, distance in enumerate(spawn_distances):
        npc_car = NPCCar()
        npc_car.reset(
            player_car.position.y,
            spawn_distance=distance,
            lane_x=lanes[index % len(lanes)],
        )
        traffic.append(npc_car)
    # Coins are spaced out and alternate between the two lanes.
    coins = [
        Coin(player_car.position.y, 520 + index * 390, index % 2)
        for index in range(5)
    ]
    return world, player_car, traffic, coins


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Driving Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    large_font = pygame.font.SysFont("Arial", 46, bold=True)

    world, player_car, traffic, coins = create_game()
    running = True
    game_over = False
    coin_count = 0

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_over and event.key == pygame.K_r:
                    world, player_car, traffic, coins = create_game()
                    coin_count = 0
                    game_over = False

        if not game_over:
            player_car.update(dt)
            for npc_car in traffic:
                npc_car.update(player_car.position.y, dt)

            # Collect coins by driving through them. Missed coins are recycled ahead.
            for index, coin in enumerate(coins):
                if player_car.rect.colliderect(coin.rect):
                    coin_count += 1
                    coin.respawn(player_car.position.y, 1700 + index * 130)
                elif coin.update(player_car.position.y, dt):
                    coin.respawn(player_car.position.y, 1700 + index * 130)

            # End the run for traffic collisions or hitting either road edge.
            traffic_collision = any(
                player_car.rect.colliderect(npc_car.rect) for npc_car in traffic
            )
            if traffic_collision or world.road.player_hit_edge(player_car.rect):
                player_car.speed = 0
                game_over = True

        camera_offset = (
            player_car.position.x - SCREEN_WIDTH // 2,
            player_car.position.y - SCREEN_HEIGHT // 2,
        )

        world.draw(screen, camera_offset)
        for npc_car in traffic:
            npc_car.draw(screen, camera_offset)
        for coin in coins:
            coin.draw(screen, camera_offset)
        player_car.draw(screen, camera_offset)

        # HUD
        hud = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 175))
        speed_text = font.render(
            f"SPEED: {player_car.get_speed_kmh()} km/h", True, (255, 255, 255)
        )
        hud.blit(speed_text, (12, 7))
        coin_text = font.render(f"POINTS: {coin_count:02d}", True, (255, 211, 65))
        hud.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 14, 7))
        screen.blit(hud, (0, 0))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 165))
            screen.blit(overlay, (0, 0))
            title = large_font.render("GAME OVER", True, (255, 90, 80))
            hint = font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
