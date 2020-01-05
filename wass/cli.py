import logging
import sys
from logging import basicConfig

import wass.config as config
from wass.slideshow import slideshow_orchestrator
from wass.web_server.server import start_web_server


def configure_logging():
    """helper function to configure logging"""
    log_format = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S %z'
    log_level = logging.WARN

    basicConfig(stream=sys.stdout, level=log_level, format=log_format, datefmt=log_datefmt)


def cli():
    configure_logging()
    if config.WEB_SERVER_ENABLED:
        start_web_server()
    slideshow_orchestrator.run()


cli()
