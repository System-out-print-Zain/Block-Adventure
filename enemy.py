import math

from pygame.surface import Surface
from entity import Entity
from obstacle import Obstacle
from sword import Sword
import pygame


class Enemy(Entity):
    """
    An enemy in Block Adventure. This is an abstract class.

    == Attributes ==
    hp: Health points
    strength: Damage this enemy deals

    == Representation Invariant ==
    hp >= 0
    Obstacle.Size < x_pos, y_pos <= Room.Size - Obstacle.Size - enemy.size
    """
    # Private Attributes
    # _invulnerability_timer: Used to keep track of an enemies period
    # of invulnerability after being hit.
    _invulnerability_timer: float
    hp: int
    strength: int

    def __init__(self, hp: int, x: float, y: float, sprite: dict[str: Surface],
                 direction: str, strength: int, speed: float) \
            -> None:
        """
        Initialize an enemy.
        <sprite> can be a single Surface or a collection of them

        == Preconditions ==
        hp > 0
        Obstacle.Size < x, y < Room.Size - Obstacle.Size - sprite.get_height()
        direction is 'u', 'd', 'r', 'l'
        """
        self.hp = hp
        self.strength = strength
        super().__init__(x, y, sprite, direction, speed)
        self._invulnerability_timer = 0.0

    def is_alive(self) -> bool:
        """
        Return whether the enemy is alive.
        """
        return self.hp > 0

    def update(self, player_coord: tuple[float, float]) -> None:
        """
        Update the state of the enemy using info from the current frame.
        """
        raise NotImplementedError

    def react_collision(self, ent: 'Entity') -> None:
        if isinstance(ent, Sword) and pygame.time.get_ticks() - \
                self._invulnerability_timer >= 500:

            self.hp -= 1
            self._invulnerability_timer = pygame.time.get_ticks()


class MindlessEnemy(Enemy):
    """
    A mindless enemy in Block Adventure.
    """

    SPEED = 1.2  # units per frame

    def __init__(self, x: float, y: float, init_direct: str) -> None:
        """
        Initialize the mindless enemy

        == Preconditions ==
        initial_direct is 'u', 'd', 'l', 'r'
        """

        from sprites import mindless_sprite
        copy = Surface.copy(mindless_sprite)
        sprites = {'u': copy, 'd': copy, 'r': copy, 'l': copy}

        super().__init__(1, x, y, sprites, init_direct, 1, MindlessEnemy.SPEED)

    def _turn_around(self) -> None:
        """
        Turn the enemy towards the opposite direction.
        """
        if self._direction == 'u':
            self._direction = 'd'
        elif self._direction == 'd':
            self._direction = 'u'
        elif self._direction == 'l':
            self._direction = 'r'
        else:
            self._direction = 'l'

    def update(self, player_coord: tuple[float, float]) -> None:
        self.move()

    def react_collision(self, ent: 'Entity') -> None:
        """
        React to a collision with <ent>.
        """
        super().react_collision(ent)
        if isinstance(ent, Obstacle):
            if self._direction == 'u':
                self.move(- (ent.y_pos + ent.size[1]) + self.y_pos)
                self._turn_around()
            elif self._direction == 'd':
                self.move(-(self.y_pos + self.size[1]) + ent.y_pos)
                self._turn_around()
            elif self._direction == 'l':
                self.move(- (ent.x_pos + ent.size[0]) + self.x_pos)
                self._turn_around()
            else:  # self.direction == 'r':
                self.move(-(self.x_pos + self.size[0]) + ent.x_pos)
                self._turn_around()


class SupervisorEnemy(Enemy):
    """
    A class representing a Supervisor enemy from Block Adventure.
    When the player is out of range, this enemy is idle and walks around
    as a patrol would. When the player is within range, this enemy pursues
    it.
    == Attributes ==
    target: The player that the Supervisor targets
    """
    # Private Attributes:
    # _pursuing: True iff the enemy is in pursuit.
    # _distance: The distance travelled in a particular direction when
    # the enemy is not pursuing.
    _pursuing: bool
    _distance: int

    STANDARD_SPEED = 0.5
    CHASE_SPEED = 1.8

    def __init__(self, x: float, y: float, init_direct: str) \
            -> None:
        """
        Initialize a Supervisor Enemy.
        """
        from sprites import supervisor_sprites
        super().__init__(3, x, y, supervisor_sprites, init_direct, 1,
                         SupervisorEnemy.STANDARD_SPEED)
        self._pursuing = False
        self._distance = 0

    def _calc_dist_to_target(self, player_coord: tuple[float, float]) -> float:
        """
        Return the distance between the Supervisor and the target.
        """
        x1 = player_coord[0]
        y1 = player_coord[1]
        x2 = self.x_pos
        y2 = self.y_pos

        return math.dist([x1, y1], [x2, y2])

    def _turn_right(self) -> None:
        """
        Turn the Supervisor to the right.
        """
        if self._direction == 'u':
            self._direction = 'r'
        elif self._direction == 'd':
            self._direction = 'l'
        elif self._direction == 'r':
            self._direction = 'd'
        else:
            self._direction = 'u'

    def standard_movement(self) -> None:
        """
        Defines the movement of the Supervisor when the player has not been
        detected.
        """
        self.speed = SupervisorEnemy.STANDARD_SPEED
        if self._distance < 100:
            self.move()
            self._distance += self.speed
        else:
            self._distance = 0
            self._turn_right()

    def pursuit_movement(self, player_coord: tuple[float, float]) -> None:
        """
        Defines the movement of the Supervisor when the player has been
        detected
        """
        self.speed = SupervisorEnemy.CHASE_SPEED
        player_x = player_coord[0]
        player_y = player_coord[1]

        y_speed = min(abs(player_y - self.y_pos), self.speed)
        x_speed = min(abs(player_x - self.x_pos), self.speed)

        if player_y < self.y_pos:
            self._direction = 'u'
            self.move(y_speed)
        elif player_y > self.y_pos:
            self._direction = 'd'
            self.move(y_speed)
        elif player_x < self.x_pos:
            self._direction = 'l'
            self.move()
        else:
            self._direction = 'r'
            self.move(x_speed)

    def update(self, player_coord: tuple[float, float]) -> None:
        if self._calc_dist_to_target(player_coord) < 150:
            self._pursuing = True
        else:
            self._pursuing = False

        if not self._pursuing:
            self.standard_movement()
        else:
            self.pursuit_movement(player_coord)

    def react_collision(self, ent: 'Entity') -> None:
        super().react_collision(ent)
        if isinstance(ent, Obstacle):
            if self._direction == 'u':
                self.move(- (ent.y_pos + ent.size[1]) + self.y_pos)
                self._turn_right()
                self._distance = 0
            elif self._direction == 'd':
                self.move(-(self.y_pos + self.size[1]) + ent.y_pos)
                self._turn_right()
                self._distance = 0
            elif self._direction == 'l':
                self.move(- (ent.x_pos + ent.size[0]) + self.x_pos)
                self._turn_right()
                self._distance = 0
            else:  # self.direction == 'r':
                self.move(-(self.x_pos + self.size[0]) + ent.x_pos)
                self._turn_right()
                self._distance = 0

