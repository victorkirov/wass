from enum import Enum
from os import listdir, walk
from os.path import isdir, isfile, join
from typing import List, Optional, Tuple

from PIL import Image
from PIL.ImageFile import ImageFile

import wass.config as config


class Direction(Enum):
    """
    Specifies the direction to move to the next image
    """
    Forward: int = 1
    Reverse: int = -1


class ImageManager:
    """
    Manages the folders where images are sourced and the current folder and image in that folder
    being displayed
    """
    def __init__(self) -> None:
        self._image_folders: List[str] = []
        self._folder_index: Optional[int] = None
        self._folder_files: List[str] = []
        self._file_index: Optional[int] = None

        self._current_image: Optional[ImageFile] = None

    @property
    def current_image(self) -> Optional[ImageFile]:
        """
        Returns the current image being displayed
        """
        return self._current_image

    @property
    def next_image(self) -> Optional[ImageFile]:
        """
        Sets the current image to the next available image and returns it
        """
        self._go_to_next_image(Direction.Forward)
        return self._current_image

    @property
    def previous_image(self) -> Optional[ImageFile]:
        """
        Sets the current image to the previous available image and returns it
        """
        self._go_to_next_image(Direction.Reverse)
        return self._current_image

    def _go_to_next_image(self, direction: Direction = Direction.Forward) -> None:
        # we haven't got a current image so initialise
        if None in (self._folder_index, self._file_index):
            self.go_to_next_folder()

        # We keep track of this in case there are no available images so we don't get lost in an
        # infinite loop while looking for one
        initial_folder_index = self._folder_index
        first_pass = True

        while True:
            # try and get the next image in the folder
            next_file_index, next_image = self._get_next_image_in_current_folder(direction)

            if next_image:
                self._current_image = next_image
                self._file_index = next_file_index
                return

            # go through folders looking for next image
            self.go_to_next_folder(direction)

            if not first_pass and initial_folder_index == self._folder_index:
                # we are back at the initial folder and haven't found any images
                break

            first_pass = False

        # no images found in any of the folders
        self._current_image = None

    def _generate_folder_list(self):
        folders = {config.ROOT_IMAGE_FOLDER}
        for dirpath, dirnames, filenames in walk(config.ROOT_IMAGE_FOLDER):
            folders.update({f'{join(dirpath, dirname)}' for dirname in dirnames})

        self._image_folders = list(folders)
        self._image_folders.sort()

    def _get_next_image_in_current_folder(
        self,
        direction: Direction,
    ) -> Tuple[Optional[int], Optional[ImageFile]]:
        new_file_index = (
            self._file_index + direction.value
            if self._file_index is not None
            else 0 if direction == Direction.Forward
            else len(self._folder_files) - 1
        )

        while 0 <= new_file_index < len(self._folder_files):
            try:
                next_image_filename = self._folder_files[new_file_index]
                next_image = Image.open(next_image_filename)
                return new_file_index, next_image
            except IOError:
                new_file_index = new_file_index + direction.value

        return None, None

    def go_to_next_folder(self, direction: Direction = Direction.Forward) -> None:
        # First step is to regenerate folder list of folders inside the root folder
        if self._folder_index is not None:
            current_folder = self._image_folders[self._folder_index]

            self._generate_folder_list()

            if current_folder not in self._image_folders:
                # old folder no longer exists so go to nearest folder to previous folder index
                self._folder_index = min(self._folder_index, len(self._image_folders) - 1)
            else:
                self._folder_index = self._image_folders.index(current_folder)
        else:
            self._generate_folder_list()

        # Second we try and find the next valid folder to go to
        new_index = (
            self._folder_index + direction.value
            if self._folder_index is not None
            else 0
        )

        while not isdir(self._image_folders[new_index % len(self._image_folders)]):
            if new_index % len(self._image_folders) == self._folder_index:
                raise RuntimeError('No valid directories configured')

            new_index += direction.value

        # we have found an existing folder so extract the files in the folder
        self._folder_index = new_index % len(self._image_folders)
        self._folder_files = [
            join(self._image_folders[self._folder_index], f)
            for f in listdir(self._image_folders[self._folder_index])
            if isfile(join(self._image_folders[self._folder_index], f))
        ]
        self._folder_files.sort()
        self._file_index = None
