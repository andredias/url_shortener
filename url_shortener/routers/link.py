import binascii

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from pydantic import HttpUrl

from ..base64_conversion import from_base64, to_base64
from ..models.link import get, get_by_url, insert

router = APIRouter()


@router.get('/{code}', response_class=RedirectResponse, status_code=301)
async def get_encoded_url(code: str) -> str:
    try:
        id_ = from_base64(code)
    except binascii.Error:
        raise HTTPException(422, 'invalid encoded url value') from None
    link = await get(id_)
    if link:
        logger.info(f'{code} -> {link.url}')
        return link.url
    raise HTTPException(404)


@router.post('/', status_code=201)
async def post_url(url: HttpUrl = Body(embed=True)) -> str:
    link = await get_by_url(str(url))
    id_ = link.id if link else (await insert(str(url)))
    code = to_base64(id_)
    logger.info(f'{url} -> {code}')
    return code
