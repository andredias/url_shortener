#!/usr/bin/env python

from subprocess import check_call
from time import sleep

from httpx import post


def run_smoke_test() -> None:
    # fmt: off
    check_call(
        [
            'docker-compose',
            '-f', 'docker-compose.yml',
            '-f', 'docker-compose.smoke_test.yml',
            'up', '-d',
        ]
    )
    # fmt: on
    sleep(2)
    url = 'https://codelab.pronus.io'
    try:
        result = post('http://localhost:5000/', json={'url': url})
        assert result.status_code == 201
        assert isinstance(result.json(), str)
        print('Smoke test passed!')
    finally:
        # fmt: off
        check_call(
            [
                'docker-compose',
                '-f', 'docker-compose.yml',
                '-f', 'docker-compose.smoke_test.yml',
                'down',
            ]
        )
        # fmt: on


if __name__ == '__main__':
    run_smoke_test()
