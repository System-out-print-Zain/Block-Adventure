from typing import Optional
from enemy import *
from player import Player
from obstacle import Obstacle
import pygame


class Room:
    """
    Defines a room in Block Adventure.

    == Attributes ==
    sprite: The visual representation of the room
    door: the doors in the room and the rooms to which they lead.
    obstacles: The obstacles in the room
    enemies: The enemies in the room

    == Representation Invariants ==
    The keys of door are 'N', 'S', 'E', and 'W'
    """
    sprite: pygame.Surface
    door: dict[str: list[bool, Optional['Room']]]
    obstacles = list[Obstacle]
    enemies = list[Enemy]

    FLOOR_COLOUR = (152, 118, 84)
    ROOM_SIZE = 600

    # Door Coordinates; (x1, x2, y1, y2)
    N_DOOR = (270, 330, 0, 0)
    S_DOOR = (270, 330, ROOM_SIZE, ROOM_SIZE)
    W_DOOR = (0, 0, 270, 330)
    E_DOOR = (ROOM_SIZE, ROOM_SIZE, 270, 330)

    def __init__(self, north: bool, south: bool, east: bool, west: bool) -> \
            None:
        """
        Initialize a room. Set the floor colour to FLOOR_COLOUR.
        Stone obstacles are placed as walls. The <north>, <south>,
        <east>, <west> arguments dictate what sides of the room
        have doors.
        """
        self.door = {'N': [], 'S': [], 'E': [],
                     'W': []}

        self.door['N'].append(north)
        self.door['S'].append(south)
        self.door['E'].append(east)
        self.door['W'].append(west)

        self.obstacles = []
        self.enemies = []

        self.sprite = pygame.Surface((Room.ROOM_SIZE, Room.ROOM_SIZE))
        # Set floor colour
        self.sprite.fill(Room.FLOOR_COLOUR)

        # Add the walls
        # Add the northern wall.
        num = Room.ROOM_SIZE//Obstacle.SIZE
        for i in range(num):
            if not north or (north and (8 >= i or i >= 11)):
                self.obstacles.\
                    append(Obstacle(Obstacle.STONE, i * Obstacle.SIZE, 0))

        # Add the southern wall.
        for i in range(num):
            if not south or (south and (8 >= i or i >= 11)):
                self.obstacles.\
                    append(Obstacle(Obstacle.STONE, i * Obstacle.SIZE,
                                    Room.ROOM_SIZE - Obstacle.SIZE))

        # Add the eastern wall.
        for i in range(num - 2):
            if not east or (east and (7 >= i or i >= 10)):
                self.obstacles. \
                    append(Obstacle(Obstacle.STONE, Room.ROOM_SIZE -
                                    Obstacle.SIZE, Obstacle.SIZE +
                                    i * Obstacle.SIZE))

        # Add the western wall.
        for i in range(num - 2):
            if not west or (west and (7 >= i or i >= 10)):
                self.obstacles. \
                    append(Obstacle(Obstacle.STONE, 0, Obstacle.SIZE +
                                    i * Obstacle.SIZE))

    def draw_room(self, surf: pygame.Surface, x: float, y: float,
                  player: Player, room_changing: bool) -> None:
        """
        Draw the room.
        If the room is changing, the player should not move and the enemies
        should not be drawn.
        """
        for obstacle in self.obstacles:
            obstacle.draw(self.sprite)

        self.handle_deaths()

        surf.blit(self.sprite, (x, y))

        if not room_changing:
            player.update()
            self.handle_collisions(player)

            for enemy in self.enemies:
                enemy.update((player.x_pos, player.y_pos))
                enemy.draw(surf)

        player.draw(surf)

    def get_obstacles(self) -> list[Obstacle]:
        """
        Return the list of obstacles in the room
        """
        return self.obstacles

    def add_obstacles(self, h: int, v: int, x: float, y: float,
                      type_obs: tuple[int, int, int]) \
            -> None:
        """
        Add a group of obstacles to the room with <h> stone obstacles in the
        x direction and <v> stone obstacles in the y direction. The
        top left corner of the wall is placed at position (x, y). The obstacles
        are placed contiguously

        == Preconditions ==
        h, v >= 1
        0 <= x, y <= Room.ROOM_SIZE
        type_obs is a constant specified in the Obstacle class.
        """

        for i in range(h):
            for j in range(v):
                self.obstacles.append(Obstacle(type_obs,
                                               x + Obstacle.SIZE * i,
                                               y + Obstacle.SIZE * j))

    def add_enemy(self, enemy: Enemy) -> None:
        """
        Add an enemy to the room
        """
        self.enemies.append(enemy)

    def get_enemies(self) -> list[Enemy]:
        """
        Return a list of all enemies in the room.
        """
        return self.enemies

    def set_neighbors(self, north: Optional['Room'],
                      south: Optional['Room'],
                      east: Optional['Room'],
                      west: Optional['Room']) -> None:
        """
        Set up the rooms connections to other rooms.
        """
        if self.door['N'][0]:
            self.door['N'].append(north)

        if self.door['S'][0]:
            self.door['S'].append(south)

        if self.door['E'][0]:
            self.door['E'].append(east)

        if self.door['W'][0]:
            self.door['W'].append(west)

    def handle_deaths(self) -> None:
        """
        Remove any enemies that have died from the room
        """
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)

    def handle_collisions(self, player: Player) -> None:
        """
        Handle any collisions in this room.
        """
        for obstacle in self.obstacles:

            if player.check_collision(obstacle):
                player.react_collision(obstacle)

            for enemy in self.enemies:

                if enemy.check_collision(obstacle):
                    enemy.react_collision(obstacle)

                if enemy.check_collision(player):
                    enemy.react_collision(player)
                    player.react_collision(enemy)

                if player.attacking and enemy.check_collision(player.sword):
                    enemy.react_collision(player.sword)

    @staticmethod
    def change_room(player: Player) -> Optional[str]:
        """
        Check whether the player is in contact with a door in <room>.
        If so, return the position of the door. If not, return None.

        Note that we need not consider which doors are active in <room>
        because if there is no door, the player can never satisfy the
        condition of being in contact with it.
        """
        temp_n = Room.N_DOOR
        temp_s = Room.S_DOOR
        temp_e = Room.E_DOOR
        temp_w = Room.W_DOOR

        if (player.x_pos + player.size[0] <= temp_w[0]) and \
                (temp_w[2] <= player.y_pos <= temp_w[3]):
            return 'W'

        elif (temp_e[0] <= player.x_pos) and \
                (temp_e[2] <= player.y_pos <= temp_e[3]):
            return 'E'

        elif (player.y_pos + player.size[1] <= temp_n[2]) and \
                (temp_n[0] <= player.x_pos <= temp_n[1]):
            return 'N'

        elif (temp_s[2] <= player.y_pos) and \
                (temp_s[0] <= player.x_pos <= temp_s[1]):
            return 'S'

    def door_to_room(self, door_dir: str) -> 'Room':
        """
        Return the room the door in direction <door_dir> leads to.

        == Preconditions ==
        door_dir is 'N', 'S', 'E', 'W'
        The door in the door_dir direction must exist in the room and
        a room must have been assigned to it using the set_neighbors
        method
        """
        return self.door[door_dir][1]


