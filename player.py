from pygame import Surface
import pygame
from pygame.locals import *
from entity import Entity
from obstacle import Obstacle
from enemy import Enemy
from sword import Sword


class Player(Entity):
    """
    Defines a player in Block Adventure.

    == Attributes ==
    attacking: Stores whether the player is attacking.
    attacked: Whether the player has been attacked.
    hp: Number of health points the player has.
    max_hp: The maximum number of hp the player can have.
    sword: the sword of the player.
    time: Stores various timers.

    == Representation Invariants ==
    hp >= 0
    """
    attacking: bool
    hp: int
    sword: Sword
    time: dict[str:float]
    attacked: bool
    max_hp: int

    SIZE = 30
    SPEED = 2.5  # standard movement speed.

    def __init__(self, x: float, y: float, hp: int) -> None:
        """
        Initialize player. Begins at position (<x>, <y>) and
        with <hp> health points
        """
        self.attacked = False
        self.max_hp = hp
        self.hp = hp
        self.sword = Sword()
        self.attacking = False
        self.time = {'ATK': 0.0, 'invulnerability': 0.0}
        from sprites import player_sprites
        super().__init__(x, y, player_sprites, 'u', 0)

    def update(self) -> None:
        """
        Update the player's position and attack mode.
        The player's attack mode should last only 0.2 seconds.
        """
        if self.attacking:
            # Check if the time elapsed since the attack was initiated
            # is surpassed. If yes the player stops attacking
            if pygame.time.get_ticks() - self.time['ATK'] >= 200:
                self.attacking = False

        self.move()

    def is_struck(self, direction_atk: str, strength_atk: int) -> None:
        """
        The player's hp is decreased by <strength_atk> and it is
        knocked back in the direction opposite to the direction in which
        it was attacked (<direction_atk>).
        """
        if pygame.time.get_ticks() - self.time['invulnerability'] >= 1000:
            self.hp -= strength_atk
            # self.attacked = True
            self.speed = 0  # When attacked the player should not move
            # voluntarily.
            self.time['invulnerability'] = pygame.time.get_ticks()

    def _set_direction(self, event: pygame.event) -> None:
        """
        Determine the direction Player should move given the
        event object. If the player has been attacked, it cannot not
        move voluntarily.
        """
        if not self.attacked:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self._direction = 'r'
                    self.speed = Player.SPEED
                    self.attacking = False
                elif event.key == K_LEFT:
                    self._direction = 'l'
                    self.speed = Player.SPEED
                    self.attacking = False
                elif event.key == K_UP:
                    self._direction = 'u'
                    self.speed = Player.SPEED
                    self.attacking = False
                elif event.key == K_DOWN:
                    self._direction = 'd'
                    self.speed = Player.SPEED
                    self.attacking = False
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    if self._direction == 'r':
                        self.speed = 0
                elif event.key == K_LEFT:
                    if self._direction == 'l':
                        self.speed = 0
                elif event.key == K_UP:
                    if self._direction == 'u':
                        self.speed = 0
                elif event.key == K_DOWN:
                    if self._direction == 'd':
                        self.speed = 0

    def _set_attack(self, event: pygame.event):
        """
        Change attacking to True if the user presses
        the space bar.
        """
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not self.attacking:
                    self.attacking = True
                    self.time['ATK'] = pygame.time.get_ticks()

    def handle_events(self, event: pygame.event) -> None:
        """
        Handle all events for the player.
        """
        self._set_attack(event)
        self._set_direction(event)

    def react_collision(self, ent: 'Entity') -> None:
        """
        React to a collision with <ent>.
        """
        if isinstance(ent, Obstacle):
            if self._direction == 'u':
                self.move(- (ent._y_pos + ent.size[1]) + self._y_pos)
            elif self._direction == 'd':
                self.move(-(self._y_pos + self.size[1]) + ent._y_pos)
            elif self._direction == 'l':
                self.move(- (ent._x_pos + ent.size[0]) + self._x_pos)
            else:  # self.direction == 'r':
                self.move(-(self._x_pos + self.size[0]) + ent._x_pos)
        elif isinstance(ent, Enemy):
            self.is_struck(ent._direction, ent.strength)

    def update_sword_position(self) -> None:
        """
        Update the position of the sword according to
        the position and direction of the player. The hit box
        of the sword is also updated according
        """
        self.sword._direction = self._direction
        if self._direction == 'd':
            self.sword.set_position((self._x_pos - 2, self._y_pos + 20))
        elif self._direction == 'u':
            self.sword.set_position((self._x_pos + 2, self._y_pos - 25))
        elif self._direction == 'r':
            self.sword.set_position((self._x_pos + 20, self._y_pos + 10))
        else:  # self.direction == 'l'
            self.sword.set_position((self._x_pos - 20, self._y_pos + 10))

    def draw(self, surf: Surface) -> None:
        """
        Blit player_sprite to surf.
        """
        self.update_sword_position()
        if self._direction == 'u':
            if self.attacking:
                self.sword.draw(surf)
            surf.blit(self.sprite['u'], (self._x_pos, self._y_pos))
        else:
            surf.blit(self.sprite[self._direction], (self._x_pos, self._y_pos))
            if self.attacking:
                self.sword.draw(surf)
