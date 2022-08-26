from random import randint, seed

from url_shortener.base64_conversion import from_base64, to_base64


def test_base64_conversion() -> None:
    seed(0)
    for _ in range(100):
        number = randint(1, 2**32)
        assert from_base64(to_base64(number)) == number
