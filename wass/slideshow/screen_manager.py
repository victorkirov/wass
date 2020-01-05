from typing import List

import screeninfo
from screeninfo.common import Monitor


class ScreenManager:
    """
    Manages which screen the slideshow is displayed on and extracts the screen properties
    """
    def __init__(self) -> None:
        self._screen_index = 0

    @property
    def width(self) -> int:
        """
        The width of the active screen
        """
        return self._current_screen.width

    @property
    def height(self) -> int:
        """
        The height of the active screen
        """
        return self._current_screen.height

    @property
    def x(self) -> int:
        """
        The x co-ordinate of the top left corner of the active screen
        """
        return self._current_screen.x

    @property
    def y(self) -> int:
        """
        The y co-ordinate of the top left corner of the active screen
        """
        return self._current_screen.y

    def go_to_next_screen(self) -> None:
        """
        Switches to the next available screen
        """
        self._screen_index = (self._screen_index + 1) % len(self._all_screens)
        print(self._screen_index)

    def go_to_previous_screen(self) -> None:
        """
        Switches to the previous available screen
        """
        self._screen_index = (
            (self._screen_index + len(self._all_screens) - 1) % len(self._all_screens)
        )

    @property
    def _current_screen(self) -> Monitor:
        return self._all_screens[self._screen_index]

    @property
    def _all_screens(self) -> List[Monitor]:
        return screeninfo.get_monitors()
