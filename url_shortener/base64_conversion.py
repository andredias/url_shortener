from base64 import urlsafe_b64decode, urlsafe_b64encode
from math import ceil

# ref: https://stackoverflow.com/a/55354665/266362


def to_base64(number: int) -> str:
    number_in_bytes = number.to_bytes(
        ceil(number.bit_length() / 8), byteorder='big'
    )
    code = urlsafe_b64encode(number_in_bytes).rstrip(b'=')
    return code.decode()


def from_base64(code: str) -> int:
    code = code.ljust(ceil(len(code) / 4) * 4, '=')  # must be multiple of 4
    number_in_bytes = urlsafe_b64decode(code.encode())
    number = int.from_bytes(number_in_bytes, byteorder='big')
    return number
