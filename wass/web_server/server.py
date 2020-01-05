import asyncio
import threading
from typing import Any

from quart import Quart, request

import wass.config as config
from wass.slideshow import slideshow_orchestrator


app = Quart(__name__)


@app.route('/api/slide/next', methods=['POST'])
async def slide_next() -> Any:
    await slideshow_orchestrator.slide_next()
    return 'OK'


@app.route('/api/slide/previous', methods=['POST'])
async def slide_previous() -> Any:
    await slideshow_orchestrator.slide_previous()
    return 'OK'


@app.route('/api/folder/next', methods=['POST'])
async def folder_next() -> Any:
    await slideshow_orchestrator.folder_next()
    return 'OK'


@app.route('/api/folder/previous', methods=['POST'])
async def foler_previous() -> Any:
    await slideshow_orchestrator.folder_previous()
    return 'OK'


@app.route('/api/screen/next', methods=['POST'])
async def screen_next() -> Any:
    await slideshow_orchestrator.screen_next()
    return 'OK'


@app.route('/api/screen/previous', methods=['POST'])
async def screen_previous() -> Any:
    await slideshow_orchestrator.screen_previous()
    return 'OK'


@app.route('/api/slideshow/play', methods=['POST'])
async def slideshow_play() -> Any:
    await slideshow_orchestrator.play()
    return 'OK'


@app.route('/api/slideshow/pause', methods=['POST'])
async def slideshow_pause() -> Any:
    await slideshow_orchestrator.pause()
    return 'OK'


@app.route('/api/delay', methods=['POST'])
async def set_delay() -> Any:
    data = await request.json
    delay = data.get('delay')
    await slideshow_orchestrator.set_delay(float(delay))
    return 'OK'


@app.route('/api/delay', methods=['GET'])
async def get_delay() -> Any:
    return str(slideshow_orchestrator.delay)


def __run():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    app.run(host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


def start_web_server() -> None:
    t = threading.Thread(target=__run)
    t.setDaemon(True)
    t.start()
