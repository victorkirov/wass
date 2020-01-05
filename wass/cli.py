import wass.config as config
from wass.slideshow import slideshow_orchestrator
from wass.web_server.server import start_web_server


def cli():
    if config.WEB_SERVER_ENABLED:
        start_web_server()
    slideshow_orchestrator.run()


cli()
