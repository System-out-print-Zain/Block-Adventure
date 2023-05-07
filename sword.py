from entity import Entity
from pygame import Surface


class Sword(Entity):
    """
    Defines the sword that a player will carry in
    Block Adventure.

    == Attributes ==
    sword_sprite: The visual representation of the sword.
    level: The upgrade level of the sword.
    abilities: The extra abilities of the sword.

    == Representation Invariants ==
    1 <= level <= 3
    The keys of sword_sprite are 'U', 'D', 'L', and 'R'
    """

    sword_sprite: dict[str: Surface]
    level: int
    abilities: list[str]

    def __init__(self) -> None:
        """
        Initialize sword. level starts at 1. Initially there are no abilities.
        """
        self.level = 1
        self.abilities = []

        from sprites import sword_sprites, SWORD_SIZE
        super().__init__(0, 0, sword_sprites, 'u', 0,

                         ((10, 0),
                          (SWORD_SIZE//2 - 5, SWORD_SIZE - 5)),

                         ((10, 5),
                          (SWORD_SIZE//2 - 5, SWORD_SIZE - 5)),

                         ((8, 10),
                          (SWORD_SIZE - 5, SWORD_SIZE//2 - 5)),

                         ((0, 10),
                          (SWORD_SIZE - 5, SWORD_SIZE//2 - 5))

                         )

    def react_collision(self, ent: 'Entity') -> None:
        pass


