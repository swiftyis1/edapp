import base64
from django.conf import settings

def encrypt_token(token: str) -> str:
    """
    Encrypts a token string symmetrically using settings.SECRET_KEY.
    """
    if not token:
        return ""
    key = settings.SECRET_KEY.encode('utf-8')
    token_bytes = token.encode('utf-8')
    encrypted = bytearray()
    for i, char in enumerate(token_bytes):
        encrypted.append(char ^ key[i % len(key)])
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypts an encrypted token string symmetrically using settings.SECRET_KEY.
    """
    if not encrypted_token:
        return ""
    key = settings.SECRET_KEY.encode('utf-8')
    encrypted_bytes = base64.b64decode(encrypted_token.encode('utf-8'))
    decrypted = bytearray()
    for i, char in enumerate(encrypted_bytes):
        decrypted.append(char ^ key[i % len(key)])
    return decrypted.decode('utf-8')
