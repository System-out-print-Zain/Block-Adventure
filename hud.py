from player import Player
from pygame import Surface
import pygame


class HUD:
    """
    A HUD (Heads-Up Display) for Block Adventure.

    == Attributes ==
    surface: the surface representing the HUD
    font: The font used for the writing on the HUD
    player: The player the HUD corresponds to.
    """
    def __init__(self, player: Player):
        self.surface = Surface((600, 100))
        self.surface.fill((100, 100, 100))
        pygame.draw.rect(self.surface, (0, 0, 100), (20, 20, 350, 70), 2)
        from sprites import player_down
        player_down = pygame.transform.scale(player_down, (40, 40))
        self.surface.blit(player_down, (30, 30))
        pygame.draw.rect(self.surface, (0, 0, 0), (70, 30, 250, 10))

        self.player = player
        self.font = pygame.font.SysFont('microsoftsansserif', 15)

        # print(pygame.font.get_fonts())

    def draw(self, surf: Surface) -> None:
        """
        Draw the HUD to the screen.
        """
        pygame.draw.rect(self.surface, (0, 0, 0), (70, 30, 250, 10))
        pygame.draw.rect(self.surface, (100, 100, 100), (320, 25, 40, 15))

        t = self.font.render(f'{max(self.player.hp, 0)} / {self.player.max_hp}',
                             True, (255, 255, 255), (100, 100, 100))
        self.surface.blit(t, (330, 25))
        if self.player.hp > 0:
            pygame.draw.rect(self.surface, (255, 0, 0), (80, 34, 230 *
                             (self.player.hp/self.player.max_hp), 3))
        surf.blit(self.surface, (0, 600))


