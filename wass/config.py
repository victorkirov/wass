import os


DEFAULT_SLIDESHOW_DELAY = float(os.environ.get('WASS_DELAY', 2))

ROOT_IMAGE_FOLDER = os.environ.get('WASS_IMAGE_FOLDER', '/home/vic/Pictures/')
ROOT_IMAGE_FOLDER = (
    ROOT_IMAGE_FOLDER
    if ROOT_IMAGE_FOLDER.endswith('/')
    else f'{ROOT_IMAGE_FOLDER}/'
)

WEB_SERVER_ENABLED = bool(os.environ.get('WASS_WEB_ENABLED', True))
WEB_SERVER_HOST = os.environ.get('WASS_HOST', '0.0.0.0')
WEB_SERVER_PORT = int(os.environ.get('WASS_PORT', 5005))
