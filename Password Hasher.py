import hashlib


class Hasher:
    def __init__(self):
        self.salt = "91cb2c45f3c534ff449e9554e3dfb53f3ecb1fb7fe962223e0e55ad386823709"


    def hash_password(self, password: str):
        return hashlib.sha256((password + self.salt).encode()).hexdigest()
