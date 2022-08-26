from fastapi import FastAPI

from url_shortener.models.link import get, get_by_url, insert


async def test_insert_get_link(app: FastAPI) -> None:
    urls = [
        'https://codelab.pronus.io/dojo/DMVBy85U874Bbahfi2cSTw',
        'https://blog.pronus.io/en/posts/python/how-to-set-up-a-perfect-python-project/',  # noqa: E501
    ]

    ids = [await insert(url) for url in urls]
    assert all(ids)
    link = await get(ids[1])
    assert link and link.url == urls[1]
    link = await get_by_url(urls[0])
    assert link and link.id == ids[0]
