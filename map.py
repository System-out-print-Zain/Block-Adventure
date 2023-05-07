from room import *
from player import Player


class GameMap:
    """
    A game map for block adventure

    == Attributes ==
    current_room: The room in which the player is currently playing.
    """
    current_room: Room

    def __init__(self) -> None:
        """
        Initialize a game map.
        """
        # The rooms included in the map
        room1 = Room1()
        room2 = Room2()
        room3 = Room3()

        # The connections between the rooms
        # Each door in every room must be assigned to a room
        # Directions must make sense; that is, if there is a western door in
        # room1 that leads to room2, then room2 must have an eastern door.
        room1.set_neighbors(east=room3, west=room2, north=None, south=None)
        room2.set_neighbors(east=room1, west=None, north=None, south=None)
        room3.set_neighbors(east=None, west=room1, north=None, south=None)

        # The room in which the player will start.
        self.current_room = room1

    def change_room(self, door_dir: str, player: Player, window:
                    pygame.Surface) -> None:
        """
        Change the current room to the room that corresponds to the door
        in direction <door_dir>. Run an animation that shifts the camera to
        the next room.

        == Preconditions ==
        door_dir is 'N', 'S', 'E', or 'W'
        The door must exist in the direction above for the current room.
        """
        next_room = self.current_room.door_to_room(door_dir)

        # Animation
        l_shifted = 0
        # The rooms shift by 3 pixels every frame.
        inc = 3.5

        while l_shifted < Room.ROOM_SIZE:
            l_shifted += inc

            if door_dir == 'W':
                next_room.draw_room(window, l_shifted - Room.ROOM_SIZE, 0,
                                    player, True)
                player.set_position((player.x_pos + inc, player.y_pos))

                self.current_room.draw_room(window, l_shifted, 0, player,
                                            True)

            elif door_dir == 'E':
                next_room.draw_room(window, Room.ROOM_SIZE - l_shifted, 0,
                                    player, True)
                player.set_position((player.x_pos - inc, player.y_pos))

                self.current_room.draw_room(window, -l_shifted, 0, player,
                                            True)

            elif door_dir == 'N':
                next_room.draw_room(window, 0, l_shifted - Room.ROOM_SIZE,
                                    player, True)

                player.set_position((player.x_pos, player.y_pos + inc))

                self.current_room.draw_room(window, 0, l_shifted, player,
                                            True)

            elif door_dir == 'S':
                next_room.draw_room(window, 0, Room.ROOM_SIZE - l_shifted,
                                    player, True)

                player.set_position((player.x_pos, player.y_pos - inc))

                self.current_room.draw_room(window, 0, -l_shifted, player,
                                            True)

            pygame.display.update()

        # Set the current room to the next room.
        self.current_room = next_room

