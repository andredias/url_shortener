from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import config
from .resources import shutdown, startup
from .routers import hello, user

routers = [
    hello.router,
    user.router,
]

app = FastAPI(
    title='URL Shortener',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
)


for router in routers:
    app.include_router(router)


@app.on_event('startup')
async def startup_event() -> None:
    await startup()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await shutdown()
