import asyncio
import logging
import threading

import wass.config as config
from wass.slideshow.image_displayer import ImageDisplayer
from wass.slideshow.image_manager import Direction, ImageManager
from wass.slideshow.screen_manager import ScreenManager


logger = logging.getLogger(__name__)


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
        """
        Switch to next slide
        """
        logger.info('Switching to next slide')
        next_image = self.image_manager.next_image
        self.displayer.display_image(next_image)
        logger.debug('New image: %s', next_image.filename)

    async def slide_previous(self) -> None:
        """
        Switch to previous slide
        """
        logger.info('Switching to previous slide')
        previous_image = self.image_manager.previous_image
        self.displayer.display_image(previous_image)
        logger.debug('New image: %s', previous_image.filename)

    async def folder_next(self) -> None:
        """
        Switch to next folder
        """
        logger.info('Switching to next folder')
        self.image_manager.go_to_next_folder(Direction.Forward)
        logger.debug('New folder: %s', self.image_manager.folder_name)

    async def folder_previous(self) -> None:
        """
        Switch to previous folder
        """
        logger.info('Switching to previous folder')
        self.image_manager.go_to_next_folder(Direction.Reverse)
        logger.debug('New folder: %s', self.image_manager.folder_name)

    async def screen_next(self) -> None:
        """
        Switch to next screen
        """
        logger.info('Switching to next screen')
        self.screen_manager.go_to_next_screen()
        self.displayer.redraw()

    async def screen_previous(self) -> None:
        """
        Switch to previous screen
        """
        logger.info('Switching to previous screen')
        self.screen_manager.go_to_previous_screen()
        self.displayer.redraw()

    async def play(self) -> None:
        """
        Start the slideshow from pause
        """
        logger.info('Playing slideshow')
        self.playing = True

    async def pause(self) -> None:
        """
        Pause the slideshow
        """
        logger.info('Pausing slideshow')
        self.playing = False

    async def set_delay(self, delay: int) -> None:
        """
        Change the delay between slides
        """
        logger.info('Delay set to %s', delay)
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
        """
        Starts the slideshow
        """
        logger.info('Starting orchestrator loop')
        t = threading.Thread(target=self._start_loop)
        t.setDaemon(True)
        t.start()

        self.displayer.run()
