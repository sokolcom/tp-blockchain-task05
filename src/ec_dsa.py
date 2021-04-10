import sys
import hashlib
import random

import config as cfg
import ec_math


def hash_message(message):
    hashed = int.from_bytes(hashlib.sha3_256(message).digest(), sys.byteorder)
    truncated = hashed >> (hashed.bit_length() - cfg.SUBGROUP_ORDER.bit_length())
    return truncated


def sign(message, private_key):
    hashed = hash_message(message)

    r = 0x0
    s = 0x0
    while (not r) or (not s):
        k = cfg.safe_random(1, cfg.SUBGROUP_ORDER)
        x, _ = ec_math.scalar_mult(k, cfg.BASE_POINT)
        r = x % cfg.SUBGROUP_ORDER
        s = ((hashed + r * private_key) * ec_math.invmod(k, cfg.SUBGROUP_ORDER)) % cfg.SUBGROUP_ORDER

    return (r, s)


def verify(message, signature, public_key):
    r, s = signature
    hashed = hash_message(message)

    inv_s = ec_math.invmod(s, cfg.SUBGROUP_ORDER)
    u1 = (inv_s * hashed) % cfg.SUBGROUP_ORDER
    u2 = (inv_s * r) % cfg.SUBGROUP_ORDER
    x, _ = ec_math.add(ec_math.scalar_mult(u1, cfg.BASE_POINT), ec_math.scalar_mult(u2, public_key))

    return (r % cfg.SUBGROUP_ORDER) == (x % cfg.SUBGROUP_ORDER)


# def hash_message(message):
#     """Returns the truncated SHA521 hash of the message."""
#     message_hash = hashlib.sha512(message).digest()
#     e = int.from_bytes(message_hash, 'big')

#     # FIPS 180 says that when a hash needs to be truncated, the rightmost bits
#     # should be discarded.
#     z = e >> (e.bit_length() - cfg.SUBGROUP_ORDER.bit_length())

#     assert z.bit_length() <= cfg.SUBGROUP_ORDER.bit_length()

#     return z


# def sign(message, private_key):
#     z = hash_message(message)

#     r = 0
#     s = 0

#     while not r or not s:
#         k = random.randrange(1, cfg.SUBGROUP_ORDER)
#         x, y = ec_math.scalar_mult(k, cfg.BASE_POINT)

#         r = x % cfg.SUBGROUP_ORDER
#         s = ((z + r * private_key) * ec_math.invmod(k, cfg.SUBGROUP_ORDER)) % cfg.SUBGROUP_ORDER

#     return (r, s)


# def verify(message, signature, public_key):
#     z = hash_message(message)

#     r, s = signature

#     w = ec_math.invmod(s, cfg.SUBGROUP_ORDER)
#     u1 = (z * w) % cfg.SUBGROUP_ORDER
#     u2 = (r * w) % cfg.SUBGROUP_ORDER

#     x, y = ec_math.add(ec_math.scalar_mult(u1, cfg.BASE_POINT),
#                     ec_math.scalar_mult(u2, public_key))

#     if (r % cfg.SUBGROUP_ORDER) == (x % cfg.SUBGROUP_ORDER):
#         return 'signature matches'
#     else:
#         return 'invalid signature'