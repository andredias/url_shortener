from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import config
from .resources import lifespan
from .routers import link

routers = [
    link.router,
]

app = FastAPI(
    title='URL Shortener',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


for router in routers:
    app.include_router(router)
