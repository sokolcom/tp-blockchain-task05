import config as cfg
from protocol import *


if __name__ == "__main__":
    car_key, car = register()

    action_msg = handshake(cfg.CMD_TOGGLE_LOCK)

    nonce, signature_car = challenge(car, action_msg)
    print("NONCE (CAR):", nonce)

    nonce, signature_carkey = response(car_key, nonce, signature_car)
    print("NONCE (CAR_KEY):", nonce)

    print("SOOOOOOOOO.....", validate(car, nonce, signature_carkey))


