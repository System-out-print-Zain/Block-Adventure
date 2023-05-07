import pygame

"""
Contains the sprites for all entities in tbe game.
"""

# Player Sprites
PLAYER_SIZE = 30

player_up = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_up.fill((200, 0, 0))

player_down = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_down.fill((200, 0, 0))
pygame.draw.rect(player_down, (0, 0, 255),
                 (5, 3, 20, 15))

player_right = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_right.fill((200, 0, 0))
pygame.draw.rect(player_right, (0, 0, 255),
                 (20, 3, 10, 15))

player_left = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_left.fill((200, 0, 0))
pygame.draw.rect(player_left, (0, 0, 255),
                 (0, 3, 10, 15))

# Dictionary of player sprites for all directions.
player_sprites = {'u': player_up, 'd': player_down, 'r': player_right,
                  'l': player_left}

# Sword sprites

SWORD_SIZE = 32

sword_up = pygame.transform.scale(pygame.image.load('images/Sword_Up.png'),
                                  (SWORD_SIZE, SWORD_SIZE))
sword_down = pygame.transform.scale(pygame.image.load('images/Sword_Down.png'),
                                    (SWORD_SIZE, SWORD_SIZE))
sword_right = pygame.transform.scale(pygame.image.load('images/Sword_Right.png')
                                     , (SWORD_SIZE, SWORD_SIZE))
sword_left = pygame.transform.scale(pygame.image.load('images/Sword_Left.png'),
                                    (SWORD_SIZE, SWORD_SIZE))

# Dictionary of sword sprites for all directions.
sword_sprites = {'u': sword_up, 'd': sword_down, 'r': sword_right,
                 'l': sword_left}


# Mindless Enemy Sprites

MINDLESS_SIZE = 25

mindless_sprite = pygame.Surface((MINDLESS_SIZE, MINDLESS_SIZE))
mindless_sprite.fill((0, 175, 0))
pygame.draw.rect(mindless_sprite, (0, 100, 0),
                 (5, 5, 15, 15))

SUPERVISOR_SIZE = 28

supervisor_sprite_l = pygame.Surface((SUPERVISOR_SIZE, SUPERVISOR_SIZE))
supervisor_sprite_l.fill((0, 0, 255))
pygame.draw.rect(supervisor_sprite_l, (0, 0, 0),
                 (0, 0, 8, 16))

supervisor_sprite_r = pygame.Surface((SUPERVISOR_SIZE, SUPERVISOR_SIZE))
supervisor_sprite_r.fill((0, 0, 255))
pygame.draw.rect(supervisor_sprite_r, (0, 0, 0),
                 (20, 0, 8, 16))

supervisor_sprite_d = pygame.Surface((SUPERVISOR_SIZE, SUPERVISOR_SIZE))
supervisor_sprite_d.fill((0, 0, 255))
pygame.draw.rect(supervisor_sprite_d, (0, 0, 0),
                 (10, 0, 8, 16))

supervisor_sprite_u = pygame.Surface((SUPERVISOR_SIZE, SUPERVISOR_SIZE))
supervisor_sprite_u.fill((0, 0, 255))

supervisor_sprites = {'u': supervisor_sprite_u, 'd': supervisor_sprite_d,
                      'l': supervisor_sprite_l, 'r': supervisor_sprite_r}

