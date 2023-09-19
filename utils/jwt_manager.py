"""
Create a secure connection.
NOTE: the key should be in an environment
"""
from jwt import encode, decode


def create_token(data: dict) -> str:
    """Creating the token from the data"""
    token: str = encode(payload=data, key="my_key", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    """Validating the data with the token"""
    data: dict = decode(token, key="my_key", algorithms=["HS256"])
    return data
