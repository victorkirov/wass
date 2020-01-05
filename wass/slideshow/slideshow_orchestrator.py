import asyncio
import threading

import wass.config as config
from wass.slideshow.image_displayer import ImageDisplayer
from wass.slideshow.image_manager import Direction, ImageManager
from wass.slideshow.screen_manager import ScreenManager


class SlideshowOrchestrator:
    """
    Runs a slideshow and exposes methods to interact with the slideshow
    """
    def __init__(self) -> None:
        self.image_manager = ImageManager()
        self.screen_manager = ScreenManager()
        self.displayer = ImageDisplayer(self.screen_manager)

        self.delay: float = config.DEFAULT_SLIDESHOW_DELAY
        self.playing = True

    async def slide_next(self) -> None:
        self.displayer.display_image(self.image_manager.next_image)

    async def slide_previous(self) -> None:
        self.displayer.display_image(self.image_manager.previous_image)

    async def folder_next(self) -> None:
        self.image_manager.go_to_next_folder(Direction.Forward)

    async def folder_previous(self) -> None:
        self.image_manager.go_to_next_folder(Direction.Reverse)

    async def screen_next(self) -> None:
        self.screen_manager.go_to_next_screen()
        self.displayer.redraw()

    async def screen_previous(self) -> None:
        self.screen_manager.go_to_previous_screen()
        self.displayer.redraw()

    async def play(self) -> None:
        self.playing = True

    async def pause(self) -> None:
        self.playing = False

    async def set_delay(self, delay: int) -> None:
        self.delay = delay

    async def _run_slideshow(self) -> None:
        while True:
            if self.playing:
                await self.slide_next()
                await asyncio.sleep(self.delay)
            else:
                await asyncio.sleep(0.1)

    def _start_loop(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self._run_slideshow())
        loop.run_forever()

    def run(self) -> None:
        t = threading.Thread(target=self._start_loop)
        t.setDaemon(True)
        t.start()

        self.displayer.run()