class Room1(Room):
    """
    The first room in Block Adventure.
    """
    def __init__(self):
        super().__init__(north=False, south=False, west=True, east=True)

        # Obstacles in Room 1.
        super().add_obstacles(1, 4, 90, 50, Obstacle.STONE)
        super().add_obstacles(1, 4, 480, 50, Obstacle.STONE)

        super().add_obstacles(12, 1, 120, 50, Obstacle.STONE)
        super().add_obstacles(1, 1, 123, 150, Obstacle.STONE)
        super().add_obstacles(2, 1, 155, 175, Obstacle.STONE)

        super().add_obstacles(2, 1, 383, 175, Obstacle.STONE)
        super().add_obstacles(1, 1, 445, 150, Obstacle.STONE)

        super().add_obstacles(1, 1, 285, 285, Obstacle.STONE)

        super().add_obstacles(1, 2, 120, 80, Obstacle.BOX)
        super().add_obstacles(1, 2, 450, 80, Obstacle.BOX)

        super().add_obstacles(3, 2, 150, 80, Obstacle.PUDDLE)
        super().add_obstacles(3, 2, 360, 80, Obstacle.PUDDLE)

        super().add_obstacles(1, 2, 240, 80, Obstacle.BOX)
        super().add_obstacles(1, 2, 330, 80, Obstacle.BOX)

        super().add_obstacles(1, 3, 50, 450, Obstacle.STONE)
        super().add_obstacles(1, 3, 520, 450, Obstacle.STONE)
        super().add_obstacles(2, 1, 80, 510, Obstacle.STONE)
        super().add_obstacles(2, 1, 460, 510, Obstacle.STONE)

        super().add_obstacles(1, 1, 85, 475, Obstacle.BOX)
        super().add_obstacles(1, 1, 485, 475, Obstacle.BOX)

        super().add_enemy(MindlessEnemy(init_direct="u", x=50, y=250))
        super().add_enemy(SupervisorEnemy(init_direct='l', x=400, y=300))


class Room2(Room):
    """
    Room number 2 in Block Adventure.
    """
    def __init__(self):
        super().__init__(north=False, south=False, west=False, east=True)

        # Obstacles in room 2

        super().add_obstacles(3, 1, 60, 60, Obstacle.BOX)
        super().add_obstacles(2, 1, 60, 100, Obstacle.BOX)

        super().add_enemy(MindlessEnemy(init_direct="l", x=50, y=150))
        super().add_enemy(MindlessEnemy(init_direct="d", x=530, y=35))


class Room3(Room):
    """
    Room number 3 in Block Adventure.
    """
    def __init__(self):
        super().__init__(north=False, south=False, west=True, east=False)

        # Obstacles in room 2

        super().add_obstacles(3, 1, 60, 60, Obstacle.BOX)
        super().add_obstacles(2, 1, 60, 100, Obstacle.BOX)

        super().add_enemy(MindlessEnemy(init_direct="u", x=50, y=150))
        super().add_enemy(MindlessEnemy(init_direct="l", x=50, y=150))
        super().add_enemy(MindlessEnemy(init_direct="d", x=50, y=150))
