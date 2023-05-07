import pygame

from hud import HUD
from player import Player
from pygame.locals import *
from map import GameMap
import sys

if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode((600, 700))
    window.fill((0, 0, 0))
    g_map = GameMap()
    player = Player(x=285, y=500, hp=3)
    hud = HUD(player)
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        clock.tick(60)
        pygame.display.set_caption(f"Block Adventure. FPS: "
                                   f"{int(clock.get_fps())}")

        hud.draw(window)

        # Change rooms if needed.
        temp = g_map.current_room.change_room(player)
        if temp is not None:
            g_map.change_room(temp, player, window)

        # Draw the room to the window
        g_map.current_room.draw_room(window, 0, 0, player, False)

        # Process events from user.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player.handle_events(event)

        # Display the new state of the window.
        pygame.display.update()

