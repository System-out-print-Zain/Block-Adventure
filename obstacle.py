from entity import Entity
from pygame import Surface


class Obstacle(Entity):
    """
    Defines an obstacle in a room. An obstacle is of a fixed size and.
    is a square. Larger obstacles are to be created by adding
    identical obstacles to the room contiguously.
    """
    # The size of a single obstacle
    SIZE = 30

    # The colors of each possible type of obstacle
    STONE = (150, 150, 150)
    BOX = (150, 75, 0)
    PUDDLE = (0, 0, 255)

    def __init__(self, colour: tuple[int, int, int], x: float, y: float) \
            -> None:
        """
        Initialize an obstacle.

        == Preconditions ==
        x, y >= 0
        """
        sprite = Surface((Obstacle.SIZE, Obstacle.SIZE))
        sprite.fill(colour)
        sprites = {'u': sprite, 'd': sprite, 'l': sprite, 'r': sprite}
        super().__init__(x, y, sprites, 'u', 0)

    def react_collision(self, ent: 'Entity') -> None:
        """
        An obstacle does not react to any collisions.
        """
        pass
