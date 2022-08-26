from httpx import AsyncClient

from url_shortener.base64_conversion import to_base64
from url_shortener.models.link import insert


async def test_get_link(client: AsyncClient) -> None:

    # non-existent code
    code = 'AbCdEf'
    resp = await client.get(f'/{code}')
    assert resp.status_code == 404

    # invalid code
    code = '._@:'
    resp = await client.get(f'/{code}')
    assert resp.status_code == 422

    # valid code
    url = 'https://codelab.pronus.io/dojo/DMVBy85U874Bbahfi2cSTw'
    id_ = await insert(url)
    code = to_base64(id_)
    resp = await client.get(f'/{code}')
    assert resp.status_code == 301


async def test_post_link(client: AsyncClient) -> None:
    url = 'https://codelab.pronus.io/dojo/DMVBy85U874Bbahfi2cSTw'
    resp = await client.post('/', json={'url': url})
    assert resp.status_code == 201
    code = resp.json()

    resp = await client.post('/', json={'url': url})
    assert resp.status_code == 201
    assert code == resp.json()
