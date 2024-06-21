import hashlib


class Hasher:

    @staticmethod
    def hash_password(password: str):
        salt = "91cb2c45f3c534ff449e9554e3dfb53f3ecb1fb7fe962223e0e55ad386823709"
        return hashlib.sha256((password + salt).encode()).hexdigest()
