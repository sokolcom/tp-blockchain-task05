import sys

import config as cfg
import ec_math 
import ec_dsa


__all__ = ["register", "handshake", "challenge", "response", "validate"]


def generate_keypair():
    private_key = cfg.safe_random(1, cfg.SUBGROUP_ORDER)
    public_key = ec_math.scalar_mult(private_key, cfg.BASE_POINT)

    return (private_key, public_key)


def register():
    priv_alice, pub_alice = generate_keypair()
    priv_bob, pub_bob = generate_keypair()

    alice = {
        "private": priv_alice,
        "public": pub_alice,
        "partner_public": pub_bob
    }
    bob = {
        "private": priv_bob,
        "public": pub_bob,
        "partner_public": pub_alice,
        "nonce": None,
        "cmd_buffer": None
    }

    return (alice, bob)


def handshake(msg):
    return ec_dsa.hash_message(msg)


def challenge(bob, msg):
    bob["cmd_buffer"] = msg
    bob["nonce"] = cfg.safe_random(0, cfg.NONCE_MAX)
    bob["nonce"] = bob["nonce"].to_bytes(bob["nonce"].bit_length(), sys.byteorder)

    return (bob["nonce"], ec_dsa.sign(bob["nonce"], bob["private"]))


def response(alice, msg, signature):
    if ec_dsa.verify(msg, signature, alice["partner_public"]):
        return (msg, ec_dsa.sign(msg, alice["private"]))
    else:
        return (False, False)


def validate(bob, msg, signature):
    return (bob["nonce"] == msg) and ec_dsa.verify(msg, signature, bob["partner_public"])
