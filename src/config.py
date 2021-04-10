import os
import sys
import math


# Field properties 
_FIELD_MODULO = 2 ** 255 - 19
SUBGROUP_ORDER = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
_CURVE_A = 486662
_CURVE_B = 1
_CURVE_C = 0

BASE_POINT = (0x9, 0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9)

CMD_TOGGLE_LOCK = b"ACTION: TOGGLE THE LOCKS"

NONCE_MAX = 2 ** 256


# Cryptographically secure random number generation using os.urandom()
def safe_random(a, b):
    bytes_amount = math.ceil(b.bit_length() / 8)

    x = _random(bytes_amount)
    while (x < a) or (x >= b):
        x = _random(bytes_amount)
    return x


def _random(bytes_amount):
    return int.from_bytes(os.urandom(bytes_amount), sys.byteorder, signed=False)
