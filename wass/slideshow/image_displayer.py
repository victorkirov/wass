import sys
import tkinter as tk
from typing import Type

from PIL import Image, ImageTk
from PIL.ImageFile import ImageFile

from wass.slideshow.screen_manager import ScreenManager


class ImageDisplayer(tk.Tk):
    """
    Displays an image on the active screen
    """
    def __init__(
        self,
        screen_manager: ScreenManager,
    ) -> None:
        tk.Tk.__init__(self)
        self.screen_manager = screen_manager

        self.overrideredirect(1)
        self.geometry(
            f'{self.screen_manager.width}x{self.screen_manager.height}'
            f'+{self.screen_manager.x}+{self.screen_manager.y}'
        )
        self.picture_display = tk.Label(self)
        self.picture_display.pack(expand=True, fill='both')

    def display_image(self, image: ImageFile):
        """
        Resizes an image to fill the screen and displays it on the active display
        """
        if not image:
            self.picture_display.config(background='black', cursor='none')
            return

        x_ratio = self.screen_manager.width / image.width
        y_ratio = self.screen_manager.height / image.height

        ratio = y_ratio if x_ratio > y_ratio else x_ratio

        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)

        resized = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_img = ImageTk.PhotoImage(resized)
        self.picture_display.config(image=resized_img, background='black', cursor='none')
        self.picture_display.image = resized_img
        self.title(image.filename)

    def redraw(self):
        """
        Redraws the canvas
        """
        self.withdraw()
        self.geometry(
            f'{self.screen_manager.width}x{self.screen_manager.height}'
            f'+{self.screen_manager.x}+{self.screen_manager.y}'
        )
        self.deiconify()

    def report_callback_exception(
        self,
        exception_type: Type,
        exception: Exception,
        *args,
        **kwargs
    ):
        """
        Catches exceptions generated in tkinter. If keyboard interrupt, then exits application.
        """
        if exception_type is KeyboardInterrupt:
            sys.exit()

    def run(self) -> None:
        self.mainloop()
