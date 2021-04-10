#!/usr/bin/python3
import sys

import config as cfg
from protocol import *


if __name__ == "__main__":
    car_key, car = register()
    print(
        "### CAR_KEY ###\n"
        f"PRIVATE:\t{hex(car_key['private'])[:16]}...\n"
        f"PUBLIC: \t({hex(car_key['public'][0])[:16]}..., {hex(car_key['public'][1])[:16]}...)"
    )
    
    print(
        "### CAR ###\n"
        f"PRIVATE:\t{hex(car['private'])[:16]}...\n"
        f"PUBLIC: \t({hex(car['public'][0])[:16]}..., {hex(car['public'][1])[:16]}...)\n"
    )

    # 1) Handshake
    action_msg = handshake(cfg.CMD_TOGGLE_LOCK)
    print(
        "(1) <HANDSHAKE>:\t CAR_KEY ============={{msg={:16.16s}...}}============> CAR"
        .format(hex(action_msg))
    )
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    # 2) Challenge
    nonce, signature_car = challenge(car, action_msg)
    print(
        "(2) <CHALLENGE>:\t CAR_KEY <============{{nonce={:16.16s}...}}=========== CAR\n"
        "                        \t <==={{sign(nonce)=(r={:8.8s}..., s={:8.8s}...)}}==="
        .format(
            hex(int.from_bytes(nonce, sys.byteorder)),
            hex(signature_car[0]), hex(signature_car[1])
        )
    )
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    # 3) Response
    nonce, signature_carkey = response(car_key, nonce, signature_car)
    if not signature_carkey:
        print("VERFICATION FAILED (CAR_KEY)\nTERMINATING...")
        exit(1)
    
    print(
        "(3) <RESPONSE>:\t\t CAR_KEY: verify(sign(nonce))\n"
        "                 \t CAR_KEY ============={{nonce={:16.16s}...}}==========> CAR\n"
        "                         \t ===={{sign(nonce)=(r={:8.8s}..., s={:8.8s}...)}}==>"
        .format(
            hex(int.from_bytes(nonce, sys.byteorder)), 
            hex(signature_carkey[0]), hex(signature_carkey[1])
        )
    )
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    # 4) Validate
    is_valid = validate(car, nonce, signature_carkey)
    print(
        f"(4) <VALIDATE>\t\t CAR:\tverify(sign(nonce)) = {is_valid}"
    )
    if is_valid:
        print("CAR: EXECUTE <ACTION>")
    else:
        print("VERIFICATION FAILED (CAR)\nTerminating...")
