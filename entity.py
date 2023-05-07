from pygame import Surface


def get_opposite(direction: str) -> str:
    """
    Return the direction opposite to <direction>.
    == Preconditions ==
    <direction> is 'u', 'd', 'r', or 'l'
    """
    if direction == 'u':
        return 'd'
    elif direction == 'd':
        return 'u'
    elif direction == 'r':
        return 'l'
    else:
        return 'r'


class Entity:
    """
    Represents anything in Block Adventure that has interactions with
    other things. Note: All entities are rectangular in
    Block Adventure.

    == Attributes ==
    size: The size of the entity. (width, height)
    _x_pos: The x position of the entity.
    _y_pos: The y position of the entity.
    sprite: The visual representation of the entity.
    _direction: direction that the entity is facing
    hit_box: Hit boxes for the entity.

    == Representation Invariants ==
    size > 0
    -direction is 'u', 'd', 'l', or 'r'
    """
    size: (float, float)
    _x_pos: float
    _y_pos: float
    _direction: str
    speed: float
    sprite: dict[str: Surface]

    class HitBox:
        """
        A hit box for an entity.

        size = (width, height)
        """
        def __init__(self, init_point: tuple[float, float],
                     ref_point: tuple[float, float],
                     size: tuple[float, float]) \
                -> None:
            self.x_pos = init_point[0]
            self.y_pos = init_point[1]
            self.set_point = lambda ent_x, ent_y: (ent_x + (init_point[0] -
                                                            ref_point[0]), ent_y
                                                         + (init_point[1] -
                                                            ref_point[1]))
            self.size = size

        def update_pos(self, ent_pos: tuple[float, float]) -> None:
            """
            Update the position of the hit box to <ent_pos>.
            """
            self.x_pos, self.y_pos = self.set_point(ent_pos[0], ent_pos[1])

    hit_box: dict[str: list[HitBox]]

    def __init__(self, x: float, y: float, sprite: dict[str: Surface],
                 direction: str, speed: float, hit_box_u=None, hit_box_d=None,
                 hit_box_r=None, hit_box_l=None) \
            -> None:
        """
        Initialize an entity.
        == Preconditions ==
        Each hit box argument, if given, are 2-tuples containing the position
        of the hit box and its size. Each argument corresponds to a different
        hit box for when the entity is facing a different direction.
        """
        self._x_pos = x
        self._y_pos = y
        self.sprite = sprite
        self.size = (sprite['u'].get_width(), sprite['u'].get_height())
        self._direction = direction
        self.speed = speed
        self.hit_box = {}

        if hit_box_u is None:
            # The hit box is perfectly fitted to the sprite of the entity
            self.hit_box['u'] = Entity.HitBox(init_point=(x, y),
                                              size=self.size,
                                              ref_point=(x, y))
        else:
            self.hit_box['u'] = Entity.HitBox(init_point=hit_box_u[0],
                                              size=hit_box_u[1],
                                              ref_point=(x, y))

        if hit_box_d is None:
            # The hit box is perfectly fitted to the sprite of the entity
            self.hit_box['d'] = Entity.HitBox(init_point=(x, y),
                                              size=self.size,
                                              ref_point=(x, y))
        else:
            self.hit_box['d'] = Entity.HitBox(init_point=hit_box_d[0],
                                              size=hit_box_d[1],
                                              ref_point=(x, y))

        if hit_box_l is None:
            # The hit box is perfectly fitted to the sprite of the entity
            self.hit_box['l'] = Entity.HitBox(init_point=(x, y),
                                              size=self.size,
                                              ref_point=(x, y))
        else:
            self.hit_box['l'] = Entity.HitBox(init_point=hit_box_l[0],
                                              size=hit_box_l[1],
                                              ref_point=(x, y))

        if hit_box_r is None:
            # The hit box is perfectly fitted to the sprite of the entity
            self.hit_box['r'] = Entity.HitBox(init_point=(x, y),
                                              size=self.size,
                                              ref_point=(x, y))
        else:
            self.hit_box['r'] = Entity.HitBox(init_point=hit_box_r[0],
                                              size=hit_box_r[1],
                                              ref_point=(x, y))

    @property
    def x_pos(self):
        return self._x_pos

    @property
    def y_pos(self):
        return self._y_pos

    def check_collision(self, ent: 'Entity') -> bool:
        """
        Check if this entity and <ent> are touching each other.
        """
        x1, x2 = min(self.hit_box[self._direction].x_pos,
                     ent.hit_box[ent._direction].x_pos), \
            max(self.hit_box[self._direction].x_pos +
                self.hit_box[self._direction].size[0],
                ent.hit_box[ent._direction].x_pos +
                ent.hit_box[ent._direction].size[0])

        y1, y2 = min(self.hit_box[self._direction].y_pos,
                     ent.hit_box[ent._direction].y_pos), \
            max(self.hit_box[self._direction].y_pos +
                self.hit_box[self._direction].size[1],
                ent.hit_box[ent._direction].y_pos +
                ent.hit_box[ent._direction].size[1])

        if x2 - x1 < self.hit_box[self._direction].size[0] + \
                ent.hit_box[ent._direction].size[0] and y2 - y1 < \
                self.hit_box[self._direction].size[1] + \
                ent.hit_box[ent._direction].size[1]:

            return True

        else:

            return False

    def draw(self, surf: Surface) -> None:
        """
        Draw the sprite of this entity to the surface <surf>.
        """
        surf.blit(self.sprite[self._direction], (self._x_pos, self._y_pos))

    def react_collision(self, ent: 'Entity') -> None:
        """
        React to a collision with <ent>
        """
        raise NotImplementedError

    def move(self, speed=None, direction=None) -> None:
        """
        Move the moving entity.
        """
        if speed is None:
            speed = self.speed
        if direction is None:
            direction = self._direction
        if direction == 'u':
            self._y_pos -= speed
            for d in 'u', 'd', 'l', 'r':
                self.hit_box[d].y_pos -= speed
        elif direction == 'd':
            self._y_pos += speed
            for d in 'u', 'd', 'l', 'r':
                self.hit_box[d].y_pos += speed
        elif direction == 'r':
            self._x_pos += speed
            for d in 'u', 'd', 'l', 'r':
                self.hit_box[d].x_pos += speed
        else:  # direction == 'l'
            self._x_pos -= speed
            for d in 'u', 'd', 'l', 'r':
                self.hit_box[d].x_pos -= speed

    def set_position(self, destination: tuple[float, float]) -> None:
        """
        Change the position of the entity to <destination>
        """
        self._x_pos, self._y_pos = destination
        for d in 'u', 'd', 'l', 'r':
            self.hit_box[d].update_pos(destination)


